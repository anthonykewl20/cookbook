#!/usr/bin/env python3
"""Shared, dependency-light helpers for the Molecular Gastronomy trial.

This module never imports the reference harness.  Model-facing scripts consume
only the public task snapshot produced by select_tasks.py; gold patches and
test_patch never enter those processes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import resource
import shlex
import shutil
import signal
import string
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATASET_NAME = "princeton-nlp/SWE-bench_Verified"
DATASET_SPLIT = "test"
VENV_PY = Path(os.path.expanduser("~/.swebench-venv/bin/python"))
DEFAULT_COOK_CMD = "REPLACE_WITH_COOK_CMD"
DEFAULT_COOK_MODEL = "REPLACE_WITH_COOK_MODEL"

PUBLIC_TASK_FIELDS = (
    "instance_id",
    "repo",
    "base_commit",
    "problem_statement",
    "difficulty",
)

_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
)
_CLAUDE_RE = re.compile(r"claude", re.IGNORECASE)
_ALLOWED_TEMPLATE_FIELDS = {
    "checkout",
    "max_compute_tokens",
    "max_tokens",
    "max_tool_calls",
    "model",
    "output_file",
    "prompt_file",
    "run_dir",
    "safe_mode",
    "timeout_seconds",
    "usage_file",
}
_SAFE_MODEL_ENV_NAMES = {
    "COLORTERM",
    "HOME",
    "LANG",
    "LOGNAME",
    "NO_COLOR",
    "PATH",
    "SHELL",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "TERM",
    "TMPDIR",
    "TZ",
    "USER",
}
_MAX_CAPTURE_BYTES = 8 * 1024 * 1024
_MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
_MAX_ARTIFACT_TOTAL_BYTES = 256 * 1024 * 1024
_MAX_ARTIFACT_FILES = 2000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_sha256(path: Path) -> str:
    """Hash a directory snapshot by relative path and file content."""
    root = Path(path)
    entries = []
    for child in sorted(root.rglob("*")):
        if child.is_symlink():
            raise ValueError(f"refusing to hash symlinked trajectory artifact: {child}")
        if child.is_file():
            entries.append(
                {
                    "path": child.relative_to(root).as_posix(),
                    "sha256": sha256_file(child),
                }
            )
    return payload_sha256(entries)


def payload_sha256(value: Any) -> str:
    return sha256_text(canonical_json(value))


def load_json(path: Path) -> Any:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any, *, overwrite: bool = False) -> None:
    """Atomically write JSON and refuse to move a frozen bar by default."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite frozen file: {path}")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validate_task_bank(bank: dict[str, Any], *, expected_count: int | None = None) -> list[dict]:
    tasks = bank.get("tasks")
    ids = bank.get("instance_ids")
    if not isinstance(tasks, list) or not isinstance(ids, list):
        raise ValueError("task bank needs lists named tasks and instance_ids")
    if expected_count is not None and len(tasks) != expected_count:
        raise ValueError(f"expected {expected_count} tasks, found {len(tasks)}")
    if ids != [task.get("instance_id") for task in tasks]:
        raise ValueError("instance_ids must exactly match tasks in frozen order")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate instance_id in task bank")
    for task in tasks:
        missing = [field for field in PUBLIC_TASK_FIELDS if field not in task]
        if missing:
            raise ValueError(f"task {task.get('instance_id')} missing public fields: {missing}")
        forbidden = {"patch", "test_patch", "FAIL_TO_PASS", "PASS_TO_PASS"} & set(task)
        if forbidden:
            raise ValueError(f"task bank contains hidden fields: {sorted(forbidden)}")
    expected_hash = bank.get("task_bank_sha256")
    actual_hash = payload_sha256(tasks)
    if expected_hash != actual_hash:
        raise ValueError("task_bank_sha256 does not match tasks")
    return tasks


def task_map(bank: dict[str, Any]) -> dict[str, dict]:
    return {task["instance_id"]: task for task in validate_task_bank(bank)}


def assert_no_secret_like_text(text: str, *, label: str) -> None:
    for pattern in _SECRET_PATTERNS:
        if pattern.search(text):
            raise ValueError(f"{label} matched a secret-like value; refusing model call")


