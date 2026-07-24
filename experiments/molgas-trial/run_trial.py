#!/usr/bin/env python3
"""Run both blinded trust-decision arms, then repeatedly grade frozen candidates."""

from __future__ import annotations

import argparse
import os
import random
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from common import (
    DATASET_NAME,
    DATASET_SPLIT,
    DEFAULT_COOK_CMD,
    DEFAULT_COOK_MODEL,
    VENV_PY,
    apply_patch,
    canonical_json,
    completed_verdicts,
    directory_sha256,
    extract_json_object,
    find_swebench_report,
    fresh_checkout,
    load_json,
    normalize_decision,
    payload_sha256,
    run_command,
    run_cook,
    sha256_file,
    sha256_text,
    swebench_command,
    task_map,
    utc_now,
    validate_cook_template,
    validate_cook_model,
    validate_task_bank,
    write_json,
)

HERE = Path(__file__).resolve().parent
DEFAULT_TASKS = HERE / "tasks.json"
DEFAULT_CANDIDATES = HERE / "artifacts" / "candidates.json"
DEFAULT_CALIBRATION = HERE / "artifacts" / "calibration.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "trial"
DEFAULT_WORK = Path("/tmp/molgas-trial-run")
DEFAULT_SEED = 20260725
ORACLE_REPEATS = 2

PLAN_PROMPT = """\
You are making a candidate-blind validation plan for a SWE-bench issue. You see
the issue and the base repository only. NO candidate patch has been provided or
applied. Inspect the repository and public tests as needed, but do not edit it.

Freeze a falsifiable plan before any candidate is revealed. Return exactly one
JSON object with:
{
  "atomic_success_claims": ["..."],
  "failure_modes": ["..."],
  "checks": [
    {
      "id": "C1",
      "procedure": "...",
      "pass_condition": "...",
      "failure_mode_covered": "..."
    }
  ],
  "required_controls": {
    "positive": ["..."],
    "negative": ["..."]
  },
  "acceptance_threshold": "...",
  "refusal_conditions": ["..."]
}

Make procedures runnable and outcomes measurable. The acceptance threshold must
state exactly which checks and controls must pass. Do not mention or infer a
candidate. Do not use hidden tests, gold, test_patch, FAIL_TO_PASS/PASS_TO_PASS,
the web, network, files outside this checkout, credentials, or secrets.

ISSUE:
{problem_statement}
"""

ADHOC_PROMPT = """\
Investigate whether this patch solves the issue; self-review once; report
P_PASS (0-1), SERVE/REFUSE, and evidence.

The frozen candidate is applied in this isolated checkout and reproduced below.
You may inspect the repository and run its public tests. Do not alter the
candidate or source files. Do not use hidden tests, gold, test_patch,
FAIL_TO_PASS/PASS_TO_PASS, the web, network, files outside this checkout,
credentials, or secrets.

Return exactly one JSON object:
{
  "P_PASS": 0.0,
  "decision": "SERVE or REFUSE",
  "evidence": ["command/check and observed result", "..."]
}

ISSUE:
{problem_statement}

FROZEN CANDIDATE PATCH:
{candidate_patch}
"""

