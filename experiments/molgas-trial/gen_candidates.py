#!/usr/bin/env python3
"""Generate and freeze two neutral candidate patches per selected task."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from common import (
    DEFAULT_COOK_CMD,
    DEFAULT_COOK_MODEL,
    assert_no_secret_like_text,
    capture_source_patch,
    fresh_checkout,
    load_json,
    payload_sha256,
    run_cook,
    sha256_file,
    sha256_text,
    utc_now,
    validate_cook_template,
    validate_cook_model,
    validate_task_bank,
    write_json,
)

HERE = Path(__file__).resolve().parent
DEFAULT_TASKS = HERE / "tasks.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "candidates.json"
DEFAULT_WORK = Path("/tmp/molgas-trial-candidates")
CANDIDATES_PER_TASK = 2

CANDIDATE_PROMPT = """\
You are producing a neutral candidate patch for a SWE-bench issue. Work only in
the repository that is your current directory. It is checked out at the issue's
base commit.

Rules:
1. Diagnose and implement the smallest complete source-code fix for the issue.
2. You may inspect and run the repository's public tests, but do not edit tests.
3. Do not use hidden tests, a gold patch, SWE-bench FAIL_TO_PASS/PASS_TO_PASS,
   files outside this checkout, the web, or the network.
4. Do not read or disclose credentials, .env files, or secrets.
5. Do not commit. Leave the proposed source changes in the working tree.
6. Use the same effort budget for every task; stop when the fix is ready.

ISSUE:
{problem_statement}
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Call one fixed neutral cook twice per task and freeze every source "
            "patch plus its SHA-256 hash. Does not run SWE-bench grading."
        )
    )
    parser.add_argument(
        "--cook-cmd",
        default=os.environ.get("COOK_CMD", DEFAULT_COOK_CMD),
        help="Shell template; see README. Defaults to COOK_CMD, then a placeholder.",
    )
    parser.add_argument(
        "--cook-model",
        default=os.environ.get("COOK_MODEL", DEFAULT_COOK_MODEL),
        help="Exact model identifier passed to every generation call.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-compute-tokens", type=int, default=16000)
    parser.add_argument("--max-tokens", type=int, default=16000)
    parser.add_argument("--max-tool-calls", type=int, default=64)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    return parser


