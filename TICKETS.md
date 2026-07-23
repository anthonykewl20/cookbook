# Tickets — the live work board

This is the one place open work is **claimed, worked and finished**. It is a *plan*, not a
record: `KNOWN-HOLES.md` holds the frozen evidence of every fault we ever found, and each
ticket below points back to it rather than repeating it — so the two cannot drift apart. When a
ticket is done, strike it here and update its hole in `KNOWN-HOLES.md` in the same commit.

**Every ticket carries a done-condition you can *measure*.** "Done" is never an opinion here —
it is a number that moved, a probe that flipped, a check that now passes. That is the
owner's standing rule: an Enhancement is measured, or it is an opinion.

Read `WHERE-WE-ARE.md` first (the step we are on), then this board.

## What the columns mean

- **Priority** — 🔴 P1 do before the next page is printed · 🟠 P2 a real correction, not blocking
  · 🟡 P3 minor or fragility · 👤 needs an owner decision · 📊 an initiative, its own track.
- **Done when** — the measurable condition that closes it. If you cannot measure it, it is not done.
- **Evidence** — the row in `KNOWN-HOLES.md` that proves it, so nobody re-argues a settled fact.

---

## 🔴 Blocking — before the next page is printed

These poison the press itself: one invalidates evidence already written down, one
manufactures false faults. **Both are now CLOSED (2026-07-23): T-12 and T-10. No blocker
remains before the next page is printed** — the press no longer invalidates evidence or
manufactures false faults.

| # | Ticket | Why it matters | Done when | Evidence |
|---|---|---|---|---|
| ~~**T-12**~~ | ~~`press/taste.py` feeds chapters 0 and 1 into its own prompt **as the voice standard they are then scored against** — so it compares each page with itself.~~ **CLOSED 2026-07-23.** Fixed: the page-under-test is withheld from its own voice standard and judged against the other (ch0↔ch1). Codex writer via `model-flow mf-3007ffb50229`, fresh Codex reviewer verified the fix correct. **Measured: the tell is gone from both — ch0 flipped SERVE 5/5 → SEND BACK (real fault: jargon *plugin*); ch1 SERVEs on a genuine comparison to ch0.** See `KNOWN-HOLES.md` and `PRESS-LOG.md`. | done | The taster judges 0 and 1 against something other than themselves; re-taste no longer gives the *"voice-standard chapter 0"* tell — **measured PASS**. | "The taster judges chapters 0 and 1 against themselves" (closed) |
| ~~**T-10**~~ | ~~The two bundled brief files quote two rules the owner **dissolved** on 2026-07-22 — the menu as an *instruction*, and instructions-vs-log as *"the only place drift can be seen"*.~~ **CLOSED 2026-07-23.** Chapter 10's brief in `briefs-7to11.json` realigned to the bound page + `core-invariants.json` (menu is a record; drift-compare is sharpest, not only). `briefs-2to6.json` was already clean. Measurement also caught a **third** staleness (reasoning-weight, from the ch9/10 reprint) and fixed it. See `KNOWN-HOLES.md` and `PRESS-LOG.md`. | done | **The ch10 probe flipped SEND BACK (baseline) → SERVE, zero faults, contradiction and unfounded both 5 — measured PASS.** Both files clean. | "The bundled briefs still carry two rules the owner dissolved" (closed) |

## 👤 Needs the owner — a decision, not a task

| # | Ticket | The question only you can answer | Done when | Evidence |
|---|---|---|---|---|
| **T-01** | The book tells the reader to write in the **operations log** on nearly every service page, and never says what the log physically *is*. Chapter 49 says the box ships one — which *names* it without ever showing the reader one. | **Does the book show one worked example of the log, or is that deliberately left local to each restaurant?** | The book either shows one worked example (labelled with the same force chapter 1 labels its pictures) **or** carries a flat rule that it is deliberately local — and no service page references "the log" without the reader having first been shown or told what it is. | "The book tells you to write in the operations log and never says what the log is" |
| **T-02** | The service chapters assume a restaurant already **standing and wired up** — bench, pass, doorman, till all plumbed in. Chapter 49 now shows one appliance, but the reader raised the same gap in **four** separate batches. | Is chapter 49's single example enough, or does the reader need to be shown *what the appliance is and how they get one* earlier, before Part Three uses it? | The reader, re-run on batches 32–36 / 37–41 / 42–46 / 47–50, **no longer** raises "what is the appliance / how do I get one." | "The service chapters assume a restaurant that is already standing and wired up" |

## 🟠 Book corrections — pages and running order

