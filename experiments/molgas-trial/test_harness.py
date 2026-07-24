"""Cheap synthetic checks at the harness's frozen public seams."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from common import (
    _safe_model_environment,
    _screen_run_artifacts,
    normalize_decision,
    payload_sha256,
    sha256_text,
    validate_cook_template,
)
from run_trial import load_plan, render_prompt, validate_plan
from score import clustered_bootstrap_ci, exact_paired_sign_flip
from select_tasks import (
    ALLOWED_DIFFICULTIES,
    ALLOWED_REPOS,
    EXCLUDED_INSTANCES,
    select_rows,
)


def fake_row(repo: str, difficulty: str, number: int) -> dict:
    return {
        "base_commit": f"{number:040x}",
        "difficulty": difficulty,
        "instance_id": f"{repo.replace('/', '__')}-{number}",
        "problem_statement": f"issue {number}",
        "repo": repo,
    }


class TaskSelectionTests(unittest.TestCase):
    def test_selection_is_seeded_band_stratified_and_eligible(self) -> None:
        rows = [
            fake_row(repo, difficulty, repo_index * 1000 + band_index * 100 + item)
            for repo_index, repo in enumerate(ALLOWED_REPOS)
            for band_index, difficulty in enumerate(ALLOWED_DIFFICULTIES)
            for item in range(10)
        ]
        rows.extend(
            [
                {
                    **fake_row("pytest-dev/pytest", "1-4 hours", 5262),
                    "instance_id": "pytest-dev__pytest-5262",
                },
                fake_row("astropy/astropy", "1-4 hours", 9999),
                fake_row("django/django", "<15 min fix", 9998),
            ]
        )
        first = select_rows(rows, count=12, seed=7)
        second = select_rows(rows, count=12, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(
            {difficulty: sum(row["difficulty"] == difficulty for row in first)
             for difficulty in ALLOWED_DIFFICULTIES},
            {difficulty: 6 for difficulty in ALLOWED_DIFFICULTIES},
        )
        self.assertTrue(all(row["repo"] in ALLOWED_REPOS for row in first))
        self.assertTrue(
            all(row["instance_id"] not in EXCLUDED_INSTANCES for row in first)
        )


class ProtocolParsingTests(unittest.TestCase):
    def test_cook_template_requires_token_cap_and_claude_safe_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing placeholders"):
            validate_cook_template("glm-exec {run_dir}")
        with self.assertRaisesRegex(ValueError, "safe-mode"):
            validate_cook_template(
                "my-claude-wrapper --model {model} --budget {max_tokens} "
                "--thinking {max_compute_tokens} --tools {max_tool_calls}"
            )
        self.assertTrue(
            validate_cook_template(
                "my-claude-wrapper {safe_mode} --model {model} "
                "--budget {max_tokens} --thinking {max_compute_tokens} "
                "--tools {max_tool_calls}"
            )
        )

    def test_decision_parser_fail_closes_malformed_output(self) -> None:
        decision, errors = normalize_decision("not JSON")
        self.assertEqual(decision["decision"], "REFUSE")
        self.assertEqual(decision["p_pass"], 0.0)
        self.assertTrue(errors)

    def test_decision_parser_accepts_registered_schema(self) -> None:
        decision, errors = normalize_decision(
            '{"P_PASS": 0.85, "decision": "SERVE", "evidence": ["pytest: 2 passed"]}'
        )
        self.assertEqual(errors, [])
        self.assertEqual(decision["decision"], "SERVE")
        self.assertEqual(decision["p_pass"], 0.85)

    def test_decision_parser_requires_evidence(self) -> None:
        decision, errors = normalize_decision(
            '{"P_PASS": 0.85, "decision": "SERVE"}'
        )
        self.assertEqual(decision["evidence"], [])
        self.assertIn(
            "evidence must be a non-empty string or list of strings", errors
        )

    def test_plan_requires_both_control_polarities(self) -> None:
        _, errors = validate_plan(
            """{
              "atomic_success_claims": ["claim"],
              "failure_modes": ["mode"],
              "checks": ["check"],
              "required_controls": {"positive": ["yes"], "negative": []},
              "acceptance_threshold": "all pass",
              "refusal_conditions": ["any failure"]
            }"""
        )
        self.assertIn("required_controls.negative must be a non-empty list", errors)

    def test_plan_rejects_non_falsifiable_null_entries(self) -> None:
        _, errors = validate_plan(
            """{
              "atomic_success_claims": [null],
              "failure_modes": ["mode"],
              "checks": [null],
              "required_controls": {"positive": ["yes"], "negative": [null]},
              "acceptance_threshold": "all pass",
              "refusal_conditions": ["any failure"]
            }"""
        )
        self.assertIn(
            "atomic_success_claims must contain only non-empty strings", errors
        )
        self.assertIn("checks[0] must be an object", errors)
        self.assertIn(
            "required_controls.negative must contain non-empty strings", errors
        )

    def test_prompt_rendering_preserves_json_braces(self) -> None:
        self.assertEqual(
            render_prompt('{"decision": "SERVE"} {issue}', issue="example"),
            '{"decision": "SERVE"} example',
        )
        self.assertEqual(
            render_prompt("{first} {second}", first="{second}", second="value"),
            "{second} value",
        )

    def test_frozen_plan_payload_is_bound_to_raw_response(self) -> None:
        plan = {
            "atomic_success_claims": ["claim"],
            "failure_modes": ["mode"],
            "checks": [
                {
                    "id": "C1",
                    "procedure": "run check",
                    "pass_condition": "exit 0",
                    "failure_mode_covered": "mode",
                }
            ],
            "required_controls": {
                "positive": ["known pass"],
                "negative": ["known fail"],
            },
            "acceptance_threshold": "C1 and controls pass",
            "refusal_conditions": ["anything fails"],
        }
        raw = json.dumps(plan)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plans").mkdir()
            (root / "cook-runs" / "plan").mkdir(parents=True)
            (root / "cook-runs" / "plan" / "final.txt").write_text(
                raw, encoding="utf-8"
            )
            record_path = root / "plans" / "task__candidate-1.json"
            record = {
                "candidate_id": "task::candidate-1",
                "errors": [],
                "plan": plan,
                "plan_sha256": payload_sha256(plan),
                "raw_response_path": "cook-runs/plan/final.txt",
                "raw_response_sha256": sha256_text(raw),
            }
            record_path.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(
                load_plan(root, "task::candidate-1")["plan_sha256"],
                payload_sha256(plan),
            )
            record["plan"]["acceptance_threshold"] = "silently rewritten"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "normalization changed"):
                load_plan(root, "task::candidate-1")


class SecretBoundaryTests(unittest.TestCase):
    def test_model_environment_drops_unallowlisted_credentials(self) -> None:
        with patch.dict(
            os.environ,
            {
                "PATH": "/usr/bin",
                "OPENAI_API_KEY": "must-not-cross-boundary",
                "UNRELATED_PRIVATE_VALUE": "also-private",
            },
            clear=True,
        ):
            environment = _safe_model_environment()
        self.assertEqual(environment, {"PATH": "/usr/bin"})

    def test_retained_secret_like_artifact_is_redacted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "trajectory.txt"
            artifact.write_text(
                "leak sk-abcdefghijklmnopqrstuvwxyz123456",
                encoding="utf-8",
            )
            violations = _screen_run_artifacts(Path(directory))
            self.assertEqual(
                violations,
                ["trajectory.txt: secret-like value redacted"],
            )
            self.assertNotIn("sk-", artifact.read_text(encoding="utf-8"))


class InferenceTests(unittest.TestCase):
    def test_exact_sign_flip_uses_task_clusters(self) -> None:
        self.assertEqual(exact_paired_sign_flip([1.0, 1.0, 1.0]), 0.25)

    def test_clustered_bootstrap_is_seeded(self) -> None:
        self.assertEqual(
            clustered_bootstrap_ci([0.5, 0.5], samples=100, seed=1),
            (0.5, 0.5),
        )


if __name__ == "__main__":
    unittest.main()
