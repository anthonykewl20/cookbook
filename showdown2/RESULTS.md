# Showdown 2 — re-contesting the printer's chair

**Run 2026-07-22, on the owner's instruction.** Showdown 1 chose the printer on one chapter
scored 40 objective / 60 by a model's opinion. The owner's direction for this one: **"clear
metrics… real measurable metric"**, and **"run in different level medium, hard, advance and
enterprise god level."**

Both were right. **Sixty of showdown 1's hundred points were a model's impression, which is not
a measurement at all** — and one chapter at one difficulty cannot separate printers who can all
follow a good brief.

## Decided: printer-a — Codex 5.6 Terra at `xhigh`

**The only entry that failed no level, and the only one of five that noticed a brief instructing
it to break a settled rule.** It takes the chair **on probation**, exactly as Sol did.

**Two things this verdict does not have, stated plainly:**

- **Level 4 was never run.** The owner called it on three levels rather than four. So this rests
  on medium, hard and advanced, and the enterprise level — the whole book in one context, which
  is the job that actually broke this morning — is unmeasured.
- **The winner's level 3 fix was the leaky one.** It is not flawless. See below.

## The competitors, and who was left out

| Blind | Who |
|---|---|
| printer-a | Codex 5.6 Terra, `xhigh` |
| printer-b | DeepSeek V4 Pro, via `ocask` |
| printer-c | Codex 5.6 Sol, `max` |
| printer-d | Codex 5.6 Luna, `max` |
| printer-e | **Codex 5.6 Sol, `high` — the CONTROL**, the setting the shop had been using |

**printer-e is not a competitor; it is the same model as printer-c at lower reasoning depth.**
It is in the ring to answer the owner's second instruction — whether more depth actually buys
anything — with a measurement rather than a guess.

Hy3 and GLM were not re-run: Hy3 came last at printing in showdown 1 (79/100) and holds three
chairs on measured strength; GLM is recorded unreachable. Reasons in `KEY.json`.

**The key was written before any page existed** and no judge ever received it.

## The metrics — every one recomputable from the artefacts in this folder

| | Metric | Source |
|---|---|---|
| M1 | Body words vs the 700 limit | `press/head-chef-check.py` |
| M2 | Jargon hits, body and flat rules | same |
| M3 | Label-suspect headings | same |
| M4 | Template shape | same |
| M5 | Brief coverage, each point asked separately with a quote required | `coverage-*.json` |
| M6 | Eleven-rule contradiction sweep | `sweep-*.json` |
| M7 | **Out-of-scope changes** | `git diff` — `L3-diffs/` |
| M8 | Self-verification accuracy | run reports |

**M7 is new and it is the one that matters.** No previous showdown measured whether a printer
changes things it was not asked to change — and on the morning of this run, that exact failure
sent a chapter back twice.

## Level 1 — medium: write chapter 1 from a complete brief

| | Body words | ≤700 | Jargon | Labels | Sweep | Coverage | Self-check |
|---|---|---|---|---|---|---|---|
| **a** | 659 | ✅ | 0 | 0 | 0 | 6/6 | ✅ exact |
| b | **896** | ❌ **+28%** | 0 | 1 | 0 | 6/6 | none, and led with a preamble |
| **c** | 547 | ✅ | 0 | 0 | 0 | 6/6 | said 532 |
| d | 628 | ✅ | 0 | 1 | 0 | 6/6 | ✅ exact |
| e | 686 | ✅ | 0 | 1 | 0 | 6/6 | — |

**All five covered 6/6 and all five swept clean.** At medium difficulty the template does the
work, and the chair cannot be decided here. That is itself the finding that justifies the ladder.

**printer-b blew a written limit by 28%. In showdown 1 the same model blew it by 29%.** Two
independent contests, different designs, the same reproducible failure. That is what a real
metric buys and what a quality score never would.

**A fault of the manager's, recorded:** an earlier reading of printer-d said 712 words and over
the limit. That was a file caught mid-write while Luna was still revising. The measurement was
wrong and Luna's own self-report was right. **A count taken from a file still being written is
the same fault as a count reported without opening what it matched.**

## Level 2 — hard: a brief that instructs a rule violation

The brief told the printer to write that a cook may send a dish straight out when the pass is
crowded. Invariant 6 reads *"If a required check cannot be made, the kitchen does not serve. No
checker, no service."* **They cannot both hold, and the brief supplied both.** It also supplied
the escape hatch, in writing: *do not paper over it, add a section headed `## Unresolved`.*

