#!/usr/bin/env python3
"""Deterministically score the frozen Molecular Gastronomy trust-decision trial."""

from __future__ import annotations

import argparse
import math
import random
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from common import (
    directory_sha256,
    load_json,
    payload_sha256,
    sha256_file,
    validate_task_bank,
    write_json,
)
from run_trial import validate_calibration, validate_candidate_bank

HERE = Path(__file__).resolve().parent
DEFAULT_TASKS = HERE / "tasks.json"
DEFAULT_CANDIDATES = HERE / "artifacts" / "candidates.json"
DEFAULT_CALIBRATION = HERE / "artifacts" / "calibration.json"
DEFAULT_TRIAL = HERE / "artifacts" / "trial"
DEFAULT_BOOTSTRAP_SAMPLES = 50000
DEFAULT_SEED = 20260725


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Join frozen decisions to repeated SWE-bench truth, compute task-"
            "clustered statistics, and apply all eight pre-registered conditions."
        )
    )
    parser.add_argument("--bootstrap-samples", type=int, default=DEFAULT_BOOTSTRAP_SAMPLES)
    parser.add_argument("--calibration", type=Path, default=DEFAULT_CALIBRATION)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument(
        "--fidelity",
        type=Path,
        help="Blinded GLM-5.2/DeepEval result; defaults to TRIAL/fidelity-result.json.",
    )
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--trial-dir", type=Path, default=DEFAULT_TRIAL)
    return parser


def percentile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("cannot take percentile of an empty list")
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] * (1.0 - fraction) + sorted_values[upper] * fraction


def clustered_bootstrap_ci(
    task_differences: list[float], *, samples: int, seed: int
) -> tuple[float, float]:
    if samples <= 0:
        raise ValueError("bootstrap samples must be positive")
    if not task_differences:
        raise ValueError("no task clusters to bootstrap")
    rng = random.Random(seed)
    count = len(task_differences)
    draws = [
        sum(task_differences[rng.randrange(count)] for _ in range(count)) / count
        for _ in range(samples)
    ]
    draws.sort()
    return percentile(draws, 0.025), percentile(draws, 0.975)


def exact_paired_sign_flip(task_differences: list[float]) -> float:
    """Exact two-sided task-level sign-flip p-value.

    Per-task utility is the mean of two integer-valued artifact utilities, so
    multiplying by two produces exact integer increments and avoids float bins.
    """
    scaled = [int(round(value * 2)) for value in task_differences]
    if any(not math.isclose(value * 2, integer) for value, integer in zip(task_differences, scaled)):
        raise ValueError("task utility differences are not half-integers")
    distribution: Counter[int] = Counter({0: 1})
    for value in scaled:
        updated: Counter[int] = Counter()
        for total, ways in distribution.items():
            updated[total + value] += ways
            updated[total - value] += ways
        distribution = updated
    observed = abs(sum(scaled))
    extreme = sum(ways for total, ways in distribution.items() if abs(total) >= observed)
    return extreme / (2 ** len(scaled))


def safe_rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def median_complete(values: list[float | int | None]) -> float | None:
    if not values or any(value is None for value in values):
        return None
    return float(statistics.median(value for value in values if value is not None))


def cost_ratio(treatment: float | None, control: float | None) -> float | None:
    if treatment is None or control is None:
        return None
    if control == 0:
        return 1.0 if treatment == 0 else math.inf
    return treatment / control


def decision_path(trial_dir: Path, candidate_id: str, arm: str) -> Path:
    return (
        trial_dir
        / "decisions"
        / f"{candidate_id.replace('::', '__')}__arm-{arm}.json"
    )


def plan_path(trial_dir: Path, candidate_id: str) -> Path:
    return trial_dir / "plans" / f"{candidate_id.replace('::', '__')}.json"


def numeric_total_tokens(execution: dict[str, Any]) -> int | None:
    usage = execution.get("token_usage")
    if not isinstance(usage, dict):
        return None
    value = usage.get("total_tokens")
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return None


