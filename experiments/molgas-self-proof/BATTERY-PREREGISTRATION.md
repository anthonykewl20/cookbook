# Molecular Gastronomy self-proof v2 — CONTROLLED battery (pre-registered BEFORE any run)

**Why v2.** v1 (one easy, source-named claim, no controls) FAILED the hy3 gate: near-zero
discriminative power. This v2 fixes every structural flaw hy3 named: real controls, a no-process
baseline arm, planted-false claims, and a **deterministic script scorer** (not an agent's judgment).

## Design
- **8 claims** (3 true, 5 false), several with traps. Ground truth is FIXED in `groundtruth.json`
  before any cook runs — true claims pinned to the verified SWE-Skills-Bench paper (arXiv 2603.15401);
  false claims constructed false by design.
- **Two arms**, identical except one variable:
  - **Process arm:** cook is given the Molecular Gastronomy recipe, then verifies.
  - **Baseline arm:** cook is told only "verify these claims" — no recipe.
- **2 cooks per arm** (4 cooks total), blind to each other and to the planted labels. Each cook
  does all 8 claims. Within-arm agreement = a static-ness read.
- **Deterministic scorer:** `verify.py` matches each cook's TRUE/FALSE verdict to the fixed label.
  No agent judgment in scoring.

## Metric (computed by the script)
- **Accuracy** per cook (correct / 8), per arm (mean).
- **Sensitivity** = true claims correctly accepted (per arm).
- **Specificity** = false claims correctly rejected (per arm) — the thing v1 could not measure at all.
- **Lift** = process-arm accuracy − baseline-arm accuracy.
- **Static-ness** = within-arm agreement between the 2 cooks.

## Pre-registered verdict bar (FIXED before runs)
- **EARNS ITS KEEP:** process accuracy beats baseline by a clear margin (>=2 of 8, i.e. >=25pp)
  AND process specificity >= baseline specificity (catches false claims at least as well).
- **NOT PROVEN:** no clear lift, or the process arm fails on false claims.
- **Honest cap:** N=8 is small -> wide error bars. A pass is "controlled, preliminary positive,"
  not "proven beyond doubt." A fail is honest and final for this shape.

## Scope
Tests the research/verify arm. The create/prototype arm is #24 (other terminal). Not for the book.
