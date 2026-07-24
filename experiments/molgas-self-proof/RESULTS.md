# Molecular Gastronomy self-proof — RESULTS (frozen for the gate)

**Task:** verify the load-bearing claim *"SWE-Skills-Bench found that 39 of 49 agent skills gave
zero lift"* against its primary source. 3 fresh cooks, blind to each other; head chef verifies
independently as the gold standard. Pre-registered bar: **static (all 3 agree) + correct (matches
the verified source) = earns its keep.**

## What the 3 cooks returned (blind, independent)
All three: **VERDICT TRUE**, figure **"39 of 49 skills yield zero pass-rate improvement, average gain
only +1.2%"**, source **arXiv 2603.15401** ("SWE-Skills-Bench: Do Agent Skills Actually Help in
Real-World Software Engineering?", Han et al., Mar 2026), high confidence. Converged exactly.

## Head-chef gold verification
- **First pass (wrong):** my casual web search grabbed **SkillsBench** (arXiv 2602.12670) — a
  *different* paper: 84 tasks, +16.2pp lift, curated skills *help*. It does NOT contain "39 of 49".
  I nearly rejected the cooks on a false basis.
- **Corrected:** fetched arXiv 2603.15401 directly. **Confirmed real**: title, 7 authors, submitted
  2026-03-16, verbatim quote present. **Claim is TRUE.** The cooks were right; my first pass was wrong.

## Against the pre-registered bar
- **Static:** YES — 3/3 cooks, same verdict, same figure, same source.
- **Correct:** YES — matches the independently verified primary source.
- **Bar:** MET. On this test, Molecular Gastronomy turned the unknown into a verified, stable answer.

## Honest caveats (do not overclaim)
1. **Research/verify arm only.** This tested finding + extracting + verifying. The "prototype in an
   isolated box / create something new" arm is #24's (other terminal). Full worth = both arms.
2. **The easy end of verification.** The claim *named* its source ("SWE-Skills-Bench"), so this is
   confirming an attributed claim, not discovering non-obvious truth. **Partial circularity.** That
   said, there was a real trap — a confusingly-similar paper (SkillsBench) — and the 3 cooks
   navigated it correctly while the head chef's first pass did not.
3. **Small sample.** N=3 cooks on 1 claim. Static-ness shown for *this* claim, not broadly.

## Conclusion — GATE FAILED (hy3); overclaim retracted
**"Earns its keep" is retracted.** hy3's gate: this was a smoke test, not a proof — near-zero
discriminative power (no controls, no no-process baseline arm, n=1 easy positive case, and a
fallible head-chef verifier miscast as the gold standard). Honest state: the process runs
end-to-end and produced one verified-correct answer; **worth is not yet measured.** Stays
experimental, out of the book. A real proof needs hy3's battery (true / subtly-false /
mis-attributed / unattributed claims, a no-process arm, N>=20, a deterministic source-matched
verifier) plus the create/prototype arm (#24, other terminal).

**Factual correction:** the SkillsBench foil-paper numbers above ("84 tasks, +16.2pp") are
contested — hy3 cites the v4 abstract as 87 tasks, +16.6pp (33.9->50.5%), and my own search and
fetch disagreed with each other (86 vs 84). That disagreement is itself evidence for hy3's point:
the head chef is a fallible checker, not a gold standard.
