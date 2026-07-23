# Molecular Gastronomy — work-in-progress (resume here)

**Tracker:** GitHub issue **#25** (the process) and **#24** (its first dish — the SWE-bench A/B).
The full narrative + pre-registrations + results live as comments on those two issues. This
folder holds the reusable harness so a fresh clone can continue.

## What Molecular Gastronomy is
A cookbook-wide process for creating anything NEW: `idea → interview → research → prototype in
an isolated box → serve ONLY once the metric is static and measurable`. Two rules: unknowns are
myth-busted (measured), not fired at the owner as questions; a fluctuating metric means the
measuring instrument is broken (fix the ruler first). Prior art: Spike / PoC / Tracer Bullet /
REPL / Build-Measure-Learn. Eval layer (what those methods lack): **measurable + static +
calibrated-with-controls + pre-registered**, chosen per dish (code → SWE-bench; prose → taster;
else → a calibrated ruler).

## Status as of 2026-07-24 (end of session)
- ✅ Process defined (#25).
- ✅ Code ruler = **SWE-bench installed + calibrated** (gold→resolved, empty→unresolved). Network-
  dependent repos (e.g. `psf/requests`) do NOT run — this sandbox has no network inside the eval
  container. Use self-contained repos (django, sympy, sphinx, scikit-learn, pytest, flask, …).
- ✅ Tracer bullet passed (one instance through the whole pipe).
- ✅ First real A/B ran (`ab_run.py`, 3 instances × 3 repeats × 2 arms, 0 failures).
  **Result: TIE** — baseline 7/9, process 7/9; static-fraction 2/3 both. **Inconclusive, not a
  failure of the process:** 2 of 3 instances were solved 3/3 by both arms (ceiling effect) and the
  1 hard instance stayed flaky in both. The run was under-powered by easy instance selection.
- ❌ Owner decision still open: where (if) Molecular Gastronomy lands in the bound book.

## NEXT (pick up here tomorrow)
1. **Re-run the A/B with HARDER instances** — pick ones where a plain cook fails often (baseline
   resolve-rate well under 100%), and more of them, so there is power to see a difference.
2. Consider a **stronger taster** (a different/larger model than the cook).
3. Keep the threshold pre-registered *before* the run.

## Setup (rebuild on any machine)
```bash
python3 -m venv ~/.swebench-venv
~/.swebench-venv/bin/pip install swebench          # harness (v4.1.0 used)
# SWE-bench_Verified auto-downloads on first run; Docker required (pulls prebuilt images
# from the `swebench` dockerhub namespace). gh must be a WRITE-access account for the board.
```

## Run it
```bash
# dry-run: print the plan only
~/.swebench-venv/bin/python ab_run.py --dry-run --instances <id1> <id2> <id3>
# smoke: 1 instance, 1 repeat, both arms
~/.swebench-venv/bin/python ab_run.py --instances pallets__flask-5014 --repeats 1
# full: N instances × REPEATS × 2 arms  (edit INSTANCES/REPEATS at top of ab_run.py, or pass flags)
~/.swebench-venv/bin/python ab_run.py --instances <id1> <id2> <id3>
```
Arms: `baseline` = one cook (single shot); `process` = cook → a **taster (never the cook)** reviews
before submit, one revision allowed. Cooks/tasters run via `glm-exec` and are **blind** to the gold
patch and the tests. Output: `ab-report.json` — per-arm resolve-rate, per-instance STATIC/FLAKY
consistency, and the process−baseline delta.
