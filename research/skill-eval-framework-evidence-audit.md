# Adversarial evidence audit of the `skill-eval` framework

**Audit date:** 2026-07-25
**Documents audited:**

- `agent-skill-effectiveness-framework.md`
- `agent-skill-effectiveness-framework-gaps.md`
- `skill-effectiveness-deepened-evidence.md`

## Bottom line

**VERDICT: TRUST-WITH-CAVEATS.**

The load-bearing arXiv papers are real. Their identifiers resolve to the named papers at the stated
dates, and every headline number requested in this audit matches the primary source. The Anthropic
infrastructure article and the official product documentation are also real.

That does **not** make the reported benchmark results independently reproduced facts, nor does it
make the framework a finished evaluation protocol. The correct reading is:

1. The citations are genuine and accurately transcribed.
2. The benchmark numbers are author-reported preprint results, not independent replications.
3. Several conclusions in the framework are broader than the experiments that support them.
4. The core measurement design is sensible.
5. The gaps review correctly identifies protocol, grader-validation, security, and operational work
   that must be incorporated before the evaluator can be trusted as a release gate.

It is safe to build a **pilot harness** from this design after incorporating those gaps. It is not safe
to implement version 0.1 literally and treat its first dashboard as proof that a Codex skill works.

## Classification rule

This audit uses the requested labels narrowly:

- **VERIFIED:** the primary source exists and states the claimed title, date, or number.
- **WRONG-NUMBERS:** the source exists but its reported number differs.
- **CANNOT-VERIFY:** a primary source could not be opened or did not substantiate the claim.
- **FABRICATED:** the identifier does not resolve, or resolves to unrelated work.

“VERIFIED” means **accurately sourced**, not independently reproduced, peer-reviewed, or free of
methodological defects.

## Priority 1: cited-evidence verification

### S6 — SkillsBench

**Classification: VERIFIED.**

Primary sources:

