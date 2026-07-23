# Where we are

The peg in the road. Two people walking to the same place have to walk the same road at the
same pace — so we plant a peg at the step we are actually on, and neither of us walks past
it alone.

Read this first, every session. Name the step in your first line, every reply.

## Read these, in this order

1. **This page** — the step we are on, and the five rules. Nothing else until you have read it.
2. `THE-PRINT-SHOP.md` — who does which job, and why each of them is there. **You are the print
   manager.** You hand out work and check it; you do not do it. That rule has been broken here
   and it is written down as a fault.
3. `CONTENTS.md` — the running order. **Settled and closed.** Correct a phrase a bound chapter
   has proved wrong; never redesign it.
4. `TASTING-CHECKLIST.md` and `THE-CONTRADICTION-PASS.md` — how a page is checked, and why the
   contradiction pass is separate from the taster.
5. `PRESS-LOG.md` and `KNOWN-HOLES.md` — what happened, and what is still wrong.
5a. `TICKETS.md` — **the live work board.** Open work, claimed and finished, each with a
   measurable done-condition. It points back to `KNOWN-HOLES.md` for the evidence. Start here to
   pick up the next job.
6. `CHAPTER-TEMPLATE.md` with `book/00-opening-the-box.md` and `book/01-the-interview.md` —
   only if you are printing. **Nothing is left to print.**
7. `OVERNIGHT.md` — **a completed order.** Read it for the rules it learned, never for the
   task. Its goal is finished.

## The step we are on

**The book is bound and the front door is honest.** All 51 chapters written, tasted, swept
against the eleven invariants and read for what they left out. The whole-book read is done. The
menu contradiction — the oldest live one — is closed. `README.md` and `CHANGELOG.md` tell the
truth about the state.

**Chapters 9 and 10 are bound, 2026-07-23.** The role-assignment rule is in the book: a role is
given, never assumed, and a job description matches a dish to a hand of the matching strength.
Measured, tasted, swept, adjudicated and bound. **Read the entry in `PRESS-LOG.md` before
touching a compression pass ever again** — the shop now has its cleanest measurement of its own
central finding, and it came out of that job:

> **The same page, damaged and undamaged, fingerprinted on both sides, through the same two
> checks.** A compression pass deleted the word *only* from a rule about the three separations,
> turning a restriction into a permission. **The taster returned SERVE, five out of five on all
> seven items. The sweep flagged a different sentence, which was correct.** Neither check can see
> a missing word, because once it is gone nothing on the page is wrong. It was found by a person
> re-reading the diff against the bound page.

**The step is the holes that are left**, in `KNOWN-HOLES.md`. In priority order:

1. **DONE, 2026-07-23 — `press/print.py` now reaches the whole book.** It was hard-limited to
   chapters 17-50, so the designated runner (`codex-exec`, the only one enforcing `owned_paths`)
   could not be used elsewhere — the hole that caused the other holes. Bound on the fifth attempt:
   the range now comes from `CONTENTS.md` and the completeness check anchors on the `book/`
   directory, so a fallen-off terminal chapter raises instead of being silently accepted. Crucial
   `model-flow`, Codex writer, Codex + DeepSeek final review APPROVED, host-authored test green.
   Full record in `PRESS-LOG.md`. **The remaining priorities below move up.**
2. **`press/taste.py` judges chapters 0 and 1 against themselves** — it feeds them in as the
   voice standard. Every tasting ever recorded for those two is worthless. Nothing else on the
   board invalidates evidence already written down.
3. **`press/briefs-*.json` still quote two rules the owner dissolved on 2026-07-22** — the menu
   as an instruction, and drift being visible in *"the only place"*. **Measured on 2026-07-23:
   a taster given one of these briefs rejected a correct chapter twice**, quoting two sentences
   that are byte-identical to the bound page. **This one is worse than it looks, because it does
   not merely fail to help — it manufactures faults, and a false fault buys a reprint of a page
   that was already right.** It will bite the next job that uses a brief. Fix it before printing.
4. The smaller ones: a fourth copy of the brief's field names in `prep.py`, chapter 44 repeating
   its own rule in eight lines, `press/briefs-*.json` also still saying *chef*, and the shop
   keeping no record of *why* it overrules a checker — six overrules, none re-readable.
5. **Needing the owner: what the operations log physically IS.** The book tells a reader to write
   in it on nearly every service page and never says what they are writing on. **This is the only
   thing on this list the owner has to answer, and it is waiting.**