def candidate_key(instance_id: str, candidate_index: int) -> str:
    return f"{instance_id}::candidate-{candidate_index}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    bank = load_json(args.tasks)
    tasks = validate_task_bank(bank, expected_count=30)
    total = len(tasks) * CANDIDATES_PER_TASK
    if args.dry_run:
        print("DRY RUN -- no clones and no cook calls.")
        print(f"would generate {total} candidates ({CANDIDATES_PER_TASK} x {len(tasks)})")
        print(f"tasks_sha256={sha256_file(args.tasks)}")
        print(f"output={args.output}")
        print(f"work_dir={args.work_dir}")
        print(f"cook_cmd_sha256={sha256_text(args.cook_cmd)}")
        print(f"cook_model={args.cook_model}")
        return 0

    is_claude = validate_cook_template(args.cook_cmd)
    cook_model = validate_cook_model(args.cook_model)
    if args.output.exists():
        raise SystemExit(f"candidate bank is already frozen: {args.output}")
    if (
        args.max_compute_tokens <= 0
        or args.max_tokens <= 0
        or args.max_tool_calls <= 0
        or args.timeout_seconds <= 0
    ):
        raise SystemExit("compute, token, tool, and timeout caps must be positive")

    artifact_root = args.output.parent
    patch_root = artifact_root / "candidate-patches"
    run_root = artifact_root / "candidate-runs"
    checkout_root = args.work_dir / "checkouts"
    mirror_root = args.work_dir / "mirrors"
    patch_root.mkdir(parents=True, exist_ok=True)
    run_root.mkdir(parents=True, exist_ok=True)
    checkout_root.mkdir(parents=True, exist_ok=True)

    candidates: list[dict] = []
    prompt_hashes: set[str] = set()
    for task in tasks:
        instance_id = task["instance_id"]
        for index in range(1, CANDIDATES_PER_TASK + 1):
            key = candidate_key(instance_id, index)
            tag = key.replace("::", "__")
            checkout = fresh_checkout(
                task,
                destination=checkout_root / tag,
                mirrors=mirror_root,
            )
            prompt = CANDIDATE_PROMPT.format(
                problem_statement=task["problem_statement"].strip()
            )
            # Hash the invariant prompt body separately from task content.
            prompt_hashes.add(sha256_text(CANDIDATE_PROMPT))
            result = run_cook(
                template=args.cook_cmd,
                checkout=checkout,
                run_dir=run_root / tag,
                prompt=prompt,
                tag=tag,
                phase="candidate_generation",
                model=cook_model,
                max_compute_tokens=args.max_compute_tokens,
                max_tokens=args.max_tokens,
                max_tool_calls=args.max_tool_calls,
                timeout_seconds=args.timeout_seconds,
            )
            failures = []
            if result["returncode"] != 0:
                failures.append(f"cook exited {result['returncode']}")
            if result["timed_out"]:
                failures.append("cook exceeded its wall-time cap")
            if result["blocked_secret_like_output"]:
                failures.append("cook output was blocked by the secret screen")
            if result["artifact_screen_violations"]:
                failures.append("cook artifacts failed retention screening")
            if result["cap_violations"]:
                failures.extend(result["cap_violations"])
            if failures:
                raise RuntimeError(f"{key}: {'; '.join(failures)}")
            patch, excluded_tests = capture_source_patch(
                checkout, task["base_commit"]
            )
            if not patch.strip():
                raise RuntimeError(f"{key}: cook produced an empty source patch")
            assert_no_secret_like_text(patch, label=f"{key} candidate patch")
            patch_dir = patch_root / instance_id
            patch_dir.mkdir(parents=True, exist_ok=True)
            patch_path = patch_dir / f"candidate-{index}.patch"
            if patch_path.exists():
                raise RuntimeError(f"refusing to overwrite candidate: {patch_path}")
            patch_path.write_text(patch, encoding="utf-8")
            candidates.append(
                {
                    "candidate_id": key,
                    "candidate_index": index,
                    "excluded_public_test_paths": excluded_tests,
                    "generated_at": result["finished_at"],
                    "instance_id": instance_id,
                    "patch_bytes": patch_path.stat().st_size,
                    "patch_path": str(patch_path.relative_to(artifact_root)),
                    "patch_sha256": sha256_file(patch_path),
                    "run": {
                        "artifact_screen_violations": result[
                            "artifact_screen_violations"
                        ],
                        "blocked_secret_like_output": result[
                            "blocked_secret_like_output"
                        ],
                        "cap_violations": result["cap_violations"],
                        "returncode": result["returncode"],
                        "timed_out": result["timed_out"],
                        "token_usage": result["token_usage"],
                        "wall_seconds": result["wall_seconds"],
                    },
                }
            )
            print(
                f"{len(candidates):02d}/{total}: {key} "
                f"bytes={patch_path.stat().st_size} sha256={sha256_file(patch_path)}"
            )

    if len(candidates) != total:
        raise AssertionError("candidate generation did not produce the fixed bank size")
    identity = [
        {
            "candidate_id": item["candidate_id"],
            "instance_id": item["instance_id"],
            "patch_sha256": item["patch_sha256"],
        }
        for item in candidates
    ]
    manifest = {
        "candidate_bank_sha256": payload_sha256(identity),
        "candidates": candidates,
        "candidates_per_task": CANDIDATES_PER_TASK,
        "cook": {
            "command_sha256": sha256_text(args.cook_cmd),
            "max_compute_tokens": args.max_compute_tokens,
            "max_tokens": args.max_tokens,
            "max_tool_calls": args.max_tool_calls,
            "model": cook_model,
            "prompt_template_sha256": prompt_hashes.pop(),
            "safe_mode": is_claude,
            "timeout_seconds": args.timeout_seconds,
        },
        "frozen_at": utc_now(),
        "schema_version": 1,
        "task_bank_file_sha256": sha256_file(args.tasks),
        "task_bank_sha256": bank["task_bank_sha256"],
    }
    write_json(args.output, manifest)
    print(f"froze {len(candidates)} candidates to {args.output}")
    print("candidate_bank_sha256:", manifest["candidate_bank_sha256"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