| # | Ticket | Priority | Done when | Evidence |
|---|---|---|---|---|
| **T-03** | *"Attention running out"* is the only growth trigger in the book, and **no page says how you would notice it** — no symptom a reader could see. Tied to **T-09** (order size may be that symptom). | 🟠 | A page names a concrete, observable symptom; the reader confirms the gap closed. | "no page says how you would notice it" |
| **T-04** | The taster's seven-question checklist is recited in chapter 19 but **never placed** — no page says where it lives or that it travels unchanged (a checklist is an instruction). | 🟠 | A page states where the checklist lives and that it travels; reader confirms. | "The taster's checklist is recited but never placed" |
| **T-05** | Chapter 44 states its governing rule **twice in eight lines** ("blank form, not a finished answer" / "blank forms, not answers"). A taster scoring 5/5 will not catch it. | 🟠 | The rule is stated once; taster SERVE and sweep clean on the reprint; body still ≤ 700 words. | "Chapter 44 states its governing rule twice in eight lines" |
| **T-06** | The book has no page carrying its own sharpest lesson: **a verdict-shaped check cannot see a missing word.** Measured on fingerprinted text — the deleted *"only"* passed the taster (SERVE 5/5) and the sweep (clean) both twice. | 🟠 | The lesson appears on a page, grounded in that measurement; sweep clean. | "A deleted word in a load-bearing rule passes every automated check" |
| **T-07** | Chapter 1 shows five agreed pictures; chapter 50 says *"use only"* ten. Two reviewers split on whether a reader would be confused. Parked for the reader's chair, which was never asked. | 🟡 | The reader's chair answers "would meeting five then ten confuse a reader?"; verdict recorded; reworded only if yes. | "Chapter 1 shows five of the book's pictures; chapter 50 shows ten" |
| **T-08** | Chapter 0 tells the reader to ask a fresh session about the tasting rule — but the plugin ships only the **test-print** rule, not the book, so today that check fails. The chapter is right; the box is behind it. | 🟡 | The plugin carries the book, and chapter 0's check passes against a fresh session. | "Chapter 0 describes a check the plugin cannot yet pass" |

## 🟠 Shop-tools corrections — the press, not the pages

None of these change a printed word, but each will bite a future job.

