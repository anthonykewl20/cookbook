# Prior art: how the field measures whether a skill actually works

> **About this file.** This is the "research before prototypes" step for the cookbook's evaluator
> feature. Before building anything else, the team read four primary sources — one benchmark and
> three official evaluation guides — to find out how other people have already solved the problem
> of scoring an agent, a skill, or a role. This file writes up what they found, in plain language,
> with citations. It also corrects an earlier finding of ours that turned out to be wrong.

---

## Headline

**Score the result, not the behavior.**

There are two ways you could try to grade how well a skill (or a role, or an agent) performed:

1. **Watch what it did** — read its own log of actions and decide, from that log, whether it
   behaved well.
2. **Check what it produced** — ignore the log, take the finished result, and run it through a
   test that was written and hidden in advance, a test the agent cannot see or influence.

Every source below points the same way: **(2) is the only one that holds up.** (1) is a trap,
because the agent whose behavior you're grading is also the one that wrote the very log you're
grading it from. Give it credit for "good behavior" and it will learn to describe good behavior,
whether or not it actually did the work.

This project proved that the trap is real, not theoretical, in its own adversarial prototypes:
a scorer built to read a head chef's action log and grade its behavior gave a **genuinely bad
session a score of 90 out of 100** in one round, and **80 out of 100** in a second, differently-built
round. Both times the log looked great and the underlying work was bad. See
`research/scorer-myth-busting-findings.md` for the full detail.

The fix that all four sources converge on: build a **deterministic outcome test** — a fixed,
hidden ruler that checks the final result — and score the **difference** a skill or role makes to
that ruler's outcome, not how convincing its self-narration is.

---

## 1. SkillsBench — measuring skills by the outcome they change

- Docs: https://www.skillsbench.ai/docs/getting-started
- Code / methodology: https://github.com/benchflow-ai/skillsbench

**The unit of measurement is one task, run twice** — once with the skill available, once without
— under otherwise identical conditions. The score that matters is the **difference between the
two runs** (called the "uplift" or "lift"): does having the skill make the same task more likely
to succeed?

Per the underlying methodology, up to **three trials** are run per task and reported with **95%
confidence intervals**, because a single run can succeed or fail by luck. A second measure,
**"normalized gain,"** adjusts for the fact that an easy task that already succeeds 90% of the
time has much less room to improve than a hard task starting from 10% — so a raw percentage-point
gain on an easy task and the same gain on a hard task are not treated as equally impressive.

**The verifier is the key design choice.** Each task ships with a deterministic, outcome-based
check — a script that tests the *result* the agent produced (does the file build, does the test
suite pass, does the output match the expected schema), not a script that inspects *how* the agent
got there. That verifier is hidden from the agent while it works. Confirmed directly from the
project's own instructions: SkillsBench requires **"Oracle must pass before agent runs"** — a known
correct reference solution has to pass the test first, before any agent attempt is scored. This
proves the task really is solvable and the verifier itself is not broken, before it is used to
judge anyone. The docs also confirm that **"with-skill and no-skill runs are explicit, comparable,
and use the same task package"** — the paired-condition design described above.

**The agent's trajectory (its log of tool calls and actions) is read only to catch cheating** —
did it peek at the hidden test, did it hard-code the expected output, did it actually use the
skill it claims credit for. A suspicious trajectory can **invalidate** a run and throw its score
out. It is never used to **raise** a score. Good behavior with a bad result still fails; the
trajectory has no power to override the outcome test.

**Why this matters, not just how it works — the precedent the field already has.** The
methodology's own reference result, SWE-Skills-Bench, evaluated 49 real, published
software-engineering skills against this design and found a mean lift of only **+1.2%** — and
**39 of the 49 skills produced zero measurable improvement**, while **3 actively made results
worse.** The honest lesson is not "skills help" — it's "most skills don't help, and you cannot
tell which do without measuring." That is the entire justification for building a measurement
system instead of trusting a skill because it reads well.

*(Note on sourcing: the two exact-URL pages cited above confirm the paired with/without design and
the oracle-must-pass-first rule directly. The specific trial count, confidence-interval figure,
normalized-gain formula, and the SWE-Skills-Bench 49-skill numbers come from the fuller methodology
already reviewed by the head chef's team in earlier research and were not re-derivable from the
getting-started page or README alone — see "quotes not independently verified" in the report back.)*

---

## 2. OpenAI — "Evals for agent skills"

- https://developers.openai.com/blog/eval-skills
- https://developers.openai.com/api/docs/guides/evaluation-best-practices

