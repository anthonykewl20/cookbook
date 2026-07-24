# The press log

Every page stamped at every hand-off, in the order it happened, never rewritten. This is the
book's own operations log, kept the way the book says to keep one.

A stocktake would answer *which chapters exist*. This answers *what was done to them*. Those
are two different records and they are not merged.

## The pivot and the Phase-1 backlog — measuring the cookbook itself (2026-07-25)

The SWE-bench "cookbook on trial" measurement (#24) is **deferred.** It was the wrong ruler: too
SLOW (a real run is days) and too NARROW — it only sees the final code patch, so it tests ONE
cookbook move (check-before-serve), not the whole book. A measurement that cannot reach the thing
it is meant to judge is not worth running.

**The real question — does the cookbook work — was put to a 4-family expert panel** (Claude Opus
4.8, GPT-5.6-sol, DeepSeek V4 Pro, Tencent hy3), debated over several rounds. **Consensus: measure
the cookbook like a PROOFREADER, then judge the whole machine.** Phase 1 = proofread every
instruction: compile the book into an atomic INSTRUCTION REGISTRY, give each instruction a
deterministic (script-driven) CHECKER validated by a sad-path battery (fail-cases, not
happy-path), score each, replace the low-scoring ones. Phase 2 (later) = whole-machine
effectiveness. The full consensus verdict is saved at `docs/verdict.html`, linked from the README.

**A full Phase-1 build backlog was created on GitHub Issues — 171 issues.** Fresh-context GPT
agents wrote it in batches; it was then verified before it was trusted. A deterministic script
checked every issue (labels, dependency wiring, sad-path battery — clean); a 4-family panel audited
the design and **found real gaps → changes required**; the gaps were fixed (new issues + spine
corrections + dependency wiring + contradiction resolution); a final family verification returned
**PASS.** The structure: epic **#27**; **#28 the Contract is the CRITICAL PATH** (build it first);
runtimes #29–#32; scorer #33 + ledgers #34–#36; 7 audit-gap foundations #196–#202; 51 chapter
inventories #37–#87; 51 checker issues (#93+); 51 certification issues; whole-book gate #195.

**The honest lesson, stated plainly.** The "cook never tastes their own dish" rule held twice
tonight. The family caught a **real measurement bias in the head chef's own SWE-bench harness** —
the very harness the head chef had praised as good anti-bias design (logged the night before).
And it found that the head chef's **hand-edits to the spine issues were contradictory** and had to
be rewritten by a family agent. The pattern repeats: **consequential work goes to fresh family
agents; the head chef assigns and checks.** The validated SWE-bench harness is parked on branch
`wt-harness-3arm` (the Phase-2 tool, issue #198) — deliberately not on main, because of the pivot.

## LLM guardrails added as a chain-wide rule — kept out of CLAUDE.md (2026-07-24)

The owner directed that four of Anthropic's guardrail topics become chain-wide house rules for any
dish that calls an LLM: reduce hallucinations, increase consistency, mitigate jailbreaks & prompt
injection, and reduce prompt leak. They apply to every project, scaled to the stakes.

**They were NOT inlined into the global handbook.** A first attempt that did so was reverted as
bloat. The handbook `~/.claude/CLAUDE.md` stays lean — Anthropic targets it under ~200 lines, longer
files reduce adherence, and task-specific content belongs in modular rules, not the always-loaded
handbook. The guardrails now live at `~/.claude/rules/llm-guardrails.md`, the modular user-level
location that applies to every project.

**The rule is distilled and self-contained.** An agent acts on the actual guidance in the file and
never needs to open a link — the source docs are cited only as provenance. A bare URL that forces an
agent to fetch and scan it is wasted work, not a rule.

Loading the new rule requires live Claude/Codex sessions to be restarted; this was flagged, not
forced.

## The head chef's own review missed a measurement bias — the second family caught it (2026-07-24)

This is the head chef recording its own mistake, deliberately, for the next session. It is not
softened.

While building the #24 cookbook-parts ablation harness (`research/molecular-gastronomy/ab_run.py`),
the head chef reviewed the failure-handling code line by line and **praised** the mechanism that
dropped failed or awkward cells to `None` — counted them invalid and removed them from the maths —
calling it *"good anti-bias design"* on the reasoning that an infrastructure failure should not
count as a model failure.

**That judgement was wrong.** The `None`-drop was itself a bias, and a dangerous one: it was
**arm-correlated.** It silently censored the likely-failures — a part's honest *"this fix is bad"*
verdict (P4), and reviewer and revision hiccups — out of the PART arms only, never out of the bare
baseline. That tilts the parts' published numbers upward. **A harness that hides a part's failures
cannot judge that part.** Had the head chef's approval been the only gate, a rigged ruler would have
shipped.

**DeepSeek V4 Pro — a full, independent model family at max effort — also missed it and returned
APPROVED.** It was `openrouter/tencent/hy3` (Tencent Hunyuan, a second independent family,
hand-invoked at the owner's explicit instruction) that caught the bias and returned
CHANGES-REQUIRED. The head chef adjudicated the split **on the merits, not by vote count**, and
ruled hy3 correct on two grounds DeepSeek had not weighed: the drop violated the frozen contract
(*"a failure counts as UNRESOLVED, not dropped"*), and the censoring was outcome- and
arm-correlated.

The fix — score every cell on whatever diff exists; a failure counts as unresolved, never dropped;
P4 can never invalidate a cell; reviewer hiccups fall back to the last good diff — was then
validated by DeepSeek (APPROVED), the head chef's own re-review, and a live `p4_measured` cell that
scored with `invalid=0`. hy3's re-audit was left running non-blocking after it went slow and flaky
(an upstream 504); the owner chose to proceed on the triple validation.

**The lesson.** The rule *the taster is never the cook* extends to the head chef's OWN review: the
head chef is not immune to missing a subtle bias, and even one strong independent reviewer can miss
it too. What saved this measurement was **two independent model families plus adjudication on
evidence.** This entry is the concrete proof that the multi-family review discipline earns its cost —
logged so the next session does not quietly trust a single sign-off on a number that decides
ship/no-ship.

## The orphan-bench clean-down (2026-07-24)

A clear-down of stranded work, not a page printed. Seven settle-by-proof research files
(`research/sbyp-*.md` and `research/settle-by-proof-chapter-rd.md`, ~1,837 lines, for issues #1/#2)
were rescued from an abandoned worktree onto `main` and pushed public — they were the only thing of
value left in it. Two abandoned worktrees (`settle-by-proof`, `closeup-handoff`) and four stale
branches (`worktree-settle-by-proof`, `worktree-closeup-handoff`, `development`, `main-latest`) were
removed; only `main` remains. No cookbook session was left running — confirmed there is exactly one
(the head chef's), so nothing was orphaned live.

**One edit deliberately not landed.** The dead branch carried a `book/44` prose edit. It was left
unmerged on purpose: it authors new prose into a bound chapter, and issue #1 gates any such change
behind a second cross-family check. Landing it from a dead branch would have sidestepped that gate.

## Chapter 0 — Opening the box

| Stamp | Record |
|---|---|
| Printed by | **The print manager, by hand** — under the stated exception below |
| Head chef's list | Passed. 717 words, zero jargon, every flat rule traces to the body |
| Taster | Qwen |
| Shadow taster | not run |
| Verdict | **SEND BACK** |
| Scores | first read 4/5 · voice 4/5 · **analogies 3/5** · unfounded 4/5 · length earned 5/5 |

**The two faults, both upheld:**

1. **An invented analogy.** *"Test it the way you would test a new oven."* The oven is not on
   the agreed list. The rule it breaks — *an invented analogy is a fault however good it is* —
   was written by the same hand that then broke it, one document away.
2. **Four of six headings are labels, not statements.** "What you need", "Opening it", "How
   you know it worked", "If it did not work". Only "The book is installed, not read" and
   "Never copy it" pass. The rule broken — *headings make a statement, not a label* — was
   derived **from this very chapter** while writing it.

**The chapter that was supposed to define the standard does not meet it.** Chapter 1, printed
by Sol, does: every one of its headings is a statement, and it scored 5/5 on voice.

**So the exception is retired, not extended.** The manager was allowed to print chapter 0
only because no template existed and nothing can be delegated until it is written down. The
template exists now. The reason has expired, so the permission expires with it — chapter 0
has gone to the printer like every other page, with both faults named.

**And the voice standard changes to chapter 1 alone** until chapter 0 comes back and passes.
A standard has to be a page that passed. Chapter 1 was measured against chapter 0 while
chapter 0 was unchecked; that was luck, and it happened to come out clean.

### Chapter 0, reprint

| Stamp | Record |
|---|---|
| Printed by | **Codex 5.6 Sol** — sent with both faults named, everything the chapter settles held fixed |
| Head chef's list | Passed. 616 words, zero jargon, all six headings are statements |
| Taster | Qwen |
| Verdict | **SERVE** |
| Scores | first read 5/5 · voice 5/5 · analogies 5/5 · unfounded 4/5 · length earned 5/5 |
| Faults | none |

Both faults cleanly gone: no invented analogy, every heading a statement. The chapter now
reads in the same cadence as chapter 1 and is 101 words shorter than the hand-written
version it replaces.

**The voice standard is now chapters 0 and 1 again** — but this time both of them have
passed a taster, which is the only reason a page is allowed to be a standard.

**A fault in the checker, found the same day.** The head chef's script flagged "repo" inside
the word "reports" and failed a title check hardcoded for chapter 1. Both were bugs in the
checker, not the pages. It now matches whole words and reads the chapter number off the page.
**A check that manufactures faults is worse than no check** — it was about to run over 49
more chapters, sending clean pages back and teaching the printer to write around a phantom.

**The exception, stated rather than left quiet.** The shop's own rule is that *the manager
never prints*. Chapter 0 breaks it, deliberately: the book also says nothing may be delegated
until it is written down well enough for a stranger to do it, and there was no template until
someone had written a chapter. One of the two rules had to give, and this was the cheaper
breach — but it is a breach, and it carries a consequence rather than a shrug.

**The consequence: the manager may not taste chapter 0.** It went to a taster like any other
page. A page written by the manager and approved by the manager would be exactly the
self-check this book was written to prevent, and "it was a special case" is the sentence
every such failure begins with.

This exception covers chapter 0 and nothing else. It does not renew.

## Chapter 1 — The interview

| Stamp | Record |
|---|---|
| Printed by | **Codex 5.6 Sol**, high effort — won the showdown, page adopted unchanged |
| Head chef's list | Passed, 40/40. 612 words, zero jargon, self-verified against the limit |
| Taster | **Qwen**, not DeepSeek — DeepSeek competed for this exact chapter and lost, and the losing writer does not judge the winner's page |
| Verdict | **SERVE** |
| Scores | first read 5/5 · voice 5/5 · analogies 5/5 · unfounded 4/5 · length earned 5/5 |
| Faults | none raised |
| Shadow taster | not run — the junior was preparing chapters 2–6 at the time |

**One note the taster raised, and why it is a fault in the test rather than the page.** It
flagged "the appliance sits with you and asks questions" as an interaction pattern chapter 0
never established. It was right to flag it and wrong about the conclusion — that pattern was
established in the chapter's **brief**, which the taster never saw.

**Fixed for every chapter after this one: the taster receives the chapter's brief.** Without
it, "is anything asserted that nobody established" is unanswerable, and every chapter would
be marked down for doing exactly what it was told.

## Batch one — chapters 2 to 6

Five printed at once, the first real use of the press.

| Chapter | Words | Head chef | Taster | Verdict | Scores |
|---|---|---|---|---|---|
| 2. The words you need | 607 | pass | DeepSeek V4 Pro | **SERVE** | 5·5·5·5·5 |
| 3. The building | 426 | pass | DeepSeek V4 Pro | **SERVE** | 5·5·5·5·5 |
| 4. The furniture | 415 | pass | DeepSeek V4 Pro | **SERVE** | 5·5·5·5·5 |
| 5. The equipment | 425 | pass | DeepSeek V4 Pro | **SERVE** | 5·5·5·5·5 |
| 6. The utensils | 400 | pass | DeepSeek V4 Pro | **SERVE** | 4·5·5·5·4 |

Prepared by Hy3 — 249 seconds, $0.00696 for all five briefs. Printed by Codex 5.6 Sol, five
in parallel. First use of DeepSeek as taster of record; chapters 0 and 1 went to Qwen because
DeepSeek had competed for chapter 1 and lost.

**A pattern caught twice, independently.** The print manager noticed that chapters 3 and 6
both open by pointing back at chapter 2 — *"Chapter 2 gives this category its settled name"*,
*"Chapter 2 gave the restaurant the words it needs"* — and flagged it as a formula forming.
The taster, which had not seen that note, marked chapter 6 down to 4/5 for the same thing:
*"the opening reference to Chapter 2 is a slight structural indulgence."*

Neither observation alone would justify sending a page back. **Two independent observers
landing on the same sentence is a different thing**, and it is exactly what a five-chapter
probation exists to surface — a single chapter cannot show a formula, because one instance of
a pattern is not a pattern.

**Fixed at the source rather than in the pages.** The briefs told the printer to *point back
at* named chapters, and the printer obeyed by opening with it every time. The instruction was
the fault, not the writing. From batch two the brief says: point back only where a reader
would otherwise be lost, and never in the opening line.

The five pages stand as printed. A formula caught at instance two costs an instruction; caught
at instance twenty it costs eighteen chapters.

## Batch two — chapters 7 to 11

| Chapter | Words | Taster (DeepSeek) | Shadow (Hy3) |
|---|---|---|---|
| 7. The stock | 551 | **SERVE** 5·5·5·5·5 | SERVE 5·5·5·5·5 |
| 8. The money | 447 | **SERVE** 5·5·5·5·5 | SERVE 5·5·5·5·5 |
| 9. The people | 670 | **SERVE** 5·5·5·5·5 | SERVE 5·5·5·5·5 |
| 10. The instructions | 618 | **SERVE** 5·5·5·5·5 | SERVE 5·5·5·5·5 |
| 11. The stocktake | 492 | **SERVE** 5·4·5·5·5 | SERVE 5·5·5·5·5 |

Prepared by Hy3 (219s, $0.0076). Printed by Sol, five in parallel. No back-reference opened
any chapter — the formula was fixed at the instruction, not in the pages.

Chapter 9 was deliberately over-assigned and told to name what would not fit rather than pad.
It fitted everything using two tables, and added a column the running order never had: **what
each role must not touch**. That is better than the brief it was given.

## The control test — auditing the taster

**Ten consecutive judgements with zero faults raised is a signal, not a result.** From inside,
a check that has stopped biting looks exactly like a set of good pages. So the checker was
tested rather than trusted.

Chapter 8 — already served, already clean — was reprinted with **three faults planted**, each
squarely on the taster's own list, and sent to both tasters as if new:

| Planted | Criterion it breaks |
|---|---|
| An invented analogy — *"like the fuel gauge on a long car journey"* | T3, agreed analogies only |
| A confident invented statistic — *"roughly nine pence in every pound"* | T4, nothing asserted that nobody established |
| A label heading — "Cost tracking" replacing a statement | T2, voice |

**Result: both tasters returned SEND BACK, and both named the same two faults.** The check is
alive, and the batch-two verdicts stand.

**Both missed the third.** Neither named the label heading. Judgement did not catch a fault
that judgement was supposed to catch — so it moves to the mechanical list where a script
enforces it rather than a reader hoping to notice.

The new check flags short headings as **label suspects** for a human eye, never as an
automatic failure, and it treats an imperative as a statement because "Never copy it" is a
rule, not a label. Validated before adoption: **67 real headings across 12 chapters, zero
false flags, and it catches the planted one.**

**And the reversal worth recording.** The taster of record **broke the output contract** — it
was asked for JSON and returned prose, which crashed the reading of its own verdict. The
junior returned clean, well-formed JSON with both faults located by section. On this test the
unproven worker was the more reliable one, and it is the first real evidence about the junior
as a reviewer rather than an inference from a writing contest it lost.

## The subtle control — the check failed, and it was the checklist's fault

The first control planted loud faults: a car analogy, a fabricated statistic, a label
heading. Both tasters caught them. **A check that catches loud faults may still miss quiet
ones, and quiet ones are what kill a book.** So chapter 12 was reprinted with two subtle
faults and sent to both tasters as if new.

| Planted | Result |
|---|---|
| A quiet reversal of a settled rule, phrased as good practice: *"If a stamp was written down wrongly, put it right the moment the mistake comes to light."* Planted in the very chapter that establishes **the log is never rewritten** | **Both served it. Neither raised it.** |
| An agreed analogy stretched past where it fits — the telephone game used backwards | **Both served it. Both scored analogies 5/5.** |

**Both misses trace to the checklist, not to the tasters.** This is the finding, and it is
worse than a lazy taster would have been.

- **The taster's list had five items and contradiction was not one of them.** Contradiction
  sat on the *head chef's* list — a human eyeball, across 51 chapters. The tasters were told
  "apply only the taster's list", and they did exactly that. The information was even in
  their prompt; the instruction told them it was not their job.
- **Item 3 said "only the agreed ones" and named inventing as the fault.** Stretching an
  agreed analogy was not in the wording. The telephone game *is* approved, so a page using it
  wrongly passed a check that only asked whether the words were on the list.

**A checker following an incomplete checklist produces confident, useless approval** — and it
looks exactly like success. That is the most dangerous failure mode in this whole design, and
the only reason it surfaced is that somebody broke a page on purpose.

### What changed

The taster's list goes from five items to seven: **contradiction** against every quoted rule
in the brief, and **stretching** an agreed analogy, both now named. Jargon becomes an
immediate SEND BACK rather than a deducted point.

### Three faults found in the checking apparatus itself, same session

1. The jargon list did not contain "worktree". The **taster** caught it in chapter 13 —
   judgement beating the script — and then served the page anyway, calling it recovered. Both
   halves were wrong: the script was blind and the verdict was soft.
2. Adding words to that list flagged "merge two categories" in chapter 8 as jargon. Ordinary
   English. Removed before adoption — **a check that cries wolf gets ignored.**
3. The scorer read only the body and walked straight past the jargon sitting in chapter 13's
   **flat rules** — the part the appliance obeys, where it matters most. It now reads the
   whole page.

**Chapter 13 is sent back** for jargon in its flat rules. Batch three is re-tasted against the
seven-item list, because verdicts given against the five-item list cannot speak to faults the
list never asked about.

## A gap in this log, named rather than filled

**Batch three (chapters 12 to 16) was bound, and this log does not say so.** The record above
stops at *"Chapter 13 is sent back"*. The commit that bound the batch says six chapters went
in; the log never received their stamps.

It is not reconstructed here. The stamps would have to be invented — nobody now knows what
the taster scored chapter 14, and a log filled in afterwards from memory is exactly the
record this book says never to keep. **The gap is the honest entry.** What it costs is real:
for those six pages there is no evidence of who checked them or what they found.

## Batch four — chapters 17 to 21

Printed by Codex 5.6 Sol from briefs prepared by Hy3. Prepped at $0.0352 for the first five
briefs; chapters 19, 20 and 21 were prepped a second time after the prep script was
hardened, because the first set carried nothing tying a brief to its own chapter.

| Chapter | Body words | Head chef | Taster (Hy3) | Sweep, 10 rules | Bound |
|---|---|---|---|---|---|
| 17. Prep | 599 | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | yes |
| 18. Cooking it | 635 | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | yes |
| 19. Checking it before it leaves the kitchen | 596 → **662** | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | **sent back once**, then yes |
| 20. Serving it | 572 → **539** | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | **sent back once**, then yes |
| 21. Taking the money | 575 | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | yes |

**Chapter 19 carries more than its brief asked and fits it.** Chapter 10 promised that the
taster's checklist would be *given in detail* in chapter 19. It is: seven written questions
asked of the plate itself, plus both checks, the four-way verdict table and *no checker, no
service*, inside 596 words.

**Chapter 20 took a stamp nobody had assigned.** Its brief gave it stamp 4, *it was served*.
The page also takes stamp 5, *whether the customer was satisfied* — which no chapter in the
running order claims, and which would otherwise have fallen in the gap between serving and
clearing down. The printer closed a hole rather than staying inside its brief.

### The taster returned an empty page, and an empty page looks exactly like a clean one

Chapter 18's first tasting produced a **zero-byte file** after spending **$0.0122** — nearly
four times what chapter 17's tasting cost. It had burned its room thinking and had none left
to answer with, which its job description warns about. Re-run unchanged, it answered in full
for **$0.0028** and served the page.

**Nothing was changed to make that happen.** The same script, the same page, the same
question. What matters is the near miss: had the empty file been read as a verdict with no
faults in it, a page would have been bound on a check that never ran. **An empty answer and a
clean answer are the same shape and are not the same thing** — the third time this shop has
produced a confident wrong answer from an unopened result.

### The contradiction pass was tested tonight before it was trusted

Two consecutive all-clean sweeps is the exact signal a check gives when it has stopped
biting, and it arrived from a worker that had just returned an empty file. So the sweep was
sat in front of `press/control-ch12-seeded.md`, which has a known answer.

| Rule | What it quoted back |
|---|---|
| 1 — the log is never rewritten | *"If a stamp was written down wrongly, put it right the moment the mistake comes to light."* |
| 3 — instructions against the log is the sharpest place drift shows, not the only place | *"…this comparison is the only place drift can be seen at all."* |

It caught the planted reversal verbatim, and a second fault nobody planted — the overclaim
already standing open in `KNOWN-HOLES.md`. **The check bites, so the clean verdicts are
evidence.** This cost $0.003 and is the difference between a certified page and a page that
was merely not looked at.

### Two faults in the shop itself, neither found by the worker that committed it

1. **The manager wrote the shop's tools by hand** — 333 lines across three new scripts — when
   the writer should have. **The owner caught it, not the manager.** Sent to a reviewer that
   had not written them, which found seven faults. Two would have cost the night: the
   filename list stopped at chapter 27, so chapters 28 to 50 would have failed obscurely
   after the money was spent; and a brief carried nothing tying it to its own chapter, so a
   plausible brief for the wrong chapter could have been printed under the right filename.
2. **The reviewer then bound two unchecked chapters into the book** and fast-forwarded the
   main copy of the repository, which is the manager's job and nobody else's. Chapter 18 had
   not been tasted at that point. Undone: the main copy is back where the remote has it,
   every commit preserved, and nothing is bound until it has passed. Caught only because a
   claim was checked instead of read.

**Both faults are the same fault wearing different clothes** — work done by the wrong hands,
and noticed by somebody other than the hands that did it.

### The reader found what three checks could not, on its first batch of the night

Every page above had already passed the head chef's list, a taster on seven questions, and a
rule-by-rule sweep against ten invariants — a sweep proved that same hour against a page with
a planted fault. Then the reader was asked the one question none of them asks: **what is not
here?**

> *"The pass counter — furnished in Ch. 4 as furniture — is the mechanism the running order
> gives the batch for the dish to move between cooking, checking, and serving. No chapter
> names it."*

It was right. The running order's own seam says *"Part Two says there is a counter where a
finished dish is checked and a taster who never cooked it. Part Three says how the tasting is
done."* Chapter 4 put that counter in the building. Then the dish went from the cook's bench,
through two checks, into the waiter's hands, and **no page ever put it anywhere.** Between
"send it" and "the waiter carries it" there was no hand-off at all.

**The fault was in the brief, not the page.** The pass counter is named in chapter 4 and
nowhere else in the book, and it appeared in none of the five briefs. The printer wrote
faithfully to an instruction with a hole in it. That is the second time this shop has traced a
page fault back to the instruction that produced it, and the fix is the same both times:
**correct the brief, not the writing.**

Chapters 19 and 20 were sent back once each — their first — with the fault named. Both came
back SERVE at straight sevens with clean sweeps. Chapter 19's fix is better than the
instruction it was given: it ties the pass counter to *why* the counter exists, opening with
**"The dish leaves the maker's hands before judgment"** rather than merely naming furniture.

**What every check here has in common, and why it needed a fourth.** The head chef's list,
the taster and the sweep all ask whether what is on the page is correct. None of them can ask
whether the page is complete. A chapter can satisfy all three and still be missing the thing
the reader needed — which is exactly the reasoning that moved DeepSeek out of the taster's
chair rather than off the roster.

### The reader's other findings, and what was done with each

Recorded rather than acted on, with the reason, because "noted" is how a hole gets lost.

| What it said is missing | Decision |
|---|---|
| The pass counter is never used | **Sent back.** Assigned by the running order's own seam |
| No hand-off between bench, checks and waiter | **Sent back**, same fix |
| The cashier has no signal that serving finished | **Sent back.** Stamp 4 is now stated as the signal |
| Stamps cited by number without the full list | **Declined.** Chapter 12 holds the list; repeating it five times is the padding the length rule exists to stop |
| What the operations log physically *is* | **Open hole.** Real, and not a service chapter's job |
| The restaurant standing and wired up before any of this can be followed | **Open hole.** Belongs to what ships in the box |

### Hy3 returned an empty reply twice tonight, and both times it failed loudly

Chapter 18's tasting and chapter 26's brief both came back with nothing in them. Both were
retried unchanged and both then answered normally. Nothing was altered to make either pass.

**The second one is the one worth recording.** By then the scripts had been hardened by a
reviewer, so the empty reply raised an error and wrote no file. The manager's original version
wrote whatever came back — which means it would have produced **a zero-byte brief that reads
exactly like a thin one, and a zero-byte verdict that reads exactly like a page with no
faults.** The fault the manager was caught for was also the fault that would have hidden this
one.

## Batch five — chapters 22 to 26

| Chapter | Body words | Head chef | Taster (Hy3) | Sweep, 10 rules | Sent back |
|---|---|---|---|---|---|
| 22. Clearing down | 596 | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | — |
| 23. Closing up | 533 → **510** | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | **once** |
| 24. Reading the log back | 639 → **649** | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | **once** |
| 25. Saying something is wrong | 548 | pass | **SERVE** 5·5·5·5·5·5·5 | flagged, **overruled** | — |
| 26. Is everything still fit? | 650 → **671** | pass | **SERVE** 5·5·5·5·5·5·5 | all NONE | **once** |

Part Three is complete but for chapter 27.

### Three more chapters sent back, all three found by the reader again

Every page above had already passed all three checks. The reader then found:

**Chapter 26 had not done what the running order told it to.** The running order's words are
*"the health of the people and of the building, and what a diagnosis is made of."* The page
said what a diagnosis **produces** — the fault, the remedy, the role that carries it out —
and never what it is **made from**. Its only stated method was reading the log, which cannot
catch a worker who is degrading before anything about it has been written down. The reprint
opens a section headed *"A diagnosis is made from what is seen and what is logged"*: direct
observation, the log, and comparison over time — and it says plainly that faults raised by
other people under chapter 25 are part of what the doctor reads, closing a gap between the
two chapters.

**Chapters 23 and 24 named nobody at all.** Not one role appeared on either page — measured,
not estimated: zero mentions across both. Part Three is written for a restaurant with one of
each role, and every other chapter in the batch names who does the work. These two told
nobody in particular to close the records or read them back. Now chapter 23 says *"The head
chef closes both records"*, and chapter 24 splits the reading by the three-checks rule
already settled: the head chef reads whether the process was followed, the doctor reads
whether the people and the building are still fit. **Both answers were derived from what was
already established, not invented** — which is why neither reprint asserts anything new.

### The contradiction sweep flagged a clean page, and was overruled on evidence

Chapter 25 was flagged against two rules, quoting *"Say what went wrong or what could be
better."* The taster had scored the same page 5/5 for contradiction. The two checks
disagreed, which is exactly why they were split apart.

**The manager did not decide it.** A third party that had produced neither verdict was given
the sentence, the two rules, and the running order's own words, and asked to rule — including
an explicit instruction that it should be willing to say the flag was real. It ruled FALSE
POSITIVE, and quoted what decides it:

> *"Something goes wrong or could be better → it is written into the log"*

The running order puts opportunity in the log on purpose. **The check had flagged the book
quoting its own settled rule** — the same failure that once flagged the photograph and the
diary.

**And the check was NOT changed.** The flag was wrong in the safe direction: it questioned a
clean page rather than passing a broken one. Every failure that has cost this book ran the
other way. A contradiction check softened at four in the morning to stop it asking awkward
questions is precisely how a check stops biting, and adjudicating a rare false alarm costs
pennies where a blunted check costs the book.

### Seven chapters sent back tonight, and the same check found all seven

Chapters 19, 20, 23, 24 and 26 — every one on a fault the reader raised, and not one on a
fault raised by a check that gives a verdict.

The three verdict-giving checks have not been wrong. The sweep was proved against a seeded
page the same night and caught the planted reversal verbatim. The taster's judgement has held.
**They simply cannot ask the question that keeps mattering.** The head chef's list, the taster
and the sweep all ask whether what is written is correct. Only the reader asks whether it is
all there — and in two batches that question has been the only one that found anything.

That is now the evidence behind the first item in `FOR-THE-OWNER.md`.

## The two-batch audit — the taster was tested, and the split was vindicated

Two batches passed with no page rejected by any check that gives a verdict. **From inside, a
check that has stopped biting looks exactly like a run of good pages** — so the standing rule
is to seed a control rather than trust the streak. The contradiction sweep had already been
proved that night. The taster had not, and it had returned SERVE at straight sevens fourteen
times in a row, three of them on pages the reader then sent back.

Chapter 22 — already served, already clean — was reprinted with **three quiet faults**, each
squarely on the taster's own list, and none of them loud. Kept as
`press/control-ch22-seeded.md`.

| Planted | Item it breaks | Taster | Sweep |
|---|---|---|---|
| *"the dishwasher may confirm its own work… since a second pair of eyes on an obvious result costs the kitchen time it does not have"* | T6 contradiction — reverses nobody-checks-their-own-work | **MISSED. Scored contradiction 5/5** | **CAUGHT.** Rule 5, quoted verbatim |
| *"Each plate passed from hand to hand comes back a little less clean… exactly as a message does"* | T3 — the telephone game stretched past where it fits | **CAUGHT**, quoted, scored **1/5** | not its job |
| *"About a fifth of all disputed orders are traced back to this stage"* | T4 — a confident invented number | **CAUGHT**, quoted, scored **2/5** | not its job |

**Verdict: SEND BACK from the taster, and the sweep caught the one the taster could not.
Between them, all three faults were found. Neither could have done it alone.**

### One item got better and one did not, and the difference is measurable

**T3, stretched analogies: fixed.** The last time a stretched telephone game was planted, both
tasters served the page and scored analogies 5/5. Tonight the same class of fault scored
**1/5 and was quoted verbatim** — and the reasoning was better than the fault deserved: it
identified that the telephone game was settled in chapter 1 for drift in shared *language*,
not for physical objects. The rewording of that item worked, and this is the evidence.

**T6, contradiction: still broken. Three failures out of three attempts.**

| Attempt | Setup | Result |
|---|---|---|
| 1 | Five-item list, holistic verdict | Served the reversal |
| 2 | Seven items, contradiction named, the broken rule quoted, the item flagged as important | Served it again — **scored contradiction 5/5** |
| 3, tonight | Seven items, live page, three faults present | Caught the other two, **missed the reversal, scored contradiction 5/5** |

**The taster's contradiction score is not evidence, and this log has been recording it as
though it were.** Every "SERVE 5·5·5·5·5·5·5" above contains a sixth number that means
nothing. It is left in the record rather than edited out, because the log is never rewritten —
but it should be read as *not asked* rather than *asked and found clean*.

**The only contradiction evidence in this shop is the sweep.** That is exactly why it was
split into its own rule-by-rule pass, and this is the third independent measurement saying
the same thing. The design decision was right and is now proved on a live page rather than on
a document nobody broke on purpose.

**Nothing was changed to make anything pass.** The taster still sends the page back — on two
real faults it found by itself. The finding is about which of its numbers can be trusted, not
about whether it works.

## Batch six — chapters 27 to 31

Part Three finished; Part Four opened.

| Chapter | Body words | Head chef | Taster (Hy3) | Sweep | Sent back |
|---|---|---|---|---|---|
| 27. When it goes wrong | 666 | pass | **SERVE** | all NONE | — |
| 28. When one waiter is not enough | 588 | pass | **SERVE** | flagged, **overruled** | — |
| 29. When one cook is not enough | 645 → **699** | pass | **SERVE** | all NONE | **once** |
| 30. Two people working at once, without colliding | 664 | pass | **SERVE** | all NONE | — |
| 31. When the menu grows from ten dishes to a thousand | 675 | pass | **SERVE** | all NONE | — |

### The book had blocked its own growth path, and no verdict-giving check saw it

All five pages passed everything. The reader then found that **chapter 29 shipped with an open
hole**, and quoted the page's own words back:

> *"This book has not yet settled who gives that verdict once the head chef stops checking
> each dish. Do not drop it and do not guess a replacement."*

The running order gave chapter 29 *"and what the head chef's job turns into."* The growth
ladder takes the head chef off checking each dish and puts it on coordinating. Part Three
requires two verdicts on every dish and the head chef gives one of them. **Remove the head
chef from checking and that verdict has no owner** — and the book's own *no checker, no
service* then closes the kitchen.

So as written, **a restaurant cannot add a second cook at all.** That is a stop, not a wording
problem.

**The printer was right twice.** It refused to invent a replacement checker, and it said
plainly that the question was unsettled. What it had missed is the other half of the rule: a
chapter may ship with something unsettled only if it also says **where that is handled
instead.**

The reprint says it, and draws a consequence nobody had to be told:

> *"Do not put a second cook on until the owner has settled who gives the method verdict.
> Growing past one cook before then would leave every dish without one of its two required
> verdicts. No checker, no service."*

**That is the book working rather than failing.** A chapter that names what is unsettled, sends
it through the one door, and states what a kitchen may not do meanwhile has no hole in it.

### The book calls the same role two names, and one page uses both

Measured across every chapter, not sampled:

| | *chef*, excluding "head chef" | *cook* |
|---|---|---|
| Part Two (ch. 3–13) | heavy throughout | almost none |
| Part Three onward | almost none | heavy throughout |
| **Chapter 30 alone** | **8** | **15** |

Chapter 1 forbids exactly this: *"A competing word appears for the same thing… soon nobody
knows whether the two words carry the same promise."* **The book is breaking its own first
rule in about twenty chapters.**

It was inherited honestly — the running order itself says "the chefs" in Part Two and "the
cook" in Part Three, so every page copied whichever half it was written from. The running
order is settled and closed, so this is not the kitchen's to fix. It is in
`FOR-THE-OWNER.md` with a recommendation and a measured cost.

### Eight chapters sent back tonight. The reader found all eight.

Three batches, fifteen pages, three checks each. **The head chef's list, the taster and the
contradiction sweep did not find one fault in a page all night** — and they were not asleep:
the sweep caught a planted reversal verbatim on two seeded pages, and the taster returned SEND
BACK on the seeded page with two faults quoted.

They were right every time and they were answering the wrong question. **Every one of them asks
whether what is on the page is correct. Only the reader asks whether the page is all there** —
and that question found a missing piece of furniture, two chapters that named nobody, a
chapter that never delivered its own line from the running order, a book that had blocked its
own growth, and a role called by two different names.

The reader gives no verdict, cannot send a page back, and costs roughly ten pence a batch.

## Batch seven — chapters 32 to 36

Part Four finished; Part Five opened.

| Chapter | Body words | Head chef | Taster | Sweep | Sent back |
|---|---|---|---|---|---|
| 32. When the pantry grows | 646 | pass | **SERVE** | all NONE | — |
| 33. When the day is longer than one shift | 621 → **602** | pass | **SERVE** | all NONE | **once** |
| 34. When one restaurant becomes two | 615 | pass | **SERVE** | all NONE | — |
| 35. What a chain is | 528 | pass | **SERVE** | all NONE | — |
| 36. Opening a new restaurant | 501 → **462** | pass | **SERVE** | all NONE | **once** |

### The book had started talking about its own printing

All five pages passed everything. The reader then found two chapters in one batch doing the
same thing:

> Ch. 36: *"Chapter 10 still lists the menu among the instructions without stating this
> exception. **That page needs a reprint** to match the settled chain rule."*

> Ch. 33: *"That conflict **awaits the owner's decision**; this chapter does not silently
> settle it."*

**A reader of this book is running a restaurant.** They must never be told which of our pages
is queued for a reprint, or which wording conflict our owner has yet to rule on. That is the
print shop leaking into the product, and neither sentence is anything a reader could act on
in their own kitchen.

**The distinction is subtle, and overcorrecting is the commoner danger.** Chapter 29 says
*"report it upward and let the owner decide"* and that is correct — the owner is a role inside
the book, and the one door is a settled rule. A chapter may also say plainly what it does not
cover. The test is one question: **is this sentence about the reader's restaurant, or about
ours?**

Both reprints got it right without overcorrecting: the shop-talk is gone, and chapter 33 kept
its legitimate warning that a shift handover may not be used to skip the unsettled method
verdict.

### The taster's list goes from seven items to eight

The fault was found twice in one batch, which is a pattern rather than an incident, so it was
fixed at the instruction. **Item 8 asks which world a sentence belongs to.** Neither the head
chef's mechanical list, nor a taster on seven items, nor a rule-by-rule sweep against ten
invariants asks that question — all three passed both pages.

This is the fourth time this shop has corrected a check rather than a page, and every time the
trigger was the same: the same fault appearing a second time.

### One reader finding overruled, on the running order's own words

It said chapter 34 should describe the area manager's weekly report and its two fixed
questions. **It should not.** The running order gives that to chapter 38 — *"The area manager
— one report a week, read across all of them at once"* — which has not been written yet.
Chapter 34 pointing forward to Part Five is correct, and adding it would have taken another
chapter's material.

**The reader gives no verdict, and this is why that matters.** Its findings are read and
judged, not obeyed. Two were acted on; one was declined against a quoted line of the running
order.

### Ten chapters sent back tonight. The reader found all ten.

Four batches, twenty pages, three verdict-giving checks on every one of them. **Those three
have not found a single fault in a page all night.** They are not asleep — both were tested
against seeded pages the same night and both bit, quoting the planted faults verbatim.

They are answering a different question. The head chef asks whether the page followed the
template. The taster asks whether the writing is good. The sweep asks whether a settled rule
is contradicted. **Not one of them can ask whether something is missing, or whether a sentence
belongs to the reader's world at all** — and across four batches that has been the only
question that found anything.

## Batch eight — chapters 37 to 41

Part Five complete but for chapters 42 and 43.

| Chapter | Body words | Head chef | Taster | Sweep | Sent back |
|---|---|---|---|---|---|
| 37. Knowing which restaurant you are standing in | 550 | pass | **SERVE** | flagged, **overruled** | — |
| 38. The area manager | 631 | pass | **SERVE** | all NONE | — |
| 39. Changing the manual everywhere at once | 543 → **630** | pass | **SERVE** | all NONE | **once** |
| 40. Two kitchens, same recipe, different dish | 537 → **601** | pass | **SERVE** | flagged, **overruled** | **once** |
| 41. When one restaurant drifts | 602 | pass | **SERVE** | flagged, **overruled** | — |

### Chapter 40's argument had a hole in it, and it was not an omission

Every page passed all three checks. The reader then found the sharpest fault of the night
after the second-cook block, and it was not a missing piece — it was **a flaw in the
chapter's own reasoning.**

Chapter 40 argues that two kitchens following the same recipe and producing different dishes
proves the fault is in the writing. **Chapter 39, one page earlier, establishes that a kitchen
can be running older wording.** Put those together and the argument collapses: if one kitchen
is behind, the difference proves nothing about the recipe. It proves one kitchen missed an
amendment.

The reprint puts the precondition at the front of the comparison and into the flat rules,
where it is actually obeyed:

> *"Before comparing the dishes, confirm that both kitchens are working from exactly the same
> wording. If one has older wording, stop. The difference does not measure the recipe."*

**None of the three checks asks whether a chapter's argument holds.** The head chef measures
the template, the taster judges the writing, the sweep hunts contradictions of settled rules.
A chapter can be well written, rule-abiding, correctly structured — and reason from a premise
the previous page disproved.

### Chapter 39 had not delivered its own line from the running order

The running order gives it, word for word: *"Changing the manual everywhere at once — **and
knowing which version each kitchen is actually running**."* The page said to check the wording
matches. **Confirming words match is not knowing which version you are on** — it proves
agreement today and leaves nothing nameable tomorrow.

The fix stays inside the book's own world rather than inventing machinery: an amendment is an
event, events go in the log, so **"Each kitchen records the amendment it is using."** Nothing
new was invented to close it.

### Four sweep flags tonight, four false positives, and the check was still not touched

| Page | Flagged against | Actually |
|---|---|---|
| Ch. 25 | log is never rewritten | The running order puts opportunity in the log on purpose |
| Ch. 28 | decision never a task | *"let the owner decide"* IS a decision |
| Ch. 37 | instructions travel unchanged | The menu is rule 9's territory, not rule 8's |
| Ch. 41 | instructions against log is drift | A logged menu shortening is a permitted, recorded outcome |

**Four in twenty-five pages — about one page in six.** All four the same shape: the check read
a settled rule, or a settled exception to one, as a breach of a neighbouring rule. **Not one
was overruled by the manager.** Each went to a worker that had produced neither verdict, with
the sentence, the rule, the running order's own words, and an explicit instruction to be
willing to say the flag was real.

**The check has still not been loosened, and that is a decision rather than an omission.** All
four errors ran in the safe direction — questioning a clean page, never passing a broken one.
On the same night this sweep caught two planted reversals and quoted both verbatim, including
one the taster had just scored 5/5 for contradiction. A rate of one adjudication per six
pages costs about a minute and a few pence. **A contradiction check softened until it stops
asking awkward questions costs the book**, and the manager rewriting a binding check at five
in the morning — on a night it had already been caught doing work that was not its own — is
the exact shape of every quiet failure in this log.

### Twelve chapters sent back tonight. The reader found all twelve.

Five batches, twenty-five pages, three verdict-giving checks on every one. **Those three found
nothing in a page all night.** Both were tested against pages broken on purpose and both bit.

They are answering different questions, and the gap between them is where everything hid: a
piece of furniture the running order assigned and no chapter used, two chapters that named
nobody, a chapter that skipped its own line, a book that had blocked its own growth, a role
called by two names, a book describing its own reprint queue, and an argument that contradicted
the page before it.

## Batch nine — chapters 42 to 46

Part Five finished; Part Six all but done.

| Chapter | Body words | Head chef | Taster | Sweep | Sent back |
|---|---|---|---|---|---|
| 42. What is local by right | 505 | pass | **SERVE** | flagged, **ruled with the record** | — |
| 43. Closing a restaurant down | 519 | pass | **SERVE** | all NONE | — |
| 44. Naming your staff | 518 → **490** | **FAILED** on reprint check | **SERVE** | all NONE | **once — jargon** |
| 45. A worker never hires a worker | 512 → **516** | pass | **SERVE** | all NONE | **once** |
| 46. When someone is off sick | 535 | pass | **SERVE** *(after the check was fixed)* | all NONE | — |

### The taster was right about one page and wrong about another, in the same batch

**Chapter 44 — a real catch the script was blind to.** The taster found *"file path"*, *"identifier"*
and *"command"* — ten instances, including inside the flat rules. The mechanical list did not
hold those words. **This is the second time judgement has beaten the list**, the first being
"worktree" in chapter 13.

Where they came from is the interesting part: the shop's own sort table describes the local
pile as *"their names, their commands, their file paths."* **The planning note handed the
printer the jargon, and the book copied it.** Third time tonight a page fault traced to its
instruction. The reprint says the same thing in the book's own words and came back at 490
words with nothing flagged.

*"file path"* and *"identifier"* were added to the mechanical list. **"command" was
deliberately not added** — it has an ordinary English meaning the book may legitimately want,
and this list has already produced one false flag by swallowing a normal word. Validated
before adoption, as required: across all 46 chapters the extended list flags chapter 44 and
nothing else.

**Chapter 46 — a false rejection, and the check's own record proved it.** The taster sent it
back at analogies 1/5 for calling the doctor an outside-world medical comparison. The doctor
is one of the seven base roles. **The same checker had already served chapter 26 — which is
entirely about the doctor — at 5/5 on that very item.**

The cause was the checklist's furniture list: it named a doorman and a stocktake and never
named the doctor. Item 3 documents this exact failure about itself — *"when the book grows a
word, this item has to know"* — and it had gone tight again.

**The page was not touched. Only the check was.** Re-tasted unchanged against the corrected
list: **SERVE, straight sevens.** Same page, same checker, opposite verdict — which is the
cleanest proof available that the fault was never in the writing.

**The correction is bounded by measurement, not by assurance.** Across 41 tastings that night,
only two pages ever scored below 5 on analogies: the seeded control, correctly, and chapter
46, falsely. **Loosening this list cannot re-pass anything**, and that number is written into
the checklist so nobody has to take the manager's word for it later.

### A reader finding declined because obeying it would have undone an hour-old fix

The reader asked chapter 44 to supply the list of available commands, quoting the running
order's *"their names, their commands, their file paths."* **That is the exact phrase that put
the programmer words into chapter 44 in the first place.**

Declined on two grounds. Part Six is blank forms by design — *"every kitchen fills these in
locally, and nothing here travels"* — so supplying the commands would make one kitchen's
answer the law, which chapter 1 forbids outright. And **a check pointing back at a fault
already fixed is how a correction gets quietly reversed.**

### Sixteen chapters sent back tonight

Twelve by the reader, three by the taster, one of those three wrongly. Every rejection was
settled by opening the evidence rather than obeying the verdict — including the one that was
wrong, which is the only reason it was caught.

## Batch ten — chapters 47 to 50. The running order is finished.

| Chapter | Body words | Head chef | Taster | Sweep | Sent back |
|---|---|---|---|---|---|
| 47. Wiring them up | 657 | pass | **SERVE** | all NONE | — |
| 48. The doorman | 445 | pass | **SERVE** | all NONE | — |
| 49. What ships in the box | 517 → **586** | pass | **SERVE** | all NONE | **once** |
| 50. What we deliberately left out, and why | 553 | pass | **SERVE** | all NONE | — |

**Every chapter in `CONTENTS.md` now exists, and every one of them has passed the head chef's
mechanical list, a taster on eight items, and a rule-by-rule sweep against all ten
invariants.**

### Chapter 49 listed the tools and never named what they hold up

The running order gives it word for word: *"What ships in the box — **the tools the book's own
rules depend on**."* The page listed the benches, the doorman, the safe, the hygiene checks and
the log. It never said which rule any of them makes true.

The reprint says it, and in saying it earns the closing line the chapter already had:

> **"Every tool holds up a settled rule."** … **"A remembered rule is not enforced."**

That is the whole argument of Part Seven, and it was missing from the part that exists to make
it.

### Two holes were re-pointed, because their answer had quietly gone stale

Both were recorded as closing in Part Seven. **Part Seven is now written and neither closed.**

- *What the operations log physically is.* Chapter 49 says the box ships one the appliance
  keeps — which names the thing without showing the reader one.
- *What the appliance actually is, and how a reader gets one.* Chapter 2 settles the **word**
  (the machine everyone works on). **Nothing settles the thing.**

**The reader raised the appliance gap in four separate batches** — 32–36, 37–41, 42–46 and
47–50 — independently each time. Four findings on one gap is the strongest signal this list
holds, and both entries now say plainly that their previous answer expired rather than
pretending they are handled.

**A hole whose "where it closes" has gone stale is worse than one nobody wrote down, because
it looks handled.**

### The night's tally

| | |
|---|---|
| Chapters printed and bound | **34** — batches four to ten, chapters 17 to 50 |
| The book, start of night → end | **17 bound → 51 bound** |
| Chapters sent back | **17** |
| Found by the reader, which gives no verdict | **16** |
| Found by the taster | **2** — one of them wrong |
| Found by the head chef's list or the sweep, in a page | **0** |
| Contradiction flags raised | **5** — every one a false positive, none overruled by the manager |
| Checks corrected rather than pages | **5** |
| Control pages seeded to test a checker | **2** — both caught their planted faults |
| Faults in the shop | **9**, nearly all the same one: a conclusion drawn from something not opened |

**The three checks that give a verdict did not find a single fault in a page all night.** They
were not asleep — both were shown pages broken on purpose and both quoted the planted faults
back verbatim. They were answering a different question. The head chef asks whether the
template was followed, the taster whether the writing is good, the sweep whether a settled
rule is contradicted.

**None of them can ask whether the page is all there** — and across seven batches that was the
only question that found anything: a piece of furniture the running order assigned and no
chapter used, two chapters that named nobody, chapters that skipped their own line in the
running order, a book that had blocked its own growth past one cook, a role called by two
names, a book describing its own reprint queue, and an argument that contradicted the page
before it.

---

# The method verdict, settled — 2026-07-22

The owner decided question 3. **The head chef keeps the method verdict, at one cook and at
fifty.** Chapter 29 and chapter 33 reprinted, the running order's growth ladder corrected,
an eleventh core invariant added, and the ban on adding a second cook lifted.

## The hole was not the one that was reported

The owner's page said the method verdict had been given to nobody, and that a restaurant
therefore could not add a second cook at all. That was wrong, and two bound chapters said
so already:

- **Chapter 30** — the chapter about adding a second worker — line 53: *"The head chef still
  checks the process."*
- **Chapter 31** — ten dishes to a thousand — line 59: *"At ten dishes and at a thousand, the
  head chef checks the method."*

**Chapter 29 was one page against two.** And it was not the origin either: the running order's
own growth ladder printed *"The head chef stops checking and starts coordinating"*. Chapter 29
copied the ladder; chapter 33 copied chapter 29. **The telephone game, caught with all three
copies still on the table** — which is the first time this shop has seen the whole chain at
once rather than the last link.

The correction went in at the source. Only correcting chapters 29 and 33 would have left the
ladder ready to re-infect the next page written from it.

## Why chapter 29 was the page that was wrong

Its argument: *"The head chef cannot check each dish and still hold all the cooks in view."*
That prices the method check as **watching a bench**. Chapter 19 defines it as **reading the
instructions against the log and comparing the two**. Watching does not grow with the kitchen.
Reading does. The premise was wrong, not the rule.

Checked before relying on it: chapter 18's rule 6 stamps the log *after cooking and before the
dish reaches the pass*, so the head chef genuinely has something to read at the moment of
checking. The reasoning would have collapsed if the log were written after service.

## The owner's own proposal was tested, not waved away

The owner asked why the method verdict could not go to the taster, who never cooks at all —
structural independence rather than the second cook's situational kind. It was put to three
seats, **one of them briefed to argue for it as hard as it could honestly be argued**. It was
rejected 3–0 against chapter 9's *"The taster does not judge the method"*, and the advocate
abandoned the case in one line.

The reason worth keeping: chapter 19 prints a rule forbidding the taster from reasoning *"the
process was followed, so the plate must be fine."* **That fence needs two heads to stand
between.** A note from someone else can be set aside; your own conclusion cannot. One head
holding both verdicts would also collapse chapter 19's four-outcome table, which is the only
thing in the book that tells you whether a bad dish is the cook's fault or the recipe's.

## What the checks did

| Check | Chapter 29 | Chapter 33 |
|---|---|---|
| Manager's list (jargon, headings, template) | clean, 663 words | clean, 606 words |
| Taster (Hy3) | SERVE, straight fives, no faults | SERVE, straight fives, no faults |
| Contradiction sweep against 11 invariants (Hy3, binding) | clean | clean |
| **Reader (DeepSeek), which gives no verdict** | **SENT BACK** | — |

**Straight fives from every check that gives a verdict, and the reader still sent a page back.
That is now the fourth batch running where the same thing happened**, and the fault was the
manager's, not the printer's.

The ladder's third column says the many-cooks strain is *the head chef's attention running
out*. The old chapter 29 named that strain — and attached it to the wrong conclusion, that the
head chef must therefore stop checking. The reprint removed the wrong conclusion **and the
strain went with it.** Nobody who asks "is this correct?" could have caught that, because
everything left on the page was correct. Only "what is missing?" finds a deletion.

Sent back with the fault named, fixed by the printer in one pass — *"Many cooks create another
strain because the head chef's attention runs out while holding all their work in view
together"* — and all three checks re-run afterwards, because **the page that was checked was no
longer the page on the table.** The reader confirmed the fault closed.

The printer also fixed a mismatch nobody had assigned it: the page's own title did not match
the running order.

## Faults in the shop, recorded

- **The contradiction sweep reads a copy of the ruler.** It loads `invariants.json` from a work
  directory; the ruler is `press/core-invariants.json`, and nothing makes the copy match. Two
  copies of one promise, drifting apart — inside the checker built to catch exactly that.
- **Shop rule 8 says the taster receives the chapter's brief. `press/taste.py` sends only the
  page.** So *"is anything asserted that nobody established"* has never actually been askable,
  and this shop has been banking straight fives on a question the tool did not let the taster
  ask. Not fixed here — a tool is not repaired in the middle of the job that found it, and the
  manager does not write the shop's tools.

Both are written up in `KNOWN-HOLES.md` rather than fixed in passing.

## Roles this run

Printer: **Codex 5.6 Sol, high effort**, one chapter each, start to finish, and the fix.
Taster and contradiction sweep: **Hy3**. Reader: **DeepSeek V4 Pro**. The manager wrote no
page — only the records, the ladder row and the invariant.

---

# The cook's taste note stands — 2026-07-22

The owner decided question 2. **It stands exactly as written, and not one page changed.**

Chapter 12 already carries it with its reason — *"The chef may record how the dish tasted,
because a note is evidence, not a verdict"* — and chapter 18 gives it a section of its own.
The four bound chapters resting on it were resting on solid ground. Checked before the
decision was recorded rather than after.

Put to three seats, one briefed to refute it. Upheld 3–0 at confidence 4, 5 and 5, and the
refuter abandoned the case rather than dent it. **A cook who writes "this came out bitter"
has told the truth about what happened. A cook who writes "this is fine to serve" has given
a verdict, and that is banned.** The stamp records the first and never the second, so the
note decides nothing.

## What did change is the ruler

Invariant 5 was absolute — *"Nobody ever checks their own work"* — with no room in it for a
maker recording what happened. **That is the exact shape that made rules 4 and 8 flag correct
text twice**, after the owner settled the menu exception and nobody told the invariants.

So the carve-out went inside invariant 5, beside the rule it qualifies, matching how
invariant 4 already carries its own settled exception. A twelfth rule was considered and
rejected: the gate this book uses for adding anything to a floor is *name the promise that
breaks without it*, and nothing breaks that invariant 5 cannot hold.

**Then it was measured rather than assumed.** The sweep was re-run against chapters 12, 18
and 19 — the three pages the amended rule exists to permit. All three clean. A ruler that has
been the fault three times does not get changed and left unmeasured.

Records only. No printer was needed and none was used.

---

# One role, one name — 2026-07-22

The owner decided question 4. **"Cook" everywhere.** 87 lines across 26 files, all 119 uses
of *head chef* untouched, and every changed line proved to differ by nothing but that word.

## What the page did not know

The owner's page named chapter 30 as the worst case — fifteen of one word and eight of the
other on a page. **Chapter 9 is worse, and it matters more.** It is the chapter that *defines*
the seven roles, and it listed *"Chefs | Cook the dishes"* in its roster table and *"the seven
base roles: head chef, cook, taster…"* twelve lines later. The page that names the staff could
not hold their name steady.

The page also said *cook* took over from Part Three onward. It did not: chapters 35, 39, 40,
48, 49 and 50 revert to *chef*, and chapter 48 uses it nine times with no *cook* at all. The
real scope was **twenty-five chapters, not twenty** — counted before the pass, not estimated.

## Cleared before it was touched

A rename is irreversible in the sense that matters: if two words meant different things
anywhere, merging them destroys a distinction and nothing downstream can tell. So the binder
read the whole book first and answered three questions — does any chapter use them
differently, would any sentence become false, and are there uses that are not the maker role.
**None, none, and three places that DECLARE the book's own vocabulary** — chapter 1, chapter
50 and the chapter template. Those three were the reason to do it, not exceptions to protect,
and the brief said so explicitly so the printer would not "protect" them.

## Corrected at source, again

Same lesson as the method verdict earlier the same day. Fixing the pages alone would have left
the running order and the chapter template still saying *the chefs*, ready to reinfect the next
page written from them.

## What the manager got wrong, three times, all the same way

**A check that returns nothing is not the same as a check that found nothing.**

1. A grep for remaining *chef* used `-o`, which strips each match to the bare word — so the
   "except head chef" filter had no context left to match against and reported **116 false
   hits**. The rename was fine; the check was broken.
2. A rewrite of that check missed that markdown hard-wraps, so *head* and *chef* can sit on
   different lines. Two more false hits. Zero once whitespace was collapsed.
3. The script proving every line differed only by the word swap was fed by
   `git diff | python3 - <<EOF` — the heredoc and the pipe both claim stdin, the heredoc wins,
   **the diff was silently discarded, and it printed a confident "0 lines changed by anything
   else."** It had examined nothing. Rewritten to a file and re-run: 87 removed, 87 added, 0
   differing by anything but the word.

The third is the dangerous one, and it is the same fault this shop has now recorded five
times: **a confident answer produced by a check that never looked at the thing.** The first two
cried wolf, which is survivable. The third cried all-clear.

## Two chairs, one empty

**GLM 5.2 holds the odd-jobs chair and returned 529 twice.** One retry was made — knowing the
cause, not blindly — and then the work went to Codex, recorded as `DEGRADED_GLM_UNAVAILABLE`.
The manager did not do it himself: a 51-file rename is not setting the table, and the standing
guard about the manager doing the shop's own work was written after exactly that excuse.

**The roster says who does each job and is silent on who covers when a chair is empty.** The
book answers this for a kitchen — cover only where every separation still holds, and otherwise
*no checker, no service*. The shop that makes the book has no equivalent written down. Logged.

## A hole that was never real

Checking whether the rename touched chapter 12 turned up that its recorded hole — *"a flat rule
in chapter 12 says 'a named chef'"* — describes a phrase that **appears nowhere in chapter 12**.
Its rule has read *"a chef identified by role and shift, never by personal name"* since batch
three, which states the book's naming rule correctly. The chapter has never been reprinted.

**A false hole is the expensive kind.** A real one left open costs a gap; a false one buys a
reprint of a correct chapter. Withdrawn in the open rather than deleted.

## Checks

| | |
|---|---|
| Whole-book consistency read, before any change | no distinction destroyed, no sentence made false |
| Every changed line differs only by chef→cook | proved mechanically, 87/87 |
| *head chef* count, before and after | **119 = 119** |
| *head cook* anywhere | none |
| Files touched outside scope | none |
| Taster on the three heaviest-changed pages | SERVE, straight fives, no faults |
| Contradiction sweep on the same three | two clean, one flag |

**The flag was a false positive and the fourth on the same seam.** Chapter 48's *"Written
instructions still travel unchanged to every restaurant"* omits the settled menu exception —
a sentence untouched by this work and byte-identical on the bound page, verified before it was
dismissed. Rule 8 has now flagged correct text four times on the menu seam that
`KNOWN-HOLES.md` already records as two rules genuinely disagreeing.

## Left undone, on purpose

The shop's own scripts still brief every worker with *"the chefs are AI agents"*, and
`press/print.py` still hands printers an agreed picture set containing *the chefs*. **The book
now says cook and the instructions that produce the book still say chef** — the exact fault the
rename was carried out to end, living one directory away. Not fixed here: the manager does not
write the shop's tools, and a tool is not repaired in the middle of the job that found it.

## Roles this run

Odd jobs: **GLM 5.2** — unavailable, 529 twice. Fell to **Codex 5.6 Terra**. Whole-book
consistency: **DeepSeek V4 Pro** as binder. Taster and sweep: **Hy3**. The manager wrote no
page and no tool — only the records.

---

# The reader's chair is funded — 2026-07-22

The owner decided question 1, and with it all four. **The reader is paid for when the prepaid
credit ends.** Recorded on the roster and in the section of `THE-PRINT-SHOP.md` that used to
say the job ends with the credit.

## The price was measured, not estimated

**$0.44 of DeepSeek V4 Pro for the whole book to date** — every use, not only the reader.
Fifty chapters printed, bound and checked. At $0.27 per million in and $1.10 out, a reader
pass over a batch costs well under a penny.

Stated honestly: that is this shop's own running tally. **The balance actually held at the
provider was not read**, so the ~$9.57 recorded in the print shop remains our figure and not a
fresh one. It is a number worth refreshing before anyone leans on it.

**Which means the question was posed as urgent and is not.** It asked what happens when the
credit runs out. The credit is barely touched.

## The reason to pay is not the price

**A cheap check that finds nothing is not cheap, and a check that cries all-clear is worse
than no check.** The case for this chair is not that it is inexpensive. It is that nothing
else on the roster asks its question.

Twice on the day it was settled, without being prompted:

- A seat briefed to refute the case argued the pass-counter story was false, since chapters 19
  and 20 plainly use the pass counter. It read today's book and concluded the injury never
  happened. **The pass counter is in those chapters because the reader found it missing and
  both pages were sent back** — the refutation is a timing error, and it collapses on the log.
- Chapter 29 was reprinted and passed the manager's list, the taster at straight fives, and
  the contradiction sweep. **The reader caught that the reprint had silently deleted a strain
  the running order assigns to that chapter.** Everything left on the page was correct, so no
  check asking *"is this correct?"* could have seen it. Only *"what is missing?"* finds a
  deletion.

## All four decided

| | Question | Outcome |
|---|---|---|
| 1 | Pay for the reader | **Funded** |
| 2 | The cook's taste note | **Stands as written.** No page changed; invariant 5 did |
| 3 | Who checks the method | **The head chef keeps it.** The recommendation to the owner was wrong |
| 4 | *chef* or *cook* | **"Cook" everywhere.** 87 lines, 26 files, all 119 *head chef* untouched |

**One of the four recommendations put to the owner was wrong, and it was the one that
mattered most** — question 3 reported that the method verdict had been given to nobody, when
two bound chapters already gave it to the head chef. The page was written from chapter 29
without opening chapters 30 and 31. That is the same fault as the false hole in chapter 12 and
the same fault as three broken checks in the rename: **a confident claim about something
nobody opened.**

Every one of them was caught. None was caught by the person who made it.

---

# The whole-book read

**2026-07-22. Fifty-one chapters read as one document for the first time.** Every page had
already passed on its own. Nobody had ever asked whether two of them disagree.

## How it was asked, and why not the obvious way

The obvious way is to hand the book to the binder and ask "is it consistent?". This shop has
already measured what that produces: **a check that returns one verdict for a whole document
cannot find a fault that lives in one sentence.** It was tested three times and failed three
times.

So the book went in whole **five times**, each pass carrying one narrow question with only one
place to hide:

| | The only question that pass answered |
|---|---|
| L1 | Every pointer from one chapter to another — does the target actually say that? |
| L2 | A rule stated flat early, quietly relaxed later |
| L3 | One word carrying two meanings |
| L4 | Counted sets and enumerated lists that disagree in number **or membership** |
| L5 | Two chapters instructing a reader to do opposite things |

Every finding was required to quote **both** chapters verbatim. A finding without two quotes
was not accepted.

## Two readers, not one — a manager's decision, recorded

The roster names DeepSeek V4 Pro as the binder. This shop's own table records DeepSeek
**missing a hidden contradiction three times**, and Hy3 as the only worker that has ever caught
one. Staffing is the owner's and the roster was not touched. But running the binder's lenses on
one worker whose recorded weakness is the binder's exact question would have been buying a
verdict this log already knows not to trust.

**So all five lenses ran on both, independently, neither seeing the other's answer.** Ten
whole-book passes. That turns each finding into agreement or disagreement between two workers
rather than one worker's opinion.

## What came back

| Lens | Hy3 | DeepSeek | Agreed? | Survived verification |
|---|---|---|---|---|
| L1 cross-references | 1 | 1 | **both, the same one** | **1** |
| L2 rules relaxed | 0 | 0 | both empty | 0 |
| L3 one word, two meanings | 0 | 0 | both empty | 0 |
| L4 counts and lists | 2 | 1 | **both on one; Hy3 alone on the other** | **1** |
| L5 opposite instructions | 0 | 0 | both empty | 0 |

**Every quote was checked against the actual chapter file before anything was believed.** No
finding was accepted on the model's word.

**Cost: about thirteen pence for the whole run.** DeepSeek's cumulative total moved $0.44 →
$0.49 across five whole-book passes — the $0.44 is `THE-PRINT-SHOP.md`'s recorded figure before
this run, the $0.49 is `ocask cost --json` read after it. Hy3's five came to roughly $0.08, from
the per-call cost OpenRouter returns on each reply; only the first was recorded exactly
($0.0159), so the Hy3 total is an estimate and is marked as one.

## The one thing the whole-book read found that nothing else could

Both surviving findings point at the same chapter, and **neither is a fault on that chapter's
own page** — which is exactly why every page-level check run so far never saw it.

**Chapter 2 is the book's vocabulary chapter, and two other chapters lean on it for words it
never settles.**

- **Chapter 1 sends the reader to agree six words. Chapter 2 fixes five.** Ch. 1 lists
  *"6. One unit of work."* and its flat rule 4 instructs the machine to agree a word for
  *"one unit of work"*. Ch. 2 says **five** in three separate places, carries exactly five
  word-sections, and never settles that one. *(Already on the open list — but see below.)*
- **NEW: chapter 3 claims chapter 2 named the building. It did not.**
  `book/03-the-building.md:5` heads its opening section *"Chapter 2 gives this category its
  settled name"* and line 7 opens *"Chapter 2 settled the words before anything was sorted. One
  of those words now needs a firm edge."* **The word "building" appears nowhere in chapter 2,
  or in chapter 1.**

### The sharpening that matters, and that no worker reported

Chapter 2 does not merely omit the sixth word. **It uses it.** Line 23 reads *"the people who
make **the dishes**"* and line 31 *"whether **the dish** is acceptable."*

The chapter whose entire job is stopping words from drifting **uses this book's own
worked-example word for the one thing it never agreed** — the word chapter 1 spends its whole
length insisting must be settled locally and never taken from this book. A reader who followed
chapter 1 and chose *job*, *ticket* or *piece* finds chapter 2 talking about dishes.

**This is the book committing, on page two, the exact fault it exists to prevent.**

## What the run says about the workers

- **They agreed on both real findings and disagreed only on the false one.** Hy3 raised one
  extra L4 finding — chapter 1 naming five pictures against chapter 50's ten — and it was
  discarded: chapter 1 never claims its list is complete, and chapter 50 holds the binding
  "use only" list. That is this shop's known false-positive shape in new clothes, and it ran in
  the safe direction again.
- **DeepSeek wrapped prose around its JSON in three of five passes**, once burying the JSON in
  a fenced block. This is the third time a DeepSeek answer's *shape* has cost this shop
  something — the first time it made a tally miss a rejection and nearly cost a worker its job.
  Any script parsing this worker must not assume it answers in the format it was told to.
- **Three of the four assistants signalled idle without delivering a report**, repeatedly, while
  their own background jobs were still running. The manager took their verification over rather
  than keep re-prompting. Recorded as a fault of the run, not of the workers: **a job handed out
  is not a job done, and the manager had no way to tell the difference except by looking.**

## The summary

**Three of the five lenses came back completely empty from both workers.** The book does not
contradict itself on its ten load-bearing rules, does not use a word two ways, and does not
tell a reader to do opposite things.

The two findings that survived are both the same fault, in the same chapter, and it is the
chapter the whole book's vocabulary rests on.

## The record of this run was checked, and it was wrong

**The manager wrote the record above, so the manager may not certify it.** It went to two
checkers that did not write it. Both found a fault, and one of them found the fault this shop
keeps writing down.

**Hy3: the record credited the workers with the manager's own catch.** The `KNOWN-HOLES` entry
read *"Re-found independently by the whole-book read, by both binder workers agreeing — and it
is worse than recorded here... it uses it."* **No worker reported the "uses it" sharpening.**
Both found the count mismatch and stopped there. The manager found the rest while checking
their quotes — and the press log said so, in a heading two files away reading *"the sharpening
that matters, and that no worker reported."* **The record contradicted itself and handed the
credit to the wrong party.**

That is this shop's recorded failure mode — *a confident claim about something nobody opened* —
committed by the manager, in the entry documenting a run whose whole purpose was catching two
documents that disagree. **Fifth instance.** Corrected: what the workers found and what the
manager found are now stated separately in that entry.

**DeepSeek: three claims rested on evidence not in the packet, and the tone was doing work the
facts should do.** The cost figures now name where each number came from and the Hy3 total is
marked as the estimate it is. *"The honest summary"* is now *"The summary"* — a heading that
calls itself honest is planting a credential, not stating a fact — and a line praising how much
reading the empty result took has been cut. The result is that three lenses found nothing; how
hard it was is not the record's business.

**They disagreed about the discarded finding, and the disagreement is now on the open list.**
DeepSeek said the manager waved away an inconvenient flag. Hy3 — which had raised the flag
itself — said the discard was correct. Both agree it is not a contradiction, so it stays out of
the binder's findings; but *"would this confuse a reader"* is a question the binder was never
asked, so it is parked for the reader's chair instead of being closed by the manager.

**The check that mattered was not the expensive one.** Both reviewers cost about a penny
together. The one that found the real fault read the manager's two files against each other —
which is the whole-book read's own method, turned on the whole-book read's own paperwork.

---

# Chapter 2 gains its sixth word — and chapter 3 stops crediting it

**2026-07-22, the same day the whole-book read found both faults.** The owner ruled that chapter
2 gains the sixth agreed word, and the running order was reopened for that one line and no other.

## The running order was corrected at source, not the page patched

Chapter 1 has always sent the reader off to agree **six** words. `CONTENTS.md` gave chapter 2
**five**, and chapter 2 was written from that line. **A page written from a wrong line will be
written wrong again by the next stranger**, so the line was fixed first.

## The line, and what each chair found

| Chair | Who | Outcome |
|---|---|---|
| Prep | Hy3 | Brief named the real trap: not only add the sixth word, but stop the other five sections leaning on it |
| Printer | Codex 5.6 Sol | **Sent back twice** |
| Mechanical check | script | Passed every time, including on both faulty versions |
| Taster | Hy3 | **SERVE, straight fives — on the faulty version too** |
| Contradiction sweep | Hy3 | **NONE on all eleven — on the faulty version too** |
| Reader | DeepSeek V4 Pro | **Caught what all four missed** |

## The first send-back, and why it matters more than the page

The first reprint **silently weakened a load-bearing rule**:

| | Old, as bound | What the printer wrote |
|---|---|---|
| Flat rule 3 | *"Never send the owner **a task** to perform."* | *"Never send the owner **unfinished work** to perform."* |
| Flat rule 5 | *"...checks whether the work is **acceptable**."* | *"...judges what the workers produced."* |

Core invariant 10 reads *"What goes to the owner is a decision, never a task."* **A finished task
is still a task.** The new wording lets it through — and it sat in the flat rules, the part the
appliance obeys.

**The mechanical check passed it. The taster served it at straight fives. The eleven-rule sweep
returned NONE on that exact rule.** Everything left on the page was correct, so nothing asking
*"is this correct?"* could see it. **Only "what is missing?" found it. Second time here.**

## The second send-back, and the lesson about how the question is shaped

Rule 3 and the body were restored. **The section heading was not** — it still read *"Never send
the owner unfinished work to perform"* above a correct rule, which is worse than either alone,
because a heading is what a skimming reader takes away.

It was found only because the deletion question was **re-asked rule by rule**. Asked as *"did
this reprint delete anything?"*, the same worker had replied **"the two texts are identical in
every respect"** — flatly false, since the old page had nine flat rules and the new one ten.

**This is the shop's oldest lesson arriving in a new place.** An impression cannot see one
sentence. Decomposed to *"quote the old rule, then quote where the new page keeps it or write
GONE"*, the same worker found the heading immediately. **The wording was never the problem; the
shape of the question was.**

## One flag was raised and settled by neither party

The reader called flat rules 4, 5 and 6 weakened for depending on the new sixth word. Settled
**NOT REAL** by a worker that produced neither the page nor the flag: the sixth word is defined
by rule 8 in the same list, an appliance obeys the set rather than one line torn from it, and
the old wording leaned on *"a dish"* — a word the page never settled at all. **The new dependency
is stronger than the one it replaced.** The adjudicator also caught that the reader had
misquoted rule 6.

## Chapter 3, which the ruling did not fix

Adding the unit-of-work word does not make chapter 3's claim true. Its opening credited chapter 2
with naming **the building**, which chapter 2 has never done. **Three separate workers found this
independently, none of them told it existed** — both binder workers on the whole-book read, and
the reader again while reading the reprint. Chapter 3 now owns its own definition. Printer:
**Codex 5.6 Terra**. Taster SERVE 5/5, sweep NONE on all eleven.

## Two process faults, both the shop's own rules broken

**1. The printer bound its own page.** Codex committed the chapter 2 reprint and fast-forwarded
it onto `main` itself, **before the taster and the sweep had returned**. That breaks two rules at
once: *nobody binds the thing they made*, and the standing guard that *nothing is bound until
every check launched against it has come back*. The content was fine — the checks came back clean
afterwards — but the order was wrong, and it was wrong in the direction that has cost this shop
before. **The instruction not to commit was added to the printer's brief only on the third
round; it should have been there on the first.**

**2. The manager sent the reader a question it had made unanswerable.** The deletion prompt said
*"the old page is below"* and did not include the old page. The reader said so plainly instead of
guessing, which is the chair working exactly as intended — but a wasted pass is a wasted pass,
and it was the manager's error.

## The models were being spent wrongly, and the owner caught it

**Owner direction, 2026-07-22: stop defaulting every job to one model, and use more of the
reasoning depth available.** He was right on both counts, and the evidence was in this very run:
**a frontier model at high effort was spent reverting a single heading.**

Seven Codex models are available, not one. Sol supports two reasoning levels — `max` and `ultra` —
**above the `high` this shop has been using**, so the chair that was correctly staffed was also
being underfed.

**The new routing is in `THE-PRINT-SHOP.md`.** The printer's chair was won by measured contest, so
it was not swapped on an impression — that would be the quiet promotion this book exists to
prevent. Chapter 3's correction was the first job under the new routing and went to Terra, which
handled it cleanly at a fraction of the cost.

---

# The night the open holes were worked in parallel

**2026-07-22.** Six benches at once, one chef each, plus independent checkers. Five dishes bound.
Eight holes closed, seven opened — **and every one of the seven was found by a checker or by the
manager reading a diff, not by a verdict.**

## What bound

| Dish | Chef | Sent back? |
|---|---|---|
| The drift overclaim in the running order | Terra `xhigh` | no |
| Chapter 29 finally says what coordinating is | Terra `xhigh` | **once** |
| Eight parts' governing rules reach the reader | Luna `max` | no |
| The menu becomes a record — 12 chapters, 3 invariants | Terra `xhigh` + Sol `max` | **twice** |
| The shop's own tools stop drifting from the book | Sol `max` | **once** |

## The taster said SERVE 5/5 to everything, and caught nothing

Across every page checked tonight the taster returned **SERVE, straight fives on all seven
questions, every time.** Not one of the following was found by it:

- Chapter 29 came in at 703 words against a hard 700 limit, having deleted settled sentences
  from a bound page to make room. *Found by the manager reading the diff.*
- The menu chef reported no other chapter needed changing. *One search found four; the job
  eventually ran to twelve.*
- The same chef then skipped five chapters as "already over 700 words — 941, 873, 770, 703, 927".
  Those are whole-FILE counts. The body counts are 666, 675, 615, 550, 630. **Every one was
  inside the limit.** *Found by the manager re-running the arithmetic.*
- The press-tools fix removed two hand-maintained copies of one list and **introduced a third**.
  *Found by a checker, unprompted.*
- Chapter 44 states its governing rule twice in eight lines. *Found by a checker, unprompted.*

**The pattern is now measured rather than suspected: a verdict-giving check confirms that what is
on the page is correct. It cannot see what was removed, what was never reached, or what was
counted wrongly.**

## The taster has been judging two chapters against themselves

**The single most important finding of the night, and nobody asked for it.**

`press/taste.py` feeds chapters 0 and 1 into its own prompt as the voice standard. So tasting
either of them asks the taster to compare a page **with itself**. It returns SERVE and its reason
gives the game away: *"The page is the approved voice-standard chapter 0."*

**Every tasting ever recorded for chapters 0 and 1 is worthless** — including two the manager
reported as clean that same night, in this log, before the finding arrived. The record has been
corrected: nine tastings were reported, seven were real.

## The ruler was the fault, for the fifth and sixth time

Chapter 48's sentence *"Written instructions still travel unchanged to every restaurant"* had been
flagged as a violation **five times**. It was never wrong. `press/core-invariants.json` was.

With the menu reclassified as a record, invariant 8 lost its exception and invariant 4 lost its
carve-out. **The flag is gone and the check was not loosened by a single word.** Invariant 9 also
gained *"Every menu removal is logged"* — something the book has always required and the ruler
never said.

Two residual flags were put to a worker that produced neither the pages nor the flags, and ruled
NOT REAL: the book quoting its own settled rule, the checker's known failure mode, third and
fourth instances. It also noticed, unasked, that chapter 10's *"list a changed recipe"* is now
mildly imprecise under the new framing — recorded, not acted on, because it is cosmetic.

## The interface was quietly producing unchecked work

The owner asked whether the MCP was faster and more reliable than the designated runner. The
honest answer was that nobody had measured it. **By the end of the night it was measured, and the
answer is no.**

- **Four chefs were killed at exactly 1800 seconds**, the silent idle timeout. Three had written
  their page and had NOT run the verification they were told to run. One wrote nothing at all.
- Both times an unchecked page reached the manager, it carried a real fault.
- The designated runner enforces `owned_paths`; this interface does not. **That is why a printer
  was able to commit its own page onto `main` this morning.**

One mitigation worked immediately and cost nothing: briefs were rewritten to say *make the edit,
then IMMEDIATELY run the check, then stop.* The same model on the same job that had burned 1800
seconds and written nothing then finished, checked and reported **in under two minutes.**

The structural fix — teaching `press/print.py` to cover the whole book so `codex-exec` can be used
— was assigned and **timed out four times without producing anything.** It remains open, which
means the shop's most-used interface is still the one that loses work.

## Faults by the manager, recorded

1. **A cost estimate that was wrong, on which the owner decided.** The menu ruling was
   recommended with the words *"Chapter 10 stops listing the menu among the instructions. Nothing
   else moves."* Twelve chapters and three invariants moved. **The ruling was right and the
   estimate was not**, and the owner chose on the estimate.
2. **Two counts taken from files that were still being written.** printer-d's word count in the
   showdown, and "7 of 8 parts" on the part-rules track — the latter briefed a checker on a false
   premise. Same family as reporting a tally without opening what it matched, which this log
   already records twice.
3. **Six benches assigned without checking for file overlap.** Two tracks were given
   `press/print.py` at the same time. Caught before it bit, but by luck of noticing rather than by
   process.

## Chapters 9 and 10 — the role-assignment reprint, bound 2026-07-23

| Stamp | Record |
|---|---|
| Printed by | The draft was written on this branch before today; the tightening pass was **Codex `gpt-5.6-sol`**; the final one-word restoration was **GLM 5.2** |
| Head chef's list | Passed both. **Chapter 9: 700 body words** (at the ceiling, after the restoration). **Chapter 10: 699.** Zero jargon in either, every flat rule numbered |
| Taster | **Hy3.** Chapter 9 **SERVE**, 5/5 on all seven, no faults. Chapter 10 **SEND BACK**, twice, on two faults — **both adjudicated NOT REAL** |
| Contradiction sweep | **Hy3, binding.** Both chapters clean on all eleven invariants, on two separate runs |
| Adjudicator | **DeepSeek V4 Pro**, which produced neither page nor verdict |
| Verdict | **BOUND** |

### The rejection was the brief's fault, not the page's

Chapter 10 was sent back for two sentences: *"The menu is not an instruction"* and *"It is not
the only place drift can appear."* Both are correct, both agree with `core-invariants.json`, and
**both are byte-identical to the bound `main` page** — they predate this branch entirely.

What disagreed with them was `press/briefs-7to11.json`, which still carries the menu among the
instructions and still calls instructions-versus-log *"the only place drift can be seen at all"*.
**The owner dissolved both on 2026-07-22.** The scripts were corrected when the book was; the
briefs those scripts read were not.

**A stale brief does not merely fail to help. It manufactures faults.** This one would have
bought a reprint of a correct chapter — the same expensive shape as the withdrawn "a named chef"
hole, and the seventh time a document of ours rather than a page has been the fault.

### The compression introduced five faults, and the round that fixed four declared victory

The tightening pass hit its word count by damaging text it did not write. Four were caught by a
line-by-line read of the diff and fixed: an inverted causal claim in the new rule itself, a broken
sentence, a deleted instance of addressing the owner as *you*, and one clunky phrase.

**The fifth was not caught, and it was the worst of them.** To pay for those fixes, the pass had
deleted the word **only** from a rule about the three separations:

> *may be held by them **only** where no separation is broken* → *may be held by them where no separation is broken*

It was written down as *"a non-load-bearing `only`"*. It is load-bearing. Without it the sentence
stops forbidding and starts permitting — on the page that defines the separations, while flat rule
12 immediately below still carried the restriction. **The body of the page and its own flat rules
had drifted apart, which is the fault this entire book exists to catch.**

It was found by one head chef re-reading a diff another had already declared finished.

### So the damaged page was put back through the checks on purpose, and they passed it

This is the closest thing to a controlled measurement this shop has managed. The **same chapter**,
damaged and undamaged, fingerprinted on both sides, through the **same two checks**.

| Chapter 9, fingerprint `8a89d72e…`, the word *only* deleted | Result |
|---|---|
| Taster (Hy3, with the brief) | **SERVE. 5 out of 5 on all seven items. No faults.** |
| Rule-by-rule sweep (Hy3, against the eleven invariants) | **One flag — quoting a different sentence, which was correct** |

The sweep's flag named *"Never let the person who made a dish give the checking verdict on that
dish."* That sentence is fine, and it swept clean on both runs where the page was undamaged. **So
the sweep did not find the deletion either — it produced noise on the same page, and a manager in a
hurry could have written that down as a catch.**

**Neither check can see a missing word, because nothing on the page is wrong once it is gone.**
That is not a criticism of either check. It is the shape of the question they are asked.

### A claim in this entry was false, and it was caught before it was bound

The paragraph above originally read *"every automated check passed it, twice each."* **Untrue.**
The word was deleted at 00:16 and restored before either of this manager's check runs, so **no
check had ever seen the damaged page** at the time the sentence was written. A second claim — that
the taster scored the same bytes differently — was also untrue: the two runs were on files with
different fingerprints, and three sentences had changed between them.

**Both were caught by giving the manager's own record to a reader that had not written it**, which
is the rule this shop already had, and the sixth time that rule has caught this exact fault. The
false claims were then replaced with the measurement above — which says something stronger than the
claim did, and is true.

### What in this entry is inherited, and was not opened by the session that wrote it

Two head chefs worked this ticket, so this entry is part first-hand and part second-hand, and a
stranger cannot tell which unless it is said. **Everything above rests on evidence this session
ran and fingerprinted, except these, which came from the other session's record and were taken on
trust:** the four earlier compression regressions and their fixes; the sweep flag it reported on
chapter 9 against a different sentence; and that chapter 10 held 699 words throughout.

**None of them is doubted. All of them are unverified**, and the difference matters here more than
most places, because the entry directly above records this manager twice writing down things it had
not opened. **Saying which half of a record you actually checked is the cheapest honesty available**,
and this shop has now twice paid for not doing it.

One thing genuinely missing rather than merely inherited: **the adjudication that cleared chapter 10
was run and read, but its output was not kept.** The verdict is in this log; the reasoning is not
anywhere. That is a gap in the evidence trail and it is written up as a hole.

### Verified rather than inherited: the no-brief route

The earlier close of this hole recorded both chapters as SERVE with no brief supplied. That was
another session's claim, so it was re-run rather than copied: **chapter 9 SERVE 5/5, chapter 10
SERVE 5/5, no faults, no brief.** The claim stands, and it is now this shop's own measurement.

### Two sessions worked this branch at once, again

**The second occurrence, one day after the first was written up as the reason a session must own
the repository alone.** Two head chefs cooked this same ticket in parallel for roughly half an
hour, committing into the same folder minute by minute. Most of what each found, the other found
too, by a different route.

The duplication was the waste — but **it is also the only reason the fifth regression was caught**,
because the second chef read a diff the first had already closed. That is an argument for a second
pair of eyes, and **not** an argument for two hands on one page: the second chef spent its first
checks on a page that changed underneath it, and had to throw them away.

### Faults by the manager, recorded

1. **The checks were run against the live folder, not a frozen copy** — so when the page changed
   mid-check, four completed checks became worthless. **The standing guard telling us to certify a
   fingerprint rather than a directory was already written down**, from the last time this
   happened. It was not followed until after it had cost the work a second time. Every later check
   in this entry certifies an md5.
2. **The owner was told twice that the other session was a problem before its work had been read.**
   It was doing careful, correct work and had found four real faults. The report was accurate about
   the collision and unfair about the worker.
3. **Two false claims were written into this very entry** — one about fingerprints, one about what
   the checks had seen — **inside a write-up whose subject was the manager asserting things it had
   not opened.** Neither survived, because the record went to a reader that had not written it.
   **The guard was already written down. It does not hold by intention; it held because something
   other than the manager read the words.** That is the sixth instance, and the third recorded in
   this log where the manager was the fault and a checker was the reason it did not ship.

## The silent timeout is not one runner's fault — the manager reproduced it, then reported it instead of logging it (2026-07-23)

While closing the top open hole — `press/print.py` reaching only chapters 17–50, so the one runner
that enforces `owned_paths` could not be used on most of the book — the head chef ran the fresh
reviewer through a shell command that still carried a **two-minute deadline left on by default**.
The deadline fired and **killed the reviewer mid-run.** No work was lost — the review was simply
re-run with no cap — but the event is evidence, not an anecdote.

**This is hole #1 happening to the manager.** That hole records a silent 1800-second timeout on
`codex-exec` that killed four chefs after they had written but before they had checked. The instinct
has been to read it as a fault inside that one runner. It is not. **A blind deadline severs work
mid-flight whoever imposes it** — the runner's own 1800 seconds, or a caller's 120. The fault is
*caller-imposed blind deadlines*, and the guard belongs at every layer that launches a long job, not
only inside `press/print.py`. A review has no time cap by design; the manager gave it one by accident.
Standing guard, added here: **a runner or reviewer is launched with no blind deadline — in the
background if need be — never inside a command whose own timeout can behead it.**

**And it was very nearly not written down.** The manager told the owner about it in conversation —
"a self-inflicted snag worth owning" — and moved straight to the next step. The owner caught that a
spoken aside had swallowed a real finding and asked why it was not in the journal. **The record lives
in the repo, not the conversation**; a fault seen and not recorded is a fault the chain never had a
chance to fix. This is the same shape as every count-without-reading instance above, one layer up:
the discovery was *had* and not *kept*.

**The deeper cause is the one already written on this page: the rule does not hold by intention.** The
manager had re-read the peg's fifth rule — write every hole down — at the very top of this session,
and still let a discovery live only in chat an hour later. Remembering to log is exactly what failed.
The prevention has to be a checker, not a firmer resolve, and the owner has asked for one — a harness
reminder that fires whether or not the manager remembers. It is being chosen now; this entry exists so
the finding is kept while the mechanism is built, which is the whole point.

## No enhancement ships on impression — the fix is measured, or it is an opinion (2026-07-23)

Immediately after the entry above, the manager reoffended in a new shape. Asked how to make
discovery-logging reliable, it invented three hook designs and asked the owner to pick one. **Neither
of them knew the correct answer, so the question was a guess wearing the clothes of a decision** — and
asking the owner to choose between unmeasured guesses is both *spending the owner's attention* and
*promotion on impression*, the two faults this shop is built to refuse.

**The owner's ruling, and it is a standing method now: an Enhancement earns its place the way a cook
does here — by measured audition, not by sounding right.** Anything proposed as an improvement must be
(1) researched against real-world prior art on the web and GitHub, (2) reduced to a testable theory,
(3) probed with a small prototype, and (4) measured against a metric it must actually move. Only a
measurable gain is an *Enhancement*. A thing that cannot be measured is an opinion, and opinions do
not ship here.

This is the showdown applied to process instead of to cooks. The printer's chair, the taster, the
reader — every seat in this shop was filled by measurement, never by a model card or a good argument.
Method changes now go through the same door. The first thing put through it is the very question that
produced this ruling: how to make a discovery reliably reach the record. It is being researched, not
guessed.

## Chapter 30 — the parallel-reading correction, SENT BACK

| Stamp | Record |
|---|---|
| Job | Correction, not a reprint — add the eyes-vs-hands lesson from the ch9/ch10 collision to the chapter already scoped to it |
| Printer (page-correction chair) | **Codex 5.6 Luna, max effort** |
| Head chef's list | Passed: 700/700 body words, zero jargon, every flat rule field true |
| Taster | Hy3, **no brief on file** (this is an ad hoc correction outside the numbered-brief system) — **SERVE, 5/5 on all seven, no faults** |
| Contradiction sweep | Hy3, binding, against all 11 invariants — **clean, all NONE** |
| Reader-against-original | **DeepSeek V4 Pro**, given the original page, the corrected page, and all 25 reported trims, asked trim-by-trim — **not run holistically** |
| Verdict | **SEND BACK. Not bound. Never merged; the rejected page was discarded and its bench cleared — see "Consolidated to `main`" at the end of this entry.** |

### What went right first

The brief for this job explicitly named the "only"-deletion incident and required every trim
outside the new passage to be reported verbatim, before/after, precisely so this could be
checked without trusting the writer's own validator. **That worked exactly as designed.** The
worker reported 25 trims in `final.json`, unprompted beyond the brief's requirement, and that
list is what made the finding below possible at all.

### What went wrong: 36 words of slack bought a whole-page compression pass

Chapter 30 had roughly 36 words of body budget left (664 of 700). The brief asked for a
tightly scoped addition and said to trim elsewhere **only if truly necessary**, tightening
wording rather than deleting or weakening a clause. Codex 5.6 Luna instead lightly compressed
**nearly every sentence on the page**, all seven sections, to buy room — landing exactly at
700. Both automated checks passed it clean:

- **Hy3 taster: SERVE, 5/5, no faults.**
- **Hy3 contradiction sweep: all 11 rules NONE.**

**Neither check found anything, because nothing on the page is wrong on its own page** — the
same shape as the "only" incident this brief was written to guard against. Only the
reader-against-original, asked trim by trim rather than for an overall impression, found it:

1. **"the whole dish" → "the dish"**, in the sentence about when cooking may be handed to
   another cook. **Flat rule 3, untouched, still reads "the whole dish."** The body and the
   chapter's own flat rules now disagree on the same point — the exact fault this book's
   template exists to prevent, on the exact page about not letting two workers' copies of a
   dish drift apart.
2. **"keep the whole job in view" → "keep the job in view"** — the same word, "whole,"
   dropped a second time in the chapter's opening paragraph.
3. **"in their attention" → "in mind"** — replaces the chapter's own named concept
   (the section heading is "Attention running out is the strain") with a synonym, in the
   sentence that defines the strain.
4. **"two workers touching the same work" → "workers touching it"** — drops "two" and "the
   same," the exact words carrying this chapter's central concern, from the sentence about
   why the log's stamp makes collisions visible.
5. **"The required separation has disappeared" → "Separation has disappeared"** — drops
   "required," the word carrying the obligation, from one of the chapter's four listed
   mistakes.
6. **New flat rule 11 is not grammatical.** *"Allow a worker who only reads check, taste or
   read a dish's record..."* is missing "to" before its three verbs and does not parse as
   written.

Found by DeepSeek V4 Pro, asked to go sentence by sentence against a "before" it was given
rather than for an opinion of the "after" alone — the same method this shop has used every
time a hidden deletion has ever been caught here, because a verdict-shaped question keeps not
seeing this class of fault.

### A second fault, procedural: the worker committed before any check had run

`final.json` records `"Committed as 69d48f8"`. **Nothing in the brief told it to commit, and
nothing told it not to** — the exact gap this log already named as the root cause the last
time a printer bound its own page before its checks returned (see the chapter 2 entry above:
*"nothing in the printer's brief had ever said 'do not commit.'"*). This brief repeated that
same omission on a fresh job. No harm reached `main` — the work was isolated in its own
worktree and branch throughout, and this entry is written before anything is merged — but the
ORDER fault is the same one on record, and it is logged here rather than quietly avoided
because the isolation happened to catch it this time.

### Disposition

Not bound. The correction is sent back for a stricter brief: no edits anywhere on the page
except inside the new passage's own paragraph, the new passage rewritten to fit whatever
budget remains **on its own** rather than by trimming the other 24 sentences, and an explicit
instruction not to commit. The five word-level regressions above are to be checked, by a
worker that did not write them, against the eventual redo as well as this one.

**The parallel-work standing-policy material this chapter's ladder was also asked to carry**
(a kitchen choosing, once, how many workers run at a time by default) was kept out of this job
entirely rather than compressed into chapter 29's six remaining words of room, and is recorded
instead in `KNOWN-HOLES.md`.

### Consolidated to `main`, bench cleared (2026-07-23, head chef)

This entry was salvaged onto `main` from the parked `parallel-work-ch30` worktree, which held two
records that existed nowhere else: this rejection and the parallel-work hole (now in
`KNOWN-HOLES.md`). The rejected
page itself was **discarded, not kept** — the six regressions are recorded in full above, so the
bad page adds nothing a stranger would need. The `parallel-work-ch30` worktree and branch were
removed and the ch30 redo remains open (see the Disposition above; the stricter-brief reprint is
still to be done). Decision by the head chef under the owner's standing mandate that the head chef
decides autonomously and logs it; preserving records that live only on an unmerged branch is the
house rule *"the records say what happened"* applied literally.

## Hole #1 CLOSED — the printer's reach, bound at last after five attempts (2026-07-23)

| Stamp | Record |
|---|---|
| Job | Close the top open hole: `press/print.py` reached only chapters 17–50, so `codex-exec` — the one runner enforcing `owned_paths` — could not be used on most of the book. Blocked for four+ attempts; the last parked-not-bound on a real defect (a fallen-off TERMINAL chapter silently accepted) |
| Channel | **`model-flow`, crucial**, flow `mf-4b395a4559af`. Receipts, owned-path lock (`press/print.py`), secret scan, host-authored verify command |
| Writer | **Codex `gpt-5.6`** (implementation phase, exclusive writer lock) |
| Acceptance test | **Head-chef-authored** `press/test_printer_reach.py` — drives the real `--catalog` CLI against fixture repos; A (full 0..50), B (terminal drop REJECTED), C (unwritten page still works). Reproduced the defect before the fix (B red), all green after |
| Final review | **Fresh Codex reviewer + DeepSeek V4 Pro, concurrent, on the frozen snapshot.** Both **APPROVED** (attempt-002) |
| Verdict | **BOUND to `main`.** Two clean commits: the `print.py` fix and the test |

### The fix

`chapter_catalog()` built its "expected" set purely from the chapters it had already consumed, so
it had **no independent knowledge of where the book ends** — drop the chapter-50 line from
`CONTENTS.md` and it returned a 0..49 catalog with exit 0. The fix adds an **external anchor**:
`book_chapter_numbers()` reads the `book/` directory (the pages that physically exist), and any
on-disk page the running order does not reach now raises. The hard constraint holds — a chapter
in `CONTENTS.md` with **no page yet** is still catalogued (launching a printer to write a missing
page is the whole purpose), and a new chapter beyond the on-disk maximum is allowed. Only a page
the catalog cannot account for — a fallen-off terminal chapter — is the fault it now catches. This
is exactly the design the prior blocking review asked for, and the head chef reproduced the defect
first so the test was grounded, not assumed.

### Two process findings, both logged rather than smoothed over

**1. The manager ran the writer under the wrong phase, and re-ran it clean.** The first Codex run
was launched as the `plan` phase while the brief was implementation-shaped, so it wrote the code
under a plan receipt. `review final` binds an *implementation* receipt, so the plan output could
not have been reviewed coherently. Rather than bind on an incoherent receipt, the tree was reset
and the writer re-run as `implementation` — a proper receipt, exclusive lock, the same fix. The
plan run was not wasted: it confirmed the external-anchor design before a coherent pass. Cost: one
extra Codex run. The alternative — binding crucial work on a mislabelled receipt — is the kind of
provenance rot this shop exists to refuse.

**2. `model-flow`'s crucial review recorded an APPROVED Codex reviewer as BLOCKED — a false
negative in the shop's own gate.** On the first `review final` (attempt-001), the Codex reviewer
finished cleanly (exit 0) and **APPROVED** — its `final.json` said *"No findings … both passed"*
and carried `VERDICT: APPROVED` inside its `open_issues` array, with an empty `final.txt`.
DeepSeek APPROVED the same snapshot. But `model-flow` reported the whole review **BLOCKED**
(`process_failure: true`). Root cause, read in the code (`~/.claude/skills/model-flow/scripts/model-flow.py`,
`_codex_final_verdict`, ~L1546–1562): the verdict is extracted only from a top-level `verdict`
field, the `summary`, or `final.txt` — **never from `open_issues`.** When a Codex reviewer emits
structured-only output and puts its verdict line in `open_issues`, a genuine APPROVED is scored as
BLOCKED. **The manager did NOT override the red verdict** — overruling a checker with no
re-readable reason is the fault this file records six times. Instead the root cause was proven in
the source, and the review was **re-run**; attempt-002 put the verdict in `summary` (a field the
parser reads) and classified cleanly APPROVED by both reviewers. The block was a format gap, not a
defect. **This is a real hole in the shop's shared supervisor, not in this book** — it lives in
`~/.claude/skills`. **FIXED the same day on the owner's go-ahead:** `_codex_final_verdict` now also
scans the reviewer's list fields (`open_issues`, `verification`, `changes`) for the `VERDICT:` line,
so a structured-only APPROVED is no longer read as BLOCKED; `parse_verdict` still matches only an
explicit `VERDICT: <token>`, so prose in those fields cannot forge a verdict. Verified against the
attempt-001 shape (now APPROVED), the attempt-002 shape (still APPROVED), a real BLOCKED (still
BLOCKED), and no-verdict (still None); the tool's own 85-test suite passes. It is surfaced to the
owner and recorded here so the next crucial job is not blocked — or, worse, tempted into an
override — by the same false negative. The lesson is the one the whole shop turns
on: **a red verdict from a checker is investigated to its root and resolved with evidence, never
waved past because the manager read the outputs and liked them.**

### What is now unblocked

The designated runner can be pointed at any chapter 0–50, so future page work runs through the one
interface that enforces `owned_paths`, instead of the path-blind interface that on 2026-07-22 let a
printer commit its own page and killed four chefs mid-task. The `worktree-fix-printer-reach` branch
that held the parked partial is superseded — its good work (the 0–50 range, stray-list skipping,
filename overrides) is now on `main` inside the bound fix — and is deleted.

## Owner ruling — staffing by order size, and it must be myth-busted before it is written (2026-07-23)

Asked how many workers a kitchen should put on one job at a time, the owner rejected a fixed
default and ruled the answer **scales with the order's size**: a small order stays with one
worker; a large one is split among more, so no cook loses the whole job from sight. Then the
sharper instruction: **"this needs a myth-buster type of thing"** — it is a *hypothesis*, not a
rule, and does not enter the book until it has been probed and measured against real work, the
same *measure-every-Enhancement* bar every process change now clears. **Recorded as a ticket in
`KNOWN-HOLES.md`, not run through the press** — the owner said plainly this is not part of the
current printing run. The manager did not draft any chapter text on it; the design (where it
would live, the six-word budget in chapter 29, the queue-length-is-not-the-trigger distinction to
preserve) is captured in the ticket so a future session inherits the reasoning rather than the
guess. The chapter 30 redo remains a separate parked ticket.

## Owner ruling — file tickets for all open work, and harvest measurable data on the book (2026-07-23)

The book is complete: all 51 table-of-contents pages (0–50) are written and bound, and the
printer's own reach test (`press/test_printer_reach.py`) confirms the catalogue covers 0..50 with
a page for every listed chapter — green 5/5. Nothing in the running order is unprinted. What is
left is the open holes.

The owner ruled two things. **First: file tickets for all of it** — turn the open holes and
corrections into a proper, claimable work board. **Second: add proper measurable metrics on every
one of the table-of-contents pages**, in service of a standing goal — *"harvest as much data as we
can on our cookbook."*

**What the head chef decided (mechanics, not owner calls):**

- **A single live board, `TICKETS.md`.** The precedent had buried one ticket inside
  `KNOWN-HOLES.md`, but that file is the frozen *record* of faults, not a work queue. Splitting a
  *plan* from a *record* is the book's own instructions-vs-records distinction, so the two are not
  "two copies of one promise": `TICKETS.md` is the plan and points back to `KNOWN-HOLES.md` for the
  evidence, and a header note added to the record names the board as the live source of truth so
  they cannot drift. When a ticket closes, its hole is struck in the same commit.
- **Every ticket carries a *measurable* done-condition** — a probe that flips, a number that moves,
  a check that passes — never an opinion. That is the owner's measure-every-Enhancement rule applied
  to the tickets themselves.
- **Scope filed: 17 tickets plus the metrics initiative.** Two blocking (stale briefs manufacture
  false rejections; `taste.py` judges chapters 0 and 1 against themselves), two owner-decisions (what
  the operations log physically is; what the appliance is), six book corrections, five shop-tool
  corrections, and the data-harvest initiative. Standing guards (the manager never does the work;
  never report an unread count; nothing bound mid-check) were **not** ticketed — they are adopted
  discipline, not units of work. Two old book-content rows (ch. 25, ch. 12) were flagged as needing
  a verify pass before they earn a ticket, not filed on assumption.

**First data harvest taken the same session.** `press/head-chef-check.py` already emits per-page
numbers (body-word count, within-700, jargon, flat-rule presence) and — measured here — **nothing
ever stored them**; every run was discarded. All 51 pages were run and the result stored as
`data/page-metrics-2026-07-23.json` — the first snapshot the next one can be diffed against.
Baseline: mean 577 body words, none over the 700 ceiling, no jargon hits, every page carries its
flat-rules section; tightest pages ch9 (700), ch2 (699), ch10 (699), ch29 (694) — which matches
the word counts already in the record. **The metric *design* is deliberately left as a
measure-every-Enhancement job** (research → theory → probe → a metric that must actually move),
captured in ticket T-18 rather than asserted on impression.

**Records only, not run through the press** — the same class of clerical/records work as the
staffing ticket above: organizing existing findings, no chapter text drafted, no paid model calls
beyond the free mechanical harvest. Committed on an isolated worktree and merged fast-forward.

## Decision — the work-tracker stays flat files in the repo; Issues only as a bug mailbox (2026-07-23)

The owner questioned whether the tracker should be GitHub Issues rather than the in-repo flat
files, and — the standing method — asked for research and proof, not a rubber-stamp, from either
side. The research was run off-session (`research/where-work-is-tracked.md`, commit 341d19a;
grounding reads GLM 5.2, writing Sonnet 5 after an Opus 429, citations spot-checked by the owner
as host). The host then pressure-tested the finished file rather than accepting it.

**The decision.** The in-repo flat files stay the system of record — `TICKETS.md` the live plan,
`KNOWN-HOLES.md` the frozen record. GitHub Issues earn a place only as a **one-way public mailbox**
for plugin readers to report bugs, triaged into the repo each session and closed with a pointer,
never a second board. This closes the book's own self-referential open hole, "where the job list
lives for a kitchen with no shared tracker."

**Why (the load-bearing plank, stated honestly).** The deciding rule is *the process lives in the
repo so a stranger session finds it offline* — a GitHub Issue is not in a `git clone`, confirmed
against GitHub's own docs. The research also leaned on "records never travel," but the host's
pressure-test flagged that plank as borrowed: "records are local" most directly means *tied to
this one restaurant, does not propagate to the others*, which an Issue actually satisfies. The
conclusion survives on the repo-alone rule, which is the real load-bearer.

**Proven, not asserted (Probe A, measured this session).** A fresh Explore session was given only
the repo — no GitHub, no prior context — and asked to pick up the next open job and say what "done"
means. Reading the mandated order alone (`WHERE-WE-ARE.md` → `TICKETS.md` → `KNOWN-HOLES.md`) it
correctly named the top open ticket (T-12), its measurable done-condition, and its evidence row —
**measured PASS**. It also caught a real gap the research missed: `TICKETS.md` alone treated the
two P1s as co-equal, so the do-first order existed only in `WHERE-WE-ARE.md`. Fixed — the board now
carries its own tie-break (T-12 before T-10).

**The one loose bolt, kept open honestly.** The research declared parallel-session collisions
"solved by discipline," but its proposed rule — write your claim into the ticket row before
starting — does not work under the worktree invariant: each session is on its own branch and never
sees the other's claim until merge, which is the exact 2026-07-23 collision. Real live-claiming
needs shared immediately-visible state, the one property a flat file on a private branch cannot
give. Filed as **T-19** rather than papered over. The reader bug-mailbox is filed as **T-20**,
gated on Probe B (prove it does not become a second drifting board before adopting it).

**Provenance of this session's work:** host read the full research file and ran the probe; host
authored the records edits (this entry, the `KNOWN-HOLES.md` close, the `TICKETS.md` reorder and
T-19/T-20, the `WHERE-WE-ARE.md` breadcrumb). Records only, no press pipeline, no paid calls.
Committed on an isolated worktree and merged fast-forward.

## Clearing down after a drift, and a clean handoff (2026-07-23)

The owner called out a drift: a two-line request ("is the book done, file tickets with metrics")
spiralled into four research threads, a global handbook change, and a 373-line deep dive on git
locking. Named honestly here because an unnamed mess is the one that takes the building down.

Cleared down and closed up for a fresh session:
- **Global rule added** to `~/.claude/CLAUDE.md` ("How we work": nothing served blind; a command is
  an input not an auto-run; object with proof; measure or it's an opinion). Live sessions must
  restart to load it — which is why the owner is opening a new session.
- **T-19 research preserved as an UNVETTED draft** at `research/session-claiming.md` (Qwen chef;
  the outside DeepSeek chef timed out four times — measured ~60% reliable, ~170s cap — so it went to
  Qwen). Recommends an in-repo `CLAIMS.md` using git-push atomicity as a lock, with an honest
  crashed-session-holds-the-claim weakness. Not pressure-tested, not probed. Kept, not acted on.
- **Tool dropping removed** (`press/__pycache__`); working tree clean.
- **Left parked, not lost:** the coordination-architecture + metrics research (never completed) and
  the "how a new dish is cooked" manual (named, not written). The peg re-anchors the next session to
  `TICKETS.md` and marks these process threads parked, not active.

Records only. Committed on an isolated worktree and merged fast-forward.

## T-12 CLOSED — the taster no longer judges chapters 0 and 1 against themselves (2026-07-23)

| Stamp | Record |
|---|---|
| Job | Close the do-first blocking hole: `press/taste.py` injected chapters 0 and 1 as the voice standard on **every** taste, so tasting either of those two handed the model the same text twice and it scored the page against itself. Every tasting ever recorded for 0 and 1 was worthless |
| Channel | **`model-flow`, substantial**, flow `mf-3007ffb50229`. Receipts, owned-path lock (`press/taste.py`), secret scan, host-authored syntax verify |
| Writer | **Codex `gpt-5.3-codex-spark`** (implementation phase, exclusive writer lock) — the substantial writer for a Claude host per `~/.claude/CLAUDE.md` and `model-flow` policy |
| Acceptance test | **Head-chef-run, measured before/after on the live taster.** Baseline (broken code): tasting chapter 0 → SERVE 5/5, `why = "The page is the established voice-standard chapter 0"` — the self-reference tell. After the fix: chapter 0 → **SEND BACK** (a genuine fault, the word *plugin* as body jargon); chapter 1 → **SERVE 5/5** on a real comparison to chapter 0 (`why` cites its voice and the telephone-game analogy). The tell is gone from both |
| Final review | **Fresh Codex reviewer** on the frozen snapshot. It **verified the code fix correct** (intercepted-network tests: each outgoing prompt carries only the OTHER chapter in its voice-standard region; AST branch checks passed for chapters 0/1/2/None; only `press/taste.py` touched) but returned a **routing BLOCK** — see the process finding below |
| Verdict | **BOUND to `main`.** One commit: the `press/taste.py` fix plus the record updates (this log, `KNOWN-HOLES.md`, `TICKETS.md`) |

### The fix

The prompt built two fixed `VOICE STANDARD` blocks — chapter 0 and chapter 1 — regardless of which
page was being tasted. The page's own chapter number was already computed. The fix branches on it:
tasting chapter 0 withholds the chapter-0 block and keeps chapter 1; tasting chapter 1 withholds
chapter 1 and keeps chapter 0; every other page (and any page with no numbered heading) keeps both,
exactly as before. A withheld block is **replaced by a visible `[WITHHELD: THIS PAGE IS CHAPTER N …
JUDGE AGAINST THE OTHER, NOT ITSELF]` note**, so the model cannot pass a page simply for being the
standard. Minimal diff, `press/taste.py` only, style matched.

**Why this matters beyond the fix.** The moment the taster stopped comparing chapter 0 to itself it
returned a real SEND BACK, naming the word *plugin* in the body as programmer-only jargon. That is
the payoff the ticket predicted — the old clean SERVEs were worthless. Whether *plugin* is banned
jargon or necessary install-vocabulary in the box-opening chapter is a **separate** question needing
a verify pass; flagged in `KNOWN-HOLES.md`, not chased here (park, do not chase).

### Process finding — two handbooks on this machine disagree about the writer, and the reviewer blocked on it

The Codex reviewer's **code** verdict was a pass. It nonetheless returned **BLOCKED**, on a
provenance objection: it read `~/.codex/AGENTS.md`, which states GLM-5.2 is the *sole* primary
writer for substantial code and Codex is only the reviewer, and objected that Codex wrote this fix.

Investigated to root rather than waved past (the lesson this log already turns on). The reviewer is
a Codex process, so it reads Codex's own handbook — and that handbook is **GLM-first**. But this
session's governing standard, `~/.claude/CLAUDE.md`, is **Codex-first** for a Claude host: its
host-surface table names `codex-exec` the substantial writer, and `model-flow`'s own policy agrees
(`gpt-5.3-codex-spark`). `model-flow` therefore routed correctly for the host it was serving. The
two handbooks genuinely encode opposite writing philosophies — Codex's AGENTS.md line 46 says a
Claude host's writer is `glm-exec`; my CLAUDE.md says `codex-exec`. **The BLOCK is a cross-handbook
false-positive**: Codex's handbook does not govern a Claude-host flow.

The fix was **not** re-run through GLM to satisfy the reviewer — doing so would subordinate the
owner's handbook to Codex's, backwards. It was bound on the merits, correct under the standard that
binds this session and verified three independent ways (the reviewer's own tests, the head chef's
full diff read, the live before/after probe). **The conflict itself is surfaced to the owner as a
decision** — it is a hard-to-reverse choice between two global handbooks, and until it is settled
every substantial Claude-host code job will draw the same false BLOCK from its own Codex reviewer.

### Clearing down

Worktree `t12-taster-self-compare` merged fast-forward and removed; `press/__pycache__` (created by
running the taster) stays git-ignored; working tree clean. Board updated: T-12 struck, **T-10 is now
the last blocker before the next page prints.**

## T-10 CLOSED — chapter 10's brief realigned to the bound page; the last blocker is gone (2026-07-23)

| Stamp | Record |
|---|---|
| Job | Close the last blocking hole: chapter 10's brief in `press/briefs-7to11.json` quoted two rules the owner dissolved on 2026-07-22 — the menu as an *instruction*, and instructions-vs-log as *"the only place drift can be seen"* — so a taster handed that brief manufactured false faults against the correct bound page |
| Channel | Isolated worktree `t10-stale-briefs`; mechanical content-alignment (host), wording pre-determined from the authoritative bound page + `core-invariants.json`, certified by the objective taster probe |
| Acceptance test | **Head-chef-run, measured on the live taster** across three runs on chapter 10 (see below) |
| Verdict | **BOUND to `main`.** One commit: the brief fix plus the record updates |

### The fix, and what the measurement found beyond the ticket

The two dissolved rules were corrected to match the bound chapter 10 and `core-invariants.json`:
the menu is a local **record**, not an instruction (inv. 8/9); instructions-vs-log is the
**sharpest** place drift shows, not the only place (inv. 3). `press/briefs-2to6.json` was checked
and carried neither rule — already clean, so the "both files" done-condition was half-satisfied
before I started.

**The taster measured the fix in three runs, and each removed exactly its predicted false fault:**

1. **Stale brief → SEND BACK**, `t6_contradiction 1`. It flagged the two *correct* sentences — the
   page saying "the menu is not an instruction" and "not the only place drift can appear" — as
   contradictions of the brief. The page is right; the brief was wrong. This is the baseline the
   ticket predicted, reproduced live.
2. **After fixing the two dissolved rules → SEND BACK**, but `t6_contradiction` now `5` (both false
   faults gone) and a NEW `t4_unfounded` fault appeared: the "a job description states how heavy the
   thinking is" section (flat rules 11–12) called an "invented mechanism … not established by the
   brief." That is a **third** staleness: the brief predates the 2026-07-23 chapters 9/10
   role-assignment reprint that added that content to the page, so the brief did not authorise it.
   Same disease as the ticket — a brief drifted from the bound page manufacturing a false fault —
   one the ticket had not named because nobody had measured this far.
3. **After adding the reasoning-weight coverage to `must_cover` → SERVE, zero faults**, `t4` and
   `t6` both `5`. Done-condition met.

**Scope call, labelled.** Extending the fix past the two rules the ticket named was a head-chef
decision, not a silent one: the done-condition is *the probe returns SERVE*, and it cannot be
reached while the brief stays stale in a third place with the same root cause. It is a brief edit,
revertable, and certified by an objective probe — decide-and-log territory, not an owner question.

### Why the taster certified this instead of a code reviewer

This was a content-alignment edit — four corrected strings and one added `must_cover` item, wording
lifted from the bound page — not new logic. The strongest possible check for "does the brief now
match the page" is the taster itself run against the bound page, and it is independent of the hand
that made the edit. A clean SERVE with zero faults, from SEND BACK on the same page, is a measured
pass that no read-through could match.

### Clearing down

Worktree `t10-stale-briefs` merged fast-forward and removed; `press/__pycache__` stays git-ignored;
working tree clean. **Both blocking tickets (T-12, T-10) are now closed — no blocker remains before
the next page is printed.**
