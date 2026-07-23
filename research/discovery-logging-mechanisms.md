# Mechanisms that make an agent capture and log its own discoveries — measured vs asserted

> **About this file.** There is no existing `research/` convention in this repo; I created the
> `research/` directory and this file as the home for this investigation. It is the only file I
> touched, and it is left uncommitted for review.
>
> **Scope.** The question: *what mechanisms reliably cause a coding agent to CAPTURE and LOG its own
> discoveries, decisions, faults, and lessons into a durable repo record WITHOUT depending on the
> model remembering — and which of those are backed by MEASURABLE evidence rather than assertion?*
>
> **Headline finding.** The mechanisms that do **not** depend on the model at all are the ones where
> a **hook script does the writing** (a `PostToolUse`/`SessionEnd`/`Stop` hook that appends to the
> journal itself). Their *reliability* is a property of the deterministic script, not the model, so
> "the model forgot" cannot happen. But — and this is the crux — **no first-party or community source
> measures the downstream quality** of what gets captured this way. The only rigorously *measured*
> results in this whole space are (a) that memory/reflection architectures improve a task metric
> (Reflexion, Generative Agents, Anthropic's memory tool), and (b) that reminder-based adherence
> **decays measurably** over a long session — which is direct evidence *against* leaning on injected
> reminders. The auto-capture hook tooling itself is entirely **asserted**, never measured.

---

## 1. Claude Code's hook system (primary source: official docs)

Reference: **Hooks reference — Claude Code Docs**, `https://docs.claude.com/en/docs/claude-code/hooks`
(301-redirects to `https://code.claude.com/docs/en/hooks`). Companion guide: **Get started with
Claude Code hooks**, `https://docs.claude.com/en/docs/claude-code/hooks-guide`.

**Caveat on version.** The live reference I fetched enumerates a *superset* of events beyond the
commonly-cited nine (it also documents `Setup`, `UserPromptExpansion`, `PermissionRequest`,
`PermissionDenied`, `PostToolUseFailure`, `PostToolBatch`, `PostCompact`, `SubagentStart`,
`TeammateIdle`, `TaskCreated`, `TaskCompleted`, `MessageDisplay`, `FileChanged`, `CwdChanged`,
`InstructionsLoaded`, `ConfigChange`, `WorktreeCreate/Remove`, `Elicitation*`). Those newer events
matter for us (`PostToolBatch`, `TaskCompleted`, `PostToolUseFailure` are all plausible capture
triggers) but a few may be newer than a given CLI build — **verify against `code.claude.com/docs/en/hooks`
for the installed version before building on the newer ones.** The nine below are the stable core.

### Two distinct capabilities, and why the distinction is the whole point

A hook can do two independent things, and confusing them is the core mistake:

1. **Inject context INTO the model** — return `hookSpecificOutput.additionalContext` (or, for
   `UserPromptSubmit`/`PreToolUse`, plain exit-0 stdout is also added to context). This is a
   *reminder*: the model still has to choose to act on it. Subject to the adherence decay in §4.
2. **Block/deny an action or block completion** — return top-level `decision: "block"` with a
   `reason`, or exit with **code 2** (stderr fed to the model). This is *coercive*: the model cannot
   proceed until the gate is satisfied.

Neither of those is the same as the third, most robust option:

3. **The hook script writes the record ITSELF** as a side effect (append to a journal file, run
   `git notes`, etc.). This needs **no model cooperation at all** — it is deterministic. The model
   "remembering" is not in the loop.

### Core nine events (triggers, key input fields, capture-relevant capabilities)

| Event | Trigger | Key input fields | Inject context? | Block / feed reason back? |
|---|---|---|---|---|
| **SessionStart** | New session, or resume/clear/compact/fork | `source`, `session_id`, `transcript_path`, `cwd` | ✅ `hookSpecificOutput.additionalContext`; exit-0 stdout added as context; can set `initialUserMessage` | ❌ cannot block; exit-2 is only an error notice, not shown to model |
| **UserPromptSubmit** | User submits a prompt, before the model sees it | `prompt`, `session_id`, `cwd` | ✅ `additionalContext`; **plain exit-0 stdout is added to context alongside the prompt** | ✅ top-level `decision: "block"` + `reason` erases the prompt; **exit 2** blocks prompt, stderr fed to model |
| **PreToolUse** | Before a tool call runs | `tool_name`, `tool_input` | ✅ `hookSpecificOutput.additionalContext`; exit-0 stdout added | ✅ `hookSpecificOutput.permissionDecision: "deny"/"ask"/"allow"` + `permissionDecisionReason`; **exit 2** blocks the call |
| **PostToolUse** | After a tool call succeeds | `tool_name`, `tool_input`, `tool_output` | ✅ `hookSpecificOutput.additionalContext`; exit-0 stdout added next to result | ✅ top-level `decision: "block"` + `reason`; **exit 2** shows stderr to model (tool already ran) |
| **Stop** | Model has finished responding | `last_assistant_message`, `session_id`, `transcript_path` | ✅ `hookSpecificOutput.additionalContext` — fed back as a system reminder so the model acts on it | ✅ **top-level `decision: "block"` + `reason` PREVENTS the model from stopping and continues the turn**; **exit 2** also prevents stop |
| **SubagentStop** | A subagent finishes | `agent_type`, `agent_id`, `last_assistant_message` | ✅ `additionalContext` | ✅ `decision: "block"` + `reason` prevents the subagent stopping; exit 2 same |
| **PreCompact** | Before context compaction | `compaction_reason` (`manual`/`auto`) | ❌ (no context injection) | ✅ `decision: "block"` + `reason` blocks compaction; exit 2 blocks |
| **Notification** | Claude Code emits a notification | `notification_type`, `message` | ❌ | ❌ side-effect only; exit-2 shown to user only |
| **SessionEnd** | Session terminates | `end_reason`, `transcript_path`, `cwd` | ❌ (nothing injected — session is ending) | ❌ side-effect only (cleanup/logging) |

**Universal precedence rule (from the reference):** `continue: false` at top level stops the model
entirely and takes precedence over any `decision: "block"`. `additionalContext`/`systemMessage`/plain
stdout are **capped at 10,000 characters**.

### What this means for durable capture (the mechanistic reading)

- **Deterministic auto-capture (no model dependence):** a `PostToolUse` hook that runs a script which
  appends `{tool, args, cwd, git-sha, timestamp}` to `journal.md`, and a `SessionEnd`/`PreCompact`
  hook that dumps the transcript for later extraction. The *capture* here is 100% reliable because
  the script writes it; the model is never asked. This is exactly the shape of the community repos in
  §2. **What is unmeasured is whether the raw captured stream contains the *finding* the user cares
  about, phrased usefully** — a `PostToolUse` log records that `pytest` ran and exited 1; it does not
  record the model's sentence "the flaky test is a timezone bug."
- **The blocking checkpoint (coerces, does not write for the model):** a `Stop` hook that checks
  "has `journal.md` been modified since `SessionStart`?" and, if not, returns
  `decision: "block", reason: "Before finishing, append today's findings to research/journal.md."`
  This does not write anything — it refuses to let the turn end until the model writes. It converts a
  *reminder the model can ignore* into a *gate the model cannot pass*. This is the single most
  promising lever for the specific failure the team reports ("surfaces a finding, then fails to write
  it"), and it is the one with **zero measured evidence either way** — hence the hypotheses in §6.
- **Injected reminders (`SessionStart`/`UserPromptSubmit` `additionalContext`):** cheapest, weakest —
  the model must still choose to log. §4 shows this class decays measurably over a session.

---

## 2. Real repositories implementing agent journaling / memory-capture hooks

Every project below is real and does what it claims. **None presents measured evidence of
effectiveness** — no before/after logging rate, no benchmark, no ablation. I checked each for metrics
and quote the closest thing to a measurement claim where one exists.

| Repo | URL | What it actually builds | Hooks used | Measured effectiveness? |
|---|---|---|---|---|
| **coleam00/claude-memory-compiler** | `https://github.com/coleam00/claude-memory-compiler` | On session end / pre-compact, captures the transcript, spawns a background Claude Agent SDK process (`flush.py`) that extracts decisions/lessons/gotchas into a daily log; `compile.py` organizes them into cross-referenced knowledge articles; `SessionStart` injects the index back in | `SessionEnd`, `PreCompact`, `SessionStart` | **No.** Zero metrics/benchmarks. Closest claim is a design assertion (attributed to Karpathy): "at personal scale (50–500 articles), the LLM reading a structured `index.md` outperforms vector similarity" — not a measurement of this system |
| **karanb192/claude-code-hooks** | `https://github.com/karanb192/claude-code-hooks` | Safety + observability hook marketplace; a `session-logger` writes a durable markdown log (cwd, git repo, files touched, bash commands, best-effort secret redaction); plugins `dead-end-registry` ("approaches you tried and reverted"), `nerf-receipts` (failure rate / edit churn / tokens per task), `standup-autopilot` | Session-boundary + tool hooks | **No.** No metrics/benchmarks/before-after. Author gave an OWASP GenAI talk but publishes no validation data |
| **disler/claude-code-hooks-mastery** | `https://github.com/disler/claude-code-hooks-mastery` | Reference implementation demonstrating all hook events, incl. logging every event | All events (educational) | **No** — teaching repo, not evaluated |
| **disler/claude-code-hooks-multi-agent-observability** | `https://github.com/disler/claude-code-hooks-multi-agent-observability` | Streams hook events to a dashboard for real-time monitoring of agent activity | `PreToolUse`/`PostToolUse`/etc. → event bus | **No** — observability, no effectiveness metric |
| **anthropics/claude-code issue #4654** | `https://github.com/anthropics/claude-code/issues/4654` | Feature request: "Persistent Local Lessons Learned Repository" — community asking Anthropic for exactly this capability natively | n/a (request) | **No** — confirms the gap is recognized and unsolved upstream |

Also referenced in community writing: Anthropic's "**Compounding Engineering**" pattern (tagging
`@claude` on PRs so review lessons feed back into `CLAUDE.md`) — described in interviews/posts, no
published measurement.

**Bottom line for §2: the tooling to capture deterministically exists and is easy. The evidence that
any given capture design actually raises the rate of *useful* findings landing in the repo does not
exist in public sources.**

---

## 3. Prior-art research patterns (what was actually MEASURED)

| Pattern | Source | What was MEASURED (metric + result) | What was only proposed |
|---|---|---|---|
| **Reflexion** — verbal self-reflection stored in an episodic memory buffer, prepended on the next attempt; no weight updates | Shinn et al., NeurIPS 2023. arXiv `https://arxiv.org/abs/2303.11366`; NeurIPS PDF `https://proceedings.neurips.cc/paper_files/paper/2023/file/1b44b878bb782e6954cd888628510e90-Paper-Conference.pdf`; code `https://github.com/noahshinn/reflexion` | **Measured.** 91% pass@1 on HumanEval (coding), vs 80% for the GPT-4 baseline. Also measured gains on ALFWorld (decision-making) and HotpotQA (reasoning) across trials, with the reflection buffer as the manipulated variable | Generalization beyond the tested benchmarks; long-horizon accumulation |
| **Generative Agents** — memory stream (time-stamped observations) + significance-gated **reflection** + retrieval scored by recency × importance × relevance | Park et al., 2023. arXiv `https://arxiv.org/abs/2304.03442`; ACM `https://dl.acm.org/doi/fullHtml/10.1145/3586183.3606763` | **Measured, with an ablation.** Human-rated believability (TrueSkill-style ranked scores): **full architecture μ=29.89**; no-reflection μ=26.88; no-reflection-or-planning μ=25.64; crowdworker μ=22.95; **no-memory/planning/reflection μ=21.21 (worst)**. Full vs prior-art effect size **d=8.16**; Kruskal–Wallis H(4)=150.29, p<0.001. This is the strongest measured evidence that *reflection/consolidation as a distinct step* carries weight | The sandbox is social simulation, not code — external validity to a repo journal is an assumption, not a result |
| **Reflection / critic / self-critique loops** generally | (Reflexion is the canonical measured instance) | Measured *within* Reflexion/Generative-Agents; the general "add a critic pass" claim is mostly asserted outside those | The generic claim that a critic always helps |
| **Anthropic memory tool + context editing** — file-backed memory Claude reads/writes across turns; context editing auto-clears stale tool results | Docs `https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool`; blog `https://claude.com/blog/context-management` (beta header `context-management-2025-06-27`) | **Measured (first-party, internal eval).** On an internal agentic-search eval: **memory tool + context editing = +39% over baseline**; **context editing alone = +29%**; a 100-turn web-search eval completed workflows that otherwise failed and **cut token use by 84%**. Note: these measure *task success with memory available*, not *the rate at which the agent chooses to record a finding* | That the same lift transfers to a discovery-logging journal (different task) is untested |

**Reading of §3 for our problem:** the measured results all say *having and consolidating memory
improves a downstream metric*. **None of them measures the capture step in isolation** — i.e., "given
the agent noticed X, how often does X end up durably recorded?" That specific rate — the one the team
wants to move — has no published measurement anywhere I found. It is the gap our probes should fill.

---

## 4. The failure mode of reminder-based approaches — MEASURED evidence

This is the strongest reason not to rely on injected reminders (`additionalContext`), and it *is*
measured:

- **Instruction drift over turns.** *Measuring and Controlling Instruction (In)Stability in Language
  Model Dialogs* (Li et al., COLM 2024), `https://arxiv.org/abs/2402.10962`. LLaMA2-chat-70B and
  GPT-3.5 show **significant instruction drift within eight rounds** of conversation; the authors tie
  it to attention decay over long exchanges and introduce a quantitative drift benchmark plus a
  mitigation ("split-softmax" reallocating attention to the system prompt). Measured: adherence to a
  standing instruction falls as the dialog grows.
- **Omission constraints decay while commission constraints persist.** *Omission Constraints Decay
  While Commission Constraints Persist in Long-Context LLM Agents*,
  `https://arxiv.org/abs/2604.20911`. Across 12 models / 8 providers, **omission compliance fell from
  73% at turn 5 to 33% at turn 16**, while "do X" (commission) compliance held at ~100%. This is
  directly on point: **"remember to log your findings" is an omission-style standing instruction —
  exactly the class shown to decay by turn 16.** A one-shot deterministic write or a hard gate is a
  commission-style constraint, the class that holds.
- **Lost in the middle.** Liu et al., TACL 2024, arXiv `https://arxiv.org/abs/2307.03172`. U-shaped
  positional performance: models use information best at the very start or very end of the context and
  **degrade in the middle** — GPT-3.5-Turbo dropped *below its no-document closed-book score (56.1%)*
  when the relevant fact sat mid-context. A "log your findings" reminder injected at session start
  drifts into the low-salience middle as the session grows. Injecting it *late* (a `Stop`-hook
  `additionalContext`, i.e., at the recency-favored end) is the position the evidence favors.

**Net:** repeated/early injected reminders are the *weakest* class and the one with measured decay.
The mechanisms that sidestep the model's attention entirely (deterministic script-writes; hard Stop
gates) are the ones the evidence points toward — but their *capture-quality* is unmeasured, which is
the whole opportunity.

