#!/usr/bin/env python3
"""ab_run.py -- Two-arm A/B over SWE-bench Verified: resolve-rate AND consistency.

Arms:
  baseline : a single "cook" agent edits the repo to fix the issue.
  process  : the cook runs, then a separate "taster" agent reviews the cook's diff
             and either APPROVEs or returns concrete corrections; if not APPROVEd,
             the cook runs once more in the same checkout with the corrections.

Each (instance, arm, repeat) is an independent cell. Outcomes are scored with the
SWE-bench evaluation harness, then aggregated into resolve-rate and a STATIC/FLAKY
consistency measure across repeats.

Run it with the SWE-bench venv interpreter (it provides the `datasets` lib):

    ~/.swebench-venv/bin/python ab_run.py            # full A/B
    ~/.swebench-venv/bin/python ab_run.py --dry-run  # print the plan only

------------------------------------------------------------------------------
IMPORTANT design note (deviation from a literal reading of the brief, with proof)
------------------------------------------------------------------------------
The brief asked to "write all predictions for an arm to one predictions JSON and
score with run_evaluation (one run_id per arm)" and resolve a (instance, repeat)
by whether "its model_name_or_path is in resolved_ids". That cannot work as
written: swebench's run_evaluation collapses the predictions list to a dict keyed
by instance_id before running anything
    predictions = {pred[instance_id]: pred for pred in predictions}
(swebench/harness/run_evaluation.py, function main). With REPEATS predictions
sharing one instance_id, only ONE survives, so the repeats are never scored, and
`resolved_ids` is a set of instance_ids (never model_name_or_path values).

This driver therefore scores ONE run per (arm, repeat):
    run_id            = f"{arm}-r{repeat}"
    model_name_or_path = f"{arm}-r{repeat}"
    predictions file  = preds/<arm>-r<repeat>.json   (one patch per instance)
    scorer report     = reports/<arm>-r<repeat>.<arm>-r<repeat>.json
A cell (instance, arm, repeat) is RESOLVED iff its instance_id is in that
(arm, repeat) report's `resolved_ids`. This is the only reading that actually
measures per-repeat outcomes.

------------------------------------------------------------------------------
Secrecy: the gold `patch` and the `test_patch` (tests) are NEVER loaded and NEVER
shown to any agent. Only repo / base_commit / problem_statement are read. The
taster runs in an isolated empty cwd (not the checkout) and only sees the problem
statement plus the cook's diff, so it cannot read tests or gold even with full
tools. Only `glm-exec` is used as a model runner.
------------------------------------------------------------------------------
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ============================ Config (edit these) ============================

# Placeholder instance ids -- REPLACE with real SWE-bench Verified instance ids.
INSTANCES = [
    "REPLACE_WITH_INSTANCE_ID_1",
    "REPLACE_WITH_INSTANCE_ID_2",
    "REPLACE_WITH_INSTANCE_ID_3",
]
REPEATS = 3
ARMS = ["baseline", "process"]

# Scratch working dir for checkouts, run dirs, predictions and reports.
WORK = Path("/tmp/ab_run_work")

DATASET_NAME = "princeton-nlp/SWE-bench_Verified"
DATASET_SPLIT = "test"

# External tools.
VENV_PY = os.path.expanduser("~/.swebench-venv/bin/python")  # has `datasets`
GLM_EXEC = "glm-exec"
WORKER_MODEL = "opus"        # glm-exec model alias (-> glm-5.2[1m])
WORKER_TIMEOUT_S = 0         # 0 = unbounded; let the model finish
SCORER_MAX_WORKERS = 2
SCORER_CACHE_LEVEL = "env"

# ============================ Derived paths =================================

CHECKOUTS = WORK / "checkouts"      # one git checkout per cell
RUN_DIRS = WORK / "runs"            # glm-exec run dirs (prompt.txt, final.txt, ...)
REVIEW_DIR = WORK / "review_cwd"    # isolated, empty cwd for the taster
PRED_DIR = WORK / "preds"           # predictions JSONs
REPORT_DIR = WORK / "reports"       # cwd for the scorer; reports land here
REPORT_OUT = Path("ab-report.json") # final aggregate (also printed)
LOG_FILE = WORK / "ab-run.log"

# Populated at runtime.
INSTANCES_DATA: dict[str, dict] = {}


# ============================ Logging / shell ===============================

def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def run(cmd, cwd=None, check=True, capture=True, env=None, timeout=None):
    """subprocess.run wrapper. cmd is a list. Returns CompletedProcess."""
    res = subprocess.run(
        [str(c) for c in cmd],
        cwd=str(cwd) if cwd else None,
        capture_output=capture,
        text=True,
        env=env,
        timeout=timeout,
    )
    if check and res.returncode != 0:
        raise RuntimeError(
            f"command failed (rc={res.returncode}): {' '.join(map(str, cmd))}\n"
            f"--- stdout (tail) ---\n{(res.stdout or '')[-2000:]}\n"
            f"--- stderr (tail) ---\n{(res.stderr or '')[-2000:]}"
        )
    return res


def git(args, cwd=None, check=True, capture=True):
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"  # never prompt for credentials
    return run(["git", *[str(a) for a in args]], cwd=cwd, check=check,
               capture=capture, env=env)


# ============================ Dataset =======================================

def load_instances(instance_ids):
    """Return {instance_id: {instance_id, repo, base_commit, problem_statement}}.

    Deliberately reads ONLY those four fields. The gold `patch` and the
    `test_patch` (the tests) are never read into memory and can never leak to an
    agent.
    """
    from datasets import load_dataset

    wanted = set(instance_ids)
    out: dict[str, dict] = {}
    for row in load_dataset(DATASET_NAME, split=DATASET_SPLIT):
        rid = row["instance_id"]
        if rid in wanted:
            out[rid] = {
                "instance_id": rid,
                "repo": row["repo"],
                "base_commit": row["base_commit"],
                "problem_statement": row["problem_statement"],
            }
            if len(out) == len(wanted):
                break
    missing = sorted(wanted - set(out))
    if missing:
        raise SystemExit(f"Instance IDs not found in {DATASET_NAME}: {missing}")
    return out


# ============================ Checkout ======================================

def fresh_checkout(repo: str, base_commit: str, dest: Path) -> Path:
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{repo}"
    log(f"    clone {url} @ {base_commit[:12]} -> {dest.name}")
    # Full clone (no --depth): base_commit may be an old commit not on a shallow tip.
    git(["clone", "--quiet", url, str(dest)], check=True, capture=True)
    git(["checkout", "--quiet", base_commit], cwd=dest, check=True, capture=True)
    return dest


# ============================ glm-exec workers ==============================

def make_run_dir(tag: str, prompt_text: str) -> Path:
    """Create a glm-exec run dir with prompt.txt (stdin) + run.spec.json."""
    rd = RUN_DIRS / tag
    if rd.exists():
        shutil.rmtree(rd)
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "prompt.txt").write_text(prompt_text, encoding="utf-8")
    spec = {
        "objective": f"SWE-bench A/B {tag}",
        "model": WORKER_MODEL,
        "timeout_seconds": WORKER_TIMEOUT_S,
    }
    (rd / "run.spec.json").write_text(json.dumps(spec), encoding="utf-8")
    return rd


def run_glm(run_dir: Path, cwd: Path) -> tuple[int, str]:
    """Invoke glm-exec <run_dir> with cwd=<cwd>. cwd becomes the worker's cwd.

    Returns (exit_code, final_text). Never raises on non-zero exit; the caller
    decides how to treat a failed worker (an empty diff scores unresolved).
    """
    log(f"    glm-exec {run_dir.name}  (worker cwd={cwd.name})")
    res = run([GLM_EXEC, str(run_dir)], cwd=cwd, check=False, capture=True)
    final = ""
    fp = run_dir / "final.txt"
    if fp.exists():
        final = fp.read_text(encoding="utf-8", errors="replace")
    return res.returncode, final


COOK_RULES = """\
You are a software engineer fixing a real bug in the repository that is your
current working directory. The repo has been checked out at the base commit that
existed when the issue was filed.

