# What a chapter is

**Derived from writing chapter 0 by hand, not invented in advance.** That order is the book's
own rule: nothing is handed to someone else until it is written down well enough that a
stranger could do it, and you only find out what a job involves by doing it.

`book/00-opening-the-box.md` is the worked example. Read it before writing anything.

## The shape

Every chapter has two faces. The body explains, for the owner. The last section states the
same rules flat, for the appliance to obey.

| Part | Required? | What it is |
|---|---|---|
| `# N. Short name` | Always | The number and name exactly as they appear in `CONTENTS.md`. Never renamed locally |
| **What this chapter settles:** one sentence | Always | What the reader can do, or stop worrying about, once they have read it |
| Body sections | Always | Plain-language headings that make a **statement**, not a label. "The book is installed, not read" — never "Installation" |
| Steps | If the chapter has actions | Numbered, in the order performed |
| What goes wrong | If it can fail | The failures in the order they should be checked, commonest first |
| The one thing never to do | If there is one | A single named trap, with the reason it is tempting |
| `## The rules, flat` | Always | Numbered, imperative, no explanation |

## The rule that governs the two faces

**Every flat rule must be derivable from the body. The flat rules never introduce anything
the body did not explain.**

They are not a summary and not a second version. They are the same rules with the reasoning
taken out — the shopping list printed from the recipe. A flat rule with no explanation above
it is a promise nobody argued for, and it is the exact drift this book exists to prevent.

## The voice

1. **No word that only means something to a programmer** appears in the body. File names and
   commands may appear as evidence beside a claim — never inside the sentence doing the
   explaining.
2. **Analogies come from the agreed set only.** The chain, the restaurant, its kitchen, a
   dish, the chefs, the taster, the appliance, the recipe and the shopping list, the
   telephone game, a building with doors. Do not invent competing ones. Do not stretch one
   past where it fits.
3. **Short declarative sentences.** If a sentence has three commas in it, it is two sentences.
4. **Write to the owner as "you".** Never "the user".
5. **Bold carries the load-bearing claim of a section**, once or twice per section. Bold
   everywhere is bold nowhere.
6. **Every claim a reader could doubt has its reason attached**, in the same breath. Not
   "verify in a fresh session" but "verify in a fresh session, because the session that
   installed it was there and may only be remembering".
7. **Body under about 700 words.** A rule that gets skimmed is a rule that gets broken, and
   long chapters get skimmed.

## Before a chapter is handed in

- It contradicts nothing in `CONTENTS.md` or `KNOWN-HOLES.md`.
- It covers everything the running order assigns to that chapter, and nothing assigned to
  another one.
- Anything it could not resolve is written into `KNOWN-HOLES.md` rather than papered over. A
  chapter does not ship with an open hole hidden inside it.