OpenAI's guidance for evaluating an agent skill starts from the same instinct: stop asking "does
this feel better?" and start capturing an **objective trace** of what actually happened — the full
event stream (every command the agent ran, in order) plus the **filesystem artifacts** it produced
(the files that exist afterward, and their contents). Confirmed directly: *"Everything is
deterministic and debuggable. If a check fails, you can open the JSONL file and see exactly what
happened."*

**Grading order, cheapest and most reliable first:**

1. **Deterministic checks** — does the expected file exist, does it build, do the commands run in
   the right order.
2. **Model or rubric grading, second** — only for qualities a fixed script cannot check (code
   style, adherence to conventions), and constrained to a structured, comparable output format so
   scores can be compared run to run.
3. Wherever a model grades, it must be **calibrated against real human judgments first** — the
   guide's own words: validate the judge's agreement with human labels **before** trusting it at
   scale, or optimizing it for cost.

**Triggering is graded as its own, separate question:** did the skill activate when it should have,
and — just as important — did it *stay quiet* when it shouldn't have. OpenAI's method uses
**negative controls**: test cases explicitly marked "this should NOT trigger the skill," so a skill
that fires too eagerly on unrelated requests gets caught, not just one that fails to fire when
needed.

**The honest gap.** OpenAI's evaluation-best-practices guide treats a score as a single number —
a point estimate against a fixed threshold (e.g., "ROUGE-L of at least 0.40") — with no built-in
machinery for run-to-run variance, repeated trials, or confidence intervals. That piece has to be
added by whoever builds the system; OpenAI's docs don't supply it. This is exactly the gap
SkillsBench's multi-trial, confidence-interval design fills.

---

## 3. Anthropic — "Develop tests / Define success"

- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

Anthropic's guidance is about defining success **before** you start measuring, and then grading
against a large set of held-out examples.

**Success criteria should be SMART** (specific, measurable, achievable, relevant) and — this is
the part that matters most for a scorer — **multidimensional and thresholded**. Confirmed
directly: *"Most use cases need multidimensional evaluation along several success criteria."*
Good criteria look like a checklist of separate numeric bars, e.g. an F1 score of at least 0.85,
99.5% of outputs non-toxic, 95% of responses under 200ms — never one collapsed overall number.

**Test on volume, not hand-picked quality.** Anthropic's own words: *"More questions with slightly
lower signal automated grading is better than fewer questions with high-quality human hand-graded
evals."* A large, held-out test set beats a small curated one, even if each individual grade on
the large set is a bit noisier.

**The grading hierarchy, most to least trustworthy:**

1. **Code-based / deterministic grading** — exact string match, unit tests, schema checks. Cheapest,
   perfectly reproducible, and hardest for the system under test to game.
2. **Similarity-based metrics** (ROUGE, cosine similarity on embeddings) — for tasks where there's
   a reference answer but exact match is too strict, e.g. summarization.
3. **LLM-judge grading — last resort, for genuinely subjective qualities only** (tone, empathy,
   coherence), and even then, confirmed directly: *"Generally best practice to use a different
   model to evaluate than the model used to generate the evaluated output"* — never let something
   grade itself.

**The honest gap.** These docs are written for grading a model's final *output* on a single-turn
or short task — there is no built-in recipe here for grading an ongoing agentic process or an
orchestration role. Extending "grade the outcome" to something like "grade a head chef role" is a
legitimate extension of the method, but it is ours to design; Anthropic's docs don't hand it to us
ready-made.

---

## 4. Anthropic — "Increase output consistency"

- https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency

This source isn't about scoring — it's about **shrinking the noise a scorer has to average over**
in the first place. An agent's output varies run to run even when nothing else changes; these are
Anthropic's documented techniques to reduce that spread:

- **Structured outputs** — the one *structural* guarantee on the list: it locks down the output's
  **format** (guaranteed valid JSON matching a schema) so a fixed verifier can parse and grade it
  cleanly. It does not, and cannot, guarantee the *decision* inside that format is the right one —
  only that the shape is reliable enough to check.
- **Specify the exact output format** in the prompt (JSON, XML, a template).
- **Prefill the assistant's response** to force a structure — but confirmed directly, this
  technique is **"not supported on Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude
  Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6"** — which rules it out for
  most of our current stack; Anthropic's own recommended substitute where prefill isn't available
  is structured outputs or plain system-prompt instructions.
- **Few-shot examples** — show the desired output rather than only describing it.
- **Retrieval** — ground repeated similar questions in the same fixed source material so answers
  don't drift.
- **Chain / decompose complex tasks** into smaller steps, each graded on its own.
- **Keep the agent in character** — a system-prompt role plus prepared responses for likely
  scenarios, for anything playing a consistent role over a long interaction.

