# The framework's gaps — an independent review before it can be trusted

> **About this file.** This is the independent review of
> `research/agent-skill-effectiveness-framework.md` — the answered design spec for the experimental
> `skill-eval`. It preserves, in substance verbatim, a gap analysis that opens with the blunt verdict that
> the framework "is strong as a measurement design, but it is not yet a complete implementation contract —
> and it is definitely not real-world proof yet. Proof begins only after the evaluator itself is built,
> validated and run against real tasks." This is the framework's **taster**: the second pair of eyes that is
> never the cook (`research/proof-over-authority.md`, Finding D). Content preserved, not rewritten to arrive;
> the provenance tags it carries (`[DERIVED]`, `[OFFICIAL—NIST]`, `[RESEARCH + TRAINED-KNOWLEDGE]`, etc.) are
> left exactly as written.
>
> **The measured-vs-asserted read this book adds.** Of the 22 gaps, only **two** rest on a **MEASURED**
> anchor: the Anthropic infrastructure-noise result (~6 pp swing → gap #5, randomise and interleave
> conditions) and the Anthropic grader-bias result (a broken grader moved a reported score from 42% to 95% →
> gaps #11 and #1, qualify the graders and meta-validate the evaluator). Those two measured facts are
> precisely what justifies the two gaps the review calls most serious. Everything else — the NIST AI RMF
> requirements, the OWASP suite, the protocol-freezing rules, the causal-estimand framing — is normative
> **ASSERTED** guidance (a well-reasoned "must," consistent with the measured anchors but not itself measured
> here). The OWASP Agentic Skills Top 10 is flagged in the text itself as an incubator project, "not a mature
> binding standard." This is the same FACT/ASSUMPTION split applied in `research/proof-over-authority.md`.
>
> **Why this matters to the house rule.** The review's closing point — *meta-validation: prove the evaluator
> can distinguish a useful skill from placebo, harm, leakage, grader failure and infrastructure noise* — is
> "proof over authority" turned on the evaluator itself. A dashboard that looks professional is an
> authority-shaped claim; it may not *close* the question of whether a skill works until the measurement
> system has passed its own pre-committed test (Finding A in `proof-over-authority.md`).

---

## Critical gaps

### 1. Validate the evaluator itself `[DERIVED]`

You need positive and negative controls proving that the measurement system can detect:

* A no-op skill
* A length-matched placebo skill
* An intentionally harmful skill
* A deliberately broken skill
* A genuinely useful skill
* Missing or corrupted telemetry
* A grader that falsely passes defective work

Without this, the framework could produce professional-looking but invalid reports.

### 2. Define the exact population being claimed `[OFFICIAL—NIST]`

"Effective for coding tasks" is too broad. Every evaluation must state:

* Target users
* Task families
* Repository types
* Languages and frameworks
* Skill invocation mode
* Risk level
* Deployment environment
* Explicitly unsupported contexts

NIST specifically requires external-validity assessment and evaluation data representative of the context of use. [NIST AI RMF Measure guidance](https://airc.nist.gov/airmf-resources/playbook/measure/)

### 3. Add production-weighted results `[DERIVED FROM OFFICIAL GUIDANCE]`

Task-macro pass rate gives every task equal weight. That can misrepresent reality.

Report at least:

* Equal-weight task pass rate
* Production-frequency-weighted pass rate
* Severity-weighted failure rate
* Critical-task pass rate
* Per-category results

A rare financial or destructive failure cannot be cancelled out by twenty easy formatting successes.

### 4. Freeze a complete experimental protocol before running `[TRAINED-KNOWLEDGE + DERIVED]`

The framework predeclares release thresholds, but it does not fully freeze:

* Sample size
* Task inclusion and exclusion
* Run order
* Rerun conditions
* Stopping rules
* Outlier handling
* Statistical method
* Multiple-comparison handling
* Which metric is primary
* Which analyses are exploratory

Without this, results can be unintentionally cherry-picked.

### 5. Randomize and interleave experiment conditions `[RESEARCH + TRAINED-KNOWLEDGE]`

Running all no-skill tests first and all skill tests later is unsafe because API load, model routing, infrastructure, caches and service changes can create false differences.

Required additions:

* Randomized condition order
* Interleaved A/B/C/D execution
* Time-blocked comparisons
* Balanced concurrency
* Recorded random seed
* Cold-versus-warm cache status
* Prevention of cross-trial state leakage

Anthropic demonstrated that infrastructure alone can move an agentic benchmark by six percentage points. [Anthropic infrastructure-noise study](https://www.anthropic.com/engineering/infrastructure-noise)

### 6. Define the causal estimand explicitly `[TRAINED-KNOWLEDGE + DERIVED]`

Your primary `B − A` comparison is correct, but it should be formally identified as an intention-to-treat comparison:

> What happens when the skill is available, whether or not it actually activates?

Do not calculate effectiveness only from runs where the skill triggered. That selects the easier or more obvious cases and can inflate the result.

Use:

* `B − A`: real deployment effect
* `C − A`: forced-use capability
* `C − B`: discovery/activation gap
* Triggered-only analysis: diagnostic, not causal proof

### 7. Replace binary "triggered" with an activation funnel `[OFFICIAL + DERIVED]`

A skill can be available but never loaded — or loaded but ignored.

Capture separately:

1. Skill advertised in metadata
2. Skill considered or selected
3. `SKILL.md` loaded
4. Reference opened
5. Script executed
6. Instructions materially followed
7. Skill-produced behavior observed

Claude officially recommends separating triggering from output quality, but the framework needs greater internal resolution. [Claude skill evaluation guidance](https://code.claude.com/docs/en/skills#evaluate-and-iterate-on-a-skill)

For Codex, some stages may remain `UNKNOWN` because current public telemetry does not guarantee direct skill-invocation events.

### 8. Capture the complete effective context `[DERIVED]`

The current manifest is not enough for full reproducibility. Capture or hash:

* System and developer instructions
* Available skill metadata
* Loaded skill contents
* Tool schemas
* MCP server versions
* CLI arguments
* Sampling parameters, when exposed
* Context-window occupancy
* Truncation events
* Prompt-cache status
* Locale, timezone and current date
* Relevant environment variables
* Dependency lockfiles
* Network-access policy

Sensitive values must be redacted while preserving verifiable hashes.

### 9. Define trigger ground truth `[DERIVED]`

Precision and recall require a trustworthy answer to "Should this skill have activated?"

Add:

* Explicit inclusion rules
* Explicit exclusion rules
* Ambiguous/abstain classification
* Independent labeling for disputed prompts
* Adjudication procedure
* False-positive versus false-negative cost matrix

A destructive skill may require extremely low false-positive activation even if that reduces recall.

### 10. Capture real external state and side effects `[OFFICIAL + DERIVED]`

Git and filesystem snapshots are insufficient for skills that operate on:

* Databases
* GitHub
* Email
* Calendars
* Cloud infrastructure
* Deployment systems
* Payment systems
* Web applications
* External APIs

Capture:

* Before-state
* Attempted action
* Authorization
* Actual committed action
* After-state
* Idempotency key
* Compensating or cleanup action

Anthropic explicitly distinguishes what an agent says it accomplished from the resulting state in the environment. [Anthropic agent-evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### 11. Qualify the graders before trusting them `[OFFICIAL + DERIVED]`

The document mentions calibration but lacks a grader acceptance gate.

Each grader needs testing against:

* Known-correct reference artifacts
* Intentionally defective mutants
* Acceptable alternative solutions
* Ambiguous cases
* Adversarial grader-bypass attempts
* Historical real failures

For human and model graders, measure disagreement and false-pass/false-fail rates. Anthropic documents cases where broken graders changed a reported score from 42% to 95%. [Anthropic agent-evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### 12. Define exact score aggregation `[DERIVED]`

The assertion schema exists, but the calculation from assertions to task result is unspecified.

You must freeze:

* Assertion weights
* Required versus optional assertions
* Partial-credit formula
* Critical-failure override
* Handling of `UNKNOWN`
* Category aggregation
* Whether failed setup can earn partial credit
* Prevention of score inflation by adding easy assertions

Otherwise two evaluator implementations can grade identical evidence differently.

### 13. Add rare-event safety statistics `[TRAINED-KNOWLEDGE]`

"Zero critical failures observed" does not prove safety.

Report:

* Number of relevant exposure opportunities
* One-sided upper confidence bound on failure probability
* Severity separately from frequency
* Whether the sample is too small to support a safety claim

The correct result may be "insufficient evidence," even with zero observed incidents.

### 14. Build an explicit adversarial security suite `[OWASP EVIDENCE + DERIVED]`

The existing safety list is too generic. Add tests for:

* Direct and indirect prompt injection
* Malicious repository instructions
* Poisoned documentation and tool output
* Credential and data exfiltration
* Memory poisoning
* Tool privilege escalation
* Goal hijacking
* Approval manipulation
* Denial-of-wallet loops
* Malicious skill dependencies
* Cross-agent cascading failures

These are documented in the [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html).

The [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) is directly relevant, but it is an incubator project — not a mature binding standard.

### 15. Separate protected evaluations physically `[DERIVED]`

The proposed layout places `protected/` underneath the same `skill-eval/` tree. Saying that it will not be mounted is not a strong enough security boundary.

Use:

* A separate operating-system account, volume or remote service
* No parent-directory traversal from the agent runner
* Separate credentials
* Read-once task delivery
* Network isolation
* Audit logging for holdout access

Hidden tests stored beside public tests are one configuration mistake away from leakage.

---

## Important operational gaps

### 16. Standardize human interaction `[DERIVED]`

For tasks requiring clarification or approval, define a scripted user simulator or fixed response policy. Otherwise one run may receive helpful answers and another may not.

Measure:

* Number and quality of clarification questions
* Unnecessary interruptions
* Human response time
* Approval requests
* Human work required
* Whether the task could proceed safely without clarification

### 17. Test context pressure and unrelated-task interference `[DERIVED]`

A skill may improve its intended tasks while harming unrelated tasks by consuming context or influencing behavior.

Add:

* Long-context tasks
* Near-context-limit tasks
* Unrelated task outcomes — not merely trigger checks
* Competing-instruction cases
* Skill-description collision cases
* Skill metadata overhead
* Truncation-induced regressions

### 18. Report tail latency and complete cost `[DERIVED]`

Median duration and cost per successful task can conceal bad behavior.

Also report:

* p50, p90, p95 and maximum duration
* Cost per assigned task, including failures
* Failed-run cost
* Timeout rate
* Peak memory and disk use
* External API/tool costs
* Human-review and repair cost
* Censored timeout handling

### 19. Add dataset governance `[OFFICIAL—NIST + DERIVED]`

For every task, record:

* Source and provenance
* Consent or legal basis
* License
* Sanitization
* Deduplication
* Creation date
* Last validation date
* Production frequency
* Severity
* Relevant user/repository segment
* Known contamination risk

Multilingual, accessibility or demographic evaluation is required only when the skill's claimed scope includes those populations.

### 20. Validate adapter and telemetry integrity `[DERIVED]`

Add end-to-end canaries proving:

* Events are not dropped
* Sequence ordering is preserved
* Process crashes are captured
* Partial JSONL is detected
* Unknown event types fail visibly
* CLI schema changes invalidate compatibility
* Raw evidence and normalized records reconcile
* Reports cannot show "verified" with incomplete telemetry

### 21. Define release rollout and rollback mechanics `[DERIVED]`

A release decision alone is insufficient.

Specify:

* Feature flag or version pin
* Shadow mode
* Canary percentage
* Progressive exposure limits
* Automatic stop conditions
* Kill switch
* Rollback owner
* Rollback verification
* Incident evidence preservation

### 22. Add evaluation-health and saturation rules `[OFFICIAL—ANTHROPIC]`

The framework says to reevaluate, but not when the suite itself becomes stale.

Trigger suite maintenance when:

* Baseline or candidate approaches saturation
* Task distribution changes
* Too many tasks become invalid
* Grader disagreement rises
* Production failures are not represented
* Development-to-production correlation falls
* Models solve tasks through unintended shortcuts

Anthropic explicitly warns that saturated evaluations stop measuring improvement reliably. [Anthropic agent-evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

---

## Not actually missing

These limitations were already acknowledged correctly in the framework:

* Multi-skill composition is deferred from version 1.
* Codex automatic skill-activation observability is unresolved.
* Cost reporting may differ across subscription and API execution.
* Release thresholds are user decisions.
* Results are scoped to a skill/model/harness/environment tuple.
* Holdout protection and production monitoring are already included.

---

## Final verdict

The document is a credible design foundation. It is not yet complete enough to claim that its measurements
are scientifically or operationally trustworthy.

The most serious missing element is **meta-validation**: proving that the evaluator can distinguish a useful
skill from placebo, harm, leakage, grader failure and infrastructure noise.

The next correct version should incorporate these gaps before implementation — not after the first dashboard
has already created false confidence.

---

## How this connects to the house rule

This review is the framework's independent check — the discipline this book already holds for pages and
dishes, applied to the measurement system itself. Three threads:

1. **Meta-validation is pre-registration turned inward.** `research/proof-over-authority.md` (Finding A) shows
   that committing the acceptance test *before* seeing the result stripped ~86% of flattering-but-false
   "wins." Gap #1 demands the same for the evaluator: define, *before* it reports anything, the controls that
   prove it can detect placebo, harm and grader failure. A measurement tool that has not passed its own test
   is an authority-shaped claim, and authority may not close a question in this kitchen.
2. **The two measured anchors carry the two heaviest gaps.** Infrastructure noise (~6 pp, **MEASURED**) is
   what makes #5 non-negotiable; grader bias (42% → 95%, **MEASURED**) is what makes #11/#1 non-negotiable.
   The rest of the 22 gaps are sound normative guidance, but these two are the ones with a number behind them.
3. **"Not actually missing" is itself the discipline.** The review names what the framework already got right
   rather than manufacturing faults — the same refusal to overclaim that `KNOWN-HOLES.md` enforces elsewhere
   in the book.

The open work, as the review states plainly: fold these gaps into the framework *before* implementation, not
after a dashboard has bred false confidence.

---

## Source list (primary)

- NIST AI RMF — Measure guidance (playbook) — `https://airc.nist.gov/airmf-resources/playbook/measure/`
- Anthropic — infrastructure-noise study — `https://www.anthropic.com/engineering/infrastructure-noise`
- Anthropic — demystifying evals for AI agents — `https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`
- Claude Code — skill evaluation guidance — `https://code.claude.com/docs/en/skills#evaluate-and-iterate-on-a-skill`
- OWASP — AI Agent Security Cheat Sheet — `https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html`
- OWASP — Agentic Skills Top 10 (incubator project) — `https://owasp.org/www-project-agentic-skills-top-10/`

Related files in this book: `research/agent-skill-effectiveness-framework.md` (the spec under review),
`research/skill-effectiveness-evaluation.md` (the method and the open questions), and
`research/proof-over-authority.md` (the measured backing for meta-validation).