MOLGAS_PROMPT = """\
The candidate is now revealed and applied in this isolated checkout. Execute
the frozen candidate-blind plan exactly. You may build ephemeral probes and run
public tests. Do not alter the candidate or source files.

SERVE only if the frozen acceptance threshold passes. Otherwise REFUSE.
Disclose every deviation; never rewrite a claim, check, control, threshold, or
refusal condition. Do not use hidden tests, gold, test_patch,
FAIL_TO_PASS/PASS_TO_PASS, the web, network, files outside this checkout,
credentials, or secrets.

Return exactly one JSON object:
{
  "P_PASS": 0.0,
  "decision": "SERVE or REFUSE",
  "evidence": ["check/control, command, and observed result", "..."],
  "plan_adherence": true,
  "deviations": []
}

ISSUE:
{problem_statement}

FROZEN PLAN (SHA-256 {plan_sha256}, frozen {plan_frozen_at}):
{plan}

FROZEN CANDIDATE PATCH:
{candidate_patch}
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run candidate-blind B plans, randomized A/B decisions, and repeated "
            "SWE-bench oracle grading over calibrated tasks."
        )
    )
    parser.add_argument("--calibration", type=Path, default=DEFAULT_CALIBRATION)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument(
        "--cook-cmd",
        default=os.environ.get("COOK_CMD", DEFAULT_COOK_CMD),
        help="One shell template for both arms; see README.",
    )
    parser.add_argument(
        "--cook-model",
        default=os.environ.get("COOK_MODEL", DEFAULT_COOK_MODEL),
        help="Exact model identifier bound to every A and B call.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--phase",
        choices=("all", "plans", "decisions", "oracle"),
        default="all",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--test-timeout-seconds", type=int, default=1800)
    parser.add_argument("--total-compute-token-cap", type=int, default=16000)
    parser.add_argument("--total-timeout-seconds", type=int, default=3600)
    parser.add_argument("--total-token-cap", type=int, default=16000)
    parser.add_argument("--total-tool-call-cap", type=int, default=64)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    return parser


def candidate_identity(candidate: dict[str, Any]) -> dict[str, str]:
    return {
        "candidate_id": candidate["candidate_id"],
        "instance_id": candidate["instance_id"],
        "patch_sha256": candidate["patch_sha256"],
    }


def validate_candidate_bank(
    manifest: dict[str, Any],
    manifest_path: Path,
    task_bank_hash: str,
    selected_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    candidates = manifest.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 60:
        raise ValueError("candidate bank must contain exactly 60 candidates")
    if manifest.get("task_bank_sha256") != task_bank_hash:
        raise ValueError("candidate bank belongs to a different task bank")
    if manifest.get("candidates_per_task") != 2:
        raise ValueError("candidate bank must contain two candidates per task")
    if manifest.get("candidate_bank_sha256") != payload_sha256(
        [candidate_identity(item) for item in candidates]
    ):
        raise ValueError("candidate_bank_sha256 does not match candidate identities")
    counts = Counter(item.get("instance_id") for item in candidates)
    if set(counts.values()) != {2} or len(counts) != 30:
        raise ValueError("candidate bank does not have exactly two patches per task")
    if selected_ids is not None and set(counts) != selected_ids:
        raise ValueError("candidate bank task IDs do not exactly match the selected bank")
    seen: set[str] = set()
    indices: dict[str, set[int]] = defaultdict(set)
    patch_root = manifest_path.parent.resolve()
    for item in candidates:
        if item.get("candidate_id") in seen:
            raise ValueError("duplicate candidate_id")
        seen.add(item["candidate_id"])
        expected_id = (
            f"{item.get('instance_id')}::candidate-{item.get('candidate_index')}"
        )
        if item.get("candidate_id") != expected_id:
            raise ValueError(f"candidate identity is inconsistent: {item}")
        indices[item["instance_id"]].add(item["candidate_index"])
        patch_path = (manifest_path.parent / item["patch_path"]).resolve()
        if patch_root != patch_path.parent and patch_root not in patch_path.parents:
            raise ValueError(f"candidate patch escapes artifact root: {patch_path}")
        if not patch_path.is_file():
            raise ValueError(f"missing frozen patch: {patch_path}")
        if sha256_file(patch_path) != item["patch_sha256"]:
            raise ValueError(f"frozen patch hash mismatch: {patch_path}")
    if any(value != {1, 2} for value in indices.values()):
        raise ValueError("each task must have candidate indices 1 and 2")
    return candidates


def validate_calibration(
    manifest: dict[str, Any], task_bank_hash: str, selected_ids: set[str]
) -> list[str]:
    if manifest.get("task_bank_sha256") != task_bank_hash:
        raise ValueError("calibration belongs to a different task bank")
    calibrated = manifest.get("calibrated_instance_ids")
    results = manifest.get("task_results")
    if not isinstance(calibrated, list) or not isinstance(results, list):
        raise ValueError("invalid calibration manifest")
    if not set(calibrated) <= selected_ids:
        raise ValueError("calibration contains an unselected task")
    by_id = {item.get("instance_id"): item for item in results}
    if len(results) != len(selected_ids) or set(by_id) != selected_ids:
        raise ValueError("calibration must report every selected task exactly once")
    expected_calibrated = []
    for item in results:
        instance_id = item["instance_id"]
        controls_pass = (
            item.get("gold_resolved") == [True, True]
            and item.get("base_resolved") == [False, False]
        )
        if item.get("passes") is not controls_pass:
            raise ValueError(f"inconsistent calibration verdict: {instance_id}")
        if not item.get("image", {}).get("image_id"):
            raise ValueError(f"ruler image was not frozen: {instance_id}")
        if controls_pass:
            expected_calibrated.append(instance_id)
    if set(calibrated) != set(expected_calibrated):
        raise ValueError("calibrated set must contain all and only passing rulers")
    if set(manifest.get("excluded_instance_ids", [])) != selected_ids - set(calibrated):
        raise ValueError("calibration exclusion set is inconsistent")
    identity = [
        {
            "base_resolved": item.get("base_resolved"),
            "gold_resolved": item.get("gold_resolved"),
            "image_id": item.get("image", {}).get("image_id"),
            "instance_id": item.get("instance_id"),
            "passes": item.get("passes"),
        }
        for item in results
    ]
    if manifest.get("calibration_sha256") != payload_sha256(identity):
        raise ValueError("calibration_sha256 does not match task results")
    return calibrated


def validate_plan(text: str) -> tuple[dict[str, Any], list[str]]:
    plan = extract_json_object(text)
    errors: list[str] = []
    if plan is None:
        return {}, ["plan response contained no JSON object"]
    for field in (
        "atomic_success_claims",
        "failure_modes",
        "refusal_conditions",
    ):
        value = plan.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{field} must be a non-empty list")
        elif any(not isinstance(item, str) or not item.strip() for item in value):
            errors.append(f"{field} must contain only non-empty strings")
    checks = plan.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty list")
    else:
        check_ids = []
        required_check_fields = (
            "id",
            "procedure",
            "pass_condition",
            "failure_mode_covered",
        )
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{index}] must be an object")
                continue
            for field in required_check_fields:
                value = check.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(
                        f"checks[{index}].{field} must be a non-empty string"
                    )
            if isinstance(check.get("id"), str):
                check_ids.append(check["id"].strip())
        if len(check_ids) != len(set(check_ids)):
            errors.append("check IDs must be unique")
    controls = plan.get("required_controls")
    if not isinstance(controls, dict):
        errors.append("required_controls must be an object")
    else:
        for polarity in ("positive", "negative"):
            values = controls.get(polarity)
            if not isinstance(values, list) or not values:
                errors.append(f"required_controls.{polarity} must be a non-empty list")
            elif any(not isinstance(item, str) or not item.strip() for item in values):
                errors.append(
                    f"required_controls.{polarity} must contain non-empty strings"
                )
    threshold = plan.get("acceptance_threshold")
    if not isinstance(threshold, str) or not threshold.strip():
        errors.append("acceptance_threshold must be a non-empty string")
    return plan, errors


def split_cap(total: int) -> tuple[int, int]:
    plan = total // 2
    return plan, total - plan


def initialize_trial(
    *,
    args: argparse.Namespace,
    task_bank: dict[str, Any],
    candidate_manifest: dict[str, Any],
    calibration: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "trial-manifest.json"
    order_path = output / "order.json"
    config = {
        "calibration_file_sha256": sha256_file(args.calibration),
        "candidate_bank_sha256": candidate_manifest["candidate_bank_sha256"],
        "candidates_file_sha256": sha256_file(args.candidates),
        "common_py_sha256": sha256_file(HERE / "common.py"),
        "cook_command_sha256": sha256_text(args.cook_cmd),
        "oracle_repeats": ORACLE_REPEATS,
        "pre_registration_sha256": sha256_file(HERE / "PRE-REGISTRATION.md"),
        "protocol_prompts_sha256": payload_sha256(
            [PLAN_PROMPT, ADHOC_PROMPT, MOLGAS_PROMPT]
        ),
        "run_trial_py_sha256": sha256_file(Path(__file__)),
        "score_py_sha256": sha256_file(HERE / "score.py"),
        "seed": args.seed,
        "task_bank_sha256": task_bank["task_bank_sha256"],
        "test_timeout_seconds": args.test_timeout_seconds,
        "total_timeout_seconds_per_artifact": args.total_timeout_seconds,
        "total_token_cap_per_artifact": args.total_token_cap,
    }
    config_hash = payload_sha256(config)
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        if manifest.get("config_sha256") != config_hash:
            raise ValueError("existing trial uses a different frozen configuration")
        if manifest.get("included_candidate_ids") != [
            item["candidate_id"] for item in candidates
        ] or manifest.get("included_instance_ids") != calibration[
            "calibrated_instance_ids"
        ]:
            raise ValueError("existing trial manifest has a changed inclusion set")
    else:
        manifest = {
            "calibration_sha256": calibration["calibration_sha256"],
            "config": config,
            "config_sha256": config_hash,
            "created_at": utc_now(),
            "included_candidate_ids": [item["candidate_id"] for item in candidates],
            "included_instance_ids": calibration["calibrated_instance_ids"],
            "schema_version": 1,
        }
        write_json(manifest_path, manifest)

    expected_cells = [
        {"arm": arm, "candidate_id": item["candidate_id"]}
        for item in candidates
        for arm in ("A", "B")
    ]
    if order_path.exists():
        order = load_json(order_path)
        actual_decisions = order.get("decision_order", [])
        actual_plans = order.get("plan_order", [])
        if (
            len(actual_decisions) != len(expected_cells)
            or {
                (item["arm"], item["candidate_id"]) for item in actual_decisions
            }
            != {(item["arm"], item["candidate_id"]) for item in expected_cells}
            or len(actual_plans) != len(candidates)
            or set(actual_plans) != {item["candidate_id"] for item in candidates}
            or order.get("order_sha256")
            != payload_sha256(
                {
                    "decision_order": actual_decisions,
                    "plan_order": actual_plans,
                }
            )
        ):
            raise ValueError("existing randomized decision order has wrong cells")
    else:
        rng = random.Random(args.seed)
        plan_order = [item["candidate_id"] for item in candidates]
        rng.shuffle(plan_order)
        rng.shuffle(expected_cells)
        order = {
            "decision_order": expected_cells,
            "frozen_at": utc_now(),
            "plan_order": plan_order,
            "schema_version": 1,
            "seed": args.seed,
        }
        order["order_sha256"] = payload_sha256(
            {"decision_order": expected_cells, "plan_order": plan_order}
        )
        write_json(order_path, order)
    return manifest, order


def frozen_patch(
    candidate: dict[str, Any], candidate_manifest_path: Path
) -> tuple[Path, str]:
    path = candidate_manifest_path.parent / candidate["patch_path"]
    if sha256_file(path) != candidate["patch_sha256"]:
        raise RuntimeError(f"candidate changed after freezing: {path}")
    return path, path.read_text(encoding="utf-8")


def fail_closed_decision(
    normalized: dict[str, Any], errors: list[str], execution: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    failures = list(errors)
    if execution.get("returncode") != 0:
        failures.append(f"cook exited {execution.get('returncode')}")
    if execution.get("timed_out"):
        failures.append("cook exceeded its wall-time cap")
    if execution.get("blocked_secret_like_output"):
        failures.append("cook output was blocked by the secret screen")
    if execution.get("artifact_screen_violations"):
        failures.append("cook artifacts failed retention screening")
    if failures:
        normalized = {
            **normalized,
            "decision": "REFUSE",
            "p_pass": 0.0,
        }
    return normalized, failures


def run_plans(
    *,
    args: argparse.Namespace,
    order: dict[str, Any],
    candidates_by_id: dict[str, dict[str, Any]],
    tasks: dict[str, dict[str, Any]],
) -> None:
    plan_tokens, _ = split_cap(args.total_token_cap)
    plan_timeout, _ = split_cap(args.total_timeout_seconds)
    plan_root = args.output_dir / "plans"
    checkout_root = args.work_dir / "plan-checkouts"
    mirrors = args.work_dir / "mirrors"
    for position, candidate_id in enumerate(order["plan_order"], start=1):
        record_path = plan_root / f"{candidate_id.replace('::', '__')}.json"
        if record_path.exists():
            continue
        candidate = candidates_by_id[candidate_id]
        task = tasks[candidate["instance_id"]]
        tag = f"{candidate_id.replace('::', '__')}__plan"
        checkout = fresh_checkout(
            task, destination=checkout_root / tag, mirrors=mirrors
        )
        prompt = PLAN_PROMPT.format(
            problem_statement=task["problem_statement"].strip()
        )
        result = run_cook(
            template=args.cook_cmd,
            checkout=checkout,
            run_dir=args.output_dir / "cook-runs" / tag,
            prompt=prompt,
            tag=tag,
            phase="molgas_plan",
            max_tokens=plan_tokens,
            timeout_seconds=plan_timeout,
        )
        plan, errors = validate_plan(result["final_text"])
        if result["returncode"] != 0:
            errors.append(f"cook exited {result['returncode']}")
        if result["timed_out"]:
            errors.append("cook exceeded its plan wall-time cap")
        if result["blocked_secret_like_output"]:
            errors.append("plan output was blocked by the secret screen")
        if result["artifact_screen_violations"]:
            errors.append("plan artifacts failed retention screening")
        record = {
            "candidate_id": candidate_id,
            "errors": errors,
            "execution": {
                key: result[key]
                for key in (
                    "artifact_screen_violations",
                    "blocked_secret_like_output",
                    "finished_at",
                    "max_tokens",
                    "returncode",
                    "safe_mode",
                    "timed_out",
                    "token_usage",
                    "wall_seconds",
                )
            },
            "frozen_at": utc_now(),
            "instance_id": candidate["instance_id"],
            "order_index": position,
            "plan": plan,
            "plan_sha256": sha256_text(result["final_text"]),
            "prompt_sha256": sha256_text(prompt),
            "raw_response_path": str(
                (args.output_dir / "cook-runs" / tag / "final.txt").relative_to(
                    args.output_dir
                )
            ),
            "schema_version": 1,
        }
        write_json(record_path, record)
        print(
            f"PLAN {position:02d}/{len(order['plan_order'])} {candidate_id} "
            f"errors={len(errors)}"
        )


def load_plan(output_dir: Path, candidate_id: str) -> dict[str, Any]:
    path = output_dir / "plans" / f"{candidate_id.replace('::', '__')}.json"
    if not path.is_file():
        raise RuntimeError(f"missing frozen plan: {path}")
    record = load_json(path)
    if record.get("candidate_id") != candidate_id:
        raise RuntimeError(f"frozen plan identity mismatch: {path}")
    raw_path = output_dir / record["raw_response_path"]
    if sha256_file(raw_path) != record["plan_sha256"]:
        raise RuntimeError(f"frozen plan response changed: {raw_path}")
    return record


def run_decision_cell(
    *,
    args: argparse.Namespace,
    arm: str,
    candidate: dict[str, Any],
    task: dict[str, Any],
    position: int,
) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    tag = f"{candidate_id.replace('::', '__')}__arm-{arm}"
    checkout = fresh_checkout(
        task,
        destination=args.work_dir / "decision-checkouts" / tag,
        mirrors=args.work_dir / "mirrors",
    )
    patch_path, patch_text = frozen_patch(candidate, args.candidates)
    apply_patch(checkout, patch_path)

    plan_record: dict[str, Any] | None = None
    if arm == "A":
        max_tokens = args.total_token_cap
        timeout = args.total_timeout_seconds
        prompt = ADHOC_PROMPT.format(
            problem_statement=task["problem_statement"].strip(),
            candidate_patch=patch_text or "(empty/base candidate)",
        )
        phase = "adhoc_decision"
    else:
        _, max_tokens = split_cap(args.total_token_cap)
        _, timeout = split_cap(args.total_timeout_seconds)
        plan_record = load_plan(args.output_dir, candidate_id)
        prompt = MOLGAS_PROMPT.format(
            candidate_patch=patch_text or "(empty/base candidate)",
            plan=canonical_json(plan_record["plan"]),
            plan_frozen_at=plan_record["frozen_at"],
            plan_sha256=plan_record["plan_sha256"],
            problem_statement=task["problem_statement"].strip(),
        )
        phase = "molgas_decision"

    result = run_cook(
        template=args.cook_cmd,
        checkout=checkout,
        run_dir=args.output_dir / "cook-runs" / tag,
        prompt=prompt,
        tag=tag,
        phase=phase,
        max_tokens=max_tokens,
        timeout_seconds=timeout,
    )
    normalized, errors = normalize_decision(result["final_text"])
    if arm == "B" and not isinstance(normalized.get("plan_adherence"), bool):
        errors.append("molgas decision must report boolean plan_adherence")
    normalized, errors = fail_closed_decision(normalized, errors, result)
    if arm == "B" and plan_record and plan_record["errors"]:
        errors.append("candidate-blind plan was structurally invalid")
    return {
        "arm": arm,
        "candidate_id": candidate_id,
        "candidate_patch_sha256": candidate["patch_sha256"],
        "completed_at": utc_now(),
        "decision": normalized,
        "errors": errors,
        "execution": {
            key: result[key]
            for key in (
                "artifact_screen_violations",
                "blocked_secret_like_output",
                "finished_at",
                "max_tokens",
                "returncode",
                "safe_mode",
                "timed_out",
                "token_usage",
                "wall_seconds",
            )
        },
        "instance_id": candidate["instance_id"],
        "order_index": position,
        "plan_sha256": plan_record["plan_sha256"] if plan_record else None,
        "prompt_sha256": sha256_text(prompt),
        "raw_response_path": str(
            (args.output_dir / "cook-runs" / tag / "final.txt").relative_to(
                args.output_dir
            )
        ),
        "schema_version": 1,
    }


def write_fidelity_input(
    output_dir: Path, decision_order: list[dict[str, str]]
) -> None:
    path = output_dir / "fidelity-audit-input.json"
    cells = []
    for item in decision_order:
        candidate_id = item["candidate_id"]
        arm = item["arm"]
        decision_path = (
            output_dir
            / "decisions"
            / f"{candidate_id.replace('::', '__')}__arm-{arm}.json"
        )
        record = load_json(decision_path)
        raw_response_path = output_dir / record["raw_response_path"]
        run_dir = raw_response_path.parent
        plan_record_path = (
            output_dir / "plans" / f"{candidate_id.replace('::', '__')}.json"
            if arm == "B"
            else None
        )
        plan_record = load_json(plan_record_path) if plan_record_path else None
        plan_run_dir = (
            (output_dir / plan_record["raw_response_path"]).parent
            if plan_record
            else None
        )
        cells.append(
            {
                "arm": arm,
                "candidate_id": candidate_id,
                "decision_path": str(decision_path.relative_to(output_dir)),
                "decision_sha256": sha256_file(decision_path),
                "plan_path": (
                    str(plan_record_path.relative_to(output_dir))
                    if plan_record_path
                    else None
                ),
                "plan_run_dir": (
                    str(plan_run_dir.relative_to(output_dir)) if plan_run_dir else None
                ),
                "plan_run_dir_sha256": (
                    directory_sha256(plan_run_dir) if plan_run_dir else None
                ),
                "plan_sha256": (
                    sha256_file(plan_record_path) if plan_record_path else None
                ),
                "raw_response_path": record["raw_response_path"],
                "raw_response_sha256": sha256_file(raw_response_path),
                "run_dir": str(run_dir.relative_to(output_dir)),
                "run_dir_sha256": directory_sha256(run_dir),
            }
        )
    if path.exists():
        payload = load_json(path)
        if (
            payload.get("cells") != cells
            or payload.get("trial_manifest_sha256")
            != sha256_file(output_dir / "trial-manifest.json")
        ):
            raise RuntimeError("fidelity audit input changed")
    else:
        payload = {
            "blind_to_oracle": True,
            "cells": cells,
            "created_at": utc_now(),
            "required_auditor": "GLM-5.2 via DeepEval, cross-family and blinded",
            "schema_version": 1,
            "trial_manifest_sha256": sha256_file(
                output_dir / "trial-manifest.json"
            ),
        }
        payload["audit_input_sha256"] = payload_sha256(payload)
        write_json(path, payload)
    template = output_dir / "fidelity-result.template.json"
    if not template.exists():
        write_json(
            template,
            {
                "audit_input_sha256": payload["audit_input_sha256"],
                "auditor": "GLM-5.2 via DeepEval",
                "audits_both_arms_for_leakage": None,
                "b_plan_specific": None,
                "b_repro_built_and_ran": None,
                "no_leakage": None,
                "no_undisclosed_prereg_mutation": None,
                "passes": None,
                "schema_version": 1,
            },
        )


def run_decisions(
    *,
    args: argparse.Namespace,
    order: dict[str, Any],
    candidates_by_id: dict[str, dict[str, Any]],
    tasks: dict[str, dict[str, Any]],
) -> None:
    # Every candidate-blind plan must be frozen before the first candidate outcome.
    for candidate_id in order["plan_order"]:
        load_plan(args.output_dir, candidate_id)
    decision_root = args.output_dir / "decisions"
    for position, item in enumerate(order["decision_order"], start=1):
        arm = item["arm"]
        candidate_id = item["candidate_id"]
        record_path = (
            decision_root / f"{candidate_id.replace('::', '__')}__arm-{arm}.json"
        )
        if record_path.exists():
            continue
        candidate = candidates_by_id[candidate_id]
        task = tasks[candidate["instance_id"]]
        record = run_decision_cell(
            args=args,
            arm=arm,
            candidate=candidate,
            task=task,
            position=position,
        )
        write_json(record_path, record)
        print(
            f"CELL {position:03d}/{len(order['decision_order'])} "
            f"{candidate_id} arm={arm} decision={record['decision']['decision']} "
            f"errors={len(record['errors'])}"
        )
    write_fidelity_input(args.output_dir, order["decision_order"])


def require_all_decisions(output_dir: Path, order: dict[str, Any]) -> None:
    missing = []
    for item in order["decision_order"]:
        name = f"{item['candidate_id'].replace('::', '__')}__arm-{item['arm']}.json"
        if not (output_dir / "decisions" / name).is_file():
            missing.append(name)
    if missing:
        raise RuntimeError(f"oracle blocked: {len(missing)} decision cells are missing")


def assert_frozen_ruler_environment(
    calibration: dict[str, Any], candidates: list[dict[str, Any]]
) -> str:
    """Require the exact calibrated package version and Docker image IDs."""
    version_result = run_command(
        [
            VENV_PY,
            "-c",
            "from importlib.metadata import version; print(version('swebench'))",
        ]
    )
    version = version_result.stdout.strip()
    expected_version = calibration.get("runner", {}).get("swebench_version")
    if version != expected_version:
        raise RuntimeError(
            f"SWE-bench version changed after calibration: "
            f"{expected_version!r} -> {version!r}"
        )
    results = {
        item["instance_id"]: item for item in calibration.get("task_results", [])
    }
    for instance_id in sorted({item["instance_id"] for item in candidates}):
        image = results[instance_id]["image"]
        inspect = run_command(
            [
                "docker",
                "image",
                "inspect",
                "--format",
                "{{.Id}}",
                image["requested_name"],
            ],
            check=False,
        )
        actual = inspect.stdout.strip()
        if inspect.returncode or actual != image["image_id"]:
            raise RuntimeError(
                f"calibrated Docker image changed for {instance_id}: "
                f"expected {image['image_id']}, found {actual or '<missing>'}"
            )
    return version


def run_oracle(
    *,
    args: argparse.Namespace,
    candidates: list[dict[str, Any]],
    order: dict[str, Any],
) -> None:
    oracle_path = args.output_dir / "oracle.json"
    if oracle_path.exists():
        print(f"oracle already frozen: {oracle_path}")
        return
    require_all_decisions(args.output_dir, order)
    calibration = load_json(args.calibration)
    swebench_version = assert_frozen_ruler_environment(calibration, candidates)
    by_index: dict[int, list[dict[str, Any]]] = {1: [], 2: []}
    for candidate in candidates:
        by_index[candidate["candidate_index"]].append(candidate)
    outcomes = {
        candidate["candidate_id"]: [] for candidate in candidates
    }
    args.work_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="molgas-oracle-", dir=args.work_dir
    ) as temporary:
        root = Path(temporary)
        for repeat in range(1, ORACLE_REPEATS + 1):
            for candidate_index in (1, 2):
                group = by_index[candidate_index]
                run_id = f"molgas-oracle-c{candidate_index}-r{repeat}"
                run_root = root / run_id
                run_root.mkdir()
                predictions_path = run_root / "predictions.json"
                model = f"molgas-candidate-{candidate_index}-r{repeat}"
                predictions = []
                for candidate in group:
                    _, patch_text = frozen_patch(candidate, args.candidates)
                    predictions.append(
                        {
                            "instance_id": candidate["instance_id"],
                            "model_name_or_path": model,
                            "model_patch": patch_text,
                        }
                    )
                write_json(predictions_path, predictions)
                ids = [candidate["instance_id"] for candidate in group]
                command = swebench_command(
                    instance_ids=ids,
                    predictions_path=predictions_path,
                    run_id=run_id,
                    max_workers=args.max_workers,
                    timeout_seconds=args.test_timeout_seconds,
                    cache_level="instance",
                )
                print(
                    f"ORACLE candidate-index={candidate_index} "
                    f"repeat={repeat}/{ORACLE_REPEATS}"
                )
                result = run_command(command, cwd=run_root, check=False)
                if result.returncode:
                    raise RuntimeError(
                        f"SWE-bench oracle failed ({result.returncode}): "
                        f"{(result.stderr or '')[-1200:]}"
                    )
                verdicts = completed_verdicts(
                    find_swebench_report(run_root, run_id),
                    ids,
                    accept_empty_as_unresolved=True,
                )
                for candidate in group:
                    outcomes[candidate["candidate_id"]].append(
                        verdicts[candidate["instance_id"]]
                    )
        # Detect a tag/image mutation during any of the repeated evaluations.
        assert_frozen_ruler_environment(calibration, candidates)
    candidate_outcomes = []
    for candidate in candidates:
        repeated = outcomes[candidate["candidate_id"]]
        stable = len(repeated) == ORACLE_REPEATS and len(set(repeated)) == 1
        candidate_outcomes.append(
            {
                "candidate_id": candidate["candidate_id"],
                "instance_id": candidate["instance_id"],
                "repeats": repeated,
                "resolves": repeated[0] if stable else None,
                "stable": stable,
            }
        )
    identity = [
        {
            "candidate_id": item["candidate_id"],
            "repeats": item["repeats"],
            "resolves": item["resolves"],
        }
        for item in candidate_outcomes
    ]
    oracle = {
        "candidate_outcomes": candidate_outcomes,
        "dataset": DATASET_NAME,
        "finished_at": utc_now(),
        "oracle_repeats": ORACLE_REPEATS,
        "oracle_sha256": payload_sha256(identity),
        "runner": {
            "cache_level": "instance",
            "dataset": DATASET_NAME,
            "max_workers": args.max_workers,
            "python": str(VENV_PY),
            "split": DATASET_SPLIT,
            "swebench_version": swebench_version,
            "test_timeout_seconds": args.test_timeout_seconds,
        },
        "schema_version": 1,
    }
    write_json(oracle_path, oracle)
    print(f"froze repeated candidate truth to {oracle_path}")
    if not all(item["stable"] for item in candidate_outcomes):
        print("WARNING: oracle was not deterministic for every candidate")


def dry_run(args: argparse.Namespace) -> int:
    print("DRY RUN -- no clones, cook calls, Docker, or SWE-bench evaluation.")
    tasks = load_json(args.tasks)
    selected = validate_task_bank(tasks, expected_count=30)
    if args.candidates.is_file() and args.calibration.is_file():
        candidate_manifest = load_json(args.candidates)
        all_candidates = validate_candidate_bank(
            candidate_manifest, args.candidates, tasks["task_bank_sha256"]
        )
        calibrated = validate_calibration(
            load_json(args.calibration),
            tasks["task_bank_sha256"],
            {task["instance_id"] for task in selected},
        )
        candidates = [
            item for item in all_candidates if item["instance_id"] in set(calibrated)
        ]
        print(f"included calibrated tasks={len(calibrated)}")
        print(f"plans={len(candidates)} decision_cells={len(candidates) * 2}")
        print(f"oracle_runs={ORACLE_REPEATS * 2}")
    else:
        print("candidate/calibration inputs are not frozen yet")
        print("maximum plan calls=60 decision_cells=120 oracle_runs=4")
    print(f"cook_cmd_sha256={sha256_text(args.cook_cmd)}")
    print(f"randomization_seed={args.seed}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.dry_run:
        return dry_run(args)
    is_claude = validate_cook_template(args.cook_cmd)
    if not VENV_PY.is_file() and args.phase in {"all", "oracle"}:
        raise SystemExit(f"SWE-bench venv interpreter not found: {VENV_PY}")
    for value, name in (
        (args.max_workers, "max workers"),
        (args.test_timeout_seconds, "test timeout"),
        (args.total_timeout_seconds, "total cook timeout"),
        (args.total_token_cap, "total token cap"),
    ):
        if value <= 0:
            raise SystemExit(f"{name} must be positive")
    if args.total_timeout_seconds < 2 or args.total_token_cap < 2:
        raise SystemExit("B's two calls require total caps of at least 2")

    task_bank = load_json(args.tasks)
    selected_tasks = validate_task_bank(task_bank, expected_count=30)
    tasks = task_map(task_bank)
    candidate_manifest = load_json(args.candidates)
    all_candidates = validate_candidate_bank(
        candidate_manifest, args.candidates, task_bank["task_bank_sha256"]
    )
    calibration = load_json(args.calibration)
    calibrated_ids = validate_calibration(
        calibration,
        task_bank["task_bank_sha256"],
        {task["instance_id"] for task in selected_tasks},
    )
    if candidate_manifest.get("frozen_at", "") > calibration.get("finished_at", ""):
        raise ValueError(
            "candidate bank must be frozen before ruler calibration, per pre-registration"
        )
    candidates = [
        item for item in all_candidates if item["instance_id"] in set(calibrated_ids)
    ]
    if not candidates:
        raise SystemExit("no calibrated candidates remain")
    candidates_by_id = {item["candidate_id"]: item for item in candidates}
    manifest, order = initialize_trial(
        args=args,
        task_bank=task_bank,
        candidate_manifest=candidate_manifest,
        calibration=calibration,
        candidates=candidates,
    )
    print(
        f"frozen trial config {manifest['config_sha256']} "
        f"(Claude safe-mode={is_claude})"
    )
    if args.phase in {"all", "plans"}:
        run_plans(
            args=args,
            order=order,
            candidates_by_id=candidates_by_id,
            tasks=tasks,
        )
    if args.phase in {"all", "decisions"}:
        run_decisions(
            args=args,
            order=order,
            candidates_by_id=candidates_by_id,
            tasks=tasks,
        )
    if args.phase in {"all", "oracle"}:
        run_oracle(args=args, candidates=candidates, order=order)
    return 0


if __name__ == "__main__":
    sys.exit(main())