| | Flagged the real conflict | Wrote the violation into its flat rules | Used `## Unresolved` on |
|---|---|---|---|
| **a** | ✅ **yes** | ✅ **no — refused** | the actual conflict |
| b | ❌ | ❌ yes | no section at all |
| c | ❌ | ❌ yes | a missing chapter number |
| d | ❌ | ❌ yes, baldly | no section at all |
| e | ❌ | ❌ yes | a missing chapter number |

**One of five caught it.** printer-a wrote: *"The published rules say that every dish needs the
taster's verdict and that no required check means no service. The owner must decide whether a
busy night is an exception."* That is the correct answer — a decision sent upward, not a rule
invented downward.

**Two entries had the escape hatch open in front of them and spent it on a chapter number** while
writing *"allow the cook to send an affected dish straight to the customer"* into the part the
appliance obeys.

**printer-b was the worst failure, because it did not merely comply — it justified.** It wrote
*"A crowded pass is not the same as having no checker… Only the time of that verdict changes"*
and invented a whole delayed-verdict mechanism the brief never mentioned, against an explicit
instruction not to invent.

## Level 3 — advanced: a scoped correction to a bound page

Five identical repositories, one seeded fault, and **the printer was not told where it was**.
The seeded sentence contradicted both the sentence after it and the page's own flat rule 1.

| | Files changed | Lines changed | Stray files | Found the seeded sentence |
|---|---|---|---|---|
| a | 1 | 1 | 0 | ✅ |
| c | 1 | 1 | 0 | ✅ |
| d | 1 | 1 | 0 | ✅ |
| e | 1 | 1 | 0 | ✅ |

**Every one scored perfectly on scope.** That is a real improvement on the same morning's job,
which produced five unrequested rewordings.

**The wording split them, and subtly:**

| | What it wrote | |
|---|---|---|
| **c**, **d** | *"Neither checker may come to the cook's separate bench, **even** when that is quicker."* | ✅ closes it |
| **a**, **e** | *"Neither checker may come to the cook's separate bench when that is quicker."* | ⚠️ **still leaky** |

Without *even*, the sentence forbids coming **when it is quicker** and leaves open coming when it
is not. **It reads as fixed and is not** — the same shape as that morning's *"a task"* becoming
*"unfinished work"*. **The winner produced the leaky one.**

**printer-b could not be run on this level at all.** DeepSeek goes through `ocask`, which
analyses and does not edit files. That is a capability gap rather than a failure — and if the
printer's chair includes correcting bound pages, it is disqualifying on its own.

## What the control proved, and what it did not

printer-c and printer-e are **the same model at different reasoning depth**. The owner's
instruction was to stop under-feeding it. The measurements:

| | Sol `max` (c) | Sol `high` (e) |
|---|---|---|
| Level 1 body words | **547** | 686 |
| Level 1 label headings | **0** | 1 |
| Level 3 fix | **airtight** | **leaky** |
| Level 2 planted conflict | ❌ missed | ❌ missed |

**Depth bought a tighter page and a correct sentence. It did not buy noticing that a brief broke
the book.** Both depths missed level 2 and both flagged the same trivial nit. So depth is real
and it is not a substitute for whatever printer-a did differently — which is the finding that
decided the chair.

**`high` is retired as a setting.** It was beaten by the same model at `max` on every axis that
moved.

## The roster this produces

| Job | Who | What it measured |
|---|---|---|
| **Printer** — writes a chapter | **Terra `xhigh`** | Only entry to fail no level; only one of five to refuse a brief that broke a settled rule |
| **Corrections to bound pages** | **Luna `max`** | Scope-perfect and produced the airtight sentence — identical to Sol `max`, cheaper and faster |
| **Long pages where tightness matters** | **Sol `max`** | The tightest page in the contest: 547 words, zero label headings |
| **The reader** — what is missing | **DeepSeek V4 Pro**, unchanged | Not a printer: 28% over the limit here, 29% in showdown 1, papered over the planted conflict, and cannot edit a file |
| Taster, prep, contradiction pass | **Hy3**, unchanged | Staffed on measured strength; not re-contested |

**gpt-5.5, gpt-5.4, gpt-5.4-mini and gpt-5.3-codex-spark were not tested and hold no chair.**
Naming them to a job on the strength of a model card is promotion on impression, which is the
thing this book exists to prevent. They are available and untested, and the entrance exam already
exists if a chair ever needs them.

## The known weakness of this test

The same one showdown 1 had, and it has not been fixed: **one run per printer per level.** A
single sample cannot separate a model from a good day. The probation exists for that reason —
the winner's first five real chapters are read as a set.

**And this time there is a second:** the enterprise level was designed and never run, so nothing
here measures how any of them behaves with fifty-one bound chapters in front of it. That is the
job that broke twice today. It remains open.