HARD RULES -- violating any of these invalidates your work:
 1. Edit ONLY the project's library/source code. Make the minimal change that
    correctly and completely resolves the issue below.
 2. Do NOT read, run, write, or modify any tests. This means: no file under any
    tests/ or test/ directory, no file whose name matches test_*.py or *_test.py,
    and no conftest.py. Behave as if tests do not exist.
 3. Do NOT use the network or the web.
 4. Do NOT make any git commit and do NOT create or switch branches. Edit files
    in place in the working tree; the harness captures the diff for you.
 5. Do NOT read, print, or disclose any credentials, API keys, .env files, or
    secrets.
 6. When the fix is complete, stop. End with a one-paragraph summary of the change.

ISSUE / PROBLEM STATEMENT:
"""


def cook_prompt(problem_statement: str, corrections: str | None = None) -> str:
    prompt = COOK_RULES + problem_statement.strip() + "\n"
    if corrections:
        prompt += (
            "\nA reviewer examined your previous attempt at this same issue and "
            "returned these concrete corrections. Re-do the fix and address every "
            "point:\n" + corrections.strip() + "\n"
        )
    return prompt


def taster_prompt(problem_statement: str, diff: str) -> str:
    diff_block = diff.strip() if diff.strip() else "(empty -- no source changes were produced)"
    return f"""\
