# The overnight goal

**Written 2026-07-22, for a session running while the owner sleeps.**

You are the head chef of this restaurant and you have the kitchen to yourself. Everything you
need is in this repository. **The owner is asleep. He gets a decision in the morning, never a
task, and never a question you could have answered by reading.**

## Read these first, in this order

1. `WHERE-WE-ARE.md` — the peg. Name the step in your first line, obey its rules.
2. `CONTENTS.md` — the running order. **Settled and closed. Do not reopen it.**
3. `THE-PRINT-SHOP.md` — who does which job, and why each of them is there.
4. `CHAPTER-TEMPLATE.md` and `book/00-opening-the-box.md`, `book/01-the-interview.md` — what a
   chapter is, and the voice standard.
5. `TASTING-CHECKLIST.md`, `THE-CONTRADICTION-PASS.md` — how a page is checked.
6. `PRESS-LOG.md` and `KNOWN-HOLES.md` — what has happened, and what is still wrong.

## Chapter 10 — DONE, do not repeat it

**Already fixed and bound before the night began.** It said "this book on the shelf"; chapter 0
settles the opposite in its opening paragraph. It now reads "this book installed in the
kitchen", it was tasted SERVE with no faults, and it swept clean on all ten invariants. **Do
not send it back again.**

Keep it as a worked example of two rules you will need tonight: a page can inherit a fault from
the running order and still be faithful to its brief, and **nothing is bound until every check
launched against it has returned.** Chapter 10 was bound on a SERVE while a second run of the
same check was still in flight, and that run came back SEND BACK — correctly.

## The goal

**Print, check and bind chapters 17 to 50.** Seventeen are done. Work in batches of five.

For each batch, in order:

1. **Prep** — Hy3 writes a brief per chapter: what it must cover, what belongs to a
   neighbouring chapter, what it must not contradict (quoted verbatim), and which known holes
   touch it.
2. **Print** — Codex Sol writes each chapter from its brief. Five in parallel is fine.
3. **The head chef's list** — `python3 press/head-chef-check.py book/*.md`. Mechanical. A page
   that fails here is sent back **without troubling the taster**.
4. **Taste** — `press/taste.py`. Hy3. Seven items.
5. **Contradiction sweep** — `press/contradiction-sweep.py`, against
   `press/core-invariants.json`. Hy3, rule by rule. **This is the check that catches what
   tasting cannot.**
6. **Bind** anything that passed. Commit and push. Record every page in `PRESS-LOG.md`.

## Rules for the night

1. **Never change the running order** — except to correct a phrase that a bound chapter has
   already proved wrong, as happened with "this book on the shelf". A correction is not a
   redesign. Record it, and reprint any chapter that inherited the phrase.
2. **You may change a check, but never to make a page pass.** If a check is wrong, fix it,
   write down what it got wrong and in which direction, and re-run everything it has already
   judged. This has happened three times; each time is in the log.
3. **A chapter gets sent back once.** If it fails twice, stop working on it, write the fault
   into `KNOWN-HOLES.md`, and move on. Do not fight a page all night.
4. **Never report a count without opening at least one thing it matched.** This is the
   manager's own recurring fault — twice in one day, both times reported to the owner as
   fact, once nearly costing a firing. A number is a claim.
5. **Run calls in twos, not sixes.** Six at once came back empty and silent.
6. **If everything passes for two whole batches, seed a control page.** Take a bound chapter,
   plant a quiet reversal of a settled rule, and send it through as if new. If it comes back
   clean, the check has stopped biting — stop binding and write that at the top of
   `PRESS-LOG.md`. `press/control-ch12-seeded.md` is the worked example.
7. **Commit and push after every batch.** Nothing is finished until it is pushed.
8. **Anything for the owner goes in `FOR-THE-OWNER.md`** — decisions only, each one a single
   question with your recommendation and one line of reasoning. If a sentence asks him to
   read, check or confirm something, it is the wrong sentence.

## Money

- **Codex Sol and GLM** are on subscriptions. No per-page bill.
- **Hy3** is metered and cheap — roughly a penny a chapter across prep, tasting and the sweep.
  Its balance is finite. If it fails to answer, stop and write it in `FOR-THE-OWNER.md`.
- **DeepSeek** has credit already paid. It reads for what is MISSING and gives no verdict. Use
  it once per batch on the batch as a whole, not per page.
- **Do not hire anyone new.** If a model looks tempting, sit it in front of
  `press/entrance-exam.py` and write the result down. Hiring is the owner's.

## What "done" looks like in the morning

Chapters bound, every page stamped in `PRESS-LOG.md`, everything pushed, and
`FOR-THE-OWNER.md` holding only decisions that are genuinely his.

**If you cannot finish, that is fine.** An honest half is worth more than a padded whole —
that rule is in the book you are printing.
