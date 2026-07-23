#!/usr/bin/env python3
"""Score an action log for adherence to head-chef handbook guidance.

The script consumes a JSONL action log (one object per line), computes summary
counts such as delegation volume, parallel delegation, and large cook edits, then
produces a single JSON dashboard object with a reproducible adherence score.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter


DELEGATE_TOOLS = {"Agent", "Task"}
COOK_TOOLS = {"Edit", "Write", "NotebookEdit"}
BOOKKEEPING_BASENAMES = {
    "KNOWN-HOLES.md",
    "TICKETS.md",
    "PRESS-LOG.md",
    "WHERE-WE-ARE.md",
}


def _safe_int(value, default: int | None = 0) -> int | None:
    """Parse an integer field defensively; fallback to default on any failure."""
    if value is None:
        return default
    try:
        if isinstance(value, float) and not math.isfinite(value):
            return default
        parsed = int(value)
    except (TypeError, ValueError, OverflowError):
        return default
    return parsed if parsed >= 0 else default


def _normalize_target(raw_target) -> str:
    if raw_target is None:
        return ""
    if not isinstance(raw_target, str):
        return str(raw_target)
    return raw_target


def _is_bookkeeping(target: str) -> bool:
    parts = [part for part in target.replace("\\", "/").split("/") if part]
    if not parts:
        return False
    basename = parts[-1]
    if basename in BOOKKEEPING_BASENAMES:
        return True
    return "records" in parts


def _is_substantial_delegation(action: dict) -> bool:
    """Heuristic used uniformly for every delegation action.

    A delegation is "substantial" when at least TWO of these conditions hold:
    1) lines_changed >= 20
    2) files_touched > 1
    3) target string length >= 24 chars (non-trivial descriptor)
    4) target contains an indicative keyword (build, implement, fix, refactor, etc.)
    """
    target = action["target"].lower()
    conditions = 0
    if action["lines_changed"] >= 20:
        conditions += 1
    if action["files_touched"] > 1:
        conditions += 1
    if len(action["target"]) >= 24:
        conditions += 1

    keywords = (
        "implement",
        "build",
        "refactor",
        "investigate",
        "analyze",
        "fix",
        "create",
        "migrate",
        "update",
        "add",
        "remove",
        "rework",
        "prepare",
        "prototype",
    )
    if any(keyword in target for keyword in keywords):
        conditions += 1
    return conditions >= 2


def _is_substantial_violation(action: dict) -> bool:
    return (
        (action["lines_changed"] > 15 or action["files_touched"] > 1)
        and not _is_bookkeeping(action["target"])
    )


def parse_log(path: str) -> dict:
    parsed_counts = {
        "total_actions": 0,
        "malformed_lines": 0,
        "delegate_count": 0,
        "substantial_delegate_count": 0,
        "cook_count": 0,
        "substantial_cook_violations": 0,
    }
    delegate_turns = Counter()

    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                parsed_counts["malformed_lines"] += 1
                continue

            if not isinstance(payload, dict):
                parsed_counts["malformed_lines"] += 1
                continue

            parsed_counts["total_actions"] += 1

            action = {
                "tool": str(payload.get("tool", "")),
                "target": _normalize_target(payload.get("target", "")),
                "turn": _safe_int(payload.get("turn"), default=None),
                "lines_changed": _safe_int(payload.get("lines_changed"), default=0),
                "files_touched": _safe_int(payload.get("files_touched"), default=1),
            }

            if action["tool"] in DELEGATE_TOOLS:
                parsed_counts["delegate_count"] += 1
                if action["turn"] is not None:
                    delegate_turns[action["turn"]] += 1
                if _is_substantial_delegation(action):
                    parsed_counts["substantial_delegate_count"] += 1

            if action["tool"] in COOK_TOOLS:
                parsed_counts["cook_count"] += 1
                if _is_substantial_violation(action):
                    parsed_counts["substantial_cook_violations"] += 1

    parsed_counts["trivial_delegate_count"] = (
        parsed_counts["delegate_count"] - parsed_counts["substantial_delegate_count"]
    )
    parsed_counts["max_parallelism"] = max(delegate_turns.values(), default=0)

    return parsed_counts



def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


# FROZEN FORMULA BLOCK (do not edit during runtime work)
#
# 1) Base score starts at 50.0.
#
# 2) Substantial delegation credit is computed from:
#    - substantial_delegate_count, where a delegation is counted as substantial only if it
#      satisfies at least 2 of the 4 heuristic signals from _is_substantial_delegation:
#      lines_changed >= 20; files_touched > 1; target string length >= 24; keyword match
#      in target (implement, build, refactor, investigate, analyze, fix, create, migrate,
#      update, add, remove, rework, prepare, prototype).
#      This 2-of-4 rule is a defensibility choice: it requires evidence of either broad impact
#      (multi-file/large-change) or an explicitly substantive task description, so one weak signal
#      alone cannot qualify a delegation as substantial.
#    - ANTI-GAMING RULE: raw delegate_count is NEVER used as a scoring input; only
#      substantial_delegate_count (the count passing the heuristic above) earns delegation credit.
#    - delegation_credit_per_action = 6.0 points each
#    - delegation_cap = 30.0 total points before displacement damping
#    - This anti-gaming cap prevents very long sessions from inflating score by sheer delegation volume.
#
# 3) Cook overrun displacement dampens delegation credit:
#    - cook_limit = 4 * substantial_delegate_count + 5
#    - cook_excess = max(0, cook_count - cook_limit)
#    - displacement factor = max(0.0, 1.0 - cook_excess / 20.0)
#    - each excess cook action beyond cook_limit removes an additional 1/20th (5%) of the
#      already-capped delegation credit (linear damping, floored at 0), so 20 or more excess
#      cooks fully displaces all delegation credit.
#
# 4) Parallelism bonus is:
#    - parallel_bonus = min(12.0, 5.0 * log2(max_parallelism)) when max_parallelism > 1
#      else 0.
#    - cap(12.0) and log2 diminishing returns reward genuine breadth without over-rewarding extreme parallelization.
#
# 5) Penalties:
#    - violation_penalty = 15.0 per substantial_cook_violation (anti-gaming for risky direct cook actions)
#    - malformed_penalty = 0.4 per malformed_lines entry.
#    - Both are subtracted from the score.
#    - The 15.0 violation penalty is intentionally more than twice a single delegation's
#      marginal value of 6.0, so one violation cannot be paid off by adding one more
#      delegation (15 > 2 * 6 = 12).
#
# 6) Final score is clamped to [0, 100] and rounded to 1 decimal place.

def compute_adherence_score(metrics: dict) -> tuple[float, dict[str, float], str]:
    base_score = 50.0
    substantial_delegate_count = metrics["substantial_delegate_count"]

    delegation_credit_per_action = 6.0
    delegation_cap = 30.0
    raw_delegation_credit = substantial_delegate_count * delegation_credit_per_action
    capped_delegation_credit = min(raw_delegation_credit, delegation_cap)

    cook_limit = (4 * substantial_delegate_count) + 5
    cook_excess = max(0, metrics["cook_count"] - cook_limit)
    displacement_factor = max(0.0, 1.0 - (cook_excess / 20.0))
    delegation_credit = round(capped_delegation_credit * displacement_factor, 3)

    if metrics["max_parallelism"] <= 1:
        parallel_bonus = 0.0
    else:
        parallel_bonus = min(12.0, 5.0 * math.log2(metrics["max_parallelism"]))

    violation_penalty = 15.0 * metrics["substantial_cook_violations"]
    malformed_penalty = 0.4 * metrics["malformed_lines"]

    raw_score = (
        base_score
        + delegation_credit
        + parallel_bonus
        - violation_penalty
        - malformed_penalty
    )

    clamped_score = _clamp(raw_score, 0.0, 100.0)
    final_score = round(clamped_score, 1)

    why = (
        f"Base 50.0 plus {delegation_credit:.1f} delegation credit from {substantial_delegate_count} "
        f"substantial delegations (raw {raw_delegation_credit:.1f}, capped {capped_delegation_credit:.1f}, "
        f"cook_limit={cook_limit}, cook_count={metrics['cook_count']}), plus parallelism of {metrics['max_parallelism']} "
        f"adding {parallel_bonus:.1f} points. "
        f"{metrics['substantial_cook_violations']} substantial cook violation(s) cost {violation_penalty:.1f} points "
        f"and final score is {final_score}."
    )
    if clamped_score != raw_score:
        why += f" (clamped from {raw_score:.1f} to {final_score})"
    if malformed_penalty > 0:
        why += f" Malformed lines cost {malformed_penalty:.1f} points across {metrics['malformed_lines']} malformed entries."

    supporting = {
        "base_score": base_score,
        "raw_delegation_credit": raw_delegation_credit,
        "capped_delegation_credit": capped_delegation_credit,
        "displacement_factor": displacement_factor,
        "displacement_adjusted_delegation_credit": delegation_credit,
        "cook_limit": cook_limit,
        "cook_excess": cook_excess,
        "parallel_bonus": parallel_bonus,
        "violation_penalty": violation_penalty,
        "malformed_penalty": malformed_penalty,
        "raw_score_before_clamp": raw_score,
    }
    return final_score, supporting, why


def main(argv: list[str] | None = None) -> int:
    args = sys.argv if argv is None else argv
    if len(args) != 2:
        print(json.dumps({"error": "Usage: score.py <path-to-log.jsonl>"}, indent=2, sort_keys=True))
        return 2

    log_path = args[1]
    try:
        metrics = parse_log(log_path)
    except (OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 1

    adherence_score, supporting, why = compute_adherence_score(metrics)

    output = {
        "total_actions": metrics["total_actions"],
        "malformed_lines": metrics["malformed_lines"],
        "delegate_count": metrics["delegate_count"],
        "substantial_delegate_count": metrics["substantial_delegate_count"],
        "trivial_delegate_count": metrics["trivial_delegate_count"],
        "cook_count": metrics["cook_count"],
        "substantial_cook_violations": metrics["substantial_cook_violations"],
        "max_parallelism": metrics["max_parallelism"],
        "adherence_score": adherence_score,
        "why": why,
        **supporting,
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
