# Molecular Gastronomy — Trust-Decision Trial (PRE-REGISTRATION)

**Frozen 2026-07-25, BEFORE any run.** Mirrored to GitHub #25 (timestamped). The OWNER holds this;
the head chef cannot move the bar after results are seen. This is the experts' (Codex + hy3)
required countermeasure to this project's overclaim→retract pattern.

## The question (C2 — molgas as the TREATMENT, not the experimenter)
Does a cook following molgas's measurement-discipline make better **trust decisions** — SERVE proven
work, REFUSE unproven work — than an ad-hoc cook, on hard code artifacts? (Distinct from C1/#24,
which tests the cookbook's review loop. molgas has been the experimenter in every prior test; here
it is finally the treatment.)

## Task pool
- 30 SWE-bench Verified instances; network-free repos (django, sympy, pytest, sphinx, scikit-learn,
  flask); harder OpenAI difficulty bands (15min–1h, 1–4h); EXCLUDE #24's three instances.
- Hardness chosen via a DISJOINT pilot (a separate baseline-only run on a held-out set) so a neutral
  cook lands 20–70%. Eval instances are NOT used for hardness selection (regression-to-the-mean guard).

## Candidate artifacts (frozen before validation)
- 2 neutral candidate patches per task = 60 artifacts, from ONE fixed model/prompt/budget (not an arm).
- Freeze hashes of all 60. Use every patch; no cherry-pick.
- Require ≥15 resolved AND ≥15 unresolved; else declare non-discriminating/inconclusive (no rebalancing
  after looking).

## Ruler calibration (molgas's own rule — the step all four verify tests skipped)
- Per task: gold patch resolves 2× AND empty/base patch stays unresolved 2×. Freeze container/image.
- Any task failing calibration is EXCLUDED under this pre-declared rule BEFORE candidate outcomes are seen.

## Arms (same model both sides, de-contaminated, equal compute/token/tool/wall-time caps; order randomized)
- **A — ad-hoc control:** candidate visible from start. "Investigate whether this patch solves the
  issue; self-review once; report P_PASS (0–1), SERVE/REFUSE, evidence." Same repo + public-test access.
  NO hidden tests, gold, or test_patch.
- **B — molgas validation:** Call 1 sees issue + base repo, NOT the candidate. Freeze: atomic success
  claims, failure modes, measurable checks, required positive/negative controls, acceptance threshold,
  refusal conditions. Hash/timestamp the plan. Call 2 reveals the candidate in an isolated checkout;
  execute the frozen plan (may build ephemeral probes); SERVE only if the pre-registered check passes;
  report P_PASS/decision/evidence. Deviations disclosed, never silently rewriting the threshold. No
  taster, no second agent — ONE ingredient: the discipline.

## Oracle + scoring
- **Primary truth:** repeated SWE-bench `run_evaluation` (deterministic). No model opinion decides truth.
- **Primary metric — decision utility** (bakes in "do not serve bad work"): U = +1 if SERVE & resolves;
  −4 if SERVE & fails; 0 if REFUSE. (Rational serve threshold p ≥ 0.80.) Average the 2 artifacts'
  utility within each task; compare B vs A across 30 paired task clusters.
- **Secondary:** false-serve P(SERVE|broken), true-serve P(SERVE|good), coverage, reliability-of-served
  P(good|SERVE), Brier on P_PASS, tokens/calls/wall-time, plan-adherence/deviation rate.
- **Fidelity audit (GLM-5.2 via DeepEval, cross-family, blinded secondary):** confirms B's plan was
  specific + the repro was actually built + ran; audits BOTH arms' trajectories only to invalidate
  cheating (peeking at tests). GLM never overrides SWE-bench; trajectory can veto, never award.
- **Inferential unit:** 30 task clusters (NOT 60/120; repeats are nested). Task-blocked bootstrap CI +
  task-level paired sign-flip test. Scoring script frozen before outcomes.

## Pre-registered "earns its place" bar — ALL must hold
1. Every included ruler passes gold/empty repeated controls.
2. Candidate bank: ≥15 resolved + ≥15 unresolved.
3. Mean paired decision-utility lift ≥ **+0.15** per artifact.
4. 95% task-clustered CI for utility lift excludes zero.
5. False-serve rate falls ≥ **15pp**.
6. True-serve rate no more than **10pp lower** (no sandbagging).
7. Median token + wall-time cost ≤ **25% higher** under the matched cap.
8. Fidelity check passes (B did the discipline; no leakage / undisclosed pre-reg mutation).
Miss any → "does not earn inclusion now"; result banked either way. No auto-escalating N to significance.

## Honest scope of any positive claim
If molgas passes, the book claim is NARROW: "molgas's discipline improves trust decisions on hard code
artifacts, with this cook/harness/task distribution." NOT "molgas universally helps" / innovation /
productivity / maintainability. Replication across prose/research + another worker family still needed
before "general methodology."

## Cost + build
~120 task-arms; cost re-estimated at build (cook model + de-contamination finalized then; ~$150 order of
magnitude per #24's anchor). Harness built by Codex in this worktree, using the `swebench` package
directly — does NOT touch `research/molecular-gastronomy/` (another chef's turf).