---

## 5. Landscape table — MEASURED vs ASSERTED

| # | Mechanism | How capture happens | Depends on model remembering? | Tag | Basis |
|---|---|---|---|---|---|
| 1 | **Deterministic auto-capture hook** (`PostToolUse`/`SessionEnd` script appends events to journal) | Script writes it | **No** | **ASSERTED** | Repos in §2 build it; none measure whether captured content is *useful*. Reliability of the write is a property of the script, not evidence about outcome |
| 2 | **Blocking `Stop`-hook checkpoint** (`decision:"block"` unless journal changed since `SessionStart`) | Model writes, but is *forced* to before it can finish | Coerced, not remembered | **ASSERTED** (mechanism documented; effect unmeasured) | Hooks reference confirms `Stop` blocking + `reason`; no one has measured the logging-rate lift |
| 3 | **Event-triggered targeted reminder** (`PostToolUse`/`Stop` `additionalContext` fired on a specific event, e.g. a failed/killed command) | Model writes if it complies | **Yes** | **ASSERTED** for the trigger; **MEASURED (negative)** for the general class — reminders decay (§4) |
| 4 | **External observer/critic pass** (second agent reads transcript, extracts findings, writes journal) | Second model writes | No (for the primary agent) | **ASSERTED** as tooling (claude-memory-compiler); **MEASURED** that a critic/reflection step helps a task metric (Reflexion, §3) — not that it captures findings faithfully |
| 5 | **Periodic reflection / consolidation** (significance-gated summarize-and-store) | Model writes on a schedule/threshold | Partly (trigger is external) | **MEASURED** for *behavioral believability* (Generative Agents ablation, d=8.16); **ASSERTED** for repo-journaling transfer |
| 6 | **Memory tool** (file-backed cross-session memory + context editing) | Model writes via tool | Yes (model calls the tool) | **MEASURED** (first-party): +39% combined / +29% context-editing / −84% tokens on internal agentic-search eval; **ASSERTED** that it transfers to discovery-logging |