| # | Ticket | Priority | Done when | Evidence |
|---|---|---|---|---|
| **T-11** | The same two brief files still say **"chef"** (worker sense) — the book says *cook*. Rename drift, one directory over from where it was fixed. | 🟠 | No worker-sense "chef" remains in the two brief files (frozen control pages and past verdicts left untouched — editing evidence destroys it); grep clean. | "The press shop's own scripts still say the chefs are AI agents" (residual) |
| **T-16** | Every check that gives a verdict writes its output to a file — **except the adjudications that overrule them.** At least six overrules; not one can be re-read. | 🟠 | The next adjudication that overrules a checker writes its reasoning to a file beside the verdict it overrules. | "The shop keeps no artefact of an adjudication" |
| **T-17** | The roster names who does each job and is **silent on who covers** an unreachable chair (GLM returned 529 twice and the printer took odd-jobs work). | 🟠 | `THE-PRINT-SHOP.md` states who covers each chair when empty (the book's own answer: cover only where every separation holds). | "The odd-jobs chair was unreachable and the work went to the printer" |
| **T-13** | `press/prep.py` still holds a **fourth hand-kept copy** of the brief's six field names. If `brief_contract.py` changed, prep would ask for the old names. | 🟡 | prep derives the prompt's field shape from `brief_contract.py`; changing a field name there changes prep with no second edit. | "A fourth copy of the brief's field names survives" |
| **T-14** | The press scripts import `brief_contract` **only because Python puts a run script's own folder on the path.** Import them any other way and they die; every run also drops `press/__pycache__`. | 🟡 | The scripts import robustly (package-relative or path-injected), so importing — not only running — works; `__pycache__` stays ignored. | "The shop's scripts now import a sibling module, and that only works one way" |
| **T-15** | `taste.py` takes a chapter's title from the page heading; `print.py` from `CONTENTS.md`. All 51 match today; if one ever drifts, the taster refuses a page the printer accepts. | 🟡 | Both take the title from one source, or fail the same way on a deliberate drift. | "The taster and the printer disagree about where a chapter's title comes from" |

## 📊 Initiative — measurable metrics on every page, and harvesting the data

| # | Ticket | Track |
|---|---|---|
| **T-18** | **Give every one of the 51 table-of-contents pages a proper, recorded, comparable metric set — and harvest the data over time.** | measure-every-Enhancement |

**The goal (owner, 2026-07-23):** harvest as much measurable data on the cookbook as we can. Every
page carries numbers we can re-read and compare, not a one-word verdict.

**Why this, specifically:** the shop's central finding is that verdict-shaped checks *miss real
faults*. A tightening pass deleted the load-bearing word *"only"* and the page still scored SERVE
5/5 and swept clean — twice each. A number you can re-read and diff over time catches what a
"SERVE" cannot, and per the owner's standing rule a "good page" has to become a **measurement**,
not an impression.

**What we already measure but throw away.** Three tools already emit per-page numbers and **none
of them are stored** — every run is discarded:
- `press/head-chef-check.py` → body-word count, within-700, jargon hits, flat-rule presence,
  label-heading suspects, headings (mechanical, free, no model call).
- `press/contradiction-sweep.py` → 11 invariant flags per page.
- `press/taste.py` → 7 checklist items per page.

**First harvest taken today:** `data/page-metrics-2026-07-23.json` — all 51 pages through
`head-chef-check.py`. Baseline: mean 577 body words, **none over the 700 ceiling**, no jargon
hits, every page has its flat-rules section; tightest pages ch9 (700), ch2 (699), ch10 (699),
ch29 (694). This is the first stored snapshot; the point is the *next* one can be diffed against it.

**The metric design is itself a measure-every-Enhancement job — do NOT assert a metric set on
impression.** Research prior art (readability scoring, documentation linting) → a testable theory
(*which metric predicts a fault a verdict misses?*) → probe it → keep only a metric that actually
moves when a page gets worse. Candidate families to *research*, not yet decide: redundancy /
repetition (would have caught T-05), rule-to-body traceability (every flat rule traced to the
body), cross-reference integrity (would have caught the ch3→ch2 fault), reading-grade level,
voice-standard distance, body-word headroom, invariant flags, taster items, and sent-back history
per page.

**Done when (measurable):**
1. Every table-of-contents page (0–50) has a recorded metric set stored where snapshots can be compared.
2. A harvest can be re-run and **diffed against a prior snapshot** to show exactly what moved.
3. The metric set was chosen by the measure-every-Enhancement method with the evidence recorded — not asserted.

---

## 🟠 Coordination and intake — from the where-work-is-tracked research (2026-07-23)

The research in `research/where-work-is-tracked.md` settled where the work lives (in-repo flat
files stay the record; see `PRESS-LOG.md`). It also surfaced two real open items.

| # | Ticket | Priority | Done when | Evidence |
|---|---|---|---|---|
| **T-19** | **Two worktree-isolated sessions can still both claim the same ticket.** The recorded fix — "write your claim into the ticket row before starting" — does **not** work under the worktree invariant: each session is on its own branch and never sees the other's claim until the branches merge, which is exactly the "commits appeared under its feet" collision of 2026-07-23. A claim needs a spot both sessions see *immediately*, and that is the one property a flat file on a private branch cannot give. | 🟠 | A claiming mechanism exists that a parallel session actually observes before starting (Probe C in the research is its test): run two sessions on the repo alone; **at most one works a given ticket, or the clash is caught before a duplicate commit lands.** | `research/where-work-is-tracked.md` §3; `WHERE-WE-ARE.md` parallel-sessions section (the two real collisions) |
| **T-20** | **No public button for plugin readers to report a bug** — the one criterion the flat files genuinely fail (C7). The research's answer: open GitHub Issues as a **one-way intake mailbox only**, never a second board. **Gated on Probe B** — prove the mailbox does not become a second drifting tracker before adopting it. | 🟡 | Probe B passes: a filed `intake` issue is, within one session, mirrored into `KNOWN-HOLES.md` (evidence) + `TICKETS.md` (plan) and **closed with a comment pointing at the commit and ticket row**, with no contradiction between issue and repo. If it keeps drifting across a few real intakes, drop it and accept the limit (readers open a PR). | `research/where-work-is-tracked.md` §4–5 |

## Parked / already filed — not fresh work

- **T-09 — Staffing by order size.** Already filed as a ticket in `KNOWN-HOLES.md` (2026-07-23):
  a hypothesis to myth-bust on the measure-every-Enhancement track before it becomes a chapter 29
  rule. Off the current printing run. See that row for the full design.

## Not filed as tickets, and why

Some open rows in `KNOWN-HOLES.md` are **standing guards** — rules the shop has already adopted
about how it works (the manager hands out work and never does it; never report a count without
opening what it matched; nothing is bound while a check is in flight; a checker certifies a hash,
not a directory). Those are adopted discipline, not units of work, so they stay in the faults
record and are not ticketed here. The old ch. 12 row "where the job list lives" is now
**answered** — the where-work-is-tracked research closed it (see `KNOWN-HOLES.md` and
`PRESS-LOG.md`). One old book-content row remains (ch. 25 "a fault seen and not recorded"): it
predates the finished chapters and **needs a verify pass** to confirm it is still open before it
earns a ticket — flagged, not filed.