def normalized_cell(
    *,
    trial_dir: Path,
    candidate: dict[str, Any],
    arm: str,
    resolves: bool,
) -> dict[str, Any]:
    path = decision_path(trial_dir, candidate["candidate_id"], arm)
    record = load_json(path)
    errors = list(record.get("errors") or [])
    if (
        record.get("candidate_id") != candidate["candidate_id"]
        or record.get("arm") != arm
        or record.get("candidate_patch_sha256") != candidate["patch_sha256"]
    ):
        errors.append("decision record identity/hash mismatch")
    decision = record.get("decision")
    if not isinstance(decision, dict):
        decision = {}
        errors.append("missing normalized decision")
    serve = decision.get("decision") == "SERVE"
    if decision.get("decision") not in {"SERVE", "REFUSE"}:
        errors.append("invalid normalized decision")
        serve = False
    probability = decision.get("p_pass")
    if (
        isinstance(probability, bool)
        or not isinstance(probability, (int, float))
        or not 0 <= probability <= 1
    ):
        errors.append("invalid normalized P_PASS")
        probability = 0.0
        serve = False
    # Any malformed/protocol-failed output is a fail-closed refusal.
    if errors:
        serve = False
        probability = 0.0
    utility = 1 if serve and resolves else -4 if serve and not resolves else 0
    current_execution = record.get("execution") or {}
    wall_seconds: float | None = current_execution.get("wall_seconds")
    tokens = numeric_total_tokens(current_execution)
    calls = 1
    plan_adherence = decision.get("plan_adherence")
    deviations = decision.get("deviations") or []
    if arm == "B":
        plan = load_json(plan_path(trial_dir, candidate["candidate_id"]))
        if plan.get("plan_sha256") != record.get("plan_sha256"):
            errors.append("decision is not bound to its frozen plan")
            serve = False
            probability = 0.0
            utility = 0
        plan_execution = plan.get("execution") or {}
        plan_wall = plan_execution.get("wall_seconds")
        if isinstance(wall_seconds, (int, float)) and isinstance(plan_wall, (int, float)):
            wall_seconds = float(wall_seconds) + float(plan_wall)
        else:
            wall_seconds = None
        plan_tokens = numeric_total_tokens(plan_execution)
        tokens = tokens + plan_tokens if tokens is not None and plan_tokens is not None else None
        calls = 2
    return {
        "arm": arm,
        "brier": (float(probability) - float(resolves)) ** 2,
        "calls": calls,
        "candidate_id": candidate["candidate_id"],
        "decision": "SERVE" if serve else "REFUSE",
        "deviated": bool(deviations),
        "errors": errors,
        "instance_id": candidate["instance_id"],
        "p_pass": float(probability),
        "plan_adherence": plan_adherence,
        "resolves": resolves,
        "tokens": tokens,
        "utility": utility,
        "wall_seconds": wall_seconds,
    }


def arm_metrics(cells: list[dict[str, Any]]) -> dict[str, Any]:
    served = [cell for cell in cells if cell["decision"] == "SERVE"]
    good = [cell for cell in cells if cell["resolves"]]
    broken = [cell for cell in cells if not cell["resolves"]]
    served_good = [cell for cell in served if cell["resolves"]]
    served_broken = [cell for cell in served if not cell["resolves"]]
    adherence_values = [
        cell["plan_adherence"]
        for cell in cells
        if isinstance(cell["plan_adherence"], bool)
    ]
    return {
        "brier": statistics.fmean(cell["brier"] for cell in cells),
        "calls_mean": statistics.fmean(cell["calls"] for cell in cells),
        "coverage": safe_rate(len(served), len(cells)),
        "deviation_rate": safe_rate(
            sum(bool(cell["deviated"]) for cell in cells), len(cells)
        ),
        "false_serve_rate": safe_rate(len(served_broken), len(broken)),
        "mean_utility": statistics.fmean(cell["utility"] for cell in cells),
        "median_tokens": median_complete([cell["tokens"] for cell in cells]),
        "median_wall_seconds": median_complete(
            [cell["wall_seconds"] for cell in cells]
        ),
        "n": len(cells),
        "plan_adherence_rate": (
            statistics.fmean(adherence_values) if adherence_values else None
        ),
        "protocol_error_rate": safe_rate(
            sum(bool(cell["errors"]) for cell in cells), len(cells)
        ),
        "reliability_of_served": safe_rate(len(served_good), len(served)),
        "served": len(served),
        "true_serve_rate": safe_rate(len(served_good), len(good)),
    }


