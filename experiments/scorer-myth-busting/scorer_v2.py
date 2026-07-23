#!/usr/bin/env python3
"""Score an enrichment action log with v2 anti-gaming constraints."""

import json
import math
import sys
from collections import defaultdict
from typing import Any, Dict, Iterable, Tuple

DELEGATION_TOOLS = {"Agent", "Task"}
COOK_TOOLS = {"Edit", "Write", "NotebookEdit"}
EXEMPT_FILENAMES = {"KNOWN-HOLES.md", "TICKETS.md", "PRESS-LOG.md", "WHERE-WE-ARE.md"}
MISSING_TARGET_BUCKET = "<missing-target>"


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _safe_non_negative_int(value: Any) -> int | None:
    parsed = _safe_int(value)
    if parsed is None or parsed < 0:
        return None
    return parsed


def _safe_float(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        value_f = float(value)
    except (OverflowError, ValueError):
        return None
    if not math.isfinite(value_f):
        return None
    return value_f


def _target_bucket(target: Any) -> str:
    if isinstance(target, str) and target:
        return target
    return MISSING_TARGET_BUCKET


def _is_exempt_bucket(target: str) -> bool:
    # Path normalization is limited to basenames using `/` and `\\` only, exact match required.
    normalized = target.replace("\\", "/")
    base = normalized.rsplit("/", 1)[-1]
    return base in EXEMPT_FILENAMES


def _max_overlapping_intervals(intervals: Iterable[Tuple[float, float]]) -> int:
    # Freeze tie-break: process all interval-ends before starts at the same timestamp,
    # which is equivalent to treating delegation intervals as [ts_start, ts_end) half-open.
    events: list[tuple[float, int, int]] = []
    for start, end in intervals:
        events.append((start, 1, 1))  # start marker (apply +1 active delegation)
        events.append((end, 0, -1))  # end marker (apply -1 after all ended before starts)

    events.sort(key=lambda item: (item[0], item[1]))

    max_overlap = 0
    active = 0
    idx = 0
    while idx < len(events):
        current_time = events[idx][0]

        while idx < len(events) and events[idx][0] == current_time and events[idx][1] == 0:
            active += events[idx][2]
            idx += 1

        while idx < len(events) and events[idx][0] == current_time and events[idx][1] == 1:
            active += events[idx][2]
            idx += 1

        if active > max_overlap:
            max_overlap = active

    return max_overlap


def _score_from_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    # Score formula (frozen for v2):
    #   score = clamp(
    #       50.0
    #       + 5.0 * min(credited_delegations, 8)
    #       + min(10.0, 2.5 * log2(max_parallelism + 1))
    #       - 22.0 * cook_file_violation_count
    #       - 1.0 * malformed_line_count,
    #       0, 100)
    #
    # Why each term is independent-only-safe:
    # - credited_delegations depends ONLY on {outcome.subagent_produced_lines,
    #   outcome.checked, outcome.gate_passed}, which are hook-originated and cannot be
    #   spoofed by the orchestrator's own narration.
    # - max_parallelism is computed only from CREDITED delegation intervals (same criteria as
    #   credited_delegation_count: subagent_produced_lines >= 20 and checked/gate_passed true),
    #   using hook-captured timestamps only.
    # - cook_file_violation_count aggregates actual_lines per target bucket (hook-measured,
    #   defaults missing to 0) across all cook actions, then applies ONLY exact basename-
    #   based exemptions.
    # - malformed_line_count is the number of unparsable/malformed action rows and is not
    #   influenced by any claim field that the orchestrator could forge.
    # - Violation penalty is set to 22 per offending file while delegation credit is capped
    #   at +5 per credited delegation (max +40), so one violation cannot be offset by
    #   a single extra credited delegation.
    #
    # Anti-gaming note:
    # - credited_delegation_count and max_parallelism are independent-only-safe: they use only
    #   hook-sourced delegation fields, and max_parallelism only measures overlap across
    #   CREDITED delegations.
    # - cook_file_violation_count is only PARTIALLY independent-only-safe (see KNOWN LIMITATION in
    #   _parse_log): its line aggregation uses hook-measured actual_lines, but bucket membership is
    #   determined by target, which is self-reported.
    # - As a result, score can be distorted via self-reported target values unless exempt names are
    #   used honestly. See KNOWN LIMITATION for concrete abuse patterns and scope.

    credited = float(metrics["credited_delegation_count"])
    violations = float(metrics["cook_file_violation_count"])
    parallelism = float(metrics["max_parallelism"])
    malformed = float(metrics["malformed_line_count"])

    base_score = 50.0
    delegation_bonus = 5.0 * min(credited, 8.0)
    parallel_bonus = min(10.0, 2.5 * math.log2(parallelism + 1.0))
    violation_penalty = 22.0 * violations
    malformed_penalty = 1.0 * malformed

    raw = base_score + delegation_bonus + parallel_bonus - violation_penalty - malformed_penalty
    clamped = max(0.0, min(100.0, raw))

    why = (
        "v2 formula: score = clamp(50 + min(credited,8)*5 + min(10, 2.5*log2(max_parallelism+1)) "
        "- 22*violations - malformed, 0-100). "
        f"(credited={int(credited)}, parallelism={int(parallelism)}, violations={int(violations)}, "
        f"malformed={int(malformed)}, delegated_bonus={delegation_bonus:.1f}, "
        f"parallel_bonus={parallel_bonus:.2f}, violation_penalty={violation_penalty:.1f}, "
        f"malformed_penalty={malformed_penalty:.1f}, raw={raw:.3f})"
    )

    return {
        "score": round(clamped, 1),
        "why": why,
        "delegation_bonus": round(delegation_bonus, 1),
        "parallelism_bonus": round(parallel_bonus, 2),
        "violation_penalty": round(violation_penalty, 1),
        "malformed_penalty": round(malformed_penalty, 1),
        "raw_score": round(raw, 3),
    }


def _parse_log(path: str) -> Tuple[Dict[str, Any], list[tuple[float, float]], list[str]]:
    metrics: Dict[str, Any] = {
        "total_delegation_count": 0,
        "real_substantial_delegation_count": 0,
        "credited_delegation_count": 0,
        "malformed_line_count": 0,
        "invalid_parallelism_timestamp_count": 0,
    }

    # KNOWN LIMITATION:
    # cook_file_violation_count is only partially independent-only-safe.
    # The aggregated quantity used for the violation (actual_lines) is independently measured and is
    # not forgeable via narration, but the per-file bucket is derived from `target` through
    # _target_bucket. Since `target` is only self-reported in frozen input, an orchestrator can:
    #   (a) mislabel a real file under an exempt basename (e.g. KNOWN-HOLES.md) to skip the penalty; or
    #   (b) split one file's edits across multiple fabricated target strings to keep each bucket <=15.
    # Eliminating this gap requires a schema field that captures file identity independently of self
    # reported fields for cook actions; that input is not available here.
    cook_per_file: dict[str, int] = defaultdict(int)
    violating_file_totals: dict[str, int] = {}
    intervals: list[tuple[float, float]] = []

    model = "unspecified"
    harness = "unspecified"

    try:
        with open(path, "r", encoding="utf-8") as handle:
            for line_no, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    metrics["malformed_line_count"] += 1
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    metrics["malformed_line_count"] += 1
                    continue

                if not isinstance(entry, dict):
                    metrics["malformed_line_count"] += 1
                    continue

                if line_no == 1 and "meta" in entry:
                    meta = entry.get("meta")
                    if isinstance(meta, dict):
                        if isinstance(meta.get("model"), str):
                            model = meta.get("model")
                        if isinstance(meta.get("harness"), str):
                            harness = meta.get("harness")
                    continue

                tool = entry.get("tool")
                if not isinstance(tool, str):
                    metrics["malformed_line_count"] += 1
                    continue

                if tool in DELEGATION_TOOLS:
                    metrics["total_delegation_count"] += 1
                    is_credited_delegation = False

                    outcome = entry.get("outcome")
                    if isinstance(outcome, dict):
                        produced = _safe_non_negative_int(outcome.get("subagent_produced_lines"))
                        if produced is not None and produced >= 20:
                            metrics["real_substantial_delegation_count"] += 1
                            checked = outcome.get("checked")
                            gate_passed = outcome.get("gate_passed")
                            if isinstance(checked, bool) and isinstance(gate_passed, bool) and checked and gate_passed:
                                metrics["credited_delegation_count"] += 1
                                is_credited_delegation = True

                    ts_start = _safe_float(entry.get("ts_start"))
                    ts_end = _safe_float(entry.get("ts_end"))
                    if ts_start is None and ts_end is None:
                        continue
                    if ts_start is None or ts_end is None or ts_end < ts_start:
                        if "ts_start" in entry or "ts_end" in entry:
                            metrics["invalid_parallelism_timestamp_count"] += 1
                        continue
                    if ts_start == ts_end:
                        continue
                    if is_credited_delegation:
                        intervals.append((ts_start, ts_end))

                elif tool in COOK_TOOLS:
                    bucket = _target_bucket(entry.get("target"))
                    file_lines = _safe_non_negative_int(entry.get("actual_lines"))
                    if file_lines is None:
                        file_lines = 0
                    cook_per_file[bucket] += file_lines

    except OSError:
        raise

    metrics["max_parallelism"] = _max_overlapping_intervals(intervals)

    cook_totals_sorted = dict(sorted(cook_per_file.items(), key=lambda item: item[0]))
    for target, total in cook_totals_sorted.items():
        if total > 15 and not _is_exempt_bucket(target):
            violating_file_totals[target] = total

    metrics["cook_actual_lines_per_file"] = cook_totals_sorted
    metrics["violating_cook_files"] = dict(sorted(violating_file_totals.items(), key=lambda item: item[0]))
    metrics["cook_file_violation_count"] = len(violating_file_totals)

    return metrics, intervals, [model, harness]


# Self-check against v1 exploit pattern:
# (a) A fake delegation with keyword-stuffed target/claimed_lines only scores if outcome.subagent_produced_lines
#     is a non-negative int >= 20 AND outcome.checked/gate_passed are both true.
# (b) Cook edits are always aggregated by target bucket using actual_lines across the full log; chunked edits to the same
#     target sum together and create at most one violation bucket whenever the total exceeds 15.


def _error(msg: str, details: str | None = None) -> None:
    payload = {"error": msg}
    if details is not None:
        payload["details"] = details
    print(json.dumps(payload, sort_keys=True, indent=2))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        _error("Usage: score_v2.py <path-to-log.jsonl>")
        return 2

    log_path = argv[1]
    try:
        metrics, _intervals, model_harness = _parse_log(log_path)
    except (OSError, UnicodeDecodeError) as exc:
        _error("Unable to read log file", str(exc))
        return 3

    scoring = _score_from_metrics(metrics)

    output = {
        "scorer_version": "v2",
        "model": model_harness[0],
        "harness": model_harness[1],
        "total_delegation_count": metrics["total_delegation_count"],
        "real_substantial_delegation_count": metrics["real_substantial_delegation_count"],
        "credited_delegation_count": metrics["credited_delegation_count"],
        "cook_file_violation_count": metrics["cook_file_violation_count"],
        "max_parallelism": metrics["max_parallelism"],
        "malformed_line_count": metrics["malformed_line_count"],
        "invalid_parallelism_timestamp_count": metrics["invalid_parallelism_timestamp_count"],
        "cook_actual_lines_per_file": metrics["cook_actual_lines_per_file"],
        "violating_cook_files": metrics["violating_cook_files"],
        "why": scoring["why"],
        "score": scoring["score"],
        "delegation_bonus": scoring["delegation_bonus"],
        "parallelism_bonus": scoring["parallelism_bonus"],
        "violation_penalty": scoring["violation_penalty"],
        "malformed_penalty": scoring["malformed_penalty"],
        "raw_score": scoring["raw_score"],
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