- [arXiv 2602.12670](https://arxiv.org/abs/2602.12670)
- [v4 paper PDF](https://arxiv.org/pdf/2602.12670v4)
- [benchflow-ai/skillsbench](https://github.com/benchflow-ai/skillsbench)

Existence and version:

- The arXiv record is titled *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse
  Tasks*.
- It was submitted on 2026-02-13 and revised as v4 on 2026-06-14.
- The public GitHub repository exists.

Claim check:

| Claim | Primary-source result | Status |
|---|---|---|
| 87 tasks | The abstract and body report 87 tasks across 8 domains. | VERIFIED |
| 18 configurations | The abstract and experiment section report 18 model-harness configurations. | VERIFIED |
| 3 trials | The experiment section targets three public trials per configuration/task/condition cell. | VERIFIED |
| 33.9% → 50.5% | The abstract and Table 2 report those exact macro pass rates. | VERIFIED |
| +16.6 percentage points | Exact match. | VERIFIED |
| 13/87 harmed | The body says, “13 of 87 tasks show negative Skills deltas.” | VERIFIED |
| GitHub repository | The named repository is public and contains tasks, verifiers, and execution tooling. | VERIFIED |

Important qualification: this verifies what v4 reports, not the correctness of every run or verifier.
The repository currently has open issues alleging or documenting
[target-output leakage](https://github.com/benchflow-ai/skillsbench/issues/1021),
[answer leakage](https://github.com/benchflow-ai/skillsbench/issues/1018),
[an exposed implementation](https://github.com/benchflow-ai/skillsbench/issues/1007),
[protected-test contamination](https://github.com/benchflow-ai/skillsbench/issues/1002), and a
[requested length-matched placebo arm](https://github.com/benchflow-ai/skillsbench/issues/1004).
Those issue reports verify that validity concerns are live; they do not by themselves quantify how
much the published aggregate would change after correction.

Safe citation: “SkillsBench v4 **reported** 33.9% versus 50.5% across its selected 87-task,
18-configuration aggregate.”

Unsafe citation: “Independent evidence proves skills improve agents by 16.6 points.”

### S7 — SWE-Skills-Bench

**Classification: VERIFIED.**

Primary sources:

- [arXiv 2603.15401](https://arxiv.org/abs/2603.15401)
- [paper PDF](https://arxiv.org/pdf/2603.15401)
- [GeniusHTX/SWE-Skills-Bench](https://github.com/GeniusHTX/SWE-Skills-Bench)

Existence:

- The arXiv record resolves to *SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World
  Software Engineering?*, submitted on 2026-03-16.

Claim check:

| Claim | Primary-source result | Status |
|---|---|---|
| 49 public SWE skills | Exact match. | VERIFIED |
| Approximately 565 task instances | Exact match. | VERIFIED |
| Deterministic verification | The paper describes pytest-based execution checks mapped to acceptance criteria. | VERIFIED |
| +1.2 mean gain | The paper reports 89.8% without versus 91.0% with skills. | VERIFIED |
| 39/49 zero improvement | The abstract says, “39 of 49 skills yield zero pass-rate improvement.” | VERIFIED |
| 3 degrade | The abstract and Table 2 report three, down to −10 points. | VERIFIED |

Unit correction: 89.8% to 91.0% is **+1.2 percentage points**, not a 1.2% relative increase. The
paper itself writes “+1.2%,” but the framework should use percentage points for consistency.

Scope qualification: the paper calls itself a “pre-print with preliminary results, work in progress.”
Its experiments use one configuration, Claude Code with Claude Haiku 4.5. The roughly 565
requirements and their deterministic tests are generated through a benchmark-construction pipeline.
The paper does not establish that +1.2 points generalizes to other models, harnesses, repositories, or
production task distributions.

### S8 — SkillLearnBench

**Classification: VERIFIED.**

Primary sources:

- [arXiv 2604.20087](https://arxiv.org/abs/2604.20087)
- [paper PDF](https://arxiv.org/pdf/2604.20087)
- [cxcscmu/SkillLearnBench](https://github.com/cxcscmu/SkillLearnBench)

Existence:

- The arXiv record resolves to *SkillLearnBench: Benchmarking Continual Learning Methods for
  Agent Skill Generation on Real-World Tasks*, submitted on 2026-04-22.

Claim check:

| Claim | Primary-source result | Status |
|---|---|---|
| Skill, trajectory, and outcome levels | The paper explicitly defines those three evaluation levels. | VERIFIED |
| Stronger models do not consistently produce better skills | Stated in the abstract and discussed in the model-scale analysis. | VERIFIED |
| External feedback helped over iterations | Reported in a four-round teacher-feedback extension. | VERIFIED |
| Self-feedback caused recursive drift | The abstract says, “self-feedback alone induces recursive drift.” | VERIFIED |

Scope qualification: the drift comparison is not a universal law about self-critique. The detailed
experiment extends Self Feedback and Teacher Feedback to four rounds on the Productivity Tools
category with Claude Sonnet 4.6. It is reasonable motivation to test external feedback, but too narrow
to prove that all self-feedback loops drift or all external feedback loops improve.

### S10 — Anthropic infrastructure noise

**Classification: VERIFIED.**

Primary source:

- [Anthropic, *Quantifying infrastructure noise in agentic coding evals*](https://www.anthropic.com/engineering/infrastructure-noise)

The article was published on 2026-02-05. It says the “gap between the most- and least-resourced
setups” on Terminal-Bench 2.0 was 6 percentage points, with p < 0.01. The body identifies this as
the difference between strict 1× resource enforcement and uncapped resources.

Critical scope correction:

- The 6-point result is an **extreme resource-configuration contrast**, not a measured estimate of
  ordinary run-to-run platform noise.
- Across the moderate configuration range, Anthropic reports a spread just below 2 points.
- Time-of-day variance is described as anecdotal and explicitly not formally quantified.

The article strongly supports pinning and reporting resources. It does not, by itself, experimentally
prove that randomizing and interleaving A/B/C/D removes API routing or time-of-day confounding.
That is sound experimental-design guidance, but it remains a derived recommendation.

### Official and first-party documentation

All named pages exist and substantively support the framework’s summaries.

| Source | Existence | What it actually supports | Status |
|---|---|---|---|
| [S1 Claude Code skill evaluation](https://code.claude.com/docs/en/skills#evaluate-and-iterate-on-a-skill) | Current official Claude Code page | Fresh sessions, with/without baselines, separate trigger and output checks, isolated runs, pass rate/time/tokens, blind version comparison, description tuning | VERIFIED |
| [S2 OpenAI skill evals](https://developers.openai.com/blog/eval-skills) | Current official OpenAI article | Prompt → trace/artifacts → checks → score; explicit/implicit/contextual/negative trigger cases; deterministic trace/artifact checks; token/thrashing checks and runtime smoke tests | VERIFIED |
| [S3 Agent Skills output evaluation](https://agentskills.io/skill-creation/evaluating-skills) | Current first-party standard documentation | Clean contexts, with/without or old-version baselines, assertions with evidence, aggregation, blind comparison, human feedback | VERIFIED |
| [S4 OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Current official OpenAI guide | Task-specific and production-shaped data, continuous evaluation, automated metrics calibrated to human labels, pairwise/pass-fail grading, edge cases | VERIFIED |
| [S5 Anthropic success criteria and evals](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | Current official Anthropic guide | Measurable multidimensional criteria, real-world task distributions, code/human/model grading, and testing LLM graders before scaling | VERIFIED |
| [S11 Claude Code programmatic mode](https://code.claude.com/docs/en/headless) and [CLI reference](https://code.claude.com/docs/en/cli-reference) | Current official Claude Code docs | JSON and stream-JSON, session and cost metadata, tool events, API retry events, structured output, version and permission controls | VERIFIED |
| [S12 Codex non-interactive mode](https://developers.openai.com/codex/non-interactive-mode) | Exists; redirects to current ChatGPT Learn documentation | `codex exec --json`, JSONL events, token usage in `turn.completed`, `--output-schema`, and sandbox guidance | VERIFIED |

Short primary-source excerpts:

- S1: “run each one in a fresh session with the skill available and again with it disabled”
- S2: “a prompt → a captured run (trace + artifacts) → a small set of checks → a score”
- S3: “Each eval run should start with a clean context”
- S4: “Design task-specific evals: Make tests reflect model capability in real-world distributions.”
- S5: “choose the fastest, most reliable, most scalable method”
- S11: “`stream-json`: newline-delimited JSON for real-time streaming”
- S12: “`stdout` becomes a JSON Lines (JSONL) stream”

Two freshness notes:

1. S3 is first-party documentation for the Agent Skills standard, not an OpenAI or Anthropic product
   page.
2. S4 now warns that the OpenAI Evals **platform** is being deprecated, with read-only status
   scheduled for 2026-10-31 and shutdown for 2026-11-30. Its general methodology remains useful,
   but a new implementation should not couple itself to that retiring platform.

The S2 registry summary slightly overstates that article by saying “cost and runtime checks.” It
discusses token budgets, unnecessary command activity, and runtime smoke checks; it does not
establish monetary-cost or wall-clock-duration grading. Its `--full-auto` examples are also stale
relative to current Codex documentation, which prefers an explicit `--sandbox workspace-write`.

## Priority 2: design validity

### Solid design guidance

These parts are defensible even without SkillsBench, SWE-Skills-Bench, or SkillLearnBench:

- **External orchestration and evaluator separation.** The system under test should not control
  tasks, graders, raw evidence, or the release decision.
- **Matched task-level A/B comparison.** Comparing skill-available against skill-unavailable on the
  same task population is the right primary deployment comparison.
- **`B − A` as intention-to-treat.** This measures the effect of making a skill available whether or
  not the agent selects it. Triggered-only analysis would condition on post-treatment behavior and can
  bias the result.
- **Deterministic-first grading.** Tests and state checks should own objective correctness; humans
  should own irreducibly subjective quality; model graders should be calibrated and subordinate to
  contradictory deterministic evidence.
- **Fresh isolated environments and complete artifacts.** These reduce state leakage and make
  failures auditable.
- **Locked holdout after candidate freeze.** This is standard protection against iterative overfitting.
- **Repeated trials with task-clustered paired analysis.** Keeping a task’s conditions and trials
  together in the bootstrap is more appropriate than treating runs as independent.
- **Separate correctness, safety, triggering, cost, and latency gates.** An opaque composite score
  would hide unacceptable trade-offs.
- **Versioning skill, suite, grader, adapter, and environment.** Effectiveness is a property of an
  evaluated configuration, not permanently of `SKILL.md`.

These are mostly normative experimental, software-testing, and governance choices. The papers
illustrate why they matter; the papers do not uniquely derive or prove them.

### Claims that depend on the recent research

| Framework claim | Evidence-supported core | Overreach to avoid |
|---|---|---|
| Skill benefit is configuration-dependent | S6 reports large differences by model-harness configuration; S7 reports a small mean in one SWE setup. | Do not claim the reported means predict a new Codex skill or production distribution. |
| Skills can harm tasks | S6 reports 13 negative task deltas; S7 reports 3 degrading skills. | Do not infer a population harm rate from those curated benchmark inventories. |
| Models and harnesses require separate evaluation | S6 directly reports harness/configuration differences. | Treat this as strong motivation, not proof about every future model/harness pair. |
| Three trials are a reasonable pilot default | S6 uses three selected public trials. | Usage by one benchmark is not a power analysis and does not establish adequacy. |
| Self-feedback drifts; external feedback improves | S8 reports that pattern in its specific iterative experiment. | Do not state it as a general law of continual learning or production feedback. |
| Infrastructure can move scores by 6 points | S10 directly measures the extreme resource contrast. | Do not call 6 points the normal background-noise floor. |

### Internal contradictions and unresolved design defects

1. **Condition C is not a pure activation estimate.** `C − B` changes both activation and prompt
   wording/salience because C names the skill. It is a useful operational contrast, but “discovery
   gap” is too causal a label. A neutral prompt-framing control or encouragement design is needed if
   the goal is to isolate activation itself.

2. **Condition D is underspecified.** A previous skill version does not say whether it is implicitly
   available like B or explicitly invoked like C. `B − D` is valid only when invocation mode and all
   other treatment details match. D also cannot be mandatory for a first release, although Phase 1
   lists A/B/C/D unconditionally.

3. **The placebo arm is optional when it is sometimes essential.** `B − A` validly measures the
   deployment effect of adding the whole skill package. It does not isolate procedural content from
   extra context, attention, scripts, or references. If the published claim is “the procedure caused
   the lift,” the length-matched/context and ablation arms must be required.

4. **Deterministic precedence assumes a qualified verifier.** The document says a deterministic
   required-test failure overrides subjective approval, yet the SkillsBench issues and Anthropic’s
   examples show deterministic graders can be wrong. Grader qualification and mutation tests must
   be an acceptance gate before precedence applies.

5. **Holdout reuse will eventually leak.** A “locked” holdout repeatedly used for release decisions
   becomes development feedback even if raw tasks stay hidden. The framework needs limited-use,
   rotating, or replenished holdouts and a policy for how much result detail authors receive.

6. **The statistical target population is not fully operationalized.** A paired bootstrap over a
   hand-built fixed task list quantifies uncertainty from resampling that list; it does not automatically
   justify inference to “coding tasks.” Sampling frame, production weights, and external-validity
   claims must be declared.

7. **Three trials and 10–20 prompts are not release proof.** The document mostly acknowledges
   this, but Phase 1/2 could still produce authoritative-looking intervals from a tiny task count.
   Power, minimum detectable effect, and an inconclusive outcome must be first-class.

8. **Run order is missing from the main specification.** The gaps review correctly requires
   randomized, interleaved, time-blocked conditions and balanced concurrency. Without that,
   model/service drift can masquerade as treatment lift.

9. **Multiple comparisons and stopping rules are missing.** A/B/C/D, categories, models, and many
   metrics create researcher degrees of freedom. The primary estimand, sample size, exclusions,
   stopping, reruns, and confirmatory versus exploratory analyses must be frozen before protected
   evaluation.

10. **Zero observed critical failures is not a safety rate.** The release rule needs exposure counts
    and a one-sided upper confidence bound, not only “no observed critical failure.”

11. **Codex activation telemetry remains incomplete.** S12 proves rich JSONL capture, but not a
    guaranteed direct event for every stage of implicit skill discovery and use. The framework is
    right to mark this unknown; reports must preserve `UNKNOWN` instead of inferring activation from
    a successful outcome.

12. **“Vendor-neutral” does not mean semantically identical evidence.** Claude and Codex expose
    different event schemas and possibly different activation observability. Store native events, but
    validate each adapter and explicitly mark unsupported normalized fields.

## Audit of the gaps review and deepened-evidence note

The gaps review is directionally strong and should be treated as required remediation, not optional
commentary. Its most important additions are evaluator meta-validation, protocol freezing,
randomized/interleaved execution, grader qualification, protected holdout separation, adapter
canaries, and rare-event safety reporting.

One load-bearing sentence needs correction. The review says a “broken grader moved a reported score
from 42% to 95%.” Anthropic’s
[actual account](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) reports a
42%→95% change after fixing several problems: rigid grading, ambiguous specifications,
non-reproducible stochastic tasks, and a less constrained scaffold. The numerical example is
**VERIFIED**, but attributing the whole jump to one broken grader is wrong.

The deepened-evidence note is unusually candid about source quality, but its word “VERIFIED” is not
uniform:

- Some entries include checked headline numbers from primary sources.
- Some confirm only scope and general findings while leaving specific figures “not re-opened.”
- Its Seleznov activation result is explicitly based on two secondary reports, not the primary data.
- Five claims are explicitly “CLAIMED-BY-WORKFLOW.”

Therefore only the note’s primary-opened facts should be cited as verified. Secondary-only,
paper-not-reopened, and claimed-by-workflow figures must retain those qualifiers or be omitted.

## Priority 3: build decision

### Safe to build now

Build a limited deterministic MVP that:

1. Runs A and B in fresh isolated workspaces.
2. Stores immutable native traces, environment manifests, diffs, and verifier evidence.
3. Uses a small development suite to prove plumbing, not skill efficacy.
4. Includes known-good, no-op, placebo, harmful, broken-grader, missing-telemetry, and leakage
   canaries to meta-validate the evaluator.
5. Produces `INCONCLUSIVE` until the protocol, population, sample size, graders, and holdout are
   qualified.

### Must be fixed before a release-gating effectiveness claim

- Freeze the full protocol and estimand.
- Define D’s invocation mode and treat C contrasts as operational rather than pure causal isolation.
- Randomize and interleave conditions.
- Power the task count and trial count for the minimum useful effect.
- Qualify graders with reference solutions, mutants, valid alternatives, and bypass attempts.
- Protect and ration holdout access; rotate or replenish it.
- Add production-frequency and severity views alongside task-macro results.
- Add rare-event safety bounds.
- Validate adapters and fail visibly on schema drift or missing telemetry.
- Require placebo/ablation arms whenever claiming that procedural content, rather than package
  availability, caused the effect.
- Have a reviewer inspect the final protocol, grader fixtures, and complete evaluator diff before the
  first protected run.

## Exact claims that must not be cited without qualification

1. Do not cite SkillsBench’s +16.6 points or 13/87 as independently reproduced truth. Cite them as
   **v4 author-reported results**, and mention the active validity issues when they are material.
2. Do not cite SWE-Skills-Bench’s result as evidence about SWE skills generally. Cite **+1.2
   percentage points in one Claude Code + Claude Haiku 4.5 preliminary setup**.
3. Do not cite SkillLearnBench as proving self-feedback generally causes recursive drift. Cite the
   **specific four-round extension** in which the pattern appeared.
4. Do not cite 6 points as normal Terminal-Bench infrastructure noise. Cite the **1× versus uncapped
   resource contrast**; the reported moderate-range spread was below 2 points.
5. Do not cite “three trials” as statistically sufficient. It is a pilot convention used by SkillsBench.
6. Do not cite OpenAI’s 10–20 prompts as release-quality proof. The article presents them as an early
   regression set.
7. Do not say a broken grader alone caused Anthropic’s 42%→95% example.
8. Do not promote any deepened-evidence figure marked secondary-only, not re-opened, or
   claimed-by-workflow to verified fact.

Subject to those restrictions, there is no fabricated S6/S7/S8/S10 evidence to name. A
**DO-NOT-TRUST** verdict would be factually unjustified. A **TRUST-AND-BUILD** verdict would ignore
the framework’s own unresolved protocol and validation gaps. **TRUST-WITH-CAVEATS** is the only
defensible verdict.
