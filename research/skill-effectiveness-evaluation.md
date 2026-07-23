# Proving a skill works — the evaluation method, its measured evidence, and the design-space question inventory

> **About this file.** This is research for an experimental feature of the cookbook: an evaluator that
> decides whether an agent *skill* (the cookbook's own, or a reader's) actually works. It preserves, in
> substance verbatim, two captured analyses: **Part A** — the defensible evaluation method and the
> measured evidence behind it; and **Part B** — the exhaustive question inventory that must be answered
> before that method is operationalised into a real system. Content was preserved, not rewritten to
> arrive; the only thing added is this book's own lens: **every claim is tagged MEASURED or ASSERTED**,
> because “this skill works” is exactly the kind of claim this book refuses to accept on authority.
>
> **Companion spec.** The answered design that turns these questions into a system lives alongside this
> file in `research/agent-skill-effectiveness-framework.md` (working name `skill-eval`): it labels every
> decision by evidence type (`[OFFICIAL-WEB]`, `[RESEARCH-WEB]`, `[DERIVED]`, `[ASSUMPTION]`,
> `[USER-DECISION]`, `[UNKNOWN]`) and carries the fuller source registry. That spec reaches two more
> **MEASURED** anchors this summary does not — **SWE-Skills-Bench** (only +1.2% mean lift for software-
> engineering skills; 39 of 49 skills gave zero improvement) and **SkillLearnBench** (stronger models did
> not consistently make or use better skills; self-feedback caused recursive drift). Read that file as the
> spec; this one as the method and the open questions behind it.

> **Headline.** The one defensible method is a **controlled, paired evaluation**: run the same real
> tasks with and without the skill under identical conditions, grade the resulting artifacts with
> independent verifiers, repeat the runs, and measure the difference. Anything weaker — one good demo,
> "the output looks better," or the agent grading its own work — is not proof. The single most important
> external finding (**MEASURED**) is that skills **also measurably harm** a real minority of tasks (13 of
> 87). So the honest prior is *a skill can help, do nothing, or actively damage* — never "skills help."

---

## 0. MEASURED vs ASSERTED — the map for this whole topic

| Claim | Tag | Basis |
|---|---|---|
| Controlled paired evaluation is the defensible method | **ASSERTED** (normative) | Method guidance shared by Anthropic + OpenAI; a well-reasoned "should," not itself a measured head-to-head |
| Skill evaluation splits into two problems: (1) was it triggered? (2) did it improve the result? | **ASSERTED** (normative guidance) | Anthropic Claude Code skill-evaluation docs |
| Curated skills lift pass rates (Codex CLI + GPT-5.5 **+19.7 pp**; Claude Code + Opus 4.7 **+18.2 pp**; all-18 mean **+16.6 pp**) | **MEASURED** | SkillsBench v4 preprint — 9,396 trajectories, deterministic test verifiers, matched no-skill and curated-skill conditions |
| 13 of 87 tasks became **worse** with skills | **MEASURED** | SkillsBench v4 |
| A public benchmark is not proof for *your* repo or production workflow | **ASSERTED** (correct external-validity caveat) | The benchmark's own scope limit |
| Infrastructure configuration alone can shift an agent coding benchmark by ~6 percentage points | **MEASURED** | Anthropic infrastructure-noise experiment |
| Grading order: deterministic verifiers → trace checks → blind human → calibrated LLM judge | **ASSERTED** (normative hierarchy) | Agent Skills evaluation spec; Anthropic + OpenAI guidance |
| Release gate: holdout lift up, 95% CI lower bound above your pre-declared minimum, no critical-failure increase, false triggering under limit, acceptable cost per success | **ASSERTED** (a proposed gate, not a measured one) | Best-practice synthesis |

**Reading.** The only **MEASURED** anchors here are the SkillsBench numbers and the Anthropic
infrastructure-noise figure. Everything else — including the method itself — is normative *guidance*:
consistent with the anchors, but not itself a measured outcome. That is the same FACT/ASSUMPTION split this
book applies everywhere (see `research/proof-over-authority.md`). The method is sound and worth building on;
it must not be mistaken for proof that it has been *measured* to work in this kitchen. The SkillsBench result
also supplies the measured reason the method insists on paired baselines and regression checks: skills do not
only help.

---

## Part A — The defensible method and the measured evidence

### A1. The defensible method

> Run the same real tasks with and without the skill, under identical conditions, grade the resulting
> artifacts with independent verifiers, repeat the runs, and measure the difference.

Anything weaker — one successful demo, "the output looks better," or the agent grading its own work — is not
proof.

### A2. What current evidence says

Anthropic's official Claude Code documentation separates skill evaluation into two problems:

1. Did Claude invoke the skill when appropriate?
2. When invoked, did the skill improve the result?

Anthropic recommends fresh isolated sessions, with-skill versus without-skill baselines, recorded pass rate,
tokens and duration, and blind A/B comparison between skill versions. Its official `skill-creator` plugin
automates this workflow.
[Claude Code skill evaluation documentation](https://code.claude.com/docs/en/skills#evaluate-and-iterate-on-a-skill)

OpenAI recommends essentially the same method for Codex: prompt → captured trace and artifacts →
deterministic checks and structured grading → comparable score. It explicitly recommends positive triggering
cases, negative controls, command/trace verification, artifact checks, build/runtime checks and token
measurements. [OpenAI's systematic skill-evaluation guide](https://developers.openai.com/blog/eval-skills)

There is also direct empirical evidence. The June 2026 SkillsBench v4 preprint evaluated:

- 87 real, production-like tasks
- 18 model–agent configurations
- Claude Code and Codex CLI included
- Three trials per task and condition
- 9,396 total recorded trajectories
- Fresh pinned containers
- Deterministic test verifiers
- Matched no-skill and curated-skill conditions

Reported pass rates were:

| Agent configuration    | Without skills | With curated skills |     Lift |
| ---------------------- | -------------: | ------------------: | -------: |
| Codex CLI + GPT-5.5    |          46.8% |               66.5% | +19.7 pp |
| Claude Code + Opus 4.7 |          43.0% |               61.2% | +18.2 pp |
| All 18 configurations  |          33.9% |               50.5% | +16.6 pp |

But 13 of the 87 tasks became worse with skills. Heavy instructions sometimes displaced a better native
strategy or forced brittle workflows. That is the important part: skills can measurably help, do nothing, or
actively damage performance. [SkillsBench methodology and results](https://arxiv.org/html/2602.12670v4)

This is strong benchmark evidence, but it is still a public research benchmark — not proof that any specific
skill works in your repository or production workflow.

### A3. The correct evaluation design

Use at least three experimental conditions:

| Condition                         | Purpose                                           |
| --------------------------------- | ------------------------------------------------- |
| A: Skill unavailable              | True no-skill baseline                            |
| B: Skill available, not mentioned | Actual auto-triggered deployment behavior         |
| C: Skill explicitly invoked       | Maximum benefit when the skill is definitely used |
| D: Previous skill version         | Optional regression comparison                    |

These comparisons reveal different things:

- **B versus A** — actual end-to-end value in ordinary use.
- **C versus A** — whether the skill's instructions are valuable at all.
- **B versus C** — how much value is lost because triggering or discovery is unreliable.
- **D versus C** — whether the new version is genuinely better.

Run every condition with:

- The exact same model identifier and reasoning setting
- The same Claude Code/Codex version
- The same task prompt and repository commit
- The same tools, permissions, network access and time limits
- A fresh session and fresh working tree
- Randomized execution order
- At least several independent runs per task
- Captured traces, diffs, artifacts and verifier results

This environment control matters. Anthropic found that infrastructure configuration alone could shift an
agent coding benchmark by six percentage points — larger than many claimed model improvements.
[Anthropic's infrastructure-noise experiment](https://www.anthropic.com/engineering/infrastructure-noise)

### A4. What must be measured

| Area              | Primary measurement                                        |
| ----------------- | ---------------------------------------------------------- |
| Triggering        | Precision, recall and false-positive rate                  |
| Task correctness  | First-attempt verifier pass rate                           |
| Skill lift        | `pass_rate_with_skill - pass_rate_without_skill`           |
| Reliability       | Variation across repeated runs and prompt paraphrases      |
| Regressions       | Tasks that passed without the skill but failed with it     |
| Safety            | Critical policy, security or destructive-action violations |
| Efficiency        | Tokens, wall time, commands and cost per successful task   |
| Human burden      | Reviewer corrections, intervention time and rework         |
| Generalization    | Performance on a locked, unseen holdout set                |
| Production impact | Acceptance rate, escaped defects and delivery time         |

For triggering:

- Precision = correct activations / all activations
- Recall = correct activations / all prompts that should activate it
- False-positive rate = incorrect activations / prompts that should not activate it

For task improvement:

- Absolute lift = `P(with skill) − P(without skill)`
- Normalized gain = `(P(with skill) − P(without skill)) / (1 − P(without skill))`
- Cost per successful task = total cost / successful tasks

First-attempt success is more honest than "eventually succeeded after five retries." A high pass@k can
conceal an unreliable skill.

### A5. How to grade results

Use this order:

1. **Deterministic verifiers first** — tests, builds, schema validation, linting, security scans, file
   invariants, browser assertions and hidden acceptance tests.
2. **Trace checks second** — whether the skill triggered, used the correct tools, followed mandatory safety
   steps and avoided useless loops.
3. **Blind human comparison for subjective properties** — reviewers should not know which output used the
   skill.
4. **Calibrated LLM judges only where deterministic grading is impossible** — use fixed rubrics, randomized
   A/B ordering and concrete evidence. Compare the judge against human ratings before trusting it.

The Agent Skills evaluation specification recommends isolated with/without runs, objective assertions, timing
measurements, blind version comparisons and human review.
[Agent Skills evaluation methodology](https://agentskills.io/skill-creation/evaluating-skills)

### A6. What constitutes proof

A defensible release gate would be:

- The skill improves the locked holdout task-success rate.
- The lower bound of the 95% confidence interval exceeds zero and your pre-declared minimum useful
  improvement.
- Critical-failure rate does not increase.
- False triggering stays under a pre-declared limit.
- Cost per successful task remains acceptable.
- Production shadow testing or randomized deployment confirms the offline result.

Use a paired bootstrap over tasks for confidence intervals. Do not pretend every repeated run is a completely
independent sample; trials from the same task are clustered.

Ten or twenty prompts are useful for early regression detection — OpenAI explicitly recommends that scale for
getting started — but they are not strong statistical proof.
[OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

### A7. Applied to our skills

For our projects, the success measurements should be concrete:

| Skill                     | Real effectiveness measurement                                                          |
| ------------------------- | --------------------------------------------------------------------------------------- |
| Prompt optimizer          | Downstream task success — not whether the rewritten prompt "looks better"               |
| Behavioral-contract skill | Hidden behavioral-test pass rate, mutation score, missing sad paths and escaped defects |
| mbot-e2e usage skill      | Seeded-defect detection rate, false positives on correct pages and diagnosis time       |
| PRD-to-code skill         | Hidden acceptance-test success, requirement traceability and reviewer correction time   |
| Code-review skill         | Valid defects found minus false alarms, confirmed by independent tests                  |

**The blunt conclusion:** stop calling a skill "complete" merely because its `SKILL.md` is comprehensive and
it worked in a few manual trials. A skill is only proven effective when it produces a reproducible positive
lift over a no-skill or previous-version baseline on unseen real tasks — and does so without unacceptable
cost or regressions.

---

## Part B — The complete question inventory (before designing the evaluator)

> Before designing the evaluator, selecting metrics, or choosing storage, we need a complete question
> inventory. The current HOW–WHEN–WHAT–WHERE frame is necessary but incomplete. It also needs **WHY, WHO,
> WHICH, AGAINST WHAT, HOW MUCH, and WHAT IF.**
>
> This whole part is **ASSERTED / normative**: it is a design-space checklist (a set of questions every
> builder *should* answer), not a set of measured findings. Its value is that it forces the pre-commitment
> discipline this book cares about — naming the acceptance test and the decision before seeing the result
> (see `research/proof-over-authority.md`, Finding A). No question below has been answered for this
> kitchen yet; that is the point.

### 1. Purpose and decision questions

* Why are we measuring skill effectiveness?
* What concrete decision must the evaluation support?
* Are we deciding whether to create, revise, release, install, enable, disable, roll back, or delete a skill?
* What does "effective" mean for the specific skill?
* Does effectiveness mean better correctness, reliability, speed, cost, safety, consistency, usability, or some combination?
* Which outcomes are mandatory?
* Which outcomes are merely desirable?
* Which regressions are unacceptable regardless of overall improvement?
* What minimum improvement would justify maintaining the skill?
* What cost increase would make the skill ineffective despite better outputs?
* What evidence would convince us that the skill is working?
* What evidence would convince an independent reviewer?
* What evidence would prove the skill is harming performance?
* What evidence would be considered inconclusive?
* Who will consume the evaluation results?
* Who has authority to approve or reject a skill version?
* Who owns the consequences when a skill passes evaluation but fails in production?

### 2. Evaluation scope questions

* Are we evaluating one skill or a general skill-evaluation framework?
* Are we evaluating instruction-only skills?
* Are we evaluating skills containing scripts?
* Are we evaluating skills containing references, templates, or assets?
* Are we evaluating skills that use external tools or MCP servers?
* Are we evaluating the skill itself or the complete model–agent–skill–tool stack?
* Can a skill meaningfully be scored independently from its model and harness?
* Must Claude Code and Codex be evaluated separately?
* Must each model version be evaluated separately?
* Must each reasoning-effort setting be evaluated separately?
* Must local, cloud, IDE, CLI, and web-agent executions be evaluated separately?
* Are implicit and explicit skill invocations separate evaluation targets?
* Are project-scoped and globally installed skills separate evaluation targets?
* Are interactions between multiple installed skills in scope?
* Are conflicts between skills in scope?
* Are hooks, repository instructions, system instructions, and skills being measured separately?
* Where does the skill's responsibility begin and end?
* Which failures should be attributed to the skill?
* Which failures should be attributed to the model, harness, tools, environment, grader, or task?

### 3. Unit-of-measurement questions

* What is the primary unit being evaluated?
* Is the unit one prompt?
* Is it one agent session?
* Is it one task attempt?
* Is it one completed artifact?
* Is it one repository change?
* Is it one user workflow?
* Is it one skill invocation?
* Is it one skill version across many tasks?
* How will multi-turn tasks be represented?
* How will tasks requiring multiple skill invocations be represented?
* How will partial completion be represented?
* How will retries be represented?
* Will a retry count as another trial or part of the same trial?
* Will human intervention end the trial?
* Will a task that succeeds after human intervention count as agent success?
* How will abandoned, timed-out, interrupted, and unscorable runs be represented?

### 4. Test-case and dataset questions

* What real-world tasks should represent the skill's intended workload?
* Where will those tasks come from?
* Will they come from production logs, real repositories, historical tickets, documents, incidents, or manually authored scenarios?
* How will sensitive production data be removed?
* How many unique tasks are required?
* How many prompt variations are required per task?
* Which ordinary cases must be included?
* Which edge cases must be included?
* Which adversarial cases must be included?
* Which malformed inputs must be included?
* Which ambiguous requests must be included?
* Which near-match requests should not activate the skill?
* Which completely unrelated requests should not activate it?
* Which environment variations must be represented?
* Which repository sizes, languages, frameworks, and architectures must be represented?
* How will task difficulty be classified?
* How will task categories be weighted?
* Should common tasks have more weight than rare tasks?
* Should high-risk tasks have more weight regardless of frequency?
* Who determines the expected result?
* Can the expected result be verified independently?
* Were test cases created before or after the skill was written?
* Could the skill contain task-specific answers?
* Could the model have seen the tasks during skill development?
* Could evaluation artifacts leak into subsequent runs?
* Which cases belong in the development set?
* Which cases belong in the regression set?
* Which cases must remain in a locked holdout set?
* Which production failures should be promoted into the regression set?
* How will the holdout set be protected from gradual contamination?
* When must the holdout set be refreshed?

### 5. Comparison and baseline questions

* Against what baseline will the skill be compared?
* Should the primary baseline be no skill?
* Should the current released skill version be another baseline?
* Should ordinary repository instructions be a baseline?
* Should raw reference documentation without procedural instructions be a baseline?
* Should a length-matched neutral-context baseline be included?
* Should expert human performance be measured?
* Should another competing skill be measured?
* Should the same skill be tested with explicit invocation and automatic discovery?
* Should there be a condition where the skill is available but intentionally irrelevant?
* How will we isolate the effect of the skill from the effect of extra context?
* How will we isolate the effect of scripts from written instructions?
* How will we isolate the effect of references and assets?
* How will we identify which part of the skill creates the improvement?
* Must every condition use exactly the same prompt?
* Must every condition use exactly the same repository state?
* Must execution order be randomized?
* Must graders be blind to the experimental condition?
* What environmental differences would invalidate a comparison?
* What model or harness changes would invalidate an existing baseline?

### 6. What triggering metrics should be captured?

* Did the agent discover the skill?
* Did the agent invoke the skill?
* Was invocation explicit or implicit?
* Should the skill have been invoked?
* Did the skill activate too early?
* Did it activate too late?
* Did it activate on an unrelated request?
* Did it fail to activate on an eligible request?
* Did another skill activate instead?
* Did multiple skills activate unnecessarily?
* How long did skill selection take?
* How many candidate skills were considered?
* Was the complete skill loaded?
* Which references, scripts, and assets were loaded?
* Were unnecessary resources loaded?
* Was the skill invoked but ignored?
* Was the skill followed partially?
* Was the skill followed incorrectly?
* How will true positives, false positives, true negatives, and false negatives be defined?
* Should trigger precision be measured?
* Should trigger recall be measured?
* Should false-positive and false-negative rates be reported separately?
* Should explicit and implicit trigger metrics be reported separately?

### 7. What execution metrics should be captured?

* Which instructions did the agent follow?
* Which instructions did it skip?
* Which instructions did it contradict?
* Which tools did it use?
* Which tools should it have used?
* Which unnecessary tools did it use?
* Were tools used in the correct order?
* Were required validation steps executed?
* Were validation results actually inspected?
* Did the agent stop after a failed validation?
* Did it claim success despite failed validation?
* Did it repeat commands unnecessarily?
* Did it enter a loop?
* Did it overwrite or damage existing work?
* Did it request unnecessary permissions?
* Did it violate the intended sandbox boundary?
* Did it access unnecessary files or data?
* Did the skill cause a heavier workflow than the task required?
* Did the skill suppress a simpler, better native approach?
* Did the skill provide a usable fallback?
* Did the agent use that fallback appropriately?
* How many tool calls, commands, retries, corrections, and failed attempts occurred?
* Which step consumed the most time or tokens?
* At what step did the run first diverge from the expected workflow?

### 8. What outcome metrics should be captured?

* Did the task actually complete?
* Did the final artifact exist?
* Did it meet the stated requirements?
* Did it pass deterministic acceptance tests?
* Did it pass hidden tests?
* Did it build successfully?
* Did it run successfully?
* Did it satisfy the required schema or file format?
* Did it preserve existing behavior?
* Did it introduce regressions?
* Did it handle sad paths?
* Did it handle boundary conditions?
* Did it introduce security vulnerabilities?
* Did it introduce inaccessible or unusable interfaces?
* Was the output complete?
* Was it correct but incomplete?
* Was it structurally valid but behaviorally wrong?
* Was it cosmetically acceptable but functionally wrong?
* Did it solve the wrong problem convincingly?
* Did it add unnecessary files, abstractions, dependencies, or code?
* Did it require human repair?
* How much human repair was required?
* Would a real reviewer accept the result?
* Would the result be merged, published, sent, deployed, or rejected?
* Did defects escape the automated graders?
* Did downstream users later discover problems?
* Was success achieved on the first attempt?
* Was success achieved only after retries?
* Should eventual success and first-attempt success be reported separately?

### 9. What quality should be graded?

* Should the final response be graded?
* Should generated files be graded?
* Should code diffs be graded?
* Should tests be graded?
* Should runtime behavior be graded?
* Should tool-selection behavior be graded?
* Should the complete execution trace be graded?
* Should instruction adherence be graded?
* Should the agent's verification claims be graded?
* Should repository cleanliness be graded?
* Should maintainability be graded?
* Should architectural fit be graded?
* Should security be graded?
* Should usability and accessibility be graded?
* Should conciseness and unnecessary complexity be graded?
* Should recovery behavior after failure be graded?
* Should the skill's decision not to act be graded?
* Should human-review burden be graded?
* Should production impact be graded separately from offline correctness?

### 10. How should grading work?

* Which requirements can be graded deterministically?
* Which requirements require human judgment?
* Which requirements require an LLM judge?
* Which requirements cannot be graded reliably?
* Should deterministic failures override all subjective scores?
* Should critical requirements be pass/fail?
* Should noncritical requirements receive partial credit?
* How should partial completion be scored?
* How should contradictory evidence be resolved?
* How should flaky tests be handled?
* How should grader failures be distinguished from agent failures?
* Should multiple graders evaluate the same run?
* How will grader disagreement be resolved?
* Must human graders be blind to the skill condition?
* Must LLM judges be blind to skill identity and version?
* Should output ordering be randomized during pairwise grading?
* Can the same model that performed the task grade its own output?
* How will LLM graders be calibrated against expert humans?
* What level of human–grader agreement is required?
* How often must grader calibration be repeated?
* How will rubric changes affect historical scores?
* How will prompt injection inside evaluated artifacts be prevented from manipulating an LLM grader?
* What evidence must accompany every passing grade?
* What evidence must accompany every failing grade?
* Can a grade be marked unknown or unscorable?
* Who can override a grade?
* Must manual overrides include a reason and audit record?
* How will we test that the graders themselves detect known defects?
* How will we prevent graders from rewarding superficial compliance?
* How will we prevent the skill from optimizing specifically for the grader?

### 11. What efficiency and cost metrics should be captured?

* How many input, output, cached, and reasoning tokens were consumed?
* What was the monetary cost?
* What was the wall-clock duration?
* What was the model-processing duration?
* What was the tool-execution duration?
* How much time was lost to retries, rate limits, or infrastructure?
* How many commands and tool calls were used?
* How many files were read or modified?
* How much context did the skill add?
* How much context did its references add?
* How often were loaded resources unused?
* What was the cost per successful task?
* What was the time per successful task?
* What was the human-review time per task?
* What was the human-repair time per failed task?
* Did the skill improve quality by an amount that justifies its overhead?
* Did the skill reduce exploration and wasted work?
* Did the skill increase cost without improving success?
* Did a cheaper model with the skill outperform a more expensive model without it?

### 12. What reliability and generalization metrics should be captured?

* Does the same task produce consistent results across repeated runs?
* How much does performance vary across prompt paraphrases?
* How much does it vary across repositories?
* How much does it vary across programming languages or domains?
* How much does it vary across models?
* How much does it vary across Claude Code and Codex?
* How much does it vary across agent versions?
* Does performance degrade on longer tasks?
* Does performance degrade with larger contexts?
* Does performance degrade when other skills are installed?
* Does the skill generalize beyond its development examples?
* Is improvement concentrated in only a few easy tasks?
* Which task classes improve?
* Which task classes regress?
* Which tasks become less reliable even if average performance improves?
* How often does the skill cause catastrophic failure?
* How often does it produce confidently incorrect results?
* How often does it fail safely?
* How sensitive is it to environmental changes?

### 13. How should metrics be captured?

* Which telemetry signals are technically available from Claude Code?
* Which telemetry signals are technically available from Codex?
* Which signals require an agent wrapper?
* Which signals require hooks?
* Which signals require CLI JSON or JSONL output?
* Which signals require filesystem inspection?
* Which signals require Git diff inspection?
* Which signals require external tracing?
* Which signals require changes to the skill itself?
* Can skill invocation be observed directly?
* Can skill-resource loading be observed directly?
* Can instruction adherence be observed directly, or only inferred?
* How will timestamps be recorded?
* How will token counts be collected?
* How will pricing be calculated and versioned?
* How will tool calls and command results be captured?
* How will stdout, stderr, exit codes, and timeouts be captured?
* How will pre-run and post-run repository state be captured?
* How will generated artifacts be collected?
* How will browser, visual, audio, or document outputs be captured?
* How will human interventions be recorded?
* How will production acceptance, rejection, rollback, and rework be recorded?
* How will telemetry work when network access is unavailable?
* How will telemetry failures affect the run?
* Should missing telemetry fail the evaluation?
* How will duplicate or partially written events be detected?
* How will one run's events be correlated across different systems?
* What unique identifiers are required for skill, version, task, trial, session, agent and artifact?

### 14. When should metrics be captured?

* Before the skill is written?
* During initial manual experimentation?
* During every evaluation run?
* Before the agent starts?
* At skill discovery?
* At skill invocation?
* At every tool call?
* After every major workflow phase?
* When files change?
* When validation commands run?
* When the agent claims completion?
* Immediately after the run?
* After human review?
* After CI finishes?
* After deployment?
* When a production defect is discovered?
* When a user corrects or rejects the result?
* When the model changes?
* When the agent harness changes?
* When the skill description changes?
* When scripts, references, or assets change?
* When permissions or environment configuration change?
* Should metrics be captured continuously or only during controlled evaluations?
* Should production telemetry capture every run or a sample?
* How will sampling bias be prevented?

### 15. When should grading occur?

* Should deterministic grading happen during the run?
* Should a failed critical check stop the run immediately?
* Should grading happen only after the agent submits a final result?
* Should process and outcome grading happen separately?
* Should human grading happen before automated grading results are revealed?
* Should production outcomes be graded immediately or after an observation window?
* When should an incomplete run be declared failed?
* When should infrastructure failures be rerun?
* How many reruns are permitted?
* When should a result be marked inconclusive instead of failed?
* When should the full evaluation suite run?
* Should it run on every skill change?
* Should a smaller regression suite run during development?
* Should the holdout suite run only before release?
* Should evaluations run when a model or harness version changes?
* Should scheduled reevaluation detect performance drift?
* When should a previously approved skill lose its approved status?

### 16. Where should capture happen?

* Should capture happen inside the skill?
* Should it happen inside the agent harness?
* Should it happen in an external wrapper?
* Should it happen through hooks?
* Should it happen in CI?
* Should it happen inside isolated containers?
* Should it happen on the developer's machine?
* Should it happen in a centralized evaluation service?
* Should offline and production capture use the same instrumentation?
* Which component owns the authoritative run identifier?
* Which component owns timing measurement?
* Which component owns token and cost measurement?
* Which component owns artifact collection?
* Which component owns human feedback collection?
* How will events from local, cloud and external tools be correlated?
* What happens when a required platform does not expose a needed signal?
* Can capture be implemented consistently across Claude and Codex?
* Which platform-specific adapters are required?

### 17. Where should data be saved?

* Where should raw traces be stored?
* Where should normalized metrics be stored?
* Where should prompts and task definitions be stored?
* Where should skill snapshots be stored?
* Where should generated artifacts be stored?
* Where should verifier results be stored?
* Where should human feedback be stored?
* Where should grader prompts and rubric versions be stored?
* Where should summary reports be stored?
* Which data belongs beside the skill?
* Which data belongs in the project repository?
* Which data belongs in a database?
* Which large artifacts require object storage?
* Which evidence must be immutable?
* Which data must remain editable?
* Which data must be version-controlled?
* Should raw evidence and derived metrics be stored separately?
* How will one metric link back to its exact trace and artifact?
* What directory or schema structure will be used?
* How will schema migrations be handled?
* How long should each data class be retained?
* What can be deleted?
* What must never be overwritten?
* How will backups and recovery work?
* How will confidential code, prompts and documents be encrypted?
* Who can read raw traces?
* Who can change grades?
* Who can delete evaluation history?
* How will access and modification be audited?

### 18. How should metrics be displayed?

* Who is the audience for the report?
* Does the author need a different view from the reviewer or manager?
* What is the primary headline metric?
* Should trigger quality and execution quality be displayed separately?
* Should implicit and explicit invocation results be separated?
* Should no-skill, old-skill and candidate-skill results appear side by side?
* Should absolute scores and score differences both be displayed?
* Should confidence intervals be displayed?
* Should sample size be visible beside every metric?
* Should development, holdout and production results be separated?
* Should per-task results be available?
* Should results be grouped by task type, risk, model and harness?
* Should regressions be more prominent than improvements?
* Should critical failures override aggregate dashboards?
* Should cost and time be shown beside quality?
* Should cost per successful task be displayed?
* Should run-to-run variance be displayed?
* Should infrastructure failures be separated from agent failures?
* Should unknown and missing data be visually distinct from zero?
* Should users be able to open the trace and artifacts supporting a score?
* Should the dashboard show exactly why a run failed?
* Should skill-version comparisons be available?
* Should model-version comparisons be available?
* Should historical trends and drift be displayed?
* Should the system generate machine-readable reports?
* Should it generate human-readable reports?
* Should it produce CI annotations or pull-request comments?
* Which metrics should block a release?
* Which metrics should only warn?
* How will the report prevent a strong average from hiding serious regressions?

### 19. Statistical-validity questions

* How many unique tasks are needed?
* How many repeated trials are needed per task?
* What minimum improvement matters practically?
* What confidence level is required?
* What statistical power is required?
* Will analysis be paired by task?
* How will repeated runs from the same task be clustered?
* How will confidence intervals be calculated?
* How will binary pass/fail outcomes be compared?
* How will continuous quality scores be compared?
* How will multiple metrics and comparisons be handled?
* How will task weighting affect the result?
* How will outliers be handled?
* How will timeouts and infrastructure errors affect the denominator?
* How will early stopping be prevented from biasing results?
* Must thresholds and analysis rules be declared before running the evaluation?
* How will benchmark overfitting be detected?
* How will practical improvement be distinguished from statistically detectable but useless improvement?

### 20. Evidence and reproducibility questions

* What must be recorded to reproduce a run?
* Must the exact skill contents be hashed?
* Must the repository commit be recorded?
* Must the model identifier and configuration be recorded?
* Must the Claude Code or Codex version be recorded?
* Must the container image and environment be recorded?
* Must tool versions and dependency lockfiles be recorded?
* Must permissions, timeouts, CPU, memory and network rules be recorded?
* Must the exact task prompt be retained?
* Must the full trace be retained?
* Can an independent party rerun the evaluation?
* Can an independent party verify the grades without rerunning the agent?
* How will tampering with traces, artifacts, results or grades be detected?
* Should evidence manifests be signed?
* How will unavailable or proprietary platform details affect reproducibility?
* What minimum evidence package must accompany every published claim?

### 21. Failure-handling questions

* What happens when the agent crashes?
* What happens when the grader crashes?
* What happens when a verifier times out?
* What happens when the network fails?
* What happens when a model request is rate-limited?
* What happens when telemetry is incomplete?
* What happens when expected artifacts are missing?
* What happens when the working tree is contaminated?
* What happens when a previous run leaves files behind?
* What happens when the model or harness changes during an experiment?
* What happens when two graders disagree?
* What happens when a deterministic test and human reviewer disagree?
* What happens when the task specification is wrong?
* What happens when a test is flaky?
* What happens when an evaluation reveals a security issue?
* Which failures permit reruns?
* How many reruns are allowed?
* How will rerun selection bias be prevented?
* Which failures must remain visible in the final report?

### 22. Security, privacy and governance questions

* Will captured prompts contain personal, customer or proprietary data?
* Will traces contain secrets or credentials?
* Will command outputs expose environment variables?
* Will generated artifacts contain regulated data?
* What must be redacted before storage?
* Can redaction destroy evidence needed for grading?
* Who is permitted to run evaluations?
* Who is permitted to inspect production traces?
* What consent is required for production telemetry?
* Which skills are too sensitive for centralized evaluation?
* Can evaluation scripts execute untrusted content?
* Can evaluated artifacts attack the grader?
* Can a malicious skill falsify its own metrics?
* Can a skill modify or delete evaluation evidence?
* How will least-privilege execution be enforced?
* What retention and deletion policies apply?
* What audit trail is required for grade overrides and release decisions?

### 23. Lifecycle and maintenance questions

* How is a skill version identified?
* What changes require a new evaluation?
* Does changing only the description require complete reevaluation?
* Does changing a script require different tests from changing prose?
* How will historical results remain connected to the exact skill version?
* When is a baseline considered stale?
* When must a model upgrade invalidate prior evidence?
* How will new production failures enter the regression suite?
* How will outdated tests be retired?
* How will grader and rubric versions be maintained?
* How will metric definitions evolve without corrupting historical comparisons?
* How frequently should approved skills be reevaluated?
* What drift signals should trigger reevaluation?
* What conditions trigger rollback?
* What conditions trigger deprecation?
* Can a skill remain approved for one model but fail approval for another?
* Can it remain approved for explicit use but be disabled for automatic invocation?

### 24. Product and architecture questions

* Is this evaluator itself a skill, plugin, CLI, library, service, dashboard, or combination?
* Which responsibilities belong in deterministic software?
* Which responsibilities belong in an agent skill?
* Which responsibilities require human review?
* Should Claude and Codex use one common evaluation schema?
* Which platform-specific adapters are unavoidable?
* Should evaluation definitions live inside each skill?
* Should a central registry manage evaluation definitions?
* Should authors be able to add custom graders?
* What grader interface must every custom grader implement?
* Should evaluation run locally, remotely, or both?
* Should it work without API credentials?
* Should it support offline replay from stored traces?
* Should it integrate with GitHub and CI?
* Should it support scheduled reevaluation?
* Should it provide a release gate?
* Should it support production A/B experiments?
* How will the evaluator evaluate itself?
* What seeded defects will prove that the evaluator catches failures?
* How will we demonstrate that it does not merely generate impressive-looking dashboards?

### 25. Final framing questions

* What exactly are we claiming when we say a skill is "effective"?
* Effective for which task population?
* Effective with which model?
* Effective in which agent harness?
* Effective under which permissions and environment?
* Effective compared with what baseline?
* Effective according to which verifier?
* Effective over how many independent trials?
* Effective at what cost?
* Effective with what known regressions?
* Effective for how long before reevaluation is required?
* What evidence package must exist before that claim is allowed?

---

## How this connects to the house rule

This is "proof over authority" (`research/proof-over-authority.md`) applied to skills. Three threads tie it
to what this book already holds:

1. **Pre-commit the acceptance test.** Part B's inventory is that discipline blown out to system scale:
   name the decision, the metric, the baseline, the holdout and the gate *before* you see whether the skill
   flatters you. That is the best-measured mechanism in `proof-over-authority.md` (Finding A: pre-registration
   stripped ~86% of the flattering-but-false "wins," 57% → 8%).
2. **The taster is never the cook.** A7's "valid defects found by independent tests" and A5's blind-human /
   independent-verifier ordering are the measured backing for the rule already in this book — the agent may
   not grade its own work.
3. **A skill "that worked in a few manual trials" is the authority failure mode.** SkillsBench's 13-of-87
   *harm* result (**MEASURED**) is direct evidence that confident-sounding success on a few demos is not
   proof — exactly the "accept a claim only on proof, never on how authoritative it sounds" stance.

The one piece of *measured* evidence this file leans on most heavily — SkillsBench — is also the one that
forces the strongest caveat: it is a public benchmark, not this kitchen. So the honest landing is the same as
`research/discovery-logging-mechanisms.md`'s: the method and the question set are ASSERTED, the only
MEASURED anchors are external, and the open work is to run our own paired evaluation so a "this skill works"
claim here is backed by a number that moved in *this* repo — not imported authority.

---

## Source list (primary)

- Claude Code skill evaluation documentation — `https://code.claude.com/docs/en/skills#evaluate-and-iterate-on-a-skill`
- OpenAI — systematic skill-evaluation guide — `https://developers.openai.com/blog/eval-skills`
- SkillsBench v4 (methodology and results) — `https://arxiv.org/html/2602.12670v4`
- Anthropic — infrastructure-noise experiment — `https://www.anthropic.com/engineering/infrastructure-noise`
- Agent Skills evaluation methodology — `https://agentskills.io/skill-creation/evaluating-skills`
- OpenAI — evaluation best practices — `https://developers.openai.com/api/docs/guides/evaluation-best-practices`