**Reading:** the only rows with a positive *measurement* (5, 6) measure a *task-success* proxy, not
capture rate. The rows that most directly solve our stated failure (1, 2) are *asserted*. That
mismatch is precisely why the team should measure rather than adopt-because-it-sounds-right.

---

## 6. Two-to-three testable HYPOTHESES (each predicts a number moving)

Baseline to establish first: **discovery-logging rate** `L` = (# distinct findings the agent voiced
in-conversation that also got written to the repo journal) / (# distinct findings it voiced). The
team's complaint is that `L` is low today; call the current value `L0` (measure it — see §7).

- **H1 (blocking checkpoint).** *A `Stop` hook that returns `decision:"block"` with reason "append
  today's findings to the journal before finishing" whenever `journal.md` has not been modified since
  `SessionStart` raises the logging rate from baseline `L0` to `L1 ≥ 0.8`, and does so more than a
  plain `SessionStart` reminder does.* Predicts `L` moves up sharply and that the *gate* beats the
  *reminder* head-to-head.
- **H2 (reminder decay is real here).** *A single `SessionStart`-injected "remember to log findings"
  reminder produces a logging rate that declines with session length — high in the first ~5 tool
  turns, materially lower past ~15 turns — mirroring the omission-constraint decay (73%→33%) in §4.*
  Predicts a **downward slope of `L` vs. turn index**, which if confirmed justifies preferring H1/H3
  over §5-style early reminders.
- **H3 (event-targeted, late-position reminder).** *Firing the reminder from a `PostToolUse`/`Stop`
  hook at the moment a finding is likely — e.g. right after a command exits non-zero (a failure the
  agent just diagnosed) — and injecting it at the recency-favored end raises per-event capture from
  baseline `p0` to `p1`, beating the same reminder injected once at session start.* Predicts that
  **position + timing** of the identical text changes the capture probability (a direct test of the
  §4 "lost in the middle" prediction inside our own workflow).

---

## 7. Metric + minimal probing-prototype design (so a later run can actually measure it)

**Shared metric — discovery-logging rate `L`.** For each trial session, an independent judge (a
second model pass or a human) reads the transcript, lists distinct *findings* (a finding = a concrete
discovery/decision/fault/lesson the agent stated), then checks the repo journal diff for that session
and marks each finding logged / not-logged. `L = logged / total`. Report `L` with a 95% CI. "Better"
= a statistically higher `L` (or, for H2/H3, a flatter slope / higher late-turn capture) at p<0.05.

**Shared harness — seeded sessions.** To get findings on demand, seed each session with a fixed task
known to surface several discoveries: e.g. "investigate why `<seeded flaky test>` fails" in a fixture
repo with 3–4 planted issues (a timezone bug, a race, a stale fixture, a wrong assertion). Each
planted issue is a *findable finding*; the judge scores whether each was both voiced and logged. Using
a fixed seed set makes trials comparable and the denominator stable.

| Probe | Seed | Arms (each run N≥20 sessions) | Count | "Better" = |
|---|---|---|---|---|
| **H1** | Fixture repo, 4 planted issues, task = "diagnose the failing suite and journal what you find" | (a) no hook (baseline `L0`); (b) `SessionStart` reminder; (c) **blocking `Stop` hook** | `L` per session | arm (c) `L ≥ 0.8` **and** (c) > (b) > (a), each gap p<0.05 |
| **H2** | Same fixture, single `SessionStart` reminder, sessions run long (≥16 tool turns) | one arm; bin findings by the turn index at which they were voiced | `L` within early (≤5) vs late (≥15) turn bins | measured **decline** early→late, CIs non-overlapping (confirms decay → justifies H1/H3) |
| **H3** | Fixture where 2 issues surface via a command exiting non-zero | (a) reminder once at `SessionStart`; (b) identical reminder fired from `PostToolUse`/`Stop` right after the non-zero exit | per-event capture `p` for the failure-triggered findings | arm (b) `p` > arm (a) `p`, p<0.05 (same text, better position/timing) |

**Trials & power.** N≥20 sessions/arm gives enough to detect a ~0.25 absolute shift in `L` at
conventional power; scale up if `L0` is mid-range (variance is highest near 0.5). Freeze the judge
prompt and the seed set across arms so the only variable is the mechanism. Log every raw judgment so
the rate is auditable, not asserted — which is the entire point of the exercise.

---

## Source list (primary)

- Claude Code hooks reference — `https://docs.claude.com/en/docs/claude-code/hooks` → `https://code.claude.com/docs/en/hooks`
- Claude Code hooks guide — `https://docs.claude.com/en/docs/claude-code/hooks-guide`
- Anthropic memory tool — `https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool`
- Anthropic context management (measured memory numbers) — `https://claude.com/blog/context-management`
- coleam00/claude-memory-compiler — `https://github.com/coleam00/claude-memory-compiler`
- karanb192/claude-code-hooks — `https://github.com/karanb192/claude-code-hooks`
- disler/claude-code-hooks-mastery — `https://github.com/disler/claude-code-hooks-mastery`
- disler/claude-code-hooks-multi-agent-observability — `https://github.com/disler/claude-code-hooks-multi-agent-observability`
- claude-code issue #4654 (persistent lessons-learned request) — `https://github.com/anthropics/claude-code/issues/4654`
- Reflexion (Shinn et al., NeurIPS 2023) — `https://arxiv.org/abs/2303.11366` · `https://github.com/noahshinn/reflexion`
- Generative Agents (Park et al., 2023) — `https://arxiv.org/abs/2304.03442` · `https://dl.acm.org/doi/fullHtml/10.1145/3586183.3606763`
- Instruction (In)Stability in Dialogs (COLM 2024) — `https://arxiv.org/abs/2402.10962`
- Omission vs commission constraint decay — `https://arxiv.org/abs/2604.20911`
- Lost in the Middle (TACL 2024) — `https://arxiv.org/abs/2307.03172`