**Not this step:** printing more — nothing in the running order is unprinted. Not this step:
reopening the running order; it was reopened twice on 2026-07-22, each time on a ruling, and is
closed again.

**Everything that happened and why is in `PRESS-LOG.md`.** Read it before printing anything. The
*how* is worth more than the *what*, and one finding matters more than any dish:

> **The checks that give a verdict do not find the faults.** On 2026-07-22 the taster returned
> SERVE 5/5 on every page it saw and caught none of the six faults found that day. Every one came
> from a checker sent to hunt something specific, or from reading a diff and redoing arithmetic.
> A verdict confirms that what is on the page is correct. It cannot see what was deleted, what was
> never reached, or what was counted wrongly.

### Two sessions worked this repository at once, and it cost real work

On 2026-07-22 two sessions carried out the same four decisions in parallel. One of them asked
the owner about the method verdict on a false premise — chapter 29 declared the question open,
and **chapters 30 and 31 had already answered it in the bound book.** Its version would have
put the contradiction back in. It was discarded and this branch reset to the other session's
work, which had found the real fault and corrected the running order at source.

**This is chapters 30 and 37 happening to the shop that printed them** — two workers at one
bench, and a session unsure which copy it was standing in. If more than one session works here
again, one of them owns the repository and the other reads only.

**It happened again on 2026-07-23, one day later.** Two head chefs cooked the same ticket —
chapters 9 and 10 — in parallel for about half an hour, committing into the same folder minute
by minute, each mostly re-finding what the other had already found. **The rule above did not
prevent it, because neither session could tell it was happening until commits appeared under
its feet.** Two things came out of it, and they point opposite ways:

- **The duplication was pure waste**, and one session's checks had to be thrown away entirely
  because the page changed underneath them mid-check.
- **It is also the only reason the fifth regression was caught**, because the second chef
  re-read a diff the first had already declared finished.

**That is an argument for a second pair of EYES. It is not an argument for a second pair of
HANDS.** The lesson is the one the book already teaches: the checker is not the cook. A second
session that only reads costs nothing and catches things; a second session that also writes
costs the work twice and moves the page while it is being checked.

**Done looks like:** every chapter written, tasted, swept for contradictions, and bound into a
book that does not contradict itself.

**Not this step:** reopening the running order. Reopening the print shop roster. Hiring
anyone. Sending the owner anything that is not a decision.

## Steps behind us

- **The whole-book read — done, 2026-07-22.** Ten whole-book passes for about thirteen pence.
  Both surviving findings were raised by both workers independently, and every quote was checked
  against the real chapter before it was believed. **The sharpest thing found was the manager's,
  not a worker's, and it came out of that checking:** chapter 2 does not merely omit the sixth
  word, **it uses it** — *"the people who make the dishes"*, *"whether the dish is acceptable"* —
  taking this book's own worked-example word for the one thing it never settled. No page-level
  check saw it, because on chapter 2's own page there is nothing wrong.
- **Chapter 2 reprinted and chapter 3 corrected — done, 2026-07-22.** Both faults the whole-book
  read found are now closed and bound. **The run's real finding was not about the page.** Three
  checks that ask *"is what is written correct?"* passed a reprint that had weakened a
  load-bearing rule, because everything left on the page was correct. The chair that asks *"what
  is missing?"* caught it, for the second time here. **The owner also caught that a frontier
  model was being spent on one-line jobs while never being run at its top reasoning levels; the
  routing in `THE-PRINT-SHOP.md` was rewritten on that direction.**
- **The record of that read was itself checked, and it was wrong.** The manager wrote it, so two
  checkers that did not write it were given it. One caught the manager crediting the workers with
  the manager's own catch — **a confident claim about something nobody opened, the fifth
  instance, inside the entry recording a run whose entire purpose was catching two documents that
  disagree.** Corrected, and the correction is in `PRESS-LOG.md`. **The lesson is not that the
  manager slipped. It is that the record was only right because something other than the manager
  read it.**
- **The overnight run — batches four to ten, chapters 17 to 50.** **Thirty-four chapters
  printed, checked four ways and bound in one night.** The book went from seventeen chapters
  to fifty-one. Parts Three, Four, Five, Six and Seven all written end to end.
- **Seventeen of those thirty-four went back once, and the reader found sixteen of them.** The three checks that
  give a verdict — the head chef's mechanical list, the taster, the rule-by-rule sweep — did
  not find one fault in a page across seven batches. They were not asleep: both were tested
  against pages broken on purpose the same night and both quoted the planted faults verbatim.
  **They answer whether what is written is correct. Only the reader asks whether it is all
  there** — and that is the question that found a missing pass counter, two chapters naming
  nobody, a chapter skipping its own line in the running order, a book that had blocked its
  own growth past one cook, a role called by two names, and a book that had started telling
  readers about its own reprint queue.
