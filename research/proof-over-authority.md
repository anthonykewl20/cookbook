# "Proof over authority" — is the house rule measured, or just asserted?

A deepen / literature-review pass. The house rule under test, as a HYPOTHESIS:

> "Neither the owner nor the head chef is assumed right, and neither is any confident-sounding source.
> A claim is accepted only on proof — primary/high-trust sources for facts, and a run, a measurement,
> or an independent check for design answers — never on who said it or how authoritative it sounds."

The job is to find the PRIOR ART and, critically, the MEASURED evidence base — and for each finding, mark
whether the support is **MEASURED** (a metric, a study) or **ASSERTED / normative** (a principle stated
as a should). That distinction is the whole point.

Sources fetched this pass (via search summaries; see "thin evidence" note at the end):

- Kaplan & Irvin 2015, NHLBI trials / pre-registration — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132382 and https://www.nature.com/news/registered-clinical-trials-make-positive-findings-vanish-1.18181
- Brynjolfsson, Hitt & Kim 2011, "Strength in Numbers" (DDD) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1819486
- Asch conformity — https://www.simplypsychology.org/asch-conformity.html
- Milgram obedience — https://courses.lumenlearning.com/waymaker-psychology/chapter/conformity-compliance-and-obedience/
- Fagan inspection / code review effectiveness — https://www.sciencedirect.com/science/article/pii/S0164121224001055 and https://eprints.bournemouth.ac.uk/18183/3/JearyPhalpMilsomHughesWebsterHolroyd.pdf
- Evidence-based medicine outcomes — https://www.ncbi.nlm.nih.gov/books/NBK470182/ and https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3028959/

---

## 1. The findings, each marked MEASURED or ASSERTED

### Finding A — Pre-registration: committing the test before seeing the result makes flattering-but-false findings vanish. **MEASURED (strongest single piece).**

Kaplan & Irvin (2015) looked at large NHLBI cardiovascular trials. **Positive results on the primary
outcome fell from 17 of 30 trials (57%) before 2000 to 2 of 25 (8%) after 2000** — a 49-point drop. The
coincident change: prospective registration on ClinicalTrials.gov went from **0% before 2000 to 100%
after**. The interpretation, in the authors' and Nature's words, is that pre-registration removed the
freedom to "measure a range of variables and select the most successful outcomes," i.e. it stripped out
selective reporting. Sources:
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132382,
https://www.nature.com/news/registered-clinical-trials-make-positive-findings-vanish-1.18181.

**Why it is the tightest support for the house rule:** this is proof-over-motivated-belief with a number.
When you must state the acceptance test *before* you can see whether it flatters you, more than four-fifths
of the "wins" that authority/incentive would have reported turn out not to survive. This is exactly
"accept a design answer only on a pre-committed measurement, not on how good the story sounds."

### Finding B — Data-driven decision-making beats "highest-paid-person's-opinion", measured at the firm level. **MEASURED (with a causal-identification caveat).**

Brynjolfsson, Hitt & Kim (2011), "Strength in Numbers," surveyed 179 large public firms: **firms adopting
data-driven decision-making (DDD) had output and productivity 5–6% higher** than their IT and other
investments predicted, with parallel effects on asset utilization, ROE, and market value. They used
instrumental-variables methods to argue the effect is not reverse causality. Source:
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1819486.

