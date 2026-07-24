# The worked example — settle contested claims by proof, not by who's speaking

A research note for the chapter that carries the house rule. It does two jobs: (1) show that the
shop making this book **already practices every part of the rule**, with cited evidence; (2) distil
**one** concrete worked example the chapter can carry — a disputed claim settled by proof rather
than by rank.

The rule under study, as a HYPOTHESIS the shop has been testing on itself:

> **A claim is settled by a run, a measurement, or an independent check — never by who said it or
> how authoritative it sounds. Authority may propose; it may not close.**

---

## 1. How the shop already practices each part of the rule

### INDEPENDENT CHECKER — the taster never checks the dish it didn't make; the sweep is a *separate* pass by a *different* worker

- **The taster is never the cook.** `TASTING-CHECKLIST.md` → "The rule that outranks all of the
  above": *"The taster never wrote the page it judges. Not in this session, not in another. If the
  only available taster wrote it, the page is not tasted today."* The same rule in the book at
  `book/19-checking-it.md` flat rule 2, and as load-bearing invariant 5 in
  `press/core-invariants.json`: *"Nobody ever checks their own work… The taster never cooked the
  dish it judges."*
- **The contradiction sweep is a separate pass run by a different worker than the taster** — and
  the reason it had to be separate is *measured*, not asserted. `THE-CONTRADICTION-PASS.md` →
  "What was measured": a chapter was broken on purpose (the log rule reversed, see the planted
  sentence at `press/control-ch12-seeded.md` lines 54–55) and handed to the taster. The taster
  **SERVED it twice**, even with the broken rule quoted in the prompt and scored 5/5 on
  contradiction. Decomposing the question rule-by-rule ("quote the sentence that makes THIS rule
  untrue, or say NONE") caught it, quoted verbatim. So the sweep was split off as its own pass,
  now held by a different worker (Hy3) than the taster — `THE-PRINT-SHOP.md` roster rows
  "Page taster" and "The contradiction pass."
- **The ban is on the specific work, not the family.** `THE-PRINT-SHOP.md` → "The rules this shop
  runs under" rule 2: whoever printed page 20 may not taste page 20, but a *fresh* session that
  never saw the work is a different worker. Independence is about not having seen the work, not
  about the model family.

### PRE-NAMED ACCEPTANCE TEST — the head-chef mechanical list, the 700-word ceiling, the seeded "control page" with a planted fault

- **The head-chef's list is mechanical where possible, so it is evidence rather than opinion.**
  `TASTING-CHECKLIST.md` → "The head chef's list": title matches `CONTENTS.md` exactly; the
  *What this chapter settles* line is one sentence; `## The rules, flat` is numbered and
  imperative; **every flat rule traces to the body**; **body under 700 words**; zero programmer
  jargon. Any failure here is sent back *without troubling the taster*. Implemented as a script
  that returns numbers, not a verdict: `press/head-chef-check.py`.
- **The 700-word ceiling is enforced by a tool**, not by a reader's impression. `TICKETS.md` →
  T-18 records the first harvest: `data/page-metrics-2026-07-23.json`, all 51 pages, **none over
  the 700 ceiling**; the script reports the number, which can be re-read and diffed.
- **The seeded control page is a pre-named acceptance test with a known answer.** A page is broken
  on purpose and used as the **entrance exam** for any worker proposed as a checker.
  `press/control-ch12-seeded.md` carries one extra sentence (lines 54–55) that reverses invariant 1
  ("the log is NEVER rewritten"); `press/entrance-exam.py` sits any candidate in front of it and
  records a *fact* — caught it, or missed it. Results in `THE-CONTRADICTION-PASS.md` → "The exam":
  **Hy3 caught it; kimi-k3 caught it at sixteen times the price; DeepSeek V4 Pro missed it three
  times.** That table is what "expertise is evidence, not proof" looks like as a number (next item).

### INDEPENDENT CONFIRMATION — a page binds only after *every* check launched against it returns

- The shop adopted this as a **standing guard after a measured fault**: chapter 10 was tasted
  SERVE, *bound*, and a later run of the same check returned SEND BACK on a real fault.
  `KNOWN-HOLES.md` row "A chapter was bound while a second check on it was still running" →
  standing guard: *"nothing is bound until every check launched against it has returned."*
  Repeated in `TICKETS.md` → "Not filed as tickets, and why" (the adopted discipline list).
- A flag raised by the sweep is **not ruled on by the manager alone**. `THE-CONTRADICTION-PASS.md`
  → "When the sweep flags a page, the manager does not rule on it alone": the flag is settled by
  *a worker that produced neither verdict*, given the sentence, the rule and the running order's
  own words, and an explicit instruction to be willing to call the flag real. The reason given is
  the manager's own temptation: *"a manager who overrules a check on its own judgement has quietly
  become the check."* (Adjudication artefacts are themselves an open hole — `KNOWN-HOLES.md` row
  "The shop keeps no artefact of an adjudication"; `TICKETS.md` T-16.)

