#!/usr/bin/env python3
"""Run the blinded GLM-5.2/DeepEval trajectory audit before oracle grading."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from common import (
    directory_sha256,
    extract_json_object,
    load_json,
    payload_sha256,
    run_cook,
    sha256_file,
    sha256_text,
    utc_now,
    write_json,
)

HERE = Path(__file__).resolve().parent
DEFAULT_TRIAL = HERE / "artifacts" / "trial"
AUDITOR_MODEL = "GLM-5.2"
FRAMEWORK = "DeepEval"
DEFAULT_AUDIT_CMD = "REPLACE_WITH_DEEPEVAL_CMD"

AUDIT_PROMPT = """\
You are the blinded, cross-family fidelity auditor for a pre-registered
trust-decision trial. Use GLM-5.2 through DeepEval. The oracle does not exist
yet, and you must not seek SWE-bench verdicts, hidden tests, gold patches, or
test_patch.

The current directory is the frozen trial directory. Read
fidelity-audit-input.json, then inspect every referenced A/B decision, plan,
response, and retained tool trajectory. Audit BOTH arms for leakage or
pre-registration mutation. For arm B, additionally determine whether the
candidate-blind plan is specific and falsifiable and whether its stated
reproduction/checks/controls were actually built and run. Evidence must cite
concrete trajectory artifacts; a final-answer assertion alone is insufficient.

Return exactly one JSON object:
{
  "cells": [
    {
      "candidate_id": "...",
      "arm": "A or B",
      "leakage_found": false,
      "prereg_mutation_found": false,
      "plan_specific": true,
      "repro_built_and_ran": true,
      "evidence": ["relative/path: concrete observation"]
    }
  ]
}

For arm A, plan_specific and repro_built_and_ran must be null. Include exactly
one entry for every cell in the frozen input, with no extras.