**Marking:** MEASURED, but it is observational firm-level data with an IV correction, not a randomized
trial — treat the 5–6% as a well-identified association, not a clean causal law. The contrast term itself,
**"HiPPO" (highest-paid-person's-opinion), is a normative/anecdotal coinage** (Kaushik), not a measured
construct — so "HiPPO is bad" is ASSERTED; "DDD firms outperform" is the MEASURED half.

### Finding C — Deference to peers or authority produces measurable error; a single independent dissenter collapses it. **MEASURED (classic lab studies).**

- **Asch conformity:** participants agreed with a group's obviously-wrong answer on about **37% of
  critical trials on average, and ~75% conformed at least once.** Decisive for the house rule: adding
  **one dissenting ally dropped conformity error from ~37% to ~5%.** Source:
  https://www.simplypsychology.org/asch-conformity.html.
- **Milgram obedience:** **65% of participants** obeyed an authority figure all the way to the maximum
  (supposed) shock, against their own judgment. Cross-cultural mean ~61–66%. Source:
  https://courses.lumenlearning.com/waymaker-psychology/chapter/conformity-compliance-and-obedience/.

**Marking:** MEASURED that deference-to-authority and deference-to-consensus each produce large,
quantified error rates — direct empirical grounding for "don't accept a claim on who said it." The
Asch dissenter result (37% → 5%) is the measured backing for *why one independent check is worth so
much*. Caveat: these are mid-20th-century lab studies with known replication debates; the direction is
robust, exact magnitudes are era- and context-dependent.

> **Cross-family correction (Tencent `hy3`, 2026-07-23 independent review):** this finding
> conflated two different mechanisms, and the correction is left visible rather than silently
> swapped. **Asch is peer-conformity, not authority-deference** — it measures going along with an
> obviously-wrong *peer majority*, and its real lesson is the value of a *designated independent
> dissenter* (the 37%→5% drop), **not** "don't defer to authority." **Milgram is the authority
> datum** (~65% obey an authority against their own judgment). So Asch belongs to the rule's
> mechanism (2) — route closure through an independent checker/dissenter — and Milgram to the
> "authority may not *close* a proof-gated claim" clause. The original text above over-credited Asch
> to the anti-authority claim.

### Finding D — An independent check (review/inspection) catches what the author cannot see in their own work. **MEASURED (high variance).**

Fagan's original inspection data found **82% of defects** via structured inspection (vs 8 defects/KLOC
by unit test). Broader syntheses put **software inspection at ~57–60% of defects on average, ranging
from 20% to 93%** depending on method, reviewers, and context. Sources:
https://eprints.bournemouth.ac.uk/18183/3/JearyPhalpMilsomHughesWebsterHolroyd.pdf,
https://www.sciencedirect.com/science/article/pii/S0164121224001055.

**Marking:** MEASURED that a second, independent reader finds a large fraction of defects the author
missed — the empirical case for "the taster is never the cook." The wide range (20–93%) is itself a
finding: independent checking works, but its yield is highly variable, so it is a mitigation, not a
guarantee.

### Finding E — Evidence-based medicine: proof improves outcomes, but the measured story is "proof *with* expert judgment", not "proof *instead of* authority". **MEASURED but MIXED — and it qualifies the strong form of the rule.**

Structured evidence-based programs show measured gains (e.g. a sepsis-care program where **mortality fell
from 24% to 17%** over seven years). But EBM's own foundational literature is explicit that it works best
*integrated with* clinical judgment, not by replacing the expert — and outcome measures can be fragile:
a cardiac-rehab review found a significant mortality reduction in 12 exercise-only trials, none in 28
comprehensive-program trials, and a significant reduction again when all were pooled — the answer moved
with how you sliced the data. Sources: https://www.ncbi.nlm.nih.gov/books/NBK470182/,
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3028959/.

**Marking:** MEASURED that evidence-based practice improves outcomes; but the same literature ASSERTS
(and shows) that discarding expert judgment is not what the evidence recommends. This is the most
important qualifier for the house rule — see the verdict.

### Finding F — "Appeal to authority" as a reason to reject authority-based claims. **ASSERTED / normative.**

The argument-from-authority fallacy is a principle of informal logic: a claim is not made true by the
status of who asserts it. This is a *normative* rule of reasoning, not a measured outcome — and it has a
built-in nuance that matters here: citing a genuine expert consensus is *legitimate evidence*, not a
fallacy; the fallacy is treating authority as **proof**. So the logic tradition supports "don't *settle*
on authority," not "ignore expertise." (No measured study; flagged normative.)

---

## 2. Operational mechanisms worth borrowing (to make "settle by proof" checkable, not aspirational)

Ranked by strength of the evidence behind them:

1. **Pre-commit the acceptance test (pre-registration).** State the pass/fail criterion *before*
   implementing or before seeing the result. Best-MEASURED mechanism here (57% → 8% flattering results
   removed). Kitchen translation: the ticket names how the answer will be checked *before* a chef cooks
   it; you do not get to invent the success criterion after seeing the output. Source: Kaplan & Irvin.

2. **Independent / blind check by someone who is not the author.** One dissenter cut conformity error
   37% → 5% (Asch); inspection by a non-author finds 57–82% of defects (Fagan et al.). Kitchen
   translation: "the taster is never the cook" — already the rule; this is its measured backing. The
   check must be *independent* (a fresh reader, ideally not told the expected answer) to get the Asch
   effect. Sources: Asch; Fagan.

