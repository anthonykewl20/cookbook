# SBYP — internal map: what the book already says about proof, authority, settling

Deep-research leg for the "settle contested claims by proof, not by who's speaking" rule.
Scope: the WHOLE bound book + the operational documents that touch the rule. Evidence is
file:line. The proposed rule is **not** quoted here from the brief — see the parent task for it.

The book already embodies a proof-over-authority discipline in several places; the open
question is whether a NEW chapter adds anything or only restates. This map is built to let
the head chef answer (a) placement, (b) reinforce/contradict, (c) renumbering cost without
re-reading the book.

---

## The 11 core invariants, verbatim

Source: `press/core-invariants.json` (11 entries). Listed in file order. Index in brackets.

1. `[0]` "The operations log is what actually happened, in the order it happened, and is
   NEVER rewritten or edited — only added to at the end."
2. `[1]` "A stocktake is a photograph, rewritten whenever it changes. A log is a diary, only
   ever appended to. They are never merged into one record."
3. `[2]` "Instructions say what SHOULD happen; the log says what DID happen. Their
   disagreement is drift, and comparing them is the SHARPEST place drift shows — not the
   only place."
4. `[3]` "The manual changes through exactly one door: a fault is raised from below, written
   into the log, reported upward, the owner decides, and it is amended once for everybody."
5. `[4]` "Nobody ever checks their own work. Whoever made a thing never approves it. The
   taster never cooked the dish it judges. The ONE thing a maker may record, already settled:
   a factual note on how their own work turned out — because a note is evidence of what
   happened, never a verdict on whether it may leave the kitchen."
6. `[5]` "If a required check cannot be made, the kitchen does not serve. No checker, no
   service."
7. `[6]` "The doctor diagnoses and prescribes but NEVER treats what it finds."
8. `[7]` "Written instructions travel to a new restaurant unchanged. Records — the menu,
   stocktake and log — never travel at all."
9. `[8]` "The menu is local because it records which chain recipes this restaurant currently
   serves: a restaurant may serve FEWER dishes than the chain, never different ones. The
   recipe itself is never local. Every menu removal is logged."
10. `[9]` "People are named by role, never by person. What goes to the owner is a decision,
    never a task."
11. `[10]` "Every dish gets two verdicts from two different heads: the head chef says whether
    the method was followed, the taster says whether the quality is right. Kitchen size never
    moves either verdict — the head chef keeps the method verdict at one cook and at fifty,
    because the method check is reading the instructions against the log, not watching a
    cook work."

