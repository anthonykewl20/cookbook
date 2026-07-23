# Myth-busting a static head-chef scorer — what three adversarial rounds proved

**Date:** 2026-07-23. **Method:** the molecular-gastronomy recipe — isolated-box prototypes, each with a
kill-criterion, adversarially attacked, measured not asserted. **Owner requirement being tested:** a
scorer that is *static* (same input → same number, forever; changes only when the scorer changes),
model- and harness-tagged, and usable as a per-role hiring verdict. Artifacts preserved under
`experiments/scorer-myth-busting/` (the two tested scorers and the decisive fixtures).

## The hypothesis on trial

*"A static, deterministic score computed from a head chef's action log can measure how well it
followed its handbook (delegate substantial work, run in parallel, check, never cook) — well enough
to hire or not hire a model in that role."*

## The rounds, and the measured result of each

| Round | Scorer | Attack | Result (measured) |
|---|---|---|---|
| 1 | v1 | black-box: naive gaming (spam 18 trivial delegations to fake a ~69% delegation rate) | **Survived.** good 75.9, cooking 0.0, gaming 0.0. The anti-gaming displacement rule refused raw delegation count. |
| 1 | v1 | staticness | **Passed.** Same log → identical SHA-256 across 3 runs. |
| 2 | v1 | **white-box** (adversary reads the code) | **BROKEN.** A genuinely bad session (`fake_good.jsonl`) scored **90/100**; a genuinely good one (`framed_good_low.jsonl`) scored **50/100**. |
| 3 | v2 (outcome-anchored) | white-box, **correct threat model** (only the delegation *description text*, `turn`, `claimed_lines` forgeable; cook file paths, real diff sizes, delegation outcomes, timestamps are hook-truth) | **BROKEN.** Bad session (`bad_scores_high.jsonl`) **80/100**; good session (`good_scores_low.jsonl`) **40/100** — no hook-truth field falsified. |
| 3 | v2 | staticness | **Passed.** Deterministic (identical hash twice). |

Every score above was reproduced by the head chef independently, not taken from a chef's word.

## What each break taught, building on the last

1. **Round 1 → naive delegation-rate is gameable, but a displacement rule beats the crude attack.**
   Not sufficient, but the anti-gaming instinct was right.

2. **Round 2 → a scorer that trusts the orchestrator's *self-report* is fundamentally gameable.** v1
   judged a delegation "substantial" from its own `target` text + self-reported numbers, with no link
   to what the delegated agent actually produced. Keyword-stuffed no-op delegations passed; honest
   terse-but-real delegations failed. Same heuristic, broken in both directions. **This independently
   rediscovered the skill-effectiveness framework's rule #1: the system being evaluated must not be
   the source of its own evidence.** Fix direction, earned not guessed: anchor substance on
   *independently captured outcomes* — the delegated work's real diff and its gate result.

3. **Round 3 → even anchored on independent outcomes, a static composite is *still* gamed — on
   ALLOCATION.** v2 credited any real+checked delegation and only flagged cooks per-file over 15 lines.
   The adversary delegated real-but-trivial busywork (whitespace, docstring reflow — honestly 20
   lines, checked, passed) for full credit, while self-cooking the *crucial* work (auth, payments,
   security, a DB migration) chunked to ≤15 lines across separate real files → zero violations → **80/100
   for a session that never delegated a single important thing.** Symmetrically, a genuinely good,
   fully-delegated session was dragged to **40** by the harsh per-file penalty on ordinary small wiring
   edits.

## The converged finding (the real answer the myth-busting was for)

**A static, deterministic scorer over hook-captured facts can measure behavioral *shape* — how much
was delegated vs cooked, how big the cooks were, whether gates ran, delegation outcomes,
timestamp-parallelism. It CANNOT measure *allocation quality* — whether the work that *mattered* was
delegated or self-cooked — because "which work mattered / how risky it was" is a judgment about the
*content* of the work, not something recoverable from line-counts, file-paths, or gate-pass facts.**

Every composite we build gets gamed on this axis, because the only signals that would fix it —
importance/risk of a piece of work — are either (a) another mechanical heuristic (gameable, as shown
three times), or (b) an LLM judgment (which *fluctuates* run-to-run and therefore fails the owner's
non-negotiable staticness test — a wobbling ruler is a broken ruler). This is the same conclusion the
framework reached from the other direction: **"do not collapse correctness, triggering, safety, cost
and reliability into an opaque weighted Skill Score. Separate metrics and explicit gates are more
honest."**

## What this means for the product (the per-role hiring scorer)

- **A single static "adherence score" that is also un-gameable is not achievable for allocation
  quality.** Shipping one as a hire/no-hire number would be shipping a ruler we have measured to be
  bendable. Three rounds say so.
- **What IS honest and static, and should be what the tool surfaces:** a *dashboard of raw
  behavioral facts*, each deterministic, model+harness+scorer-version tagged, diffable over time —
  delegate/cook counts and volumes, gates-run, delegation outcomes, timestamp-parallelism — **plus
  explicit hard gates** on the things that ARE mechanically checkable (e.g. "did it self-cook a file
  the environment *declared* crucial", using an external work-class declaration rather than the
  scorer's guess). The hire decision rests on the facts + gates, not on a collapsed number.
- **Open direction, not yet tested (a possible round 4):** tie importance to an *external
  declaration* the orchestrator does not control — e.g. `model-flow`'s crucial/substantial/mechanical
  work-class per dish — so "self-cooked a crucial dish" becomes a deterministic violation. The
  unresolved question is who declares/verifies that class without reintroducing self-report. This is
  the fork for the owner.

## Bearing on the head-chef handbook (T-21)

The scorer work also sharpened T-21. Two things the handbook needs that the *driver text alone*
cannot give: (1) **a deterministic hook that CAPTURES the action log** — because injected reminders
were measured to decay (73%→33% by turn 16), the log cannot depend on the model remembering to write
it; and (2) whatever scoring ships, it must read that independent hook log, never the orchestrator's
narration. The driver text in the plugin remains necessary but is not, by itself, either the metric
or a guarantee of behaviour.
