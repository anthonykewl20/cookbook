# Settle-by-proof — INITIAL VALIDATION (independent)

Validator opened the real source behind each claim and stamped it. It did **not**
trust the research files. Format: stamp — what the source actually shows.

Legend: **VALIDATED** = source confirms the claim as stated. **PARTIALLY VALIDATED**
= the point is real but a citation or sub-claim is wrong (see note). **NOT VALIDATED**
= source contradicts the claim. **UNCERTAIN** = could not confirm from the source.

---

## Summary table

| # | Claim | Stamp | Headline |
|---|---|---|---|
| 1 | RENUMBER COST | **VALIDATED** | 25 sequential files 26–50; CONTENTS.md:3 says SETTLED/closed. |
| 2 | PRESS TOOLING "0–50 hard-coded, a 51st chapter breaks it" | **PARTIALLY VALIDATED** | Real 50-caps exist in `prep.py:32,44` and `read-for-missing.py:32` — but the cited lines are mostly message-strings/comments, and `print.py` (the printer) does NOT break. |
| 3 | CROSS-REFERENCES (26 refs, 17 chapters; densest = ch 19 + ch 24 → "chapter 26") | **VALIDATED** | Case-insensitive grep: exactly 26 refs across 17 files; chapter 26 (the doctor) is the most-referenced, pulled by ch 19 (×2) and ch 24 (×3). |
| 4 | REINFORCE/CONTRADICT invariants 4/10 vs 3/9 | **VALIDATED** (on characterization) | The parentheticals match invariants 3, 4, 9, 10 verbatim (research uses 0-indexed numbering). The reinforce/tension framing is the research's analysis, not something the file asserts. |
| 5 | STUDIES (Kaplan & Irvin; Asch) | **VALIDATED** | File cites PLOS ONE (K&I) and Asch's 1956 *Psychological Monographs*; both qualifiers present (OBSERVATIONAL + "no causal inferences"; peer-conformity, not authority). |
| 6 | STRESS-TEST RECEIPTS (deleted "only"; broken page 5/5) | **VALIDATED** | KNOWN-HOLES.md:43 (deleted "only" passed taster 5/5 + sweep clean ×11); PRESS-LOG.md:444-489 + THE-CONTRADICTION-PASS.md (seeded reversal scored contradiction 5/5). |
| 7 | DRIFT ("ten" rules in the pass vs eleven in the JSON) | **VALIDATED** | JSON holds 11 (counted); THE-CONTRADICTION-PASS.md:58 (also :40, :59) says "ten". |

**The one claim that did not validate cleanly is #2.** Everything else holds.

---

## Evidence per claim

### 1. RENUMBER COST — VALIDATED

- `book/` files numbered 26–50: counted programmatically = **25 files**, sequential
  (`26-is-everything-still-fit.md` … `50-what-we-deliberately-left-out-and-why.md`), no
  gaps. Inserting after ch 25 → new ch 26 → these 25 shift to 27–51. Arithmetically exact.
- `CONTENTS.md:3-5` — `"**Status: SETTLED by the owner, 2026-07-21. Nothing written
  yet.** This page is the running order, not the book. It is now closed: chapters get
  written against it, and it is not reopened without the owner saying so."` So the
  running order is locked, which is what makes the renumber costly (it reopens a closed
  order AND moves 25 chapters).

### 2. PRESS TOOLING — PARTIALLY VALIDATED (correct thesis, wrong citations)

The thesis "press tooling caps at 50, so a 51st chapter breaks part of it" is **real** —
but the specific lines cited are mostly the wrong places, and the implication that the
*printer* breaks is false.

What the cited lines actually show:
- `press/print.py:62` and `:77` — the string `"…from 0 to 50"` appears only inside
  **error-message text**, not a functional bound. `:150` is `brief_path =
  os.path.join(SP, f"brief-{chapter}.json")` — a path build, nothing about a range.
- `press/print.py:44` — the regex `(?:0|[1-9]\d?)` accepts **0–99**, not 0–50.
- `press/print.py` parsing logic is **adaptive**: `max_chapter = max(catalog)`;
  `expected = set(range(0, expected_number))` is derived from CONTENTS.md. A 51st
  chapter in CONTENTS.md would be accepted; only the *message strings* would go stale.
- `press/test_printer_reach.py:10` is a docstring comment ("max is 50"); the assertions
  at :89/:98/:118 compare against `max_book = max(all_books)`, i.e. **derived from disk**.
  The test would still pass with 51 chapters.
- `press/head-chef-check.py:11,13` are comments **about jargon words**. There is no
  chapter-range logic anywhere in that file. The citation is simply wrong.

Where the 50-cap ACTUALLY lives (not cited by the research):
- `press/prep.py:32` — `re.fullmatch(r"(?:1[7-9]|[2-4][0-9]|50)", value)` (regex caps at 50)
- `press/prep.py:44` — `if 17 <= number <= 50:` (**functional** bound; ch 51 rejected here)
- `press/prep.py:131` — usage `"CHAPTER (17-50)"`
- `press/read-for-missing.py:32` — same `(?:1[7-9]|[2-4][0-9]|50)` regex (caps at 50)

**Bottom line:** a 51st chapter WOULD break `prep.py` and `read-for-missing.py`
(functional `<= 50` / regex caps), so the claim's direction is right. But it would NOT
break `print.py` (the printer) — that tool is adaptive. The research pointed at
message-strings and jargon-comments and missed the two files where the cap is real.

### 3. CROSS-REFERENCES — VALIDATED