def validate_cook_template(template: str) -> bool:
    if not template or template.strip() == DEFAULT_COOK_CMD:
        raise ValueError(
            "COOK_CMD is still the placeholder; set COOK_CMD or pass --cook-cmd"
        )
    assert_no_secret_like_text(template, label="COOK_CMD")
    fields = {
        field_name
        for _, field_name, _, _ in string.Formatter().parse(template)
        if field_name is not None
    }
    unknown = fields - _ALLOWED_TEMPLATE_FIELDS
    if unknown:
        raise ValueError(f"unknown COOK_CMD placeholders: {sorted(unknown)}")
    required = {"max_compute_tokens", "max_tokens", "max_tool_calls", "model"}
    missing = required - fields
    if missing:
        raise ValueError(
            "COOK_CMD must pass the fixed model and every matched cap; missing "
            f"placeholders: {sorted(missing)}"
        )
    is_claude = bool(_CLAUDE_RE.search(template))
    if is_claude and "--safe-mode" not in template and "safe_mode" not in fields:
        raise ValueError("Claude COOK_CMD must contain --safe-mode or {safe_mode}")
    return is_claude


def validate_cook_model(model: str) -> str:
    if not model or model.strip() == DEFAULT_COOK_MODEL:
        raise ValueError(
            "cook model is still the placeholder; set COOK_MODEL or pass "
            "--cook-model"
        )
    assert_no_secret_like_text(model, label="cook model identifier")
    return model.strip()


def _safe_model_environment() -> dict[str, str]:
    """Pass paths/locale only; never inherit API keys, tokens, or credentials."""
    environment = {
        name: os.environ[name]
        for name in _SAFE_MODEL_ENV_NAMES
        if name in os.environ
    }
    environment.update(
        {
            name: value
            for name, value in os.environ.items()
            if name.startswith("LC_")
        }
    )
    return environment


def _limit_cook_file_size() -> None:
    _, hard = resource.getrlimit(resource.RLIMIT_FSIZE)
    limit = _MAX_ARTIFACT_BYTES
    if hard != resource.RLIM_INFINITY:
        limit = min(limit, hard)
    resource.setrlimit(resource.RLIMIT_FSIZE, (limit, hard))


def _read_bounded(handle: Any) -> tuple[str, bool]:
    handle.flush()
    handle.seek(0)
    value = handle.read(_MAX_CAPTURE_BYTES + 1)
    if len(value) > _MAX_CAPTURE_BYTES:
        return value[:_MAX_CAPTURE_BYTES], True
    return value, False


def _screen_run_artifacts(run_dir: Path) -> list[str]:
    """Remove links/overflow and redact secret-like retained wrapper artifacts."""
    violations: list[str] = []
    files: list[Path] = []
    for path in sorted(run_dir.rglob("*")):
        relative = path.relative_to(run_dir).as_posix()
        if path.is_symlink():
            path.unlink()
            violations.append(f"{relative}: symlink removed")
        elif path.is_file():
            files.append(path)
    if len(files) > _MAX_ARTIFACT_FILES:
        for path in files[_MAX_ARTIFACT_FILES:]:
            relative = path.relative_to(run_dir).as_posix()
            path.unlink()
            violations.append(f"{relative}: file-count overflow removed")
        files = files[:_MAX_ARTIFACT_FILES]

    total = 0
    for path in files:
        relative = path.relative_to(run_dir).as_posix()
        size = path.stat().st_size
        total += size
        if size > _MAX_ARTIFACT_BYTES or total > _MAX_ARTIFACT_TOTAL_BYTES:
            path.write_text(
                "[BLOCKED: artifact exceeded retention limit]\n",
                encoding="utf-8",
            )
            violations.append(f"{relative}: oversized artifact redacted")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            assert_no_secret_like_text(text, label=relative)
        except ValueError:
            path.write_text(
                "[BLOCKED: artifact matched a secret-like value]\n",
                encoding="utf-8",
            )
            violations.append(f"{relative}: secret-like value redacted")
    return violations


def _format_cook_command(
    template: str,
    *,
    checkout: Path,
    run_dir: Path,
    model: str,
    max_compute_tokens: int,
    max_tokens: int,
    max_tool_calls: int,
    timeout_seconds: int,
    is_claude: bool,
) -> str:
    values = {
        "checkout": shlex.quote(str(checkout.resolve())),
        "max_compute_tokens": str(max_compute_tokens),
        "max_tokens": str(max_tokens),
        "max_tool_calls": str(max_tool_calls),
        "model": shlex.quote(model),
        "output_file": shlex.quote(str((run_dir / "final.txt").resolve())),
        "prompt_file": shlex.quote(str((run_dir / "prompt.txt").resolve())),
        "run_dir": shlex.quote(str(run_dir.resolve())),
        "safe_mode": "--safe-mode" if is_claude else "",
        "timeout_seconds": str(timeout_seconds),
        "usage_file": shlex.quote(str((run_dir / "usage.json").resolve())),
    }
    return template.format_map(values)


