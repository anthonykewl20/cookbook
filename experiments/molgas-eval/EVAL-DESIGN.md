# Molecular Gastronomy — its own eval suite (design)

## Why this exists
Two improvised fact-check batteries **ceiling'd (lift 0)**: fact-checking is too easy for current
agents, with or without any process. Molgas can only be scored on tasks **hard enough that ad-hoc
work fails.** This suite is built to measure real lift, per owner direction: develop-tests method
+ SWE-bench + DeepEval.

## Goal
Benchmark and score Molecular Gastronomy: does following it produce **better-validated new things**
than doing the same job ad-hoc? Metric = **LIFT** (molgas − baseline) on hard tasks, against a
pre-registered bar.

## Two rulers (the owner's tools)
- **Code arm — SWE-bench.** Hard Verified tasks (baseline resolve-rate well under 100%). Two cooks:
  molgas-process vs ad-hoc. Score by hidden tests (deterministic). Lift = resolve-rate delta. Tests
  the *prototype + verify* half.
- **Prose arm — DeepEval.** Hard research/reasoning tasks (synthesis, claim-checking on contested
  ground, decision memos). Two cooks: molgas vs ad-hoc. Score by DeepEval metrics (faithfulness,
  answer-relevance…) + an LLM **judge that is NOT the cook** (develop-tests rule). Lift = score
  delta. Tests the *research + verify* half.

## Method (develop-tests, applied)
- SMART targets fixed **first**.
- Many cases; include nasty edge cases (ambiguous, trap, adversarial).
- Held-out set, scored only at the end.
- Grade with a **different model** than generated.
- **Anti-ceiling rule (learned twice):** if the baseline arm scores near-perfect, the task set is
  too easy — STOP, swap in harder cases before trusting any lift number. A ceiling proves nothing.

## Scope / non-overlap
- Prose arm is mine: a fresh DeepEval venv (the system Python is uv-managed — never pip into it).
- Code arm coordinates with #24 (shared SWE-bench infra). Different subject (molgas the process vs
  the cookbook) — not a duplicate.
- Experimental. Not for the book.

## Build order
1. Prose arm (DeepEval) — mine, no clash. First.
2. Code arm (SWE-bench) — alongside #24.

## Results so far — the prose arm CEILINGS (3 times)
- v1 fact-check battery: ceiling (lift 0).
- v2 controlled fact-check battery (4 cooks, traps): ceiling (lift 0).
- Prose faithfulness/refusal (molgas vs baseline, 10 Qs): **ceiling again — both 10/10, lift 0.** The
  plain cook refused the unanswerable questions on its own, without any process.
- **Pattern (3 ceilings):** on verify / QA / refuse tasks, a competent plain cook already does the
  right thing. molgas adds nothing measurable there. Headroom exists ONLY on hard creative tasks
  (build working code on hard problems) — i.e., SWE-bench, the code arm, = #24.
- **Conclusion:** DeepEval/prose cannot benchmark molgas (proven 3x). The real benchmark is the
  SWE-bench code arm. Recommend letting #24's result stand as molgas's create-arm score.

## ⚠️ RETRACTION — hy3 gate FAIL (2026-07-24). The "Conclusion" above is VOID.

hy3 reviewed this method and the "3 ceilings." **Gate FAIL — accepted, not appealed.** The claims
above are **retracted, un-gated, pending a proper re-run:**

- **"DeepEval/prose can't benchmark molgas (proven 3x)"** — DeepEval was *never run* (and can't run
  here yet: no LLM key is configured). Eyeballed, not measured. Cannot prove a tool useless by not
  using it.
- **"3 ceilings prove prose/verify can't benchmark molgas"** — **restriction-of-range error.** When
  the baseline already scores 100%, the test has ~zero power to detect any effect. These tasks were
  too easy, not the medium useless. (Also: the "independent" cooks are one model family — correlated
  priors, not independent; gold was bootstrapped from those same priors.)
- **"Let #24 stand as molgas's benchmark"** — #24 is a self-diagnosed under-powered TIE; laundering a
  null into a benchmark. #24 is ONE battery inside molgas's eval, not molgas's eval.

**What hy3 credits as sound (kept):** outcome-lift A/B, a deterministic judge separate from the cook,
the `--safe-mode` de-contamination catch, pre-registration, McNemar, a compute-control arm. Machinery
good; discipline lapsed at the finish line.

**Required before any of this counts:** (1) power/ceiling pre-check — disqualify any task where
baseline > ~75%, compute N for +10pp @ p<0.05, power 0.8; (2) actually run DeepEval with a
cross-family judge calibrated vs human labels (report κ); (3) redesign tasks for headroom (baseline
must fail a real fraction); (4) write molgas's own two-arm eval spec, distinct from #24; (5) re-gate
before recording anything as proven.

**Status: unproven, un-gated. Owner directs the path.**
