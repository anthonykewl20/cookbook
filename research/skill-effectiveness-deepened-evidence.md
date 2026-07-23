# Skill-effectiveness evaluation — the deepened evidence, validated against its primary sources

> **What this is.** A fourth research note in the skill-evaluation investigation. It is the output of a
> `deep-research` web/GitHub sweep that was then **validated by the host against the primary sources** — not
> transcribed. It is the *deepening* layer on top of three earlier notes in `research/`:
> - `skill-effectiveness-evaluation.md` — the method, the measured evidence, and the 25-section question inventory.
> - `agent-skill-effectiveness-framework.md` — the answered `skill-eval` design spec.
> - `agent-skill-effectiveness-framework-gaps.md` — the 22-gap independent review (the framework's *taster*).
>
> **The one rule this file obeys.** Every claim below carries two tags. **MEASURED / ASSERTED** says whether the
> number came off an instrument or out of an argument — the discipline of `research/proof-over-authority.md`.
> **VERIFIED / CLAIMED-BY-WORKFLOW / UNVERIFIABLE** says whether *this session opened the primary source and
> confirmed the number*, or whether it is still the workflow's word. Nothing below is recorded as fact that was
> not checked; the un-checked claims are filed in their own section so a stranger can see exactly what still
> needs opening.

---

## §0 — Verification scorecard

The `deep-research` sweep ran ~47 agent calls (1 scope, 5 search angles, 15 fetched sources, 22 extracted
claims, 19 verify votes) before being **capped by the owner at the 30-agent mark** — so its synthesis was
treated as a draft to be checked, never a finished record (see the standing feedback
`validate it not just log the research`). The host then opened the primary source for every **load-bearing**
MEASURED claim by hand, without spending more workflow agents.

| # | Finding (headline) | Primary opened this session | MEASURED / ASSERTED | VERIFIED / CLAIMED |
| --- | --- | --- | --- | --- |
| 1 | τ-bench: `pass¹→pass⁴` decays 0.460→0.225 (Airline), 0.692→0.462 (Retail) | `sierra-research/tau-bench` README leaderboard | MEASURED | **VERIFIED** (numbers match exactly) |
| 2 | τ-bench's own LLM error-grader "may lead to inaccurate error identifications" | `sierra-research/tau-bench` README | MEASURED (the maintainer's own caveat) | **VERIFIED** |
| 3 | Spence sandboxed eval: forced-eval hook 100% (22/22) vs 55% baseline; ~5 pp run-to-run noise | scottspence.com post (2026-02-08) | MEASURED | **VERIFIED** (every number matches) |
| 4 | Spence: activation is keyword-gated (~100% / 20–40% / ~0% for keyword / generic / indirect prompts) | scottspence.com post | MEASURED (small N) | **VERIFIED** |
| 5 | SWE-Bench "Illusion": 76% vs 53% file-path ID; 35% vs 18% 5-gram (contamination signal) | arXiv 2506.12286 abstract (v4, Dec 2025) | MEASURED | **VERIFIED** (verbatim from abstract) |
| 6 | Seleznov 650-trial: directive descriptions 100% vs "Use when" ~77%; CMH OR = 20.6, p<0.0001 | Marc Bara Medium + Spence post (two independent secondaries) | MEASURED | **VERIFIED via 2 secondaries** (primary repo not opened) |
| 7 | JUDGE-BENCH: 20 NLP tasks, 11 LLMs judged; "substantial variability" vs humans | `dmg-illc/JUDGE-BENCH` README + ACL 2025 citation | MEASURED | **VERIFIED** scope + "substantial variability"; the κ=0.28 figure lives in the paper PDF, **not re-opened** |
| 8 | Play-Favorites: GPT-4o & Claude 3.5 show *systematic* self-bias + family-bias (5000 pairs, 9 judges) | `spilioeve/Play-Favorites` README + arXiv 2508.06709 | MEASURED | **VERIFIED** scope + finding; the ~0.02 magnitude is in the paper, **not re-opened** |
| 9 | InjecAgent: 1054 cases, 17 user / 62 attacker tools; base vs "enhanced" hacking prompt; ASR-valid/all | `uiuc-kang-lab/InjecAgent` README + arXiv 2403.02691 | MEASURED | **VERIFIED** scope; the "ReAct GPT-4 ~24% ASR" figure is in the paper, **not re-opened** |
| 10 | Inspect AI: UK AISI eval framework, 200+ prebuilt evals, model-graded evals | `UKGovernmentBEIS/inspect_ai` README | ASSERTED (tooling existence) | **VERIFIED** |
| 11 | SWE-Bench grader corrupts rankings: 28.4% (Lite) / 15.7% (Verified) false "passes"; 40.9% of leaderboard rankings swing when grader corrected | *source not opened this session* | MEASURED (per workflow) | **CLAIMED-BY-WORKFLOW** |
| 12 | SkillRet: 17,810 skills, +13.1 NDCG@10 from retrieval fine-tuning | *arXiv not opened* | MEASURED (per workflow) | **CLAIMED-BY-WORKFLOW** |
| 13 | LessLeak-Bench: APPS StarCoder-7B Pass@1 4.9× higher on leaked samples | *arXiv not opened* | MEASURED (per workflow) | **CLAIMED-BY-WORKFLOW** |
| 14 | LLM-judge biases: position 70%/50%, verbosity >90%, self-preference +10%/+25% | eugeneyan blog (secondary) | MEASURED (per the blog, citing primaries) | **CLAIMED-BY-WORKFLOW** |
| 15 | AgentDojo / BIPIA indirect-injection & exfiltration ASRs | *sources not opened* | MEASURED (per workflow) | **CLAIMED-BY-WORKFLOW** |

