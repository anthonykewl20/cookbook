# The brief — chapter 1, The interview

Identical for every printer. Nobody sees anybody else's work.

---

## The job

Write **chapter 1 of the Cookbook: "The interview"**. Return the finished chapter as
Markdown and nothing else — no preamble, no commentary, no explanation of your choices.

You are writing for a reader who is **not a programmer**. That is a hard requirement, not a
style preference. If a word only means something to a programmer, it does not belong in the
sentence doing the explaining.

## What this book is

A book about running a chain of restaurants, where the restaurants are software projects,
the chefs are AI agents, and the dishes are units of work. The reader is the **owner**.

The book's purpose, in one line: **the same dish every time, whoever is working.** The staff
are never the same twice and none of them remember yesterday, so the people cannot be the
constant — the process has to be. The manual is the only thing allowed to hold still.

## What chapter 1 must cover

It sits in **Part One — Agreeing on words**, which is the first conversation in a new chain,
before any work at all. Part One is about language only. No staff are hired in it and no
work is done in it.

The chapter must settle all of the following, in whatever order reads best:

1. **Why words come first.** Nothing can be agreed, checked or handed over until both sides
   mean the same thing by the same word.
2. **It is an interview, not a form.** The appliance — the machine the chefs work on — sits
   with the new owner and asks questions, and the two of them arrive at the words together.
   The owner is not filling in blanks somebody else chose.
3. **The book's own words are a worked example, not the law.** This book says restaurant,
   kitchen, dish, chef, taster. Those are *one owner's* way of seeing, and that owner happens
   to think visually. Another owner may think in workshops, or studios, or plain blunt terms
   with no picture in them at all. Publishing one owner's pictures as law would impose them
   on every reader.
4. **What has to be named, and what does not.** Some things must have an agreed word or the
   rest of the book cannot be followed — who owns the place, who runs it day to day, who does
   the work, who checks it, the machine they all work on, and one unit of work. Everything
   else can wait.
5. **Where the agreed words are written down.** Locally, in that kitchen, never back into
   this book. The book ships blank on this and stays blank.
6. **The words are then fixed.** Once agreed, nobody invents a competing word for the same
   thing later, and nobody stretches an agreed word into a more convenient meaning. Both are
   how a shared language quietly stops being shared.

## Hard constraints

- **Body under 700 words**, not counting the flat rules at the end.
- Follow the template below exactly.
- Contradict nothing stated in this brief.
- Do not invent facts about how the interview is conducted mechanically — no commands, no
  file formats, no tooling. This chapter is about the conversation, not the machinery.
- If something genuinely cannot be resolved from this brief, do not paper over it. Add a
  final section headed `## Unresolved` listing it. That section is not part of the chapter
  and does not count against the word limit.

---

# THE TEMPLATE — follow this exactly

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
   dish, the cooks, the taster, the appliance, the recipe and the shopping list, the
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


---

# THE WORKED EXAMPLE — chapter 0, written by hand

Match this voice. Do not copy its subject matter.

# 0. Opening the box

**What this chapter settles:** how to get the book working, and how to know that it did.

## The book is installed, not read

This book is unusual in one way, and it matters before anything else: **the machine reads it
too.**

An ordinary cookbook sits on a shelf. Somebody takes it down, reads a page, puts it back, and
then cooks from memory. This one does not work like that. It is fitted into the kitchen
itself — and once it is in, every cook who comes on shift is already working to it, whether
or not any of them ever opens it.

That is the whole point. Your staff are never the same twice, and a book on a shelf depends
on somebody remembering to take it down. Remembering is exactly what a stranger cannot do.

So opening the box is not "begin reading at chapter one". It is something you do once, to a
machine.

## You need only two things

Two things, and nothing else.

- **The appliance** — the machine your cooks work on.
- **The address of the box** — `anthonykewl20/cookbook`.

Nothing to pay for, no account to make, nothing to set up first.

## Two lines open the box

Type these two lines into the appliance:

```
/plugin marketplace add anthonykewl20/cookbook
/plugin install chain-standards@cookbook
```

The first tells the appliance where the box is. The second takes the book out and puts it on
the wall.

## A fresh session proves it worked

Do not take the machine's word for it. **A book that reports itself installed and is not is
worse than no book at all** — you will spend a month believing rules are being followed that
nobody ever received.

Give the book a real question and check the answer. **Start a fresh session** — not the one
you installed from — and ask it what the rule is about who tastes a dish. If it answers
without you having told it, the book is on the wall.

The fresh session is the part that matters. The session you installed from was there when it
happened, and may simply be remembering the conversation. A session that was not there is a
stranger, and strangers are what this book is built for. If a stranger knows the rule, every
future stranger will know it too.

## Three checks find what failed

Check these three things, in this order.

1. **You are in the session that installed it.** Start a new one and ask again.
2. **The appliance was already open before you installed.** Close it and open it again.
3. **Still nothing.** Then the box did not open, and nothing in this book applies yet. Fix
   this before reading on — every chapter after this one assumes the machine received it.

## Never copy it

There is one thing to get wrong here, and it is tempting.

Do not copy the book's words into your own notes. Not a paragraph, not a rule you liked, not
"just the important part".

The moment two written copies of one promise exist, they begin to drift. Somebody improves
one of them. Somebody trims the other. Neither copy is wrong on the day it is made, and a
year later they say different things and nobody can say which is the real rule. That is not
carelessness. It is what always happens, and the only defence is to never make the second
copy.

The book is installed. It is not transcribed. If you want it to say something different, you
change the book — and there is exactly one door for that, described in Part Three.

---

## The rules, flat

*The same rules as above, with the explanation removed. This is the part the appliance
obeys.*

1. This book is installed, never copied. If its wording appears in any local file, that copy
   is wrong by definition — delete it and point at the book.
2. Nothing in this book applies until the box is open **and** verified.
3. Verification is performed by a session that did not install it. An installing session may
   not verify its own installation.
4. If the book is not installed, say so and stop. Never proceed on remembered rules.