3. **Prefer a run/measurement to an argument for design answers.** DDD firms +5–6% (Brynjolfsson et al.).
   Kitchen translation: where a question can be settled by executing something, execute it — the house
   rule's "a run, a measurement" clause has direct measured support. Source: Brynjolfsson, Hitt & Kim.

4. **Base-rate / prediction tracking; adversarial (devil's-advocate / red-team) review.** These are
   commonly recommended operationalizations (log predictions and score them; assign someone to argue the
   opposite). I did **not** source a clean measured outcome for either this pass — treat as
   plausible-but-unsourced-here. Flagged THIN.

---

## 3. FACT vs ASSUMPTION

**MEASURED FACTS (each cited above):**
- NHLBI trials: positive primary outcomes 57% (pre-2000) → 8% (post-2000), registration 0% → 100%. [Kaplan & Irvin 2015]
- DDD firms: +5–6% output/productivity, IV-corrected. [Brynjolfsson, Hitt & Kim 2011]
- Asch: ~37% average conformity to a wrong answer, ~75% conform once; one ally → ~5%. [Asch]
- Milgram: ~65% full obedience to authority. [Milgram]
- Inspection: Fagan 82%; general ~57–60% average, 20–93% range. [Fagan; Jeary et al.; ScienceDirect 2024]
- Sepsis program: mortality 24% → 17% over 7 years; cardiac-rehab result moves with data-slicing. [EBM sources]

**ASSERTED / NORMATIVE (not measured):**
- "Appeal to authority is a fallacy" — a rule of logic, not an outcome study. Legitimate expert
  consensus is evidence, so the principle is "don't *settle* on authority," not "authority is worthless."
- "HiPPO is bad" as a slogan — anecdotal coinage; the *measured* claim is the DDD productivity gap.
- EBM's own position that evidence should be *combined with* clinical judgment is a normative stance that
  the outcome data is consistent with, not a measured head-to-head of "proof alone vs expert alone."

**THIN EVIDENCE (flagged):**
- I read search-engine summaries of the primary studies, not the full papers (did not fetch the Kaplan
  PLOS ONE PDF, the Brynjolfsson SSRN paper, or Asch/Milgram primaries directly). The numbers are
  consistent across multiple independent secondary sources, so I treat them as well-attested, but the
  citations are one hop removed from the source.
- Asch/Milgram carry known replication and ethics debates; direction is robust, exact magnitudes are
  context-dependent.
- No measured outcome sourced this pass for pre-registration *outside* medicine, for red-teaming, or for
  base-rate/forecast tracking (Tetlock-style). Those operational mechanisms are recommended in the
  literature but I did not verify a metric for them here.

---

## 4. Verdict

**The principle has GENUINE MEASURED support, not merely normative assertion — but its *strong* form
overshoots what the evidence shows.**

What is measured: committing a test before you see the result removes ~86% of the flattering-but-false
"wins" (57%→8%); an independent check collapses judgment error (Asch 37%→5%) and catches most defects
(57–82%); and running the data beats opinion at the firm level (+5–6%). Deference to authority and to
consensus each produce large, quantified error rates. So "settle by proof, and by an independent check,
rather than by who said it" is **empirically backed**, and the specific clauses of the rule ("a run, a
measurement, or an independent check") map onto the best-measured mechanisms.

The caveat the evidence forces: the medical literature — the most-studied domain — does **not** find that
you should *discard* expertise; it finds that proof works best *with* expert judgment, and the logic
tradition agrees that expert consensus is legitimate evidence. So the rule's phrase "never on who said it
or how authoritative it sounds" is right as a bar on *settling* a question, but if read as "expertise is
irrelevant" it goes past the evidence. **The defensible form: authority may propose and may raise a
claim's prior, but it may not *close* a question — closure requires proof or an independent check.**

**One mechanism worth adopting first, because it is the best-measured and the cheapest:** pre-commit the
acceptance test. Write down how a claim or a dish will be judged *before* it is produced. That single
discipline is what drove the 57%→8% result, and it turns "settle by proof" from an aspiration into
something checkable — you can see whether the test was named up front or invented afterward to fit.
