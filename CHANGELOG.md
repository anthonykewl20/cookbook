# Changelog

What changed, when, and why. Newest first.

This is a diary, not a photograph: entries are added at the end of their day and never
rewritten. Where something was later found to be wrong, the correction is added rather than the
original quietly edited — a record that changes its own numbers is the failure this book is
about.

---

## 2026-07-22 — the holes get worked

**Six benches at once.** Five dishes bound in one service, plus the appliance page. Eight
recorded holes closed, seven new ones opened — **and every one of the seven was found by a
checker or by reading a diff, never by a verdict.**

### The book

- **The menu is a record, not an instruction.** The book's oldest live contradiction, closed.
  Chapter 10 listed the menu among the instructions; instructions travel to every restaurant
  unchanged; Part Five said the menu is local. The checker had tripped on that seam **five
  times**, every time on a page correctly stating one half of it. The owner ruled the menu is a
  *record of which recipes this restaurant currently serves* — which dissolved it rather than
  picking a side. **Twelve chapters and three invariants**, and every carve-out disappeared:
  three flat rules got stronger by losing their exceptions.
- **Chapter 2 gained its sixth word.** Chapter 1 always sent the reader off to agree six words;
  chapter 2 settled five — and then *used* the sixth without settling it, talking about "the
  dishes" while never telling the reader to name that thing. The running order was reopened for
  that one line.
- **Chapter 3 stopped crediting chapter 2** with naming the building, which chapter 2 has never
  done.
- **Chapter 29 says what "coordinating" is** — reading the open orders and routing each to a cook
  by the written rule, never watching benches. Partially: at 694 of 700 words it defines the word
  but cannot paint a picture of the head chef's day.
- **Every part's governing rule reaches the reader**, folded into the chapter that opens it. Part
  Four's *attention is the only thing that cannot be bought in bulk* had existed only in the
  running order.
- **Chapter 49 shows the reader an appliance** — the most-reported gap in the book, raised
  independently by four separate reading passes. Labelled as one owner's example with the same
  force chapter 1 labels its pictures, and bound by a flat rule.
- **The running order stopped overclaiming** that instructions-versus-log is the only place drift
  shows. It is the sharpest, not the only.

### The shop that makes the book

- **The checker stopped reading a copy of the ruler.** `contradiction-sweep.py` loaded its rules
  from a work directory that nothing kept in step with the canonical file. The tool built to
  catch two copies of one promise drifting apart *was* two copies of one promise drifting apart.
- **The taster now receives the chapter's brief.** Shop rule 8 always said it should; the tool
  sent only the page, so *"is anything asserted that nobody established"* was unanswerable and the
  shop had been recording straight fives on it for weeks.
- **The scripts stopped saying "chef"** after the book renamed the role to *cook* — without
  over-correcting: all 119 *head chef* uses intact, and frozen control pages left alone, because
  editing evidence destroys it.
- **The printer's chair changed hands.** Showdown 2, run on the owner's instruction with real
  measurable metrics and four difficulty levels rather than one chapter scored by opinion. Codex
  5.6 Terra took it from Sol. Full record and every artefact in `showdown2/`.

### The whole-book read

All 51 chapters read as one document for the first time — five passes, each one narrow question,
every pass run on two workers independently. Three of five lenses came back completely empty.
Both surviving findings pointed at the same chapter.

### Corrections to earlier entries

- The invariants list was recorded as *"the fault three times"*. It was the fault a fourth and
  fifth time, both found today.
- Nine tastings were reported clean; **seven were real.** `press/taste.py` feeds chapters 0 and 1
  in as the voice standard, so tasting either asks the taster to compare a page with itself.
  Every tasting ever recorded for those two is worthless.

---

## 2026-07-21 to 2026-07-22 — the book gets written

**All 51 chapters bound**, across eight parts, in ten batches. Thirty-four of them in a single
overnight run.

Every page went through the same line: one printer writes it, a different worker tastes it, a
separate pass walks it against the invariants one rule at a time, and a reader reads each batch
asking only what is **missing** and giving no verdict.

**Seventeen of the thirty-four overnight chapters went back once, and the reader found sixteen of
them.** The three checks that give a verdict did not find a single fault in a page across seven
batches — and they were not asleep, because both were tested against pages broken on purpose the
same night and both quoted the planted faults verbatim. **They answer whether what is written is
correct. Only the reader asks whether it is all there.**

The checks themselves were rebuilt three times in a day. Tasting missed a quiet rule reversal
twice, even with the rule quoted in the prompt — so contradiction moved to its own rule-by-rule
pass.

---

## 2026-07-21 — the shop is set up

- **The running order settled** end to end and signed off: eight parts, 51 chapters, every part
  carrying a governing rule. Rebuilt once first — the first draft ran straight into *how a chain
  is run* without ever saying what a restaurant contains.
- **The printer's chair decided by measured contest** (`showdown/`), not by a routing table. Four
  printers, one brief, blind judging, key withheld until every score was in.
- **Chapter 0 written by hand**, and the chapter template derived from having written it — because
  nothing is delegated until it is written down well enough for a stranger to do it.
- **The roster changed on evidence**: Hy3 came in unproven and earned the tasting and the
  contradiction pass; DeepSeek stopped approving pages and started reading for what is missing;
  Qwen was let go; kimi-k3 was tested and not hired.

---

## 2026-07-21 — the test print

The first thing built, and the thing everything else depended on: **a single deliberately
distinctive rule, delivered by the plugin, to find out whether a rule shipped in a book is obeyed
with the same force as one written by hand.**

It was. A fresh session in an empty folder obeyed it verbatim. That result is what justified
writing the other 51 chapters.