**Drift spotted while listing (tangential, but the contradiction pass is the right machinery
for it):** `THE-CONTRADICTION-PASS.md:58` says the sweep runs against "the book's **ten**
load-bearing rules", but the JSON carries **eleven**. Same family of mismatch the pass itself
warns about (`THE-CONTRADICTION-PASS.md:71` — "the analogy check once flagged the book's own
settled words"). Flag, do not fix here.

---

## (a) Which PART is chapter 25 in, and what surrounds it?

`CONTENTS.md:182` opens **Part Three — The base framework**, which runs chapters 14–27
(`CONTENTS.md:309–326`: "The chapters run in the order service actually runs", ending at
"27. When it goes wrong"). Part Four — Growth begins at chapter 28 (`CONTENTS.md:328`).

Chapter 25 sits in the **after-service / fault-raising cluster at the tail of Part Three**:

- `CONTENTS.md:322` — 24. Reading the log back — the procedure, the waste, the errors, the memory
- `CONTENTS.md:323` — 25. Saying something is wrong — anyone may raise a fault; nobody may fix the manual
- `CONTENTS.md:324` — 26. Is everything still fit? — the health of the people and of the building
- `CONTENTS.md:326` — 27. When it goes wrong — sent back, out of stock, and how to undo

So the neighbours are: **24 reads the log and surfaces a fault → 25 raises it → 26 diagnoses
fitness of people/building → 27 undoes a wrong action.** Chapter 25 itself stops at "report
the written fault upward" (`book/25-saying-something-is-wrong.md:21`); it deliberately does
NOT settle whether the claim is true — "The later decision belongs to the owner, not to the
kitchen that found the fault" (`book/25-saying-something-is-wrong.md:21`).

**Thematic fit of "settle contested claims by proof" beside 25:** defensible but not the only
fit. 24→25 is the *raising* arc; the proposed rule is the *checking/settling* arc, which the
book otherwise puts in **chapter 19 (Checking it)** and the contradiction pass. A chapter
beside 25 would read as "now that the fault is raised, how is the contested claim closed?" —
which is a real gap (25 explicitly hands the decision upward without saying how a contested
claim gets *settled*). The checking-cluster chapters (19) and the Part Seven "what the book
enforces by itself" slot (`CONTENTS.md:464`, ch 48–49) are the competing homes; the cost
analysis below is for the stated option (new ch 26).

---

## (b) Does the proposed rule REINFORCE or CONTRADICT anything currently bound?

Headline: **it reinforces far more than it contradicts.** Most of the rule is already bound,
scattered across the checking discipline. The one real tension — not a flat contradiction —
is with the **owner's closing authority** (invariants `[3]` and `[9]`), and the new chapter
must be worded so it does not reverse the one door.

### REINFORCES (same direction; the rule generalizes a discipline the book already enforces)

- **Invariant `[4]` (core-invariants.json:6)** — "Nobody ever checks their own work. Whoever
  made a thing never approves it. The taster never cooked the dish it judges." → the rule's
  "confirmation independent of both author and owner" is the same separation, lifted from the
  plate to any contested claim.
- **Invariant `[10]` (core-invariants.json:12)** — "Every dish gets two verdicts from two
  different heads" → author-independent confirmation is already the load-bearing rule.
- **`book/19-checking-it.md:37`** — "The taster may never reason, 'The process was followed,
  so the plate must be fine.' Its own quality verdict is final." → a role's say-so (even a
  correct process) cannot substitute for the check. This is proof-over-deference, verbatim in
  spirit.
- **`book/19-checking-it.md:9`** and **`book/12-the-operations-log.md:29`** — "a note is
  evidence, not a verdict" / "a note is evidence, not a verdict. The cook may never approve
  their own work." → the rule's "expertise is evidence not proof" is the exact distinction,
  already settled in chapter 12.
- **`book/18-cooking-it.md:30`** — "That note is not a checking verdict and does not mean the
  dish may leave the kitchen. The maker never approves the dish." → same.
- **`THE-CONTRADICTION-PASS.md:5–6`** — "A separate check, run separately, because the taster
  cannot do it. That is not an opinion about the taster. It was measured twice, and it failed
  twice." → the rule's "measured, not asserted" stance is the book's own posture; proof-gating
  is itself a measured result, not a preference.
- **`THE-CONTRADICTION-PASS.md:82–83`** — "the manager is the person most tempted to wave away
  an inconvenient flag at four in the morning, and a manager who overrules a check on its own
  judgement has quietly become the check." → authority may not *close* or overrule a check on
  its own say. This is the closest existing statement to the rule's "authority may propose but
  not close a proof-gated claim."
- **`TASTING-CHECKLIST.md:115–117`** — "The taster never wrote the page it judges… the kitchen
  does not serve a dish nobody checked." → author-independent closure, again.
- **`book/25-saying-something-is-wrong.md:17`** — "A fault seen but not recorded is a fault the
  chain never had a chance to fix. Failing to record it is itself a failure of the way the
  restaurant is run." → the rule extends 25's "raise it in the log" into "settle it by proof";
  the new chapter is a natural continuation, not a new topic.

### TENSIONS to reconcile — NOT flat contradictions, but the new chapter must not reverse these

- **Invariant `[3]` (core-invariants.json:5)** — "The manual changes through exactly one door:
  a fault is raised from below, written into the log, reported upward, **the owner decides**,
  and it is amended once for everybody." The proposed rule's clause "authority may not close a
  proof-gated claim" + "confirmation independent of both author and owner" could *read* as
  stripping the owner's decision role. **Reconciliation:** proof closes the *claim* (is it
  true?); the owner still closes the *amendment* (does the manual change?). A passing
  acceptance test must not become a side-channel around the one door — `book/25-saying-something-is-wrong.md:32`
  already forbids the kitchen amending any instruction that travels. The new chapter has to
  say this explicitly.
