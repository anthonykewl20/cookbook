# The contradiction pass

**A separate check, run separately, because the taster cannot do it.** That is not an opinion
about the taster. It was measured twice, and it failed twice.

## What was measured

A page was broken on purpose: chapter 12 — the chapter that establishes **the log is never
rewritten** — was given one extra sentence.

> *"If a stamp was written down wrongly, put it right the moment the mistake comes to light.
> A log nobody trusts is worse than no log, so accuracy comes before tidiness of record."*

It sounds like good practice. It reverses the rule the chapter exists to establish. Then the
page was handed to checkers as if it were new.

| Attempt | Question asked | Result |
|---|---|---|
| 1 | Taster's five-item list, holistic verdict | **Both tasters SERVED it** |
| 2 | Taster's list extended to seven items, contradiction named, the broken rule quoted in the prompt, the item flagged as new and important | **Both tasters SERVED it again — and scored contradiction 5/5** |
| 3 | **Rule by rule: "quote the sentence that makes THIS rule untrue, or say NONE"** | **Caught, quoted verbatim, against both rules it breaks** |

**Attempt 2 is the important one.** The checker was told exactly what to look for, given the
rule verbatim, and told the item mattered. It still certified the page as free of the fault it
was holding. **So the wording was never the problem — the shape of the question was.**

A holistic verdict makes a reader average a page into an impression, and an impression cannot
see one reversed sentence in six hundred words. Asking rule by rule forces a search instead of
an impression.

## The rule this establishes

> **A check that returns one verdict for a whole page cannot find a fault that lives in one
> sentence.** Decompose the question until each answer has one place to hide.

## The false-positive control

Every run is done twice — once on the broken page and once on the correct one. A checker that
flags the correct page is not being careful, it is being useless in the other direction. Both
workers that passed returned NONE on all ten rules for the clean page.

## The exam

`press/control-ch12-seeded.md` is now the **entrance exam** for any worker proposed as a
checker. It has a known answer. Anyone can be sat down in front of it, and the result is a
fact rather than an impression.

Results so far:

| Worker | Sabotaged page | Clean page | Price per page | Verdict |
|---|---|---|---|---|
| **Hy3** | **caught it** | clean | ~$0.003 | Passed |
| **kimi-k3** | **caught it** | clean | **$0.048** | Passed, at sixteen times the price |
| DeepSeek V4 Pro | missed it, three times | clean | — | Failed |

## What it runs against

`press/core-invariants.json` — the book's ten load-bearing rules. Every chapter is swept
against all ten before it is bound in.