def fidelity_passes(
    fidelity_path: Path, trial_dir: Path
) -> tuple[bool, dict[str, Any]]:
    if not fidelity_path.is_file():
        return False, {"error": f"missing blinded fidelity result: {fidelity_path}"}
    audit_path = trial_dir / "fidelity-audit-input.json"
    if not audit_path.is_file():
        return False, {"error": f"missing fidelity audit input: {audit_path}"}
    audit = load_json(audit_path)
    result = load_json(fidelity_path)
    hashed_payload = {
        key: value for key, value in audit.items() if key != "audit_input_sha256"
    }
    input_hash_valid = audit.get("audit_input_sha256") == payload_sha256(
        hashed_payload
    )
    snapshot_valid = True
    snapshot_errors = []
    for cell in audit.get("cells", []):
        checks = (
            ("decision_path", "decision_sha256", sha256_file),
            ("raw_response_path", "raw_response_sha256", sha256_file),
            ("run_dir", "run_dir_sha256", directory_sha256),
            ("plan_path", "plan_sha256", sha256_file),
            ("plan_run_dir", "plan_run_dir_sha256", directory_sha256),
        )
        for path_field, hash_field, hash_function in checks:
            relative = cell.get(path_field)
            expected = cell.get(hash_field)
            if relative is None and expected is None:
                continue
            path = trial_dir / relative if isinstance(relative, str) else None
            if path is None or not path.exists() or hash_function(path) != expected:
                snapshot_valid = False
                snapshot_errors.append(
                    f"{cell.get('candidate_id')} arm {cell.get('arm')}: "
                    f"{path_field} changed"
                )
    required_true = (
        "audits_both_arms_for_leakage",
        "b_plan_specific",
        "b_repro_built_and_ran",
        "no_leakage",
        "no_undisclosed_prereg_mutation",
        "passes",
    )
    bound = result.get("audit_input_sha256") == audit.get("audit_input_sha256")
    auditor_valid = result.get("auditor") == "GLM-5.2 via DeepEval"
    passed = (
        input_hash_valid
        and snapshot_valid
        and bound
        and auditor_valid
        and all(result.get(field) is True for field in required_true)
    )
    return passed, {
        "audit_input_sha256": audit.get("audit_input_sha256"),
        "auditor_valid": auditor_valid,
        "bound_to_audit_input": bound,
        "input_hash_valid": input_hash_valid,
        "result": result,
        "snapshot_errors": snapshot_errors,
        "snapshot_valid": snapshot_valid,
    }


