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

## When the sweep flags a page, the manager does not rule on it alone

Measured over one night, the sweep produced **two false positives in sixteen pages**, and both
had the same shape: **it flagged the book stating its own settled rule.**

| Page | Quoted as a violation | Actually |
|---|---|---|
| Ch. 25 | *"Say what went wrong or what could be better."* | The running order puts opportunity in the log on purpose: *"Something goes wrong or could be better → it is written into the log"* |
| Ch. 28 | *"Raise the fault, add it to the log, report it upward and let the owner decide."* | That is the one door, stated almost verbatim. The owner gets a decision, which is what rule 10 requires |

A third instance predates this: the analogy check once flagged the book's own settled words
for the stocktake and the log.

### The remedy, which worked both times

**A flag is settled by a worker that produced neither verdict.** It is given the sentence, the
rule, the running order's own words, and an explicit instruction that it should be willing to
say the flag is real. It answers a few narrow yes/no questions and quotes what decides it.

This costs about a minute and a few pennies, and it exists because of one specific danger:
**the manager is the person most tempted to wave away an inconvenient flag at four in the
morning**, and a manager who overrules a check on its own judgement has quietly become the
check.

### The check was NOT loosened, and that is deliberate

Both false positives were wrong in the **safe** direction — questioning a clean page rather
than passing a broken one. Every failure that has cost this book ran the other way. On the
same night this sweep caught a planted reversal of *nobody checks their own work* and quoted
it verbatim, on a page the taster had just scored 5/5 for contradiction.

**A check that occasionally asks an awkward question and is answered on evidence is working. A
check softened until it stops asking is the one that ends up certifying a broken page.**