You are a code reviewer. Below are a problem statement and a proposed source diff
that intends to resolve it. Judge ONLY whether the diff correctly and completely
addresses the problem statement.

HARD RULES:
 1. Do NOT read, run, or reference any tests. No tests exist for you; do not
    speculate about them.
 2. Do NOT propose adding or modifying tests.
 3. If the diff correctly resolves the problem, reply with EXACTLY the single
    word: APPROVE
    Otherwise reply with ONLY a short numbered list of concrete, specific
    corrections the author must make. No preamble, no closing remarks -- just the
    numbered items.

PROBLEM STATEMENT:
{problem_statement.strip()}

PROPOSED DIFF:
{diff_block}
"""


# ============================ Diff capture ==================================

def is_test_path(path: str) -> bool:
    parts = path.lower().replace("\\", "/").split("/")
    base = parts[-1]
    if base.startswith("test_") or base.endswith("_test.py") or base == "conftest.py":
        return True
    return any(seg in ("tests", "test") for seg in parts[:-1])


def filter_test_paths(diff_text: str) -> str:
    """Drop whole-file blocks whose target path looks like a test file/dir."""
    if not diff_text or not diff_text.strip():
        return ""
    blocks = re.split(r"(?m)(?=^diff --git )", diff_text)
    kept = []
    for blk in blocks:
        if not blk.strip():
            continue
        m = re.match(r"diff --git a/(.*?) b/(.+)", blk)
        if m:
            path = m.group(2).split()[0]
            if is_test_path(path):
                log(f"    excluding test path from diff: {path}")
                continue
        kept.append(blk)
    return ("".join(kept).rstrip() + "\n") if kept else ""


def capture_source_diff(checkout: Path, base_commit: str) -> str:
    """Full delta from base_commit to current working tree, minus test paths.

    `git add -A` mirrors the working tree (including new/untracked source files
    and any commits the cook may have made) into the index; `git diff --cached
    <base_commit>` then yields the complete patch relative to the base tree. We
    do NOT commit. The checkout is disposable, so leaving the index staged is
    harmless.
    """
    git(["add", "-A"], cwd=checkout, check=True, capture=True)
    res = git(["diff", "--cached", base_commit], cwd=checkout, check=True, capture=True)
    return filter_test_paths(res.stdout)


# ============================ One cell ======================================

def run_cell(instance_id: str, arm: str, repeat: int) -> str:
    """Run one (instance, arm, repeat) and return its source-only diff string."""
    inst = INSTANCES_DATA[instance_id]
    ps = inst["problem_statement"]
    base = inst["base_commit"]
    tag = f"{instance_id}__{arm}__r{repeat}"

    checkout = CHECKOUTS / tag
    fresh_checkout(inst["repo"], base, checkout)

    # --- cook ---
    cook_rd = make_run_dir(f"{tag}__cook", cook_prompt(ps))
    crc, _ = run_glm(cook_rd, cwd=checkout)
    diff = capture_source_diff(checkout, base)
    log(f"    [{tag}] cook rc={crc} diff_len={len(diff)}")

    # --- process arm: taste, then maybe re-cook ---
    if arm == "process":
        # Taster runs in an isolated EMPTY cwd with prompt-only input, so it can
        # neither see the checkout's tests/gold nor contaminate the working tree.
        taster_cwd = REVIEW_DIR / f"{tag}__taste"
        if taster_cwd.exists():
            shutil.rmtree(taster_cwd)
        taster_cwd.mkdir(parents=True, exist_ok=True)
        taste_rd = make_run_dir(f"{tag}__taste", taster_prompt(ps, diff))
        trc, tfinal = run_glm(taste_rd, cwd=taster_cwd)
        verdict = (tfinal or "").strip()
        log(f"    [{tag}] taster rc={trc} verdict_head={verdict[:80]!r}")
        if not verdict.upper().startswith("APPROVE"):
            recook_rd = make_run_dir(f"{tag}__recook", cook_prompt(ps, corrections=verdict))
            rrc, _ = run_glm(recook_rd, cwd=checkout)
            diff = capture_source_diff(checkout, base)
            log(f"    [{tag}] recook rc={rrc} diff_len={len(diff)}")

    (PRED_DIR / f"{tag}.diff").write_text(diff, encoding="utf-8")
    return diff


# ============================ Scoring =======================================

def score_arm_repeat(arm: str, repeat: int, predictions: list[dict]) -> set[str]:
    """Score one (arm, repeat). Returns the set of resolved instance_ids."""
    run_id = f"{arm}-r{repeat}"
    model = run_id  # == model_name_or_path used in each prediction
    pred_path = PRED_DIR / f"{run_id}.json"
    pred_path.write_text(json.dumps(predictions), encoding="utf-8")

    ids = sorted(p["instance_id"] for p in predictions)
    cmd = [
        VENV_PY, "-m", "swebench.harness.run_evaluation",
        "-d", DATASET_NAME,
        "-s", DATASET_SPLIT,
        "-i", *ids,
        "-p", str(pred_path),
        "--max_workers", str(SCORER_MAX_WORKERS),
        "-id", run_id,
        "--cache_level", SCORER_CACHE_LEVEL,
    ]
    log(f"    score {run_id}: {len(ids)} instance(s) -> {pred_path.name}")
    res = run(cmd, cwd=REPORT_DIR, check=False, capture=True)
    if res.returncode != 0:
        log(f"    WARN: scorer for {run_id} exited rc={res.returncode}; "
            f"stderr tail: {(res.stderr or '')[-600:]}")

    resolved: set[str] = set()
    report_path = REPORT_DIR / f"{model}.{run_id}.json"
    if not report_path.exists():
        cands = sorted(REPORT_DIR.glob(f"*.{run_id}.json"))
        if cands:
            report_path = cands[0]
    if report_path.exists():
        try:
            rep = json.loads(report_path.read_text(encoding="utf-8"))
            resolved = set(rep.get("resolved_ids", []))
            log(f"    score {run_id}: resolved={len(resolved)}/{len(ids)} "
                f"({sorted(resolved)})")
        except (OSError, json.JSONDecodeError) as e:
            log(f"    WARN: could not parse report {report_path}: {e}")
    else:
        log(f"    WARN: no report file found for {run_id}")
    return resolved


# ============================ Aggregation ===================================

def aggregate(outcomes: dict, instances: list[str], failures: list) -> dict:
    arm_stats: dict[str, dict] = {}
    for arm in ARMS:
        resolved_count = 0
        total = 0
        per_instance: dict[str, dict] = {}
        for inst in sorted(instances):
            seq = [bool(outcomes[arm][r].get(inst, False)) for r in range(REPEATS)]
            resolved_count += sum(seq)
            total += len(seq)
            per_instance[inst] = {
                "outcomes": seq,
                "resolved_count": int(sum(seq)),
                "consistency": "STATIC" if len(set(seq)) == 1 else "FLAKY",
            }
        n = len(instances)
        static_count = sum(
            1 for inst in instances if per_instance[inst]["consistency"] == "STATIC"
        )
        arm_stats[arm] = {
            "total_runs": total,
            "resolved_count": int(resolved_count),
            "resolve_rate": round(resolved_count / total, 4) if total else 0.0,
            "num_instances": n,
            "static_instances": static_count,
            "static_fraction": round(static_count / n, 4) if n else 0.0,
            "per_instance": per_instance,
        }

    delta: dict = {}
    if len(ARMS) >= 2:
        a, b = ARMS[0], ARMS[1]
        ra, rb = arm_stats[a]["resolve_rate"], arm_stats[b]["resolve_rate"]
        sa, sb = arm_stats[a]["static_fraction"], arm_stats[b]["static_fraction"]
        delta = {
            "resolve_rate_delta": round(rb - ra, 4),
            "higher_resolve_arm": (
                b if rb > ra else a if ra > rb else "tie"
            ),
            "static_fraction_delta": round(sb - sa, 4),
            "more_static_arm": (
                b if sb > sa else a if sa > sb else "tie"
            ),
            "note": (
                f"resolve_rate_delta = {b} - {a}; "
                f"static_fraction_delta = {b} - {a}"
            ),
        }

    return {
        "config": {
            "instances": sorted(instances),
            "repeats": REPEATS,
            "arms": ARMS,
        },
        "arms": arm_stats,
        "delta": delta,
        "failures": failures,
    }


# ============================ Dry run =======================================

def dry_run(instances: list[str]) -> int:
    log("DRY RUN -- no dataset load, no clones, no agents, no scoring.")
    cells = 0
    for repeat in range(REPEATS):
        for arm in ARMS:
            run_id = f"{arm}-r{repeat}"
            for inst in sorted(instances):
                cells += 1
                actions = [
                    f"clone+checkout {inst}",
                    f"cook glm-exec (model={WORKER_MODEL})",
                ]
                if arm == "process":
                    actions += [
                        "taster glm-exec (APPROVE | numbered corrections)",
                        "if not APPROVE: recook glm-exec once",
                    ]
                actions += ["capture source diff (test paths excluded)"]
                log(f"  PLAN {inst} | {arm} | r{repeat}: " + " -> ".join(actions))
            log(f"  PLAN SCORE {run_id}: preds/{run_id}.json -> "
                f"reports/{run_id}.{run_id}.json  (resolved_ids keyed by instance_id)")
    log(f"plan totals: {cells} cell(s); {len(ARMS) * REPEATS} scorer run(s).")
    log("NOTE: scored one run_id per (arm, repeat), not one per arm -- see the "
        "module docstring for the proof (run_evaluation collapses duplicate "
        "instance_ids, so all repeats of an instance cannot share one arm file).")
    return 0


# ============================ Main ==========================================

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Two-arm A/B over SWE-bench Verified.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the plan of runs without executing agents/scoring.")
    ap.add_argument("--instances", nargs="*",
                    help="Override the INSTANCES list (instance ids).")
    ap.add_argument("--repeats", type=int, default=None,
                    help="Override REPEATS.")
    args = ap.parse_args(argv)

    instances = args.instances if args.instances else list(INSTANCES)
    global REPEATS
    if args.repeats is not None:
        REPEATS = args.repeats

    for d in (CHECKOUTS, RUN_DIRS, REVIEW_DIR, PRED_DIR, REPORT_DIR):
        d.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        return dry_run(instances)

    if not shutil.which(GLM_EXEC):
        log(f"ERROR: '{GLM_EXEC}' not found on PATH.")
        return 2
    if not Path(VENV_PY).exists():
        log(f"ERROR: venv interpreter not found: {VENV_PY}")
        return 2

    global INSTANCES_DATA
    INSTANCES_DATA = load_instances(instances)

    outcomes = {arm: {r: {} for r in range(REPEATS)} for arm in ARMS}
    failures: list[dict] = []

    for repeat in range(REPEATS):
        for arm in ARMS:
            model = f"{arm}-r{repeat}"
            preds: list[dict] = []
            for inst in sorted(instances):
                log(f"== cell {inst} | {arm} | r{repeat} ==")
                try:
                    diff = run_cell(inst, arm, repeat)
                except Exception as e:  # tolerate a failed cell; count unresolved
                    log(f"FAILED cell {inst}/{arm}/r{repeat}: {e}")
                    failures.append({
                        "instance": inst, "arm": arm, "repeat": repeat,
                        "stage": "cook", "error": str(e),
                    })
                    diff = ""
                preds.append({
                    "instance_id": inst,
                    "model_name_or_path": model,
                    "model_patch": diff,
                })
            try:
                resolved = score_arm_repeat(arm, repeat, preds)
            except Exception as e:
                log(f"FAILED scoring {arm}/r{repeat}: {e}")
                failures.append({
                    "arm": arm, "repeat": repeat, "stage": "score", "error": str(e),
                })
                resolved = set()
            for inst in sorted(instances):
                outcomes[arm][repeat][inst] = inst in resolved

    report = aggregate(outcomes, instances, failures)
    print(json.dumps(report, indent=2))
    REPORT_OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    log(f"report written to {REPORT_OUT.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
