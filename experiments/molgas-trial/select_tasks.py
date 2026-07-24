#!/usr/bin/env python3
"""Freeze 30 eligible SWE-bench Verified tasks without using outcome data."""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from pathlib import Path

from common import (
    DATASET_NAME,
    DATASET_SPLIT,
    PUBLIC_TASK_FIELDS,
    payload_sha256,
    utc_now,
    write_json,
)

HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "tasks.json"
DEFAULT_SEED = 20260725
DEFAULT_COUNT = 30

ALLOWED_REPOS = (
    "django/django",
    "pallets/flask",
    "pytest-dev/pytest",
    "scikit-learn/scikit-learn",
    "sphinx-doc/sphinx",
    "sympy/sympy",
)
ALLOWED_DIFFICULTIES = ("15 min - 1 hour", "1-4 hours")
EXCLUDED_INSTANCES = {
    "pallets__flask-5014",
    "pylint-dev__pylint-8898",
    "pytest-dev__pytest-5262",
    "pytest-dev__pytest-7490",
}


def select_rows(rows: list[dict], *, count: int, seed: int) -> list[dict]:
    """Seeded, band-stratified round-robin selection across eligible repos."""
    if count <= 0:
        raise ValueError("count must be positive")
    eligible = [
        row
        for row in rows
        if row.get("repo") in ALLOWED_REPOS
        and row.get("difficulty") in ALLOWED_DIFFICULTIES
        and row.get("instance_id") not in EXCLUDED_INSTANCES
    ]
    if len(eligible) < count:
        raise ValueError(f"only {len(eligible)} eligible tasks for requested count {count}")

    # Split the bank as evenly as possible across the two pre-registered bands.
    quotas = {
        ALLOWED_DIFFICULTIES[0]: (count + 1) // 2,
        ALLOWED_DIFFICULTIES[1]: count // 2,
    }
    rng = random.Random(seed)
    selected: list[dict] = []
    for difficulty in ALLOWED_DIFFICULTIES:
        by_repo: dict[str, list[dict]] = {repo: [] for repo in ALLOWED_REPOS}
        for row in eligible:
            if row["difficulty"] == difficulty:
                by_repo[row["repo"]].append(row)
        for repo, candidates in by_repo.items():
            candidates.sort(key=lambda item: item["instance_id"])
            random.Random(f"{seed}:{difficulty}:{repo}").shuffle(candidates)

        band: list[dict] = []
        active_repos = [repo for repo in ALLOWED_REPOS if by_repo[repo]]
        while len(band) < quotas[difficulty] and active_repos:
            cycle = list(active_repos)
            rng.shuffle(cycle)
            for repo in cycle:
                if len(band) == quotas[difficulty]:
                    break
                if by_repo[repo]:
                    band.append(by_repo[repo].pop())
                if not by_repo[repo]:
                    active_repos.remove(repo)
        if len(band) != quotas[difficulty]:
            raise ValueError(
                f"difficulty {difficulty!r} has only {len(band)} tasks; "
                f"needs {quotas[difficulty]}"
            )
        selected.extend(band)

    # The frozen order itself is randomized; downstream scripts preserve it.
    rng.shuffle(selected)
    public = [{field: row[field] for field in PUBLIC_TASK_FIELDS} for row in selected]
    ids = [row["instance_id"] for row in public]
    if len(ids) != len(set(ids)):
        raise AssertionError("selection produced duplicate instance IDs")
    return public


def load_rows(dataset_arrow: Path | None) -> list[dict]:
    from datasets import Dataset, load_dataset

    if dataset_arrow is not None:
        return list(Dataset.from_file(str(dataset_arrow)))
    return list(load_dataset(DATASET_NAME, split=DATASET_SPLIT))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Freeze a seeded, difficulty-stratified SWE-bench Verified task bank. "
            "No candidate or model outcome data is read."
        )
    )
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument(
        "--dataset-arrow",
        type=Path,
        help="Optional cached Arrow file; otherwise load the Hugging Face dataset.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = load_rows(args.dataset_arrow)
    tasks = select_rows(rows, count=args.count, seed=args.seed)
    bank = {
        "allowed_difficulties": list(ALLOWED_DIFFICULTIES),
        "allowed_repos": list(ALLOWED_REPOS),
        "dataset": DATASET_NAME,
        "excluded_instance_ids": sorted(EXCLUDED_INSTANCES),
        "frozen_at": utc_now(),
        "instance_ids": [task["instance_id"] for task in tasks],
        "schema_version": 1,
        "seed": args.seed,
        "selection_policy": (
            "Seeded 50/50 OpenAI difficulty-band stratification; within each "
            "band, seeded round-robin across eligible repositories. No outcome data."
        ),
        "split": DATASET_SPLIT,
        "task_bank_sha256": payload_sha256(tasks),
        "tasks": tasks,
    }
    write_json(args.output, bank)
    repo_counts = Counter(task["repo"] for task in tasks)
    band_counts = Counter(task["difficulty"] for task in tasks)
    print(f"froze {len(tasks)} task ids to {args.output}")
    print("repos:", dict(sorted(repo_counts.items())))
    print("difficulty:", dict(sorted(band_counts.items())))
    print("task_bank_sha256:", bank["task_bank_sha256"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