def _numeric_usage(path: Path) -> dict[str, int] | None:
    if not path.exists():
        return None
    raw = load_json(path)
    if not isinstance(raw, dict):
        raise ValueError(f"usage file must contain a JSON object: {path}")
    out: dict[str, int] = {}
    aliases = {
        "compute_tokens": ("compute_tokens", "thinking_tokens", "reasoning_tokens"),
        "input_tokens": ("input_tokens", "prompt_tokens"),
        "output_tokens": ("output_tokens", "completion_tokens"),
        "tool_calls": ("tool_calls", "tool_call_count"),
        "total_tokens": ("total_tokens",),
    }
    for destination, names in aliases.items():
        for name in names:
            value = raw.get(name)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                out[destination] = value
                break
    if "total_tokens" not in out and {"input_tokens", "output_tokens"} <= set(out):
        out["total_tokens"] = out["input_tokens"] + out["output_tokens"]
    return out or None


def run_cook(
    *,
    template: str,
    checkout: Path,
    run_dir: Path,
    prompt: str,
    tag: str,
    phase: str,
    model: str,
    max_compute_tokens: int,
    max_tokens: int,
    max_tool_calls: int,
    timeout_seconds: int,
) -> dict[str, Any]:
    """Run one cook process with a fixed shell template and a hard wall timeout.

    Prompt is supplied on stdin and as prompt.txt.  Final output is taken from
    final.txt when the command writes it, otherwise from stdout.  A command
    wrapper may write usage.json; only numeric token counts are retained.
    """
    is_claude = validate_cook_template(template)
    model = validate_cook_model(model)
    assert_no_secret_like_text(prompt, label=f"{tag} prompt")
    if (
        max_compute_tokens <= 0
        or max_tokens <= 0
        or max_tool_calls <= 0
        or timeout_seconds <= 0
    ):
        raise ValueError("cook compute, token, tool, and wall-time caps must be positive")

    run_dir = Path(run_dir)
    if run_dir.exists():
        raise FileExistsError(f"refusing to overwrite cook run: {run_dir}")
    run_dir.mkdir(parents=True)
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    write_json(
        run_dir / "run.spec.json",
        {
            "command_sha256": sha256_text(template),
            "max_compute_tokens": max_compute_tokens,
            "max_tokens": max_tokens,
            "max_tool_calls": max_tool_calls,
            "model": model,
            "objective": f"Molecular Gastronomy trial: {tag}",
            "phase": phase,
            "safe_mode_required": is_claude,
            "timeout_seconds": timeout_seconds,
        },
    )
    command = _format_cook_command(
        template,
        checkout=checkout,
        run_dir=run_dir,
        model=model,
        max_compute_tokens=max_compute_tokens,
        max_tokens=max_tokens,
        max_tool_calls=max_tool_calls,
        timeout_seconds=timeout_seconds,
        is_claude=is_claude,
    )
    env = _safe_model_environment()
    env.update(
        {
            "MOLGAS_CHECKOUT": str(Path(checkout).resolve()),
            "MOLGAS_MAX_COMPUTE_TOKENS": str(max_compute_tokens),
            "MOLGAS_MAX_TOKENS": str(max_tokens),
            "MOLGAS_MAX_TOOL_CALLS": str(max_tool_calls),
            "MOLGAS_MODEL": model,
            "MOLGAS_OUTPUT_FILE": str((run_dir / "final.txt").resolve()),
            "MOLGAS_PROMPT_FILE": str((run_dir / "prompt.txt").resolve()),
            "MOLGAS_RUN_DIR": str(run_dir.resolve()),
            "MOLGAS_TIMEOUT_SECONDS": str(timeout_seconds),
            "MOLGAS_USAGE_FILE": str((run_dir / "usage.json").resolve()),
        }
    )

    started = time.monotonic()
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stdout_file, (
        tempfile.TemporaryFile(mode="w+", encoding="utf-8")
    ) as stderr_file:
        process = subprocess.Popen(
            command,
            cwd=str(checkout),
            env=env,
            shell=True,
            executable="/bin/bash",
            stdin=subprocess.PIPE,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            start_new_session=True,
            preexec_fn=_limit_cook_file_size,
        )
        timed_out = False
        try:
            process.communicate(prompt, timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
        stdout, stdout_truncated = _read_bounded(stdout_file)
        stderr, stderr_truncated = _read_bounded(stderr_file)
    wall_seconds = time.monotonic() - started

    final_path = run_dir / "final.txt"
    final_too_large = (
        final_path.exists() and final_path.stat().st_size > _MAX_CAPTURE_BYTES
    )
    if final_too_large:
        final_text = "[BLOCKED: final response exceeded retention limit]\n"
    elif final_path.exists():
        final_text = final_path.read_text(encoding="utf-8", errors="replace")
    else:
        final_text = stdout
    blocked = False
    try:
        assert_no_secret_like_text(final_text, label=f"{tag} response")
    except ValueError:
        blocked = True
        final_text = "[BLOCKED: response matched a secret-like value]\n"
    if final_too_large or (stdout_truncated and not final_path.exists()):
        blocked = True
    final_path.write_text(final_text, encoding="utf-8")
    artifact_violations = _screen_run_artifacts(run_dir)
    usage_path = run_dir / "usage.json"
    usage = (
        None
        if any(item.startswith("usage.json:") for item in artifact_violations)
        else _numeric_usage(usage_path)
    )
    cap_violations = []
    if usage is not None:
        for field, cap in (
            ("compute_tokens", max_compute_tokens),
            ("total_tokens", max_tokens),
            ("tool_calls", max_tool_calls),
        ):
            if usage.get(field, 0) > cap:
                cap_violations.append(
                    f"{field}={usage[field]} exceeded declared cap {cap}"
                )
    if usage_path.exists():
        usage_path.unlink()
    if usage is not None:
        write_json(run_dir / "usage.normalized.json", usage)
    execution = {
        "artifact_screen_violations": artifact_violations,
        "blocked_secret_like_output": blocked,
        "cap_violations": cap_violations,
        "command_sha256": sha256_text(template),
        "finished_at": utc_now(),
        "max_compute_tokens": max_compute_tokens,
        "max_tokens": max_tokens,
        "max_tool_calls": max_tool_calls,
        "model": model,
        "phase": phase,
        "returncode": process.returncode,
        "safe_mode": is_claude,
        "stderr_sha256": sha256_text(stderr or ""),
        "stderr_truncated": stderr_truncated,
        "stdout_sha256": sha256_text(stdout or ""),
        "stdout_truncated": stdout_truncated,
        "timed_out": timed_out,
        "token_usage": usage,
        "wall_seconds": wall_seconds,
    }
    write_json(run_dir / "execution.json", execution)
    return {**execution, "final_text": final_text}


def run_command(
    command: list[str | Path],
    *,
    cwd: Path | None = None,
    check: bool = True,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        [str(part) for part in command],
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if check and result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): "
            f"{' '.join(shlex.quote(str(part)) for part in command)}\n"
            f"stdout tail: {(result.stdout or '')[-1500:]}\n"
            f"stderr tail: {(result.stderr or '')[-1500:]}"
        )
    return result


