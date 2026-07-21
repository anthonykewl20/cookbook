# The showdown — results

**Still blind.** The key naming which model wrote which page is deliberately not in this
commit. It lands when the owner has given his verdict on the two finalists, so that the
order of events is on the record rather than asserted afterwards.

## Section A — following the template (40)

Scored by the print manager. A1, A4 and A5 come from a script anyone can rerun
(`mechanical-checks.json`). A2 and A3 are read judgements, and their reasons are given so
they can be argued with.

| | A1 shape /10 | A2 coverage /10 | A3 no contradiction /10 | A4 length /5 | A5 jargon /5 | **A** |
|---|---|---|---|---|---|---|
| printer-a | 10 | 10 | **8** | 5 (681) | 5 | **38** |
| printer-b | 10 | 10 | 10 | 5 (612) | 5 | **40** |
| printer-c | 10 | 10 | **7** | 0 (737) | 5 | **32** |
| printer-d | 10 | 10 | 10 | 0 (903) | 5 | **35** |

**All four** produced the title, the *what this chapter settles* line and numbered flat
rules, covered all six things the brief required, and scored **zero on jargon**. The
template held across every printer, which is itself a result: the template is doing its job.

**A3 deductions, with reasons:**

- **printer-a (8).** Its list of the six things to name fills them in with this book's own
  words — the chef, the taster, the appliance, the dish — a few lines after saying those
  words are only one owner's example. It also imports "the taster is never the cook", which
  is a Part Three rule and not language.
- **printer-c (7).** It opens by stating "Your chain is a set of restaurants. The chefs are
  the workers. The dishes are units of work" as plain fact, then later says those same words
  are examples nobody has to use. The chapter contradicts itself inside four paragraphs.

**A4 is binary** because the brief made it a hard constraint. Two printers stayed inside 700
words. Two did not, one of them by 29%.

## Section B — quality (60)

Judged blind by a model that was not competing, against chapter 0 as the voice standard.

| | B1 understood /25 | B2 sounds like the book /20 | B3 agreed analogies /15 | **B** |
|---|---|---|---|---|
| printer-a | 20 | 16 | 14 | **50** |
| printer-b | 22 | 16 | 14 | **52** |
| printer-c | 19 | 14 | 14 | **47** |
| printer-d | 24 | 19 | 15 | **58** |

Judge's ranking: **d, b, a, c**. Its reasons are in `judge-verdict.json` verbatim.

## The matrix

| | A /40 | B /60 | **Total** | Time | Price of the page |
|---|---|---|---|---|---|
| printer-b | 40 | 52 | **92** | 72s | not metered — subscription |
| printer-d | 35 | 58 | **93** | 88s | ~$0.002 (estimated from the rate card) |
| printer-a | 38 | 50 | **88** | **731s** | not metered — subscription |
| printer-c | 32 | 47 | **79** | 41s | $0.0034 (measured) |

## What this does and does not show

**One point between the top two is not a result.** It is a single chapter scored by a single
judge, and a one-point margin out of a hundred is noise. Anyone who reports this as "d beat
b" is overreading it. The honest finding is that **printer-b and printer-d are tied**, and
they are tied in an interesting way:

- **printer-d writes better and obeys worse.** It won quality by six points and lost
  compliance by five, because it went 29% over a limit it had been given in writing.
- **printer-b was the only printer that checked itself against the constraint** before
  handing in — its run report states the word count it verified. Over one chapter that is
  a curiosity. Over fifty, it is the difference between a book and a pile of pages.

**Three findings that were not the question but matter more than the ranking:**

1. **The money question mostly dissolved.** Two of the four run on subscriptions, so the
   page has no invoice attached. The two that are metered cost a fifth of a penny each. Cost
   is not what should decide this.
2. **Speed varies by an order of magnitude.** 41 seconds against 731. Across 51 chapters
   that is the difference between an afternoon and several days.
3. **The cheapest printer came last on both axes** — but it was last by a small margin while
   costing almost nothing, which is exactly the profile of a good prep cook and a poor
   printer. That is the job it already has.

## The unresolved half

The owner is the final word on B2 — whether a page sounds like his book. No model can
overrule him on it, so the contest is not decided until he has read the two finalists blind.
That verdict, and the key, go in the next commit.