- **Invariant `[9]` (core-invariants.json:10)** — "What goes to the owner is a decision, never
  a task." Same axis as above: the owner decides among options; the rule settles which option
  is *true*. Compatible, but only if "proof closes the claim" is not confused with "proof
  decides the manual".
- **`CONTENTS.md:295` / `book/19-checking-it.md:37`** — "Its own quality verdict is final" /
  "The taster's word is final." A role holds final closing authority on quality. Under the
  proposed rule the taster's verdict must count *because it is the independent check*, not
  because of role authority — the new chapter must not imply the taster's final word is "just
  authority". (Reconcilable: the taster is literally the independent, non-author confirmer the
  rule requires.)
- **`book/24-reading-the-log-back.md:49`** — "Do not repair the disagreement on the page. The
  disagreement is the finding." → the rule's "settle by proof" must not be read as "make the
  disagreement go away by authority". It settles what is *true*, it does not silence the
  record.

### Net

The rule is **mostly a generalization and a naming** of a discipline the book already runs
(ch 12, ch 18, ch 19, the contradiction pass, invariant `[4]` and `[10]`). What is genuinely
NEW and not yet bound: (i) the **pre-named, author-independent acceptance test** stated as a
closure condition (pre-registration — the strongest measured mechanism in
`research/proof-over-authority.md`, Finding A), and (ii) "routine claims close on a cited
source". Those two are the load-bearing additions; the rest is restatement.

---

## (c) Renumbering cost of inserting a new chapter at position 26 (current 26–50 → 27–51)

The book is currently chapters **0–50 = 51 chapters** (`book/` listing; `press/print.py:62`
enforces "0 to 50"; `press/test_printer_reach.py:10` asserts "every chapter 0..50 (max is
50)"). After insertion: 0–51 = 52 chapters.

### Files that rename (each also needs its title line "N. Title" bumped)

`book/26-is-everything-still-fit.md` … `book/50-what-we-deliberately-left-out-and-why.md`
→ renumber to `27-…` through `51-…`. **25 files rename**, plus **1 new file** is created.

### CONTENTS.md — the locked table of contents (`CONTENTS.md:3` "Status: SETTLED… It is now closed")

- **25 running-order entries** shift +1: the numbered lines at `CONTENTS.md:324, 326, 369–375,
  413–423, 459–462, 468–469, 473` (chapters 26 through 50). Each needs its leading number and
  its filename bumped, and the new ch 26 entry inserted after the ch 25 line (`CONTENTS.md:323`).