def _safe_remove_tree(path: Path, owned_root: Path) -> None:
    path = path.resolve()
    owned_root = owned_root.resolve()
    if path == owned_root or owned_root not in path.parents:
        raise ValueError(f"refusing to remove path outside owned scratch root: {path}")
    if path.exists():
        shutil.rmtree(path)


def fresh_checkout(task: dict, *, destination: Path, mirrors: Path) -> Path:
    """Create a detached checkout, using one network clone per repository."""
    destination = Path(destination)
    mirrors = Path(mirrors)
    mirrors.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _safe_remove_tree(destination, destination.parent)

    mirror = mirrors / (task["repo"].replace("/", "__") + ".git")
    if not mirror.exists():
        run_command(
            ["git", "clone", "--quiet", "--mirror", f"https://github.com/{task['repo']}", mirror]
        )
    run_command(["git", "clone", "--quiet", mirror, destination])
    run_command(["git", "checkout", "--quiet", "--detach", task["base_commit"]], cwd=destination)
    return destination


def is_test_path(path: str) -> bool:
    parts = path.lower().replace("\\", "/").split("/")
    base = parts[-1]
    if base.startswith("test_") or base.endswith("_test.py") or base == "conftest.py":
        return True
    return any(part in {"test", "tests"} for part in parts[:-1])