**The key point for a scorer:** every one of these techniques *reduces the spread* of outcomes a
score has to average over — it makes the same input produce a more consistent result. **None of
them removes the need for repeated trials and confidence intervals.** They stack with
multi-trial measurement; they don't replace it.

---

## What this means for the cookbook's scorer

Putting the four sources together, a robust, comparable, hard-to-game score for a role or a skill
looks like this:

- **Held-out task "batteries."** A fixed set of real tasks the system under test has never seen
  used for grading, each one an objective ruler for one slice of capability (SWE-Bench is one
  such battery, already working on this machine — see below).
- **Score = outcome lift, not behavior score.** Run each task twice — with the skill/role, and
  without — and score the difference in outcome, exactly as SkillsBench does. Not "did it look
  like it followed the process," but "did having it change whether the task actually got solved."
- **A deterministic verifier is the ruler**, hidden from the agent, and gated by an oracle check
  (a known-correct solution must pass first, proving the task and the verifier are both sound).
  Same recorded run in, same verdict out — every time, forever, unless the verifier itself changes
  version.
- **Consistency techniques + multiple trials + confidence intervals handle the rest.** Structured
  outputs, format specs, few-shot examples, and decomposition (source 4) shrink the natural
  run-to-run wobble; repeated trials and confidence intervals (source 1) measure what wobble is
  left honestly, instead of pretending one run is the truth.
- **Every score is tagged** with the exact verifier/scorer version, the model, and the harness it
  ran under — because a score from a different verifier version, or a different model, is not
  the same measurement and must never be silently compared as if it were.
- **The agent's own trajectory is used only as an anti-cheat check** — did it peek at the hidden
  test, did it actually invoke the skill it's claiming credit for — never as a source of positive
  score. This is the exact discipline that SkillsBench's oracle-gating and trajectory-auditing
  already encode, and the one our own myth-busting rounds proved is missing when you score from
  the agent's self-report instead.

**SWE-Bench is the first working battery.** It has already been verified on this machine as a
working static ruler: a gold (correct) patch resolves the task, an empty or wrong patch does not,
and the same recorded run produces the same verdict every time it's re-checked. That is a real,
proven instance of "deterministic outcome verifier" from source 1 and 3 above, not a hypothetical.

**The honest limit, stated up front rather than discovered later:** SWE-Bench Lite is mostly
single-file bug fixes in existing repositories. It tests one slice — coding-outcome correctness —
and says nothing directly about, say, whether a head-chef orchestration role delegates well or
manages a team of agents well. That is exactly why the design above is a **pluggable set of
batteries**, not one fixed benchmark: SWE-Bench proves the *mechanism* (deterministic, oracle-gated,
outcome-only scoring) works end to end; other batteries, built the same way, would be needed to
cover other slices of what the cookbook's roles and skills actually do.

---

## Correction to our earlier finding

Our own `research/scorer-myth-busting-findings.md` concluded that a robust static score for a
role was **"not achievable"** — specifically for judging "allocation quality" (did the role
delegate the work that actually mattered) from a static, deterministic scorer over its own action
log.

**That conclusion was wrong, and the prior art above shows why:** the myth-busting rounds were
scoring the wrong thing. All three rounds built a scorer that reads the orchestrator's own
**behavior log** — its self-reported delegation descriptions, claimed line counts, which files it
touched — and tries to grade the *process* from that log. Every version was broken by an
adversary who could write a better-looking log without doing better work. That is precisely the
failure mode all four sources above warn about independently: grading self-reported process is
gameable because the system being scored also controls the evidence you're scoring it from.

**The myth-busting itself was not wasted — its narrower finding stands.** "A static scorer over an
agent's own action log can be gamed to score bad process as good" is correct, well-proven, and
consistent with the prior art. What was wrong was generalizing that into "therefore no robust
static score is achievable at all." The fix, confirmed by every source in this file: stop scoring
the log of what the agent *did*, and instead score the outcome of what it *produced*, checked by
a verifier the agent never gets to touch or narrate. A robust, static, hard-to-game score is
achievable — it was just aimed at the wrong target the first time.

---

## Source list

- SkillsBench — getting started: https://www.skillsbench.ai/docs/getting-started
- SkillsBench — repository / methodology: https://github.com/benchflow-ai/skillsbench
- OpenAI — "Evals for agent skills": https://developers.openai.com/blog/eval-skills
- OpenAI — evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Anthropic — Develop tests / Define success: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Anthropic — Increase output consistency: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency
- Our own prior finding being corrected: `research/scorer-myth-busting-findings.md`