Case-insensitive grep `chapter["']?s?[ "]+(2[6-9]|3[0-9]|4[0-9]|50)` over `book/`:
**26 matches across 17 distinct files.** (A case-SENSITIVE grep finds only 11/8 — the
research's count only reproduces when "Chapter" with a capital C is included.)

Densest cluster: **chapter 26** is the most-referenced single chapter (5 incoming):
`book/19-checking-it.md` (lines 15, 75) and `book/24-reading-the-log-back.md` (lines 14,
32, 79) both point to it as the doctor / "is everything still fit" chapter — confirmed by
the target file `book/26-is-everything-still-fit.md` and the in-text wording ("The
doctor's question … belongs to chapter 26"). Minor imprecision: ch 24 has **3** refs to
ch 26, ch 19 has **2**; the claim's "ch 19 and ch 24" cluster is correct, ch 24 is the
denser of the two.

### 4. REINFORCE/CONTRADICT — VALIDATED (on characterization)

`press/core-invariants.json` read verbatim. Note the research uses **0-indexed**
numbering (invariant 4 = the 5th string), which is consistent with the 11-entry file:

- invariant[4] — "Nobody ever checks their own work… a note is evidence of what happened,
  never a verdict on whether it may leave the kitchen." → matches "(nobody checks their
  own work; a note is evidence not a verdict)". **Fair.**
- invariant[10] — "Every dish gets two verdicts from two different heads…" → matches
  "(two verdicts from two heads)". **Fair.**
- invariant[3] — "The manual changes through exactly one door… the owner decides, and it
  is amended once for everybody." → matches "(the owner decides)". **Fair.**
- invariant[9] — "People are named by role, never by person. What goes to the owner is a
  decision, never a task." → matches "(what goes to the owner is a decision, not a
  task)". **Fair.**

All four parentheticals are accurate. The reinforce/tension relationship is the research's
analytical read (the JSON does not assert relationships between invariants); it is
plausible but out of scope for source-checking.

### 5. STUDIES (spot-check) — VALIDATED

Per instructions, this confirms the file is honest about its sources and qualifiers, not a
re-run of the web checks.

- Kaplan & Irvin: `research/sbyp-studies.md:28-31` cites **PLOS ONE** 10(8): e0132382
  (doi:10.1371/journal.pone.0132382) — a real primary source. Numbers 57%→8% with
  registration 0%→100% are stated (lines 32-36); labelled **OBSERVATIONAL** (line 25);
  authors' causation disclaimer quoted verbatim — *"the design of the study does not allow
  causal inferences"* (lines 43-46). Qualifier present. **Honest.**
- Asch: lines 97-102 cite the **1956 *Psychological Monographs*** monograph
  (doi:10.1037/h0093718) and the 1955 *Scientific American*. Figures 35.7% conform / ~5%
  with one dissenter (lines 104-108). Framing explicitly verified as **peer-conformity,
  not authority** (lines 115-122). Qualifier present. **Honest.**

### 6. STRESS-TEST RECEIPTS — VALIDATED

Both incidents are real and say what is claimed:

- **Deleted "only"** — `KNOWN-HOLES.md:43` (the long CLOSED entry on ch 9/10): the
  compression pass "deleted the word 'only' from a rule about the three separations —
  *'may be held by them **only** where no separation is broken'* became *'may be held by
  them where no separation is broken'*". It "is load-bearing: without it the sentence
  stops forbidding and starts permitting." And: "**Both the taster (SERVE 5/5) and the
  rule-by-rule sweep (clean on all eleven) passed the weakened sentence, twice each.**"
  Found by a second head chef re-reading a diff already declared finished.
- **Broken page certified 5/5** — `PRESS-LOG.md:444-489` (and `THE-CONTRADICTION-PASS.md`):
  ch 22 was reprinted with a planted reversal of *nobody-checks-their-own-work*; the taster
  "**MISSED. Scored contradiction 5/5**" (line 458). Across three attempts the taster
  served the reversal every time, scoring contradiction 5/5 in attempts 2 and 3 (lines
  477-479). The ch 12 seeded reversal ("the log may be corrected") was likewise served by
  both tasters and scored 5/5 on the very contradiction item.

The framing — that these prove the independent (non-author) taster verdict is an
insufficient guard on its own — is exactly the conclusion the book itself draws
(`THE-CONTRADICTION-PASS.md`, `PRESS-LOG.md:481-489`).

### 7. DRIFT — VALIDATED

- `press/core-invariants.json` — `len(json.load(...))` = **11** entries.
- `THE-CONTRADICTION-PASS.md:58` — "`press/core-invariants.json` — the book's **ten**
  load-bearing rules." (Also :40 "all ten rules" and :59 "all ten".)
- Mismatch confirmed. Corroborating evidence the research did not need but which
  confirms the drift direction: `PRESS-LOG.md:1380` and `KNOWN-HOLES.md:43` already say
  "all **eleven**", and `print.py:154-157` counts the total dynamically from the JSON
  (so it would print "11"). The logs caught up to eleven; the contradiction-pass doc is
  still stuck at ten.

---

## Notes the head chef will want

- **Claim 2 is the material one.** The renumber/landing argument only needs "the press
  tooling carries a 50 assumption," which is true in `prep.py` and `read-for-missing.py`.
  But if the chapter writes that `print.py` "breaks," that is false and will not survive
  a reader opening the file. Cite `prep.py:32,44` and `read-for-missing.py:32` for the
  functional caps; treat `print.py` as adaptive (stale messages only).
- **Claim 3 must be reproduced case-insensitively** or it undercounts (11 vs 26).
- **Invariant numbering is 0-indexed** in the research; say so in the chapter or a reader
  who counts from 1 will think invariant 4 is the wrong rule.