- **Every check was measured rather than trusted.** A page was broken on purpose and shown to
  the taster: it caught two faults of three, and **missed the planted contradiction while
  scoring contradiction 5/5 — its third failure from three attempts.** The sweep caught that
  exact sentence. So the taster's contradiction score is recorded as *not asked*, and the
  sweep is the only contradiction evidence this shop has.
- **The sweep flagged five clean pages and no faulty one** — every time the book quoting its
  own settled rule, and **three of the five on one seam**: the menu being both an instruction
  and local. None was overruled by the manager; each went to a worker that had produced
  neither verdict. **The check was not loosened**, because every error ran in the safe
  direction — and three trips on one seam is the check saying two rules genuinely disagree.
- **The taster rejected a clean page once**, calling the doctor an outside-world comparison
  when the doctor is one of the seven base roles. The page was not touched; the checklist was,
  because its furniture list named a doorman and never named the doctor. Re-tasted unchanged:
  SERVE.
- **Batch three (chapters 12-16)** — bound, after chapter 13 was sent back for jargon in its
  flat rules and chapters 10 and 12 were sent back for contradictions the rule-by-rule pass
  found. Chapter 12's fault was in its flat rules and it had already passed two rounds of
  tasting with straight fives.
- **The checks were rebuilt in a day, three times.** Tasting missed a quiet rule reversal
  twice, even with the rule quoted in front of it — so contradiction moved to its own
  rule-by-rule pass. The analogy check was then too loose, then too tight, then right.
- **The roster changed on evidence.** Hy3 came in unproven and now holds the tasting and the
  contradiction pass. DeepSeek stopped approving pages and now reads for what is missing.
  Qwen was let go. kimi-k3 was tested and not hired.
- **Batches one and two (chapters 2-11)** — bound.
- **The showdown, chapter 0 and the template** — done.

## The five rules

1. **Name the step** at the top of every reply, so drift shows in the first line instead of
   three paragraphs down.
2. **Park, do not chase.** Anything spotted further up the road goes on the list below. It is
   not lost, and it is not answered now.
3. **Either of us can call drift** — the owner to the head chef, and the head chef to the
   owner. Called drift means stop and look at the peg. Not a complaint; a course correction.
4. **Say what you are assuming, every time.** An assumption named out loud is a decision the
   owner can overrule. An assumption nobody noticed is a foundation nobody checked — and
   everything built on top of it comes down together. The danger is never the wrong guess; it
   is the guess that was never labelled as one.
5. **Write every hole down, and close it.** Weaknesses go in `KNOWN-HOLES.md` the moment they
   are spotted. Closing them is the whole reason this book is being written; a chapter does
   not ship with an open hole in it.

## Parked for later

Things worth deciding, at the step where they belong.

| Parked | Belongs to |
|---|---|
| Where the job list lives when a kitchen has no GitHub — plain documents, a structured file, or a small database | writing the job-list chapter |
| Whether the book is published openly from day one, or kept private first | before publishing, not before writing |
| Whether the same staff work across every restaurant, or each hires its own | writing the staffing part |

## Steps behind us

- **Set up the print shop** — done. A separate repository, its own history.
- **Test print** — done, passed. A rule delivered by the book is obeyed like a hand-written
  one, proven in a fresh session in an empty folder.
- **First running order** — done, then rebuilt. The first draft ran straight into *how a
  chain is run* without ever saying what a restaurant contains. The owner caught it. The
  inventory now comes first, and everything else is written on top of it.
- **The running order** — SETTLED end to end and signed off by the owner, 2026-07-21. Eight
  parts, 51 chapters, every part carrying a governing rule. `CONTENTS.md` is closed.
- **The chain part (Part Five)** — settled. Instructions travel, records never do. A new
  restaurant inherits every written instruction unchanged and nothing else. The menu is
  local; the recipe never is. A chain is a measuring instrument for the manual.
- **The base framework (Part Three)** — settled. Seven roles and three pairs of hands, three
  checks on three different questions, one door for changing the manual, and no service
  without a checker. Part Four has its governing rule: nothing is delegated until it is
  written down well enough for a stranger to do it.
- **The inventory (Part Two)** — settled. Eleven categories, each with a test for what
  belongs in it, so a new owner can sort their own things without asking us. The last thing
  settled: a stocktake and a log are two different records and must never be one thing.