def capture_source_patch(checkout: Path, base_commit: str) -> tuple[str, list[str]]:
    """Capture all source changes relative to base, excluding public-test paths."""
    run_command(["git", "add", "-A"], cwd=checkout)
    names = run_command(
        ["git", "diff", "--cached", "--name-only", "-z", base_commit], cwd=checkout
    ).stdout.split("\0")
    changed = [name for name in names if name]
    excluded = sorted(path for path in changed if is_test_path(path))
    source_paths = [path for path in changed if path not in excluded]
    if not source_paths:
        return "", excluded
    patch = run_command(
        [
            "git",
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            base_commit,
            "--",
            *source_paths,
        ],
        cwd=checkout,
    ).stdout
    return patch, excluded


def apply_patch(checkout: Path, patch_path: Path) -> None:
    if Path(patch_path).stat().st_size == 0:
        return
    run_command(["git", "apply", "--index", "--binary", Path(patch_path)], cwd=checkout)


def extract_json_object(text: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    for index, character in enumerate(text):
        if character != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def normalize_decision(text: str) -> tuple[dict[str, Any], list[str]]:
    raw = extract_json_object(text)
    errors: list[str] = []
    if raw is None:
        raw = {}
        errors.append("response contained no JSON object")
    lowered = {str(key).lower(): value for key, value in raw.items()}
    decision = str(lowered.get("decision", "")).upper()
    if decision not in {"SERVE", "REFUSE"}:
        errors.append("decision must be SERVE or REFUSE")
        decision = "REFUSE"
    p_pass = lowered.get("p_pass")
    if isinstance(p_pass, bool) or not isinstance(p_pass, (int, float)):
        errors.append("P_PASS must be a number in [0, 1]")
        p_pass = 0.0
    p_pass = float(p_pass)
    if not 0.0 <= p_pass <= 1.0:
        errors.append("P_PASS must be a number in [0, 1]")
        p_pass = min(1.0, max(0.0, p_pass))
    evidence = lowered.get("evidence", [])
    if isinstance(evidence, str):
        evidence = [evidence]
    if (
        not isinstance(evidence, list)
        or not evidence
        or not all(isinstance(item, str) and item.strip() for item in evidence)
    ):
        errors.append("evidence must be a non-empty string or list of strings")
        evidence = []
    deviations = lowered.get("deviations", [])
    if isinstance(deviations, str):
        deviations = [deviations]
    if not isinstance(deviations, list) or not all(
        isinstance(item, str) for item in deviations
    ):
        errors.append("deviations must be a string or list of strings")
        deviations = []
    adherence = lowered.get("plan_adherence")
    if adherence is not None and not isinstance(adherence, bool):
        errors.append("plan_adherence must be boolean when present")
        adherence = None
    return (
        {
            "decision": decision,
            "deviations": deviations,
            "evidence": evidence,
            "p_pass": p_pass,
            "plan_adherence": adherence,
            "raw_response_sha256": sha256_text(text),
        },
        errors,
    )


def swebench_command(
    *,
    instance_ids: list[str],
    predictions_path: str | Path,
    run_id: str,
    max_workers: int,
    timeout_seconds: int,
    cache_level: str = "env",
) -> list[str | Path]:
    """Return the direct package invocation mirrored from the reference harness."""
    return [
        VENV_PY,
        "-m",
        "swebench.harness.run_evaluation",
        "-d",
        DATASET_NAME,
        "-s",
        DATASET_SPLIT,
        "-i",
        *instance_ids,
        "-p",
        predictions_path,
        "--max_workers",
        str(max_workers),
        "-t",
        str(timeout_seconds),
        "-id",
        run_id,
        "--cache_level",
        cache_level,
    ]


def find_swebench_report(directory: Path, run_id: str) -> dict[str, Any]:
    candidates = sorted(Path(directory).glob(f"*.{run_id}.json"))
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one SWE-bench report for {run_id}, found {len(candidates)}"
        )
    return load_json(candidates[0])


def completed_verdicts(
    report: dict[str, Any],
    instance_ids: list[str],
    *,
    accept_empty_as_unresolved: bool = False,
) -> dict[str, bool]:
    requested = set(instance_ids)
    resolved = set(report.get("resolved_ids", []))
    unresolved = set(report.get("unresolved_ids", []))
    if accept_empty_as_unresolved:
        unresolved |= set(report.get("empty_patch_ids", []))
    error = set(report.get("error_ids", []))
    classified = resolved | unresolved
    if error & requested:
        raise RuntimeError(f"SWE-bench errors: {sorted(error & requested)}")
    missing = requested - classified
    if missing:
        raise RuntimeError(f"SWE-bench did not classify: {sorted(missing)}")
    if (resolved & unresolved) & requested:
        raise RuntimeError("SWE-bench report classifies an instance twice")
    return {instance_id: instance_id in resolved for instance_id in instance_ids}