### EXPERTISE IS EVIDENCE, NOT PROOF — a credible worker's claim still gets checked; the "reader" reads for what's missing rather than approving

- **The reader's chair gives no verdict by design.** `THE-PRINT-SHOP.md` → "The reader": *"Its real
  strength is heavy reading. It is poor at approving and good at noticing, so it is asked what is
  absent rather than whether a page passes."* Across seven batches it was the only question that
  found anything — `PRESS-LOG.md` batches four and five: *"The reader found all ten"* sent-back
  pages that three verdict-giving checks had passed.
- **A credible worker's claim is still checked.** The manager reported as fact that the taster of
  record had *never* rejected a page. That was false — it came from a script that counted a data
  field and missed a prose answer. `THE-PRINT-SHOP.md` → "A correction, because the manager got
  this wrong first time": *"A count is not evidence until you have looked at what it skipped."*
- **A worker is not promoted on impression, however good it sounds.** `THE-PRINT-SHOP.md` → "What
  is actually true": all three of DeepSeek, Qwen and Hy3 reject when a fault is obvious; **only one
  has ever caught a fault that was hiding.** The credible name is hired on the measurement, not on
  its model card. kimi-k3 *passed* the entrance exam and was still **not hired**, because sixteen
  times the price for the same answer is not earned — `THE-PRINT-SHOP.md` → "Tested and not hired."

---

## 2. The worked example the chapter can carry — the rule proving itself

**The dispute.** The hardest contested claim in this kitchen is not about a page. It is the rule
itself: *should "settle by proof, not authority" be a load-bearing rule of this book at all?* The
authority answer is cheap and always available — "the head chef says so, and the head chef is
credible." Closing the question that way would be exactly the fault the rule warns against.

**How it was settled instead — by proof, four times over, then by an independent reviewer family.**

1. **The rule was not asserted; it was measured on the shop's own pages.** The shop's central
   finding is that a verdict-shaped check cannot see a missing word. This was *not* an argument —
   it was a controlled experiment: the same chapter (`press/control`-style, fingerprint
   `8a89d72e…`), damaged and undamaged, through the same two checks. With the load-bearing word
   *only* deleted, **the taster returned SERVE 5/5 and the sweep raised one flag — on a different,
   correct, sentence.** Neither check saw the deletion. `KNOWN-HOLES.md` row "A deleted word in a
  load-bearing rule passes every automated check this shop has"; `CHANGELOG.md` 2026-07-23, "The
   measurement that matters more than the pages." A claim that could have been asserted on the
   head chef's credibility was instead reduced to a fingerprint anyone can re-run.

2. **The contested chair was settled by measured contest, not by the model card.** Who prints the
   book was a real dispute. The model card would have settled it by authority. Instead the owner
   called a re-contest with **real metrics and four difficulty levels**; the deciding level was one
   that instructed the printer to break a settled rule, and **only one of five entries refused**.
   `showdown2/RESULTS.md`; `THE-PRINT-SHOP.md` → "The chair changed hands, on measurement." The
   verdict names what it refused to do: *"naming a model to a job off its model card is promotion
   on impression, which is the thing this book exists to prevent."*

3. **The pre-named acceptance test was committed before the result was seen.** The printer showdown
   was blind — *"the key was written before any page existed and no judge ever received it"*
   (`showdown2/RESULTS.md`); the seeded control page is a chapter with a planted fault and a known
   answer, sat in front of any candidate as an **entrance exam** (`THE-CONTRADICTION-PASS.md` →
   "The exam"). This is the rule's cheapest, best-measured mechanism: state how the claim will be
   judged *before* you see whether it flatters you.

4. **The rule was confirmed by an independent reviewer family, not by the head chef.** The
   literature review behind the rule (`research/proof-over-authority.md`) was corrected by a
   **cross-family reviewer (Tencent `hy3`, 2026-07-23 independent review)** that found a real error
   — Finding C had conflated the Asch peer-conformity result with the Milgram authority-obedience
   result. The correction was **left visible** in the file rather than silently swapped, which is
   the shop's own "the log is never rewritten, only added to" discipline turned on the research
   about the rule. The head chef's say-so was never the closer; an independent family was.

**The punchline for the chapter.** The rule "settle by proof, not authority" was itself settled by
proof, not authority. A reader who asks "but who says the taster can't be the cook?" can be answered
the weak way — "the head chef" — or the strong way: **"here is a chapter broken on purpose that the
taster certified clean; here is a fingerprinted page where every verdict-shaped check missed a word
the rule depends on; here is a chair that changed hands because one model of five refused to break a
rule."** The strong answer does not invoke rank at all. That is the worked example: the moment the
kitchen's own rule is paid for in the kitchen's own coin.

**Why this beats a generic example.** A borrowed example (a clinical trial, a famous obedience
study) demonstrates the rule in someone else's kitchen. This one demonstrates it in *the reader's*
kitchen, while they are reading it — the rule is measured on the very book in their hands. It is
also the sharpest self-reference the shop has produced: the discipline that says "a record is never
silently edited" was applied to the record of the discipline itself.
