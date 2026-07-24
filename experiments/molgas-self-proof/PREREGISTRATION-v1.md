# Molecular Gastronomy — self-proof (pre-registered BEFORE any run)

**Why this exists.** Owner directive, 2026-07-24: Molecular Gastronomy (#25) is **experimental, not
for the book, and must prove its worth** before it is served anywhere. "Unproven" is the work, not a
stop. This file fixes the pass-mark **before** any cook runs — the process's own rule
(*serve only once the metric is static and measurable*).

**Stays in `experiments/`. Not the book. Not the other chef's `research/molecular-gastronomy/` turf.**

## The worth-claim under test
Molecular Gastronomy's central promise (and the book's whole reason for being): **following the
process turns an unknown into a verified, STABLE answer — the same result whoever works.** A process
that wobbles is a broken ruler, not a result.

## The task (a real, checkable "new thing": verified knowledge)
Use Molecular Gastronomy to **independently verify a load-bearing claim the project relies on**,
against its primary source. The claim (load-bearing in `WHERE-WE-ARE.md` / the eval rationale:

> **"SWE-Skills-Bench found that 39 of 49 agent skills gave zero lift — i.e., most skills do not help."**

This is the kind of claim the whole "measure, don't trust" thesis rests on. If it is wrong, that
matters. Verifying it is real research work, not a lookup.

## Method
- **3 fresh cooks**, each working alone, blind to the others and to the head chef's own answer.
- Each is given the Molecular Gastronomy recipe and told to: research the **primary** source, extract
  the exact figure **word-for-word**, compare to the claim, and return a verdict **only if grounded**
  in the source (else say *cannot verify* — no guessing).
- **Head chef independently verifies the same claim** as the gold standard, blind to the cooks until
  they have answered.

## Metric — FIXED NOW, before any cook runs
- **Correctness (per cook):** the cook's verdict + figure matches the head chef's gold (the primary
  source).
- **Static-ness:** all 3 cooks return the **same** verdict and figure.

## Pre-registered verdict rule (decided before results)
- **EARNS ITS KEEP (static + correct):** all 3 cooks correct AND mutually consistent. → Molecular
  Gastronomy reliably turned an unknown into a verified, stable answer. Worth demonstrated (on the
  research+verify arm).
- **NOT YET (flaky or wrong):** any cook wrong, OR the cooks diverge. → the process is under-specified
  on the research/verify dimension; tighten the recipe (name the exact verify steps) and re-run. A
  wobbling metric means the ruler is broken — fix it before trusting any verdict.
- **CEILING CAVEAT (the #24 lesson):** if the claim turns out trivially easy to verify, convergence
  is uninformative about *added* worth. If that happens, escalate to a harder claim and re-run — do
  not declare success on a ceiling.

## Scope of this proof
This exercises Molecular Gastronomy's **research → measure → serve-only-if-verified** arm. The
**prototype-in-an-isolated-box** arm is being exercised by #24's code work on the other terminal.
**Full** worth = both arms proven. This run is one of the two.

## What this is NOT
- Not a chapter. Not for the book.
- Not a contest with #24 — different arm, different bench, no shared files.
- The "serve Molecular Gastronomy into the book" decision stays with the owner, and only after worth
  is shown across both arms.