- **3 prose "Chapter N" references** to current chapters >25: `CONTENTS.md:377` ("Chapter 34
  is the hand-off"), `CONTENTS.md:425` ("Chapter 40 is why a chain is worth having"),
  `CONTENTS.md:438` ("Chapter 42 — the menu is local"). These become 35, 41, 43.
- CONTENTS.md is explicitly owner-locked, so this re-open is an **owner decision**, not an
  editorial one (`CONTENTS.md:3–5`, "not reopened without the owner saying so").

### Cross-references *inside the book* that point at a chapter >25 (each breaks when N→N+1)

**26 instances across 17 chapters.** Full list (file:line → target):

- `book/19-checking-it.md:15` → 26, `:75` → 26 (the doctor "belongs to chapter 26")
- `book/24-reading-the-log-back.md:14` → 26, `:32` → 26, `:79` → 26
- `book/26-is-everything-still-fit.md:43` → 27 (treatment)
- `book/29-when-one-cook-is-not-enough.md:45` → 30, `:65` → 30
- `book/31-when-the-menu-grows-….md:55` → 32, `:91` → 32
- `book/33-when-the-day-is-longer-than-one-shift.md:23` → 29, `:24` → 32
- `book/34-when-one-restaurant-becomes-two.md:45` → 35 and → 36
- `book/35-what-a-chain-is.md:25` → 36, `:31` → 42
- `book/37-knowing-which-restaurant-….md:33` → 42
- `book/40-two-kitchens-same-recipe-….md:21` → 39
- `book/41-when-one-restaurant-drifts.md:35` → 40
- `book/43-closing-a-restaurant-down.md:54` → 38
- `book/45-a-worker-never-hires-a-worker.md:66` → 27
- `book/46-when-someone-is-off-sick.md:40` → 45
- `book/47-wiring-them-up.md:59` → 49, `:87` → 49
- `book/48-the-doorman.md:31` → 49
- `book/49-what-ships-in-the-box.md:23` → 48

(The densest cluster is the five "chapter 26" references in ch 19 and ch 24 — the doctor
chapter is pointed at from both sides, so inserting *before* it touches the most pages.)

### Cross-references in the operational documents

- **`TASTING-CHECKLIST.md`** — 4 instances targeting >25: `:57` (Chapter 46), `:59` (chapter
  26), `:66` (chapter 46), `:91` (chapter 29).
- **`THE-CONTRADICTION-PASS.md`** — 1 instance: `:69` (Ch. 28). The `:8` (ch 12) and `:68`
  (Ch. 25) refs are ≤25 and do not move.
- **Records / logs (drift risk, not book breakage — these are history, not canon):**
  `FOR-THE-OWNER.md` 6, `WHERE-WE-ARE.md` 2, `TICKETS.md` 3, `KNOWN-HOLES.md` 11. Whether to
  rewrite history-docs on a renumber is an owner call; leaving them dated is consistent with
  the log-is-a-diary rule (invariant `[0]`).

### Tooling that hardcodes the chapter range (will break unless updated)

- **`press/print.py`** — enforces "0 to 50" at `:62` and `:77`, and reads a per-chapter
  `brief-{chapter}.json` at `:150`. Both bounds must become "0 to 51"; any existing
  `brief-NN.json` for 26–50 rename to 27–51.
- **`press/test_printer_reach.py`** — asserts "every chapter 0..50 (max is 50)" at `:10` and
  checks `max(int(k) for k in data) == max_book` at `:89–98`. Must move to 51.
- **`press/head-chef-check.py:11,13`** — code comments naming "chapter 44" (bumps to 45).
- **`press/briefs-7to11.json:117`** — "(chapter 42 later…)" (bumps to 43).

### Cost summary

| Surface | Count |
|---|---|
| Book files renamed (title bumped) | 25 |
| New book file created | 1 |
| CONTENTS.md edit sites (25 list + 3 prose + 1 insert) | ~29, and it is owner-locked |
| In-book cross-refs to ch>25 (17 chapters) | 26 |
| `TASTING-CHECKLIST.md` refs | 4 |
| `THE-CONTRADICTION-PASS.md` refs | 1 |
| Press tooling hardcoded-range sites | ≥4 (print.py ×2, test_printer_reach ×2, plus brief renames) |
| History-doc drift (optional rewrite) | 22 across 4 files |

This is a genuinely expensive insert: it touches the locked CONTENTS, 25 file renames, 26
in-book cross-references, and the printer tooling's range guards. The cheapest alternative —
one the chef should weigh — is to fold the rule's *new* content (pre-named acceptance test;
routine-claims-cite-a-source) into an existing chapter that already carries the discipline
(ch 19 or the contradiction pass), or place it in Part Seven ("what the book enforces by
itself", `CONTENTS.md:464`) where the contradiction pass already lives operationally. Both
avoid the 25-file renumber.

---

## Where the rule already lives (so the chef can see what a new chapter would generalize)

- **The two-verdict check:** `book/19-checking-it.md` (whole chapter), `CONTENTS.md:295–307`,
  invariant `[10]`.
- **Evidence-is-not-verdict:** `book/12-the-operations-log.md:29`, `book/18-cooking-it.md:30`,
  `book/19-checking-it.md:9`, invariant `[4]`.
- **The measured contradiction pass (rule-by-rule, not holistic):** `THE-CONTRADICTION-PASS.md`
  in full; especially `:33–34` ("A check that returns one verdict for a whole page cannot find
  a fault that lives in one sentence") and `:82–83` (authority may not overrule a check on its
  own judgement).
- **Fault-raising stops short of settling:** `book/25-saying-something-is-wrong.md:21` ("The
  later decision belongs to the owner, not to the kitchen that found the fault") — this is the
  gap a "settle by proof" chapter would fill.
- **Existing literature review for the rule:** `research/proof-over-authority.md` (already in
  the repo). Its verdict (`:190–191`) lands on the same reconciliation this map found: "authority
  may propose and may raise a claim's prior, but it may not *close* a question — closure
  requires proof or an independent check."