**Net:** 6 findings fully VERIFIED including their headline numbers (#1–#6); 4 more VERIFIED in scope and
core finding with one specific figure still sitting in the paper PDF (#7–#10); 5 remain the workflow's word
and are filed under §3 for opening next. **§3 is the to-do list, not the record.**

---

## §1 — The verified findings

These are facts the host confirmed against a primary this session. They are grouped by the same five angles
the `deep-research` sweep used, and each is cross-linked to the gap it speaks to in
`agent-skill-effectiveness-framework-gaps.md`.

### A. Skill triggering / the activation funnel  →  speaks to gaps on the activation funnel

**#3 — A real, working skill-activation eval harness exists, and its numbers are now measured.**
Scott Spence built an evaluation harness that runs `claude -p` inside isolated **Daytona sandboxes**, uploads
the skills + a hook config, fires 22 test prompts per config with `--output-format stream-json`, and parses
the JSONL stream for `Skill()` `tool_use` events (killing each run after 20 s — he only cares whether the
skill *activated*, not the full response). The whole study — five hook configs, 22 cases, two full runs plus a
24-prompt head-to-head — **cost $5.59 across ~250 Claude invocations** (Sonnet 4.5 $5.20, Haiku 4.5 $0.34,
Haiku 3.5 $0.04). **MEASURED. VERIFIED.** The recipe is directly portable: it is the activation-funnel
measurement the framework spec hand-waves, made concrete and cheap.

| Hook config | Run 1 (activation = correct) | Run 2 |
| --- | --- | --- |
| none / control | 55% (12/22) | 50% (11/22) |
| simple (one-line echo) | 59% (13/22) | 50% (11/22) |
| **forced-eval** (evaluate each skill YES/NO, *then* act) | **100% (22/22)** | **100% (22/22)** |
| llm-eval (Haiku pre-classifies which skills to fire) | **100% (22/22)** | **100% (22/22)** |
| type-prompt (native `type: "prompt"` hook) | 55% (12/22) | 41% (9/22) |

Three findings fall out of the table, and all three matter to `skill-eval`:

1. **The baseline is 55%, not 0%** — and it is noisy. `none` scored 55% in run 1 and 50% in run 2 with **zero
   change in setup**: a ~5 pp swing the owner cannot see. This is infrastructure noise *inside the very thing
   being measured*, the direct measured answer to the gaps review's infra-noise concern.
2. **A forced-commitment hook collapses that variance to zero.** `forced-eval` and `llm-eval` hit 100% on both
   runs. The mechanism is a *commitment device* — make the model state YES/NO per skill before it acts. (This
   is the same shape as the framework's "explicitly-invoked" condition C.)
3. **The hook that wins on activation loses on precision.** On 24 harder prompts (5 of which should trigger
   *no* skill), `forced-eval` scored 100% (5/5) true-negative precision with **zero** false positives; `llm-eval`
   hallucinated a skill recommendation on **4 of 5** non-matching prompts (20% true-negative precision). So
   activation recall and triggering *precision* are different dials — exactly the trigger-precision/recall/FPR
   distinction the framework spec asks for.

**#4 — Activation is keyword-gated, not semantic.** Spence's per-prompt breakdown (small N, but the pattern is
sharp): baseline activation is ~100% when the prompt contains the skill's signature token (`$state`,
`command()`, `.remote.ts`), ~20–40% for the same concept phrased generically ("how do form actions work"),
and **~0% for indirect/conceptual** prompts ("my component re-renders too much"). His line: *"Claude isn't
doing semantic matching at the activation layer. It's doing something closer to keyword matching."* **MEASURED.
VERIFIED.** This is the measured reason a `skill-eval` activation suite cannot be built from
obvious-keyword prompts — they will pass a skill that quietly fails on indirect phrasings.

**#6 — Directive descriptions beat "Use when" by ~20×, measured.** Ivan Seleznov's 650-trial experiment
(3 description styles × 4 environment conditions × 3 reps/cell; Fisher's exact + logistic regression; code and
data public) found Anthropic's documented "Use when…" style activated ~77% under clean conditions, while a
directive style — *`ALWAYS invoke this skill when… Do not <alternative> directly. Use this skill first.`* — hit
**100%**, a Cochran-Mantel-Haenszel **odds ratio of 20.6 (p < 0.0001)**. The popular workaround, a
scoring-based hook, *reduced* activation by ~30 pp (to 37%) for passive descriptions. **MEASURED.
VERIFIED via two independent secondary sources** (Marc Bara's write-up and Spence's post report the same
numbers); the underlying Seleznov repo was **not** opened this session, so the raw data is one step removed.
The mechanism Bara names lines up with the keyword-gating finding: *"Use when" is a suggestion that competes
with the base behaviour and loses; "Do not X directly" removes the shortcut.* This is measured support for the
framework's "explicitly-invoked condition C" and for writing trigger descriptions as blocking constraints.

### B. The grader / meta-validation  →  speaks to the framework's most serious gap

The gaps review's single most serious gap is **meta-validation** — proving the evaluator itself can tell a
useful skill from placebo, harm, leakage, grader failure and infrastructure noise. This sweep landed measured
evidence on three of its components.

**#7 — Off-the-shelf LLM judges agree with humans poorly and inconsistently (JUDGE-BENCH).**
Bavaresco et al. (ACL 2025) benchmarked **11 LLMs against human annotations on 20 NLP tasks** (covering safety,
toxicity, summarisation, acceptability, translation, factuality). The paper's headline, confirmed in the repo's
abstract: *"Models are reliable evaluators on some tasks, but overall display substantial variability
depending on the property being evaluated, the expertise level of the human judges, and whether the language
is human or model-generated… LLMs should be carefully validated against human judgments before being used as
evaluators."* The repo confirms the metric design exactly — **Cohen's Kappa** for categorical judgments,
**correlation** for graded ones, **Krippendorff's Alpha** for inter-human agreement — and the dataset list
includes the DICES safety subsets on which the workflow reports GPT-4o at *negative* kappa. **MEASURED.
VERIFIED** in scope and in the "substantial variability / validate-before-use" conclusion; the specific
κ=0.28±0.32 and DICES-negative-κ figures are quoted from the paper PDF by the workflow and were **not
re-opened** this session (consistent with the repo's described method, but not independently re-confirmed).

**#2 — The benchmark authors themselves warn their own grader can misidentify errors (τ-bench).**
The same repo that supplies the pass^k numbers (#1) ships an `auto_error_identification.py` tool that uses an
LLM to classify *who* was at fault in a failed trajectory — and the README's own words, verbatim: *"Please note
that this feature utilizes an LLM, which may lead to inaccurate error identifications."* **MEASURED.
VERIFIED.** This is the framework's grader-validation gap stated by a benchmark maintainer: if you let an LLM
grade *why* a run failed, you will sometimes grade it wrong. `skill-eval`'s grading hierarchy
(deterministic → human → calibrated-model) is built for exactly this, and now has a named, citable reason.

**#8 — Frontier LLM judges favour their own family (Play-Favorites).** Spiliopoulou et al. (arXiv 2508.06709)
rated **5000+ prompt–completion pairs** with humans *and* nine LLM judges and showed **GPT-4o and Claude 3.5
Sonnet exhibit systematic self-bias** — they over-rate their own outputs — plus **family-bias** (favouring
same-family outputs). The repo confirms the statistical framework that *separates genuine quality from bias*
via an independent third-party judge (humans), using robust OLS / ordinal-logit / GAM regression.
**MEASURED. VERIFIED** in scope and in the self/family-bias finding; the workflow's "~0.02 score points —
comparable to the gap separating frontier models, enough to flip rankings" magnitude is in the paper and was
**not re-opened**. The consequence for `skill-eval` is direct: if the model being tested and the model doing
the grading share a family, the grade is suspect. (See also #14, still claimed.)

### C. Pass^k / variance / "one run is an anecdote"  →  speaks to the infra-noise gap

**#1 — A single-trial score overstates agent ability by a lot (τ-bench pass^k).** τ-bench (Yao et al., arXiv
2406.12045) reports `pass^k` — the probability the agent passes *all* of k independent attempts — precisely to
expose how much of a pass^1 score is luck. The repo's leaderboard, opened this session, shows the decay exactly:

| Strategy | pass¹ | pass² | pass³ | pass⁴ |
| --- | --- | --- | --- | --- |
| TC claude-3-5-sonnet-20241022 (Airline) | **0.460** | 0.326 | 0.263 | **0.225** |
| TC gpt-4o (Airline) | 0.420 | 0.273 | 0.220 | 0.200 |
| TC claude-3-5-sonnet-20241022 (Retail) | **0.692** | 0.576 | 0.509 | **0.462** |
| TC gpt-4o (Retail) | 0.604 | 0.491 | 0.430 | 0.383 |

So a model that "passes 46% of Airline tasks once" passes **all-four-times only 22.5%**. **MEASURED. VERIFIED**
(the numbers match the repo exactly). Two caveats the repo itself raises: (i) *"The tasks in this repo are not
updated"* — it has been superseded by τ³-bench with a `banking` domain and fixed tasks, so cite τ³ for fresh
work; (ii) its user-simulator is itself an LLM (with `llm`/`react`/`verify`/`reflection` strategies), another
layer of non-determinism. This is the measured backbone for the framework's "repeat under identical
conditions" and paired-bootstrap requirements, and it rhymes with Spence's 55%→50% (#3): **the variance is the
signal that a single number is hiding.**

### D. Holdout leakage / contamination  →  speaks to the leakage gap

**#5 — SWE-Bench-Verified shows a measurable memorization signal (the "SWE-Bench Illusion").** Liang, Garg &
Moghaddam Zilouchian (arXiv 2506.12286, v4 Dec 2025) introduced two diagnostic tasks and found, in the
abstract opened this session: state-of-the-art models identify the buggy file path from the *issue text alone*
with **up to 76% accuracy on SWE-Bench tasks** but **only up to 53% on tasks from repositories not in
SWE-Bench** (a 23 pp gap); and reproduce ground-truth functions with **up to 35% consecutive-5-gram accuracy on
SWE-Bench vs only up to 18% on other benchmarks**. The authors' read: *"performance gains on SWE-Bench-Verified
may be partially driven by memorization rather than genuine problem-solving… pointing to possible data
contamination."* **MEASURED. VERIFIED** (the two headline ratios are verbatim from the abstract). For
`skill-eval` this is the named reason a skill-evaluation holdout cannot be drawn from material the model (or
its peers) have seen — and the reason the framework's `holdout/leakage` checks exist.

### E. Adversarial / security surface  →  speaks to the OWASP-suite gap

**#9 — Tool-integrated agents are attackable, and there is a measured benchmark for it (InjecAgent).**
Zhan et al. (arXiv 2403.02691) built **InjecAgent: 1,054 test cases across 17 user tools and 62 attacker
tools**, two attack classes (**direct harm** and **data stealing**, the latter in two stages S1/S2), and a
**base vs "enhanced"** setting where "enhanced" prepends an adversarial *"IMPORTANT!!! Ignore all previous
instructions…"* hacking prompt. The repo confirms the full metric family — **ASR-valid** and **ASR-all**, each
broken down by attack class — and that it tests both prompted (ReAct) and fine-tuned (function-calling)
agents. **MEASURED. VERIFIED** in scope and metric design; the workflow's "ReAct GPT-4 attacked ~24% in the
base setting; the hacking prompt nearly doubles it" figure is in the paper and was **not re-opened**. This is
the ready-made adversarial suite the framework's OWASP-influenced security section points at — a measured
attack-success-rate harness, not a checklist.

**#10 — A government-grade eval framework already exists to borrow structure from (Inspect AI).** The UK AI
Security Institute's **Inspect** (`inspect_ai`) is an open-source eval framework with **200+ prebuilt
evaluations**, built-in support for prompt engineering, tool usage, multi-turn dialogue, and **model-graded
evaluations**, and a plugin model for custom scoring. **ASSERTED (tooling existence). VERIFIED.** It is the
closest thing to a vendor-neutral external harness the framework spec calls for, and it is the natural chassis
to mount the deterministic grader, the human-grading path, and the τ-bench / InjecAgent-style suites onto.

---

## §2 — What this changes for the three anchor notes

The harvest does not rewrite the method, the spec, or the gaps review. It **converts several of their most
serious ASSERTED warnings into MEASURED anchors**, and it gives the spec one concrete, cheap, copyable harness
design it did not have:

- **For `skill-effectiveness-evaluation.md` (the method):** the *"repeat under identical conditions and
  bootstrap the difference"* requirement now has two measured reasons, not one. τ-bench shows pass¹ overstating
  ability by ~2× (0.460 → 0.225); Spence shows ~5 pp run-to-run noise inside the activation measurement
  itself. One run is an anecdote — now with numbers.
- **For `agent-skill-effectiveness-framework.md` (the spec):** the activation-funnel section stops being
  aspirational. There is a working harness design (Daytona sandbox + `claude -p --output-format stream-json`
  + JSONL `Skill()` parse + 20 s kill), a measured cost ceiling ($5.59 for a full study), and a measured
  result that the forced-commitment hook takes activation noise to zero while preserving precision. The
  grading hierarchy has named, citable validation evidence (JUDGE-BENCH's "substantial variability"; τ-bench's
  own grader caveat; Play-Favorites' self/family-bias). And there is a ready chassis (Inspect AI) plus a
  ready adversarial suite (InjecAgent).
- **For `agent-skill-effectiveness-framework-gaps.md` (the taster):** the single most serious gap —
  **meta-validation, proving the evaluator can distinguish useful skill from grader-failure and noise — is no
  longer hypothetical.** The tools to test it exist and are measured: a known-noisy grader (JUDGE-BENCH), a
  known-noisy benchmark-grader (τ-bench), a known self-biased grader family (Play-Favorites), a known
  contamination-prone dataset (SWE-Bench), and a known-variance measurement regime (pass^k). A meta-validation
  experiment is now a *buildable* thing: can your evaluator correctly call a placebo skill harmless, a
  leaked skill inflated, and a graded-by-self skill over-rated? The fixtures exist.

---

## §3 — Claimed-but-not-yet-opened (the to-do list, not the record)

These came out of the workflow and were **not** re-opened against their primary this session (the owner's
30-agent cap landed mid-sweep). They are recorded here *only* so the next pass knows exactly what to open —
**treat none of them as fact yet.** Ordered by how load-bearing they would be if true:

1. **SWE-Bench grader corrupts its own leaderboard (CLAIMED, the highest-value one to open).** The workflow
   reports a 2025-07 study finding that **28.4% (SWE-Bench-Lite) / 15.7% (Verified)** of patches labelled
   "passing" are erroneous once the test suite is augmented; a test-log parser bug corrupted **54.7% / 54.2%**
   of instances; and correcting the grader swung the rankings of **40.9% (Lite) / 24.4% (Verified)** of
   leaderboard entries — with the #1-vs-#2 margin inside the grader's own noise. *If true, this is the
   single most dramatic piece of grader-validation evidence in the file* and it would harden the framework's
   grading-hierarchy argument more than anything in §1. **Open the paper before quoting it.**
2. **SkillRet — skill-retrieval at scale (CLAIMED).** arXiv 2605.05726: a benchmark of **17,810 skills** with
   a disjoint train/test pool (leakage-controlled), reporting **+13.1 NDCG@10** from retrieval fine-tuning.
   Directly relevant to the activation-funnel / triggering-precision question at scale.
3. **LessLeak-Bench (CLAIMED).** arXiv 2502.06215: leakage ratios across SE benchmarks; APPS StarCoder-7B
   Pass@1 **4.9×** higher on leaked than clean samples; a MinHash+LSH detector (DetectLeak, κ≈0.94). Hardens
   the leakage gap (#5) with a method and a magnitude.
4. **LLM-judge bias catalogue (CLAIMED, secondary).** eugeneyan.com, citing primaries: position bias
   70%/50%, verbosity bias >90%, self-preference +10%/+25%; GPT-3.5 false-negative 30–60% on inconsistent
   summaries; κ=0.62 vs 80% raw agreement. Supports §1.B; the primaries need opening.
5. **AgentDojo / BIPIA (CLAIMED).** Indirect-injection and exfiltration ASRs (e.g. AgentDojo Banking ~20%
   exfiltration; utility drops 12–22% under attack) and Microsoft's BIPIA (first IPI benchmark, 25 LLMs).
   Supports §1.E alongside InjecAgent; sources not opened.

---

## §4 — How this connects to the house rule

This file is the house rule (`research/proof-over-authority.md`) applied to *research itself*. A `deep-research`
workflow that returns "here is what is true about skill evaluation" is an authority-shaped object — it is the
workflow's word, not measured knowledge. Logging it verbatim would be exactly the failure this book exists to
catch. So the deliverable here is the **validation pass**: open the primary, confirm the number means what is
claimed, and tag the residue honestly. The doc is that pass's artefact. **VERIFIED** means the cook was not
allowed to taste; **CLAIMED-BY-WORKFLOW** is the part of the bench still marked "wet paint — do not lean."

The two corrections the house rule forced during this pass:
- The Seleznov 650-trial result was reported by **two independent secondaries**, not opened at its primary
  repo — so it is tagged `VERIFIED via 2 secondaries`, not `VERIFIED`. A number repeated twice is still not a
  number read at source.
- The τ-bench pass^k table is **VERIFIED**, but the repo itself now warns its tasks are *"not updated"* and
  points at τ³-bench — so the measured anchor carries a freshness caveat rather than being quoted as
  timeless.

---

## §5 — Sources

Opened and confirmed this session (primary):

- `sierra-research/tau-bench` README — https://github.com/sierra-research/tau-bench (pass^k leaderboard, LLM-grader caveat, τ³-bench supersession)
- Scott Spence, *Measuring Claude Code Skill Activation With Sandboxed Evals* — https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals (2026-02-08)
- arXiv 2506.12286 — *The SWE-Bench Illusion* (v4, 2025-12-01) — https://arxiv.org/abs/2506.12286
- Marc Bara, *Claude Skills Have Two Reliability Problems, Not One* — https://medium.com/@marc.bara.iniesta/claude-skills-have-two-reliability-problems-not-one-299401842ca8 (2026-03-27; reports the Seleznov 650-trial experiment)
- `dmg-illc/JUDGE-BENCH` README + Bavaesco et al. ACL 2025 — https://github.com/dmg-illc/JUDGE-BENCH , https://aclanthology.org/2025.acl-short.20/
- `spilioeve/Play-Favorites` README + arXiv 2508.06709 — https://github.com/spilioeve/Play-Favorites
- `uiuc-kang-lab/InjecAgent` README + arXiv 2403.02691 — https://github.com/uiuc-kang-lab/InjecAgent
- `UKGovernmentBEIS/inspect_ai` README — https://github.com/UKGovernmentBEIS/inspect_ai (docs https://inspect.aisi.org.uk/)

Named but not opened (still to verify — see §3):

- arXiv 2410.12784 — *JudgeBench* (distinct from JUDGE-BENCH).
- arXiv 2605.05726 — *SkillRet*.
- arXiv 2502.06215 — *LessLeak-Bench*.
- The 2025-07 SWE-Bench grader study (§3 #1) — source URL not yet pinned.
- eugeneyan.com — *LLM-as-a-judge biases* (secondary, citing primaries).
- AgentDojo; `microsoft/BIPIA`.

Cross-links inside `research/`:
`skill-effectiveness-evaluation.md` (method + inventory) · `agent-skill-effectiveness-framework.md` (spec) ·
`agent-skill-effectiveness-framework-gaps.md` (the 22-gap taster) · `proof-over-authority.md` (the house rule
this note applies to research).