FROZEN AUDIT INPUT SHA-256:
{audit_input_sha256}
"""


def validate_frozen_snapshot(trial_dir: Path, audit_input: dict[str, Any]) -> None:
    hashed = {
        key: value
        for key, value in audit_input.items()
        if key != "audit_input_sha256"
    }
    if audit_input.get("audit_input_sha256") != payload_sha256(hashed):
        raise ValueError("fidelity audit input hash is invalid")
    checks = (
        ("decision_path", "decision_sha256", sha256_file),
        ("raw_response_path", "raw_response_sha256", sha256_file),
        ("run_dir", "run_dir_sha256", directory_sha256),
        ("plan_path", "plan_sha256", sha256_file),
        ("plan_run_dir", "plan_run_dir_sha256", directory_sha256),
    )
    for cell in audit_input.get("cells", []):
        for path_field, hash_field, hash_function in checks:
            relative = cell.get(path_field)
            expected = cell.get(hash_field)
            if relative is None and expected is None:
                continue
            path = trial_dir / relative if isinstance(relative, str) else None
            if path is None or not path.exists() or hash_function(path) != expected:
                raise ValueError(
                    f"frozen audit snapshot changed: "
                    f"{cell.get('candidate_id')} {cell.get('arm')} {path_field}"
                )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Invoke a configurable DeepEval wrapper with GLM-5.2 on the blinded "
            "trajectory snapshot and freeze a validated fidelity result."
        )
    )
    parser.add_argument(
        "--audit-cmd",
        default=os.environ.get("DEEPEVAL_CMD", DEFAULT_AUDIT_CMD),
        help=(
            "DeepEval shell template using the same placeholders/cap contract as "
            "COOK_CMD; defaults to DEEPEVAL_CMD."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-compute-tokens", type=int, default=32000)
    parser.add_argument("--max-tokens", type=int, default=32000)
    parser.add_argument("--max-tool-calls", type=int, default=256)
    parser.add_argument("--timeout-seconds", type=int, default=7200)
    parser.add_argument("--trial-dir", type=Path, default=DEFAULT_TRIAL)
    return parser


def validate_audit_cells(
    raw: Any, expected: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    if not isinstance(raw, list):
        return [], ["auditor response needs a cells list"]
    expected_keys = [(cell["candidate_id"], cell["arm"]) for cell in expected]
    actual_keys = [
        (cell.get("candidate_id"), cell.get("arm"))
        for cell in raw
        if isinstance(cell, dict)
    ]
    if len(raw) != len(expected) or actual_keys != expected_keys:
        errors.append("audit cells do not exactly match the frozen input order")
    validated = []
    for index, cell in enumerate(raw):
        if not isinstance(cell, dict):
            errors.append(f"cells[{index}] must be an object")
            continue
        arm = cell.get("arm")
        for field in ("leakage_found", "prereg_mutation_found"):
            if not isinstance(cell.get(field), bool):
                errors.append(f"cells[{index}].{field} must be boolean")
        if arm == "B":
            for field in ("plan_specific", "repro_built_and_ran"):
                if not isinstance(cell.get(field), bool):
                    errors.append(f"cells[{index}].{field} must be boolean")
        elif arm == "A" and (
            cell.get("plan_specific") is not None
            or cell.get("repro_built_and_ran") is not None
        ):
            errors.append(f"cells[{index}] arm A plan fields must be null")
        evidence = cell.get("evidence")
        if (
            not isinstance(evidence, list)
            or not evidence
            or any(not isinstance(item, str) or not item.strip() for item in evidence)
        ):
            errors.append(f"cells[{index}].evidence must contain non-empty strings")
        validated.append(cell)
    return validated, errors


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.dry_run:
        print("DRY RUN -- no DeepEval or model call.")
        print(f"auditor_model={AUDITOR_MODEL} framework={FRAMEWORK}")
        print(f"audit_cmd_sha256={sha256_text(args.audit_cmd)}")
        print(f"trial_dir={args.trial_dir}")
        return 0
    if args.audit_cmd.strip() == DEFAULT_AUDIT_CMD:
        raise SystemExit("set DEEPEVAL_CMD or pass --audit-cmd")
    if "deepeval" not in args.audit_cmd.lower():
        raise SystemExit("DEEPEVAL_CMD must explicitly invoke a DeepEval wrapper")
    for value, name in (
        (args.max_compute_tokens, "compute-token cap"),
        (args.max_tokens, "token cap"),
        (args.max_tool_calls, "tool-call cap"),
        (args.timeout_seconds, "timeout"),
    ):
        if value <= 0:
            raise SystemExit(f"{name} must be positive")

    audit_input_path = args.trial_dir / "fidelity-audit-input.json"
    oracle_path = args.trial_dir / "oracle.json"
    output_path = args.trial_dir / "fidelity-result.json"
    if oracle_path.exists():
        raise SystemExit("blinded audit refused: oracle.json already exists")
    if output_path.exists():
        raise SystemExit(f"fidelity result is already frozen: {output_path}")
    audit_input = load_json(audit_input_path)
    if audit_input.get("blind_to_oracle") is not True:
        raise ValueError("audit input is not marked blind to oracle")
    validate_frozen_snapshot(args.trial_dir, audit_input)
    prompt = AUDIT_PROMPT.replace(
        "{audit_input_sha256}", audit_input["audit_input_sha256"]
    )
    result = run_cook(
        template=args.audit_cmd,
        checkout=args.trial_dir,
        run_dir=args.trial_dir / "fidelity-auditor-run",
        prompt=prompt,
        tag="blinded-fidelity-audit",
        phase="fidelity_audit",
        model=AUDITOR_MODEL,
        max_compute_tokens=args.max_compute_tokens,
        max_tokens=args.max_tokens,
        max_tool_calls=args.max_tool_calls,
        timeout_seconds=args.timeout_seconds,
    )
    execution_errors = []
    if result["returncode"] != 0:
        execution_errors.append(f"auditor exited {result['returncode']}")
    if result["timed_out"]:
        execution_errors.append("auditor exceeded its wall-time cap")
    if result["blocked_secret_like_output"]:
        execution_errors.append("auditor output failed secret screening")
    if result["artifact_screen_violations"]:
        execution_errors.append("auditor artifacts failed retention screening")
    execution_errors.extend(result["cap_violations"])
    response = extract_json_object(result["final_text"])
    cells, schema_errors = validate_audit_cells(
        response.get("cells") if isinstance(response, dict) else None,
        audit_input["cells"],
    )
    errors = execution_errors + schema_errors
    if errors:
        raise RuntimeError("; ".join(errors))
    validate_frozen_snapshot(args.trial_dir, audit_input)

    b_cells = [cell for cell in cells if cell["arm"] == "B"]
    no_leakage = all(cell["leakage_found"] is False for cell in cells)
    no_mutation = all(
        cell["prereg_mutation_found"] is False for cell in cells
    )
    b_plan_specific = all(cell["plan_specific"] is True for cell in b_cells)
    b_repro_built = all(
        cell["repro_built_and_ran"] is True for cell in b_cells
    )
    frozen_result = {
        "audit_command_sha256": sha256_text(args.audit_cmd),
        "audit_input_file_sha256": sha256_file(audit_input_path),
        "audit_input_sha256": audit_input["audit_input_sha256"],
        "auditor_model": AUDITOR_MODEL,
        "audits_both_arms_for_leakage": len(cells) == len(audit_input["cells"]),
        "b_plan_specific": b_plan_specific,
        "b_repro_built_and_ran": b_repro_built,
        "cells": cells,
        "completed_at": utc_now(),
        "framework": FRAMEWORK,
        "no_leakage": no_leakage,
        "no_undisclosed_prereg_mutation": no_mutation,
        "passes": no_leakage and no_mutation and b_plan_specific and b_repro_built,
        "raw_response_sha256": sha256_text(result["final_text"]),
        "schema_version": 1,
    }
    write_json(output_path, frozen_result)
    print(
        f"froze blinded {AUDITOR_MODEL}/{FRAMEWORK} audit: "
        f"passes={frozen_result['passes']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
