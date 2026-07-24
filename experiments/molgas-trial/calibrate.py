#!/usr/bin/env python3
"""Calibrate every selected SWE-bench ruler with repeated gold/base controls."""

from __future__ import annotations

import argparse
import json
import platform
import sys
import tempfile
from pathlib import Path
from typing import Any

from common import (
    DATASET_NAME,
    DATASET_SPLIT,
    VENV_PY,
    find_swebench_report,
    load_json,
    payload_sha256,
    run_command,
    sha256_file,
    sha256_text,
    swebench_command,
    utc_now,
    validate_task_bank,
    write_json,
)

HERE = Path(__file__).resolve().parent
DEFAULT_TASKS = HERE / "tasks.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "calibration.json"
CONTROL_REPEATS = 2

# SWE-bench does not execute predictions whose model_patch is "".  This patch
# creates a zero-byte inert file so the base behavior is genuinely graded.
NOOP_BASE_PATCH = """\
diff --git a/.molgas-empty-control b/.molgas-empty-control
new file mode 100644
index 0000000..e69de29
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run gold twice and an inert base-equivalent patch twice per task "
            "through swebench.harness.run_evaluation."
        )
    )
    parser.add_argument("--cache-level", choices=("env", "instance"), default="instance")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--test-timeout-seconds", type=int, default=1800)
    parser.add_argument(
        "--temp-root",
        type=Path,
        default=Path("/tmp"),
        help="Gold predictions and evaluator logs live here and are deleted on exit.",
    )
    return parser


def report_outcomes(
    report: dict[str, Any], instance_ids: list[str]
) -> dict[str, bool | None]:
    resolved = set(report.get("resolved_ids", []))
    unresolved = set(report.get("unresolved_ids", []))
    errors = set(report.get("error_ids", []))
    empty = set(report.get("empty_patch_ids", []))
    outcomes: dict[str, bool | None] = {}
    for instance_id in instance_ids:
        memberships = sum(
            instance_id in group for group in (resolved, unresolved, errors, empty)
        )
        if memberships != 1:
            outcomes[instance_id] = None
        elif instance_id in resolved:
            outcomes[instance_id] = True
        elif instance_id in unresolved:
            outcomes[instance_id] = False
        else:
            outcomes[instance_id] = None
    return outcomes


def image_name(instance_id: str) -> str:
    key = f"swebench/sweb.eval.x86_64.{instance_id.lower()}:latest"
    return key.replace("__", "_1776_")


def inspect_images(instance_ids: list[str]) -> dict[str, dict[str, Any]]:
    frozen: dict[str, dict[str, Any]] = {}
    for instance_id in instance_ids:
        name = image_name(instance_id)
        result = run_command(["docker", "image", "inspect", name], check=False)
        if result.returncode:
            raise RuntimeError(
                f"could not freeze image identity for {instance_id} ({name}): "
                f"{(result.stderr or '')[-500:]}"
            )
        raw = json.loads(result.stdout)
        if not isinstance(raw, list) or len(raw) != 1:
            raise RuntimeError(f"unexpected docker inspect output for {name}")
        item = raw[0]
        frozen[instance_id] = {
            "architecture": item.get("Architecture"),
            "image_id": item.get("Id"),
            "os": item.get("Os"),
            "repo_digests": sorted(item.get("RepoDigests") or []),
            "repo_tags": sorted(item.get("RepoTags") or []),
            "requested_name": name,
        }
        if not frozen[instance_id]["image_id"]:
            raise RuntimeError(f"docker inspect returned no immutable image ID for {name}")
    return frozen


def swebench_version() -> str:
    result = run_command(
        [
            VENV_PY,
            "-c",
            "from importlib.metadata import version; print(version('swebench'))",
        ]
    )
    return result.stdout.strip()


def run_control(
    *,
    kind: str,
    repeat: int,
    instance_ids: list[str],
    root: Path,
    max_workers: int,
    test_timeout_seconds: int,
    cache_level: str,
) -> dict[str, bool | None]:
    run_id = f"molgas-cal-{kind}-r{repeat}"
    run_root = root / run_id
    run_root.mkdir()
    if kind == "gold":
        predictions: str | Path = "gold"
    else:
        predictions = run_root / "base-predictions.json"
        model = f"calibration-base-r{repeat}"
        write_json(
            predictions,
            [
                {
                    "instance_id": instance_id,
                    "model_name_or_path": model,
                    "model_patch": NOOP_BASE_PATCH,
                }
                for instance_id in instance_ids
            ],
        )
    command = swebench_command(
        instance_ids=instance_ids,
        predictions_path=predictions,
        run_id=run_id,
        max_workers=max_workers,
        timeout_seconds=test_timeout_seconds,
        cache_level=cache_level,
    )
    print(f"running {kind} control repeat {repeat}/{CONTROL_REPEATS}")
    result = run_command(command, cwd=run_root, check=False)
    if result.returncode:
        raise RuntimeError(
            f"SWE-bench {kind} repeat {repeat} failed ({result.returncode}): "
            f"{(result.stderr or '')[-1200:]}"
        )
    return report_outcomes(find_swebench_report(run_root, run_id), instance_ids)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    bank = load_json(args.tasks)
    tasks = validate_task_bank(bank, expected_count=30)
    ids = [task["instance_id"] for task in tasks]
    if args.dry_run:
        print("DRY RUN -- no Docker or SWE-bench evaluation.")
        for repeat in range(1, CONTROL_REPEATS + 1):
            for kind in ("gold", "base"):
                prediction = "gold" if kind == "gold" else "<temporary-base-predictions.json>"
                command = swebench_command(
                    instance_ids=ids,
                    predictions_path=prediction,
                    run_id=f"molgas-cal-{kind}-r{repeat}",
                    max_workers=args.max_workers,
                    timeout_seconds=args.test_timeout_seconds,
                    cache_level=args.cache_level,
                )
                print(" ".join(str(part) for part in command))
        print("would inspect and freeze 30 immutable Docker image IDs")
        return 0

    if args.output.exists():
        raise SystemExit(f"calibration is already frozen: {args.output}")
    if not VENV_PY.is_file():
        raise SystemExit(f"SWE-bench venv interpreter not found: {VENV_PY}")
    if args.max_workers <= 0 or args.test_timeout_seconds <= 0:
        raise SystemExit("worker and timeout values must be positive")
    args.temp_root.mkdir(parents=True, exist_ok=True)

    controls = {
        instance_id: {"gold_resolved": [], "base_resolved": []}
        for instance_id in ids
    }
    # This directory contains all evaluator logs (including gold material) and
    # is removed before calibration.json is written.
    with tempfile.TemporaryDirectory(
        prefix="molgas-calibration-", dir=args.temp_root
    ) as temporary:
        root = Path(temporary)
        for repeat in range(1, CONTROL_REPEATS + 1):
            gold = run_control(
                kind="gold",
                repeat=repeat,
                instance_ids=ids,
                root=root,
                max_workers=args.max_workers,
                test_timeout_seconds=args.test_timeout_seconds,
                cache_level=args.cache_level,
            )
            base = run_control(
                kind="base",
                repeat=repeat,
                instance_ids=ids,
                root=root,
                max_workers=args.max_workers,
                test_timeout_seconds=args.test_timeout_seconds,
                cache_level=args.cache_level,
            )
            for instance_id in ids:
                controls[instance_id]["gold_resolved"].append(gold[instance_id])
                controls[instance_id]["base_resolved"].append(base[instance_id])
        images = inspect_images(ids)

    task_results: list[dict[str, Any]] = []
    calibrated_ids: list[str] = []
    for task in tasks:
        instance_id = task["instance_id"]
        gold = controls[instance_id]["gold_resolved"]
        base = controls[instance_id]["base_resolved"]
        passed = gold == [True, True] and base == [False, False]
        if passed:
            calibrated_ids.append(instance_id)
        task_results.append(
            {
                "base_resolved": base,
                "gold_resolved": gold,
                "image": images[instance_id],
                "instance_id": instance_id,
                "passes": passed,
            }
        )
    calibrated_tasks = [
        task for task in tasks if task["instance_id"] in set(calibrated_ids)
    ]
    identity = [
        {
            "base_resolved": result["base_resolved"],
            "gold_resolved": result["gold_resolved"],
            "image_id": result["image"]["image_id"],
            "instance_id": result["instance_id"],
            "passes": result["passes"],
        }
        for result in task_results
    ]
    manifest = {
        "calibrated_instance_ids": calibrated_ids,
        "calibrated_tasks": calibrated_tasks,
        "calibration_sha256": payload_sha256(identity),
        "control_repeats": CONTROL_REPEATS,
        "dataset": DATASET_NAME,
        "excluded_instance_ids": [
            instance_id for instance_id in ids if instance_id not in set(calibrated_ids)
        ],
        "finished_at": utc_now(),
        "no_op_base_patch_sha256": sha256_text(NOOP_BASE_PATCH),
        "runner": {
            "cache_level": args.cache_level,
            "dataset": DATASET_NAME,
            "max_workers": args.max_workers,
            "platform": platform.platform(),
            "python": str(VENV_PY),
            "split": DATASET_SPLIT,
            "swebench_version": swebench_version(),
            "test_timeout_seconds": args.test_timeout_seconds,
        },
        "schema_version": 1,
        "task_bank_file_sha256": sha256_file(args.tasks),
        "task_bank_sha256": bank["task_bank_sha256"],
        "task_results": task_results,
    }
    write_json(args.output, manifest)
    print(
        f"calibrated {len(calibrated_ids)}/{len(ids)} tasks; "
        f"froze result to {args.output}"
    )
    if manifest["excluded_instance_ids"]:
        print("excluded:", manifest["excluded_instance_ids"])
    print("calibration_sha256:", manifest["calibration_sha256"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