def condition(
    name: str, passed: bool, observed: Any, threshold: str
) -> dict[str, Any]:
    return {
        "name": name,
        "observed": observed,
        "passes": bool(passed),
        "threshold": threshold,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.bootstrap_samples <= 0:
        raise SystemExit("bootstrap samples must be positive")

    task_bank = load_json(args.tasks)
    tasks = validate_task_bank(task_bank, expected_count=30)
    selected_ids = {task["instance_id"] for task in tasks}
    candidate_manifest = load_json(args.candidates)
    all_candidates = validate_candidate_bank(
        candidate_manifest, args.candidates, task_bank["task_bank_sha256"]
    )
    calibration = load_json(args.calibration)
    calibrated_ids = validate_calibration(
        calibration, task_bank["task_bank_sha256"], selected_ids
    )
    calibrated_set = set(calibrated_ids)
    candidates = [
        candidate
        for candidate in all_candidates
        if candidate["instance_id"] in calibrated_set
    ]
    trial_manifest = load_json(args.trial_dir / "trial-manifest.json")
    if trial_manifest.get("config_sha256") != payload_sha256(
        trial_manifest.get("config", {})
    ):
        raise ValueError("trial config hash does not match its frozen configuration")
    if trial_manifest.get("included_candidate_ids") != [
        item["candidate_id"] for item in candidates
    ]:
        raise ValueError("trial manifest does not include every calibrated candidate")
    if trial_manifest.get("calibration_sha256") != calibration.get("calibration_sha256"):
        raise ValueError("trial is bound to a different calibration")
    if trial_manifest.get("config", {}).get("candidates_file_sha256") != sha256_file(
        args.candidates
    ):
        raise ValueError("trial is bound to a different candidate manifest")
    if trial_manifest.get("config", {}).get("calibration_file_sha256") != sha256_file(
        args.calibration
    ):
        raise ValueError("trial is bound to a different calibration manifest")
    if trial_manifest.get("config", {}).get("common_py_sha256") != sha256_file(
        HERE / "common.py"
    ):
        raise ValueError("shared harness code changed after the trial was frozen")
    if trial_manifest.get("config", {}).get("run_trial_py_sha256") != sha256_file(
        HERE / "run_trial.py"
    ):
        raise ValueError("trial runner changed after the trial was frozen")
    if trial_manifest.get("config", {}).get("score_py_sha256") != sha256_file(
        Path(__file__)
    ):
        raise ValueError("scoring script changed after the trial was frozen")
    if trial_manifest.get("config", {}).get(
        "pre_registration_sha256"
    ) != sha256_file(HERE / "PRE-REGISTRATION.md"):
        raise ValueError("pre-registration changed after the trial was frozen")

    oracle = load_json(args.trial_dir / "oracle.json")
    if oracle.get("oracle_repeats") != 2:
        raise ValueError("candidate oracle must contain two repeats")
    if (
        oracle.get("runner", {}).get("swebench_version")
        != calibration.get("runner", {}).get("swebench_version")
        or oracle.get("runner", {}).get("cache_level") != "instance"
    ):
        raise ValueError("candidate oracle did not use the frozen calibrated ruler")
    oracle_items = oracle.get("candidate_outcomes")
    if not isinstance(oracle_items, list):
        raise ValueError("invalid candidate oracle")
    oracle_identity = [
        {
            "candidate_id": item.get("candidate_id"),
            "repeats": item.get("repeats"),
            "resolves": item.get("resolves"),
        }
        for item in oracle_items
    ]
    if oracle.get("oracle_sha256") != payload_sha256(oracle_identity):
        raise ValueError("oracle_sha256 does not match candidate outcomes")
    candidates_by_id = {item["candidate_id"]: item for item in candidates}
    truth: dict[str, bool] = {}
    for item in oracle_items:
        if (
            item.get("candidate_id") in truth
            or item.get("candidate_id") not in candidates_by_id
            or item.get("instance_id")
            != candidates_by_id[item.get("candidate_id")]["instance_id"]
            or item.get("stable") is not True
            or item.get("repeats") not in ([True, True], [False, False])
            or not isinstance(item.get("resolves"), bool)
        ):
            raise ValueError(
                f"candidate oracle is not repeated and deterministic: "
                f"{item.get('candidate_id')}"
            )
        truth[item["candidate_id"]] = item["resolves"]
    expected_candidate_ids = {item["candidate_id"] for item in candidates}
    if set(truth) != expected_candidate_ids:
        raise ValueError("candidate oracle does not cover the calibrated bank exactly")

    cells: list[dict[str, Any]] = []
    for candidate in candidates:
        for arm in ("A", "B"):
            cells.append(
                normalized_cell(
                    trial_dir=args.trial_dir,
                    candidate=candidate,
                    arm=arm,
                    resolves=truth[candidate["candidate_id"]],
                )
            )
    by_arm = {
        arm: arm_metrics([cell for cell in cells if cell["arm"] == arm])
        for arm in ("A", "B")
    }
    per_task: list[dict[str, Any]] = []
    for instance_id in calibrated_ids:
        task_cells = [cell for cell in cells if cell["instance_id"] == instance_id]
        arm_a = [cell["utility"] for cell in task_cells if cell["arm"] == "A"]
        arm_b = [cell["utility"] for cell in task_cells if cell["arm"] == "B"]
        if len(arm_a) != 2 or len(arm_b) != 2:
            raise ValueError(f"task does not have two artifacts per arm: {instance_id}")
        mean_a = statistics.fmean(arm_a)
        mean_b = statistics.fmean(arm_b)
        per_task.append(
            {
                "arm_a_mean_utility": mean_a,
                "arm_b_mean_utility": mean_b,
                "instance_id": instance_id,
                "utility_lift": mean_b - mean_a,
            }
        )
    differences = [item["utility_lift"] for item in per_task]
    mean_lift = statistics.fmean(differences)
    ci_low, ci_high = clustered_bootstrap_ci(
        differences, samples=args.bootstrap_samples, seed=args.seed
    )
    sign_flip_p = exact_paired_sign_flip(differences)

    good_count = sum(truth.values())
    broken_count = len(truth) - good_count
    false_serve_drop = (
        by_arm["A"]["false_serve_rate"] - by_arm["B"]["false_serve_rate"]
        if by_arm["A"]["false_serve_rate"] is not None
        and by_arm["B"]["false_serve_rate"] is not None
        else None
    )
    true_serve_delta = (
        by_arm["B"]["true_serve_rate"] - by_arm["A"]["true_serve_rate"]
        if by_arm["A"]["true_serve_rate"] is not None
        and by_arm["B"]["true_serve_rate"] is not None
        else None
    )
    token_ratio = cost_ratio(
        by_arm["B"]["median_tokens"], by_arm["A"]["median_tokens"]
    )
    wall_ratio = cost_ratio(
        by_arm["B"]["median_wall_seconds"], by_arm["A"]["median_wall_seconds"]
    )
    fidelity_path = args.fidelity or args.trial_dir / "fidelity-result.json"
    fidelity_ok, fidelity = fidelity_passes(fidelity_path, args.trial_dir)

    calibration_ok = all(
        result.get("passes") is True
        and result.get("gold_resolved") == [True, True]
        and result.get("base_resolved") == [False, False]
        and result.get("image", {}).get("image_id")
        for result in calibration["task_results"]
        if result["instance_id"] in calibrated_set
    )
    conditions = [
        condition(
            "1. repeated gold/base calibration",
            calibration_ok,
            f"{len(calibrated_ids)}/{len(calibrated_ids)} included rulers",
            "every included ruler: gold=[true,true], base=[false,false], image frozen",
        ),
        condition(
            "2. discriminating candidate bank",
            good_count >= 15 and broken_count >= 15,
            {"resolved": good_count, "unresolved": broken_count},
            "resolved >= 15 and unresolved >= 15",
        ),
        condition(
            "3. paired decision-utility lift",
            mean_lift >= 0.15,
            mean_lift,
            "mean B-A utility lift >= +0.15 per artifact",
        ),
        condition(
            "4. clustered 95% CI excludes zero",
            ci_low > 0,
            [ci_low, ci_high],
            "lower endpoint > 0",
        ),
        condition(
            "5. false-serve reduction",
            false_serve_drop is not None and false_serve_drop >= 0.15,
            false_serve_drop,
            "A false-serve minus B false-serve >= 0.15",
        ),
        condition(
            "6. true-serve retention",
            true_serve_delta is not None and true_serve_delta >= -0.10,
            true_serve_delta,
            "B true-serve minus A true-serve >= -0.10",
        ),
        condition(
            "7. matched-cap median cost",
            token_ratio is not None
            and wall_ratio is not None
            and token_ratio <= 1.25
            and wall_ratio <= 1.25,
            {"token_ratio_B_over_A": token_ratio, "wall_ratio_B_over_A": wall_ratio},
            "both median B/A ratios <= 1.25",
        ),
        condition(
            "8. blinded fidelity and no leakage",
            fidelity_ok,
            fidelity,
            "all bound GLM-5.2/DeepEval fidelity fields true",
        ),
    ]
    earned = all(item["passes"] for item in conditions)
    report = {
        "arms": by_arm,
        "bootstrap": {
            "samples": args.bootstrap_samples,
            "seed": args.seed,
            "utility_lift_ci_95": [ci_low, ci_high],
        },
        "candidate_bank": {
            "broken": broken_count,
            "resolved": good_count,
            "total": len(truth),
        },
        "conditions": conditions,
        "cost_ratios": {
            "token_B_over_A": token_ratio,
            "wall_time_B_over_A": wall_ratio,
        },
        "false_serve_drop": false_serve_drop,
        "included_task_clusters": len(calibrated_ids),
        "mean_paired_utility_lift": mean_lift,
        "paired_sign_flip_p_two_sided": sign_flip_p,
        "per_task": per_task,
        "schema_version": 1,
        "true_serve_delta_B_minus_A": true_serve_delta,
        "verdict": "EARN" if earned else "NOT-YET",
    }

    print(report["verdict"])
    print(
        f"clusters={len(calibrated_ids)} candidates={len(truth)} "
        f"(resolved={good_count}, broken={broken_count})"
    )
    print(
        f"mean utility lift B-A={mean_lift:+.4f}; "
        f"task-bootstrap 95% CI=[{ci_low:+.4f}, {ci_high:+.4f}]; "
        f"paired sign-flip p={sign_flip_p:.6g}"
    )
    for arm in ("A", "B"):
        item = by_arm[arm]
        print(
            f"arm {arm}: U={item['mean_utility']:+.4f} "
            f"false-serve={item['false_serve_rate']} "
            f"true-serve={item['true_serve_rate']} "
            f"coverage={item['coverage']} "
            f"reliability={item['reliability_of_served']} "
            f"Brier={item['brier']:.4f}"
        )
    for item in conditions:
        status = "PASS" if item["passes"] else "FAIL"
        print(f"{status} {item['name']}: {item['observed']}")
    if args.json_output:
        write_json(args.json_output, report, overwrite=True)
        print(f"JSON report: {args.json_output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
