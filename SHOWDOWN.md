# The showdown — choosing the printer

**Status: design agreed, not yet run.**

Sol is the expensive chair. Before fifty chapters are printed in it, it has to earn it
against cheaper hands, on the actual job, measured — not chosen because a routing table
written for code says so.

## What is being decided

**Who prints the chapters.** One job, one winner. This does not reopen the taster, the
binder, or the junior's prep work — those were staffed on strengths nobody is disputing.

## The competitors

Four, spanning the whole price range, chosen so the result actually answers the question:

| Printer | Why it is in the ring |
|---|---|
| **Codex 5.6 Sol**, high effort | The expensive incumbent. The one on trial |
| **DeepSeek V4 Pro** | The strongest cheap alternative. Excluding it would rig the test |
| **Hy3** (Tencent) | The junior, about a third of DeepSeek. If it can print, the economics change completely |
| **GLM 5.2**, max effort | The routing table says it is for small mechanical work. This tests whether that is true of prose, or just assumed |

**Claude does not compete.** The manager never prints, and a manager who competes cannot
reject the pages fairly afterwards.

## The task

All four write **the same chapter — ch. 1, The interview** — from the **same brief**, word
for word identical, with no knowledge of each other's work. Chapter 0 is written by hand
first, because the template has to come from someone doing the job before it can be handed
to anybody.

## The matrix

Scored out of 100. Every score is recorded with its reason, so any line can be rechecked by
someone who was not there.

### A. Following the template — 40 points, objective

Anybody can verify these. No judgement involved.

| # | Test | Points |
|---|---|---|
| A1 | Every section the template requires is present | 10 |
| A2 | Covers everything the running order assigns to that chapter | 10 |
| A3 | Contradicts nothing already settled in `CONTENTS.md` or `KNOWN-HOLES.md` | 10 |
| A4 | Within the length bound | 5 |
| A5 | Jargon count — words that only mean something to a programmer. Zero scores full | 5 |

### B. Quality — 60 points, judged blind

| # | Test | Points |
|---|---|---|
| B1 | A non-technical reader understands it on the first read | 25 |
| B2 | It sounds like this book — plain, analogy-first, short declarative sentences | 20 |
| B3 | Uses the agreed analogies and invents no competing ones | 15 |

### C. Cost and time — measured, never blended into the score

Recorded separately and deliberately kept out of the total: **money against quality is the
owner's judgement, and a single blended number would hide it inside a formula.**

| Measured | Reported as |
|---|---|
| Money spent on the page | Dollars, and projected across all 51 chapters |
| Wall-clock to produce it | Minutes |

**The winner is declared on score. The owner decides whether that win is worth its price.**

## Judging, and how it is kept honest

- **Blind.** The four pages are saved as `printer-a` … `printer-d`. Nobody scoring them knows
  which model wrote which. The key is held back until every score is in.
- **Section A is scored by the print manager**, and shown as a filled-in checklist rather
  than a number, so the owner can recheck any line without trusting it.
- **Section B is judged by a model that is not competing**, so no one is marking their own
  work — the same rule the kitchen runs on.
- **The owner is the final word on B2.** The book's voice is his way of seeing; no model and
  no manager can overrule him on whether a page sounds right.
- **Everything is kept.** The brief, all four pages verbatim, every scorecard, and the key —
  committed to this repo. A showdown nobody can recheck is an opinion with a table around it.

## The known weakness of this test

One chapter is one data point. The real risk with a printer is not a bad page — it is a
**voice that drifts over fifty pages**, and a single chapter cannot show that. So the winner
is on probation: the first five real chapters are read as a set, and if the voice wanders,
the showdown is rerun with what was learned. That reread is written into the plan now, before
anyone has a stake in the result.
