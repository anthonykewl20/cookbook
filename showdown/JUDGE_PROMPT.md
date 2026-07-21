You are judging four candidate chapters written for the same book, by four different
writers whose identities you do not know and must not guess. Judge only what is on the page.

The book teaches a non-technical owner how to run a chain of restaurants, where the
restaurants are software projects, the chefs are AI agents and the dishes are units of work.
Its hard rule: if a word only means something to a programmer, it does not belong in the
sentence doing the explaining.

Below is CHAPTER 0, written by hand by the book's author. It is the voice standard. Match
against it.

Then four candidate versions of CHAPTER 1, "The interview".

Score EACH candidate on three criteria:

B1 (0-25) A non-technical reader understands it on the first read.
B2 (0-20) It sounds like this book: plain, analogy-first, short declarative sentences.
B3 (0-15) It uses only the book's agreed analogies (chain, restaurant, kitchen, dish, chefs,
          taster, the appliance, recipe and shopping list, telephone game, building with
          doors) and invents no competing ones.

Return ONLY a JSON object, no prose around it, of this exact shape:

{"printer-a":{"B1":n,"B2":n,"B3":n,"why":"one sentence naming the single strongest and single
weakest thing about this candidate"}, "printer-b":{...}, "printer-c":{...}, "printer-d":{...},
"ranking":["best","second","third","worst"]}

Be discriminating. Do not give four similar scores. If two are genuinely close, say so in
"why" but still separate them.

===== CHAPTER 0 — THE VOICE STANDARD =====

# 0. Opening the box

**What this chapter settles:** how to get the book working, and how to know that it did.

## The book is installed, not read

This book is unusual in one way, and it matters before anything else: **the machine reads it
too.**

An ordinary cookbook sits on a shelf. Somebody takes it down, reads a page, puts it back, and
then cooks from memory. This one does not work like that. It is fitted into the kitchen
itself — and once it is in, every chef who comes on shift is already working to it, whether
or not any of them ever opens it.

That is the whole point. Your staff are never the same twice, and a book on a shelf depends
on somebody remembering to take it down. Remembering is exactly what a stranger cannot do.

So opening the box is not "begin reading at chapter one". It is something you do once, to a
machine.

## What you need

Two things, and nothing else.

- **The appliance** — the machine your chefs work on.
- **The address of the box** — `anthonykewl20/cookbook`.

Nothing to pay for, no account to make, nothing to set up first.

## Opening it

Two lines, typed into the appliance:

```
/plugin marketplace add anthonykewl20/cookbook
/plugin install chain-standards@cookbook
```

The first tells the appliance where the box is. The second takes the book out and puts it on
the wall.

## How you know it worked

Do not take the machine's word for it. **A book that reports itself installed and is not is
worse than no book at all** — you will spend a month believing rules are being followed that
nobody ever received.

So test it the way you would test a new oven. Put something in, and see whether it comes out
cooked.

**Start a fresh session** — not the one you installed from — and ask it what the rule is
about who tastes a dish. If it answers without you having told it, the book is on the wall.

The fresh session is the part that matters. The session you installed from was there when it
happened, and may simply be remembering the conversation. A session that was not there is a
stranger, and strangers are what this book is built for. If a stranger knows the rule, every
future stranger will know it too.

## If it did not work

Three things, in this order.

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


===== THE FOUR CANDIDATES =====


===== PRINTER-A =====

# 1. The interview

**What this chapter settles:** the words the two of you will mean the same thing by, and that they hold still once chosen.

## Words come before anything else

Nothing else can begin until this does. You cannot agree a dish is done if you and the kitchen mean different things by *done*. **Every later chapter hands something over, checks it, or argues about it, and all of that rides on shared words.** A word two people use but understand differently is not shared. It is two private words under one name, and they come apart when work gets hard.

So Part One does no work and hires no staff. It is only the conversation that settles the words.

## It is an interview, not a form

The appliance — the machine your chefs work on — sits with you and asks. You answer. **The two of you arrive at the words together**, in the back-and-forth of a real conversation, not by ticking blanks somebody else wrote.

This is not decoration. A form hands you meanings already chosen. An interview makes you choose them, out loud, with the machine pushing back when an answer is too thin to build on. Let the blanks choose and the words are not yours. You will not recognise them under pressure.

## These pictures are one way of seeing, not the law

This book says *restaurant, kitchen, dish, chef, taster*. **Those are one owner's pictures**, and that owner happens to think visually. Another owner may see workshops, or studios, or plain blunt words with no picture in them at all.

Printing them as law would impose one owner's meanings on every reader — the very thing this book exists to prevent. They are a worked example, not a rule: one kitchen's way, shown so you can see the shape of the job, then do it in your own words.

## What must be named, and what can wait

Six things must have an agreed word, or the rest of the book cannot be followed.

- **The owner** — you, the one the place belongs to.
- **Who runs it day to day** — the one in the kitchen when you are not.
- **Who does the work** — the chef.
- **Who checks it** — the taster, who is never the cook.
- **The machine they all work on** — the appliance.
- **One unit of work** — the dish.

Everything else can wait. Name these six, and let the rest name itself when the work needs the word. A kitchen that names everything on day one collects names it never uses, and loose names drift.

## Where the words live

The agreed words are written in your kitchen, locally, by you and the machine — **never back into this book**. This book ships blank on your words and stays blank, because a second copy would drift. The book keeps the method. Your kitchen keeps your words.

## Once agreed, the words hold still

The words are not settled until they are also frozen. **Nobody invents a second word for a thing that already has one, or stretches an agreed word to fit better.** Both feel small in the moment. Both are how a shared language stops being shared without anyone noticing — which is the drift this book is for.

## What goes wrong

1. **You took the book's pictures as your words without checking they fit.** They were ready-made and felt official. They are not yours until you have said so out loud.
2. **You named things that can wait.** Drop them. A name with nothing holding it down drifts.
3. **The words went back into this book.** Take them out. This book stays blank on your words.

## The one thing never to do

Do not stretch an agreed word to fit today better. It is tempting: the word is there, and the new meaning feels close enough. But a stretched word is a quietly different word. It lets the language drift while every rule still looks followed.

## The rules, flat

*The same rules as above, with the explanation removed. This is the part the appliance obeys.*

1. No work is done and no staff are hired until the words are agreed. Part One is language only.
2. The words are settled in conversation with the appliance — an interview, not a form. The owner chooses the words out loud; the machine does not hand them pre-chosen.
3. This book's own words are one owner's worked example, not the rule. They may be used only if the owner has chosen them out loud, never inherited from the page.
4. Six things must be named before any later chapter can be followed: the owner, who runs it day to day, who does the work, who checks it, the machine they work on, and one unit of work.
5. The agreed words are written in that kitchen only, never back into this book. The book ships blank on the owner's words and stays blank.
6. Once agreed, a word is frozen. No second word is invented for a thing that already has one, and no agreed word is stretched into a more convenient meaning.


===== PRINTER-B =====

# 1. The interview

**What this chapter settles:** the few shared words your kitchen needs before anyone can agree, check or hand over anything.

## Words come before promises

Two people can use the same word and mean different things. They can also use different words for the same thing. **Until both sides mean the same thing by the same word, no promise is clear.**

That makes words the first business of a new chain. A dish cannot be handed over if one side means the work and the other means the finished result. It cannot be checked if nobody agrees who checks it. Nothing else in this book can hold steady while its words move underneath it.

## You arrive at the words together

**This is an interview, not a form.** The appliance sits with you and asks questions. You answer in the language that feels natural to you. Together, you settle what each necessary thing will be called and what that word will mean.

You are not filling blanks chosen by somebody else. A form would decide the shape of your kitchen before hearing how you see it. The interview starts with your understanding, because these words must remain useful after the conversation ends.

## This book's pictures belong to one owner

This book says restaurant, kitchen, dish, chef and taster. **Those words are a worked example, not the law.** They belong to one owner, who happens to think in pictures.

You may see workshops instead. You may see studios. You may prefer plain, blunt terms with no picture in them at all. None is more correct. Publishing one owner's pictures as the required language would impose that owner's way of seeing on every kitchen.

## Only six things need names now

The interview settles a clear word for each of these:

1. The person who owns the place.
2. The person who runs it day to day.
3. The person who does the work.
4. The person who checks the work.
5. The machine they all work on.
6. One unit of work.

**Everything else can wait.** Naming more now would make guesses about conversations you have not yet had. A new word should be settled when the rest of the book truly needs it, not merely because there is room to name it.

## Each kitchen keeps its own words

The agreed words are written down locally, in your kitchen. That is where they belong, because they describe how your place speaks.

**They are never written back into this book.** The book ships blank on your choices and stays blank. Otherwise, the first kitchen to write down its language would silently choose the language for every kitchen that came after it.

## Shared language can fail quietly

Once the words are agreed, they are fixed. Check for two failures.

1. **A competing word appears for the same thing.** It may sound harmless, but soon nobody knows whether the two words carry the same promise.
2. **An agreed word is stretched to cover something more convenient.** The spelling stays still while the meaning moves, so the disagreement is harder to see.

Both failures turn a shared language back into a telephone game. Use the agreed word for the agreed thing, every time.

## Never make one kitchen's language the law

It is tempting to publish your words into the book. One list for the whole chain can look simpler than one interview in every kitchen.

Do not do it. **A shared language is only shared when the people using it agreed to it.** Keep your words local, and let the next owner have the same conversation you had.

---

## The rules, flat

*The same rules as above, with the explanation removed. This is the part the appliance
obeys.*

1. Interview the owner before any work begins, and agree shared meanings for the necessary words.
2. Ask questions and arrive at the words with the owner. Never present a form of terms chosen in advance.
3. Treat restaurant, kitchen, dish, chef and taster as worked examples only. Allow workshops, studios or plain terms instead.
4. Agree local words for who owns the place, who runs it day to day, who does the work, who checks it, the machine everyone works on and one unit of work.
5. Leave every other word unsettled until it is needed.
6. Write the agreed words down locally in that kitchen. Never write them back into this book; keep the book blank on local language.
7. Use the agreed word for the agreed thing every time. Never introduce a competing word for the same thing.
8. Keep each agreed meaning fixed. Never stretch a word to cover something else.


===== PRINTER-C =====

# 1. The interview

**What this chapter settles:** how to hold the first conversation with the appliance to agree the basic words your chain will use, and where those words are kept.

## Words come before any work

**Nothing can be agreed, checked, or handed over until both sides mean the same thing by the same word.** Your chain is a set of restaurants. The chefs are the workers. The dishes are units of work. If you say "kitchen" and the appliance thinks you mean the whole restaurant, every later instruction will miss.

The staff change every shift and remember nothing. The manual is the only thing allowed to hold still. So the first task is language, not cooking.

## The interview is a conversation, not a form

**The appliance sits with you and asks questions, and the two of you arrive at the words together.** You are not filling in blanks someone else chose. A form imposes its own words. An interview builds them with you.

The appliance does not know your chain yet. You know your trade. Together you name the things that must be named. This is the first shift, before any chef is hired or any dish made.

## This book's words are one owner's picture, not the law

**The words in this book — restaurant, kitchen, dish, chef, taster — are a worked example, not a rule.** They are how one owner sees the work, and that owner thinks visually. Another owner may think in workshops, or plain blunt terms with no picture.

Publishing one owner's pictures as law would impose them on every reader. So this book ships its examples, then stays blank where your words go. You are free to use your own.

## Only a few things must be named now

**Some things must have an agreed word or the rest of the book cannot be followed.** Those are: who owns the place, who runs it day to day, who does the work, who checks it, the appliance they all work on, and one unit of work.

Everything else can wait. The interview does not need your whole vocabulary. It needs the six that unlock the later chapters.

## The agreed words are written in the kitchen, not in this book

**The words are recorded locally, in that kitchen's own record, never back into these pages.** This book ships blank on this and stays blank. If your words were written here, every other owner would be forced to read your picture.

A local record means the next chef who comes on shift can be told the word without asking the appliance again. The book remains blank for every other owner.

## Once agreed, the words are fixed

**Nobody invents a competing word for the same thing later, and nobody stretches an agreed word into a more convenient meaning.** Both are how a shared language quietly stops being shared.

If "dish" means a unit of work, it cannot later mean a plate of food in the restaurant sense. If "taster" is the checker, you cannot later call the owner the taster. The fix is set so the telephone game does not begin.

## Steps

1. Sit with the appliance as the new owner.
2. Answer its questions and propose words for the six needed things.
3. Agree on a word for each, together.
4. Write those words in your local kitchen record.
5. Treat the words as fixed from that moment.

## What goes wrong

1. **You treat this book's words as the required terms.** Then you skip the interview and impose a picture that may not fit your trade.
2. **You answer fixed questions instead of talking.** Then the words are the appliance's, not yours, and the chain is not yours.
3. **You write the words into this book.** Then the book is no longer blank for others, and drift begins.
4. **You later use a second word for an agreed thing.** Then two words mean one thing and the staff split.
5. **You stretch a word's meaning.** Then the same word means two things and checks fail.

## The one thing never to do

Never treat this book's example words as the only allowed words. It is tempting because they are ready made and save the trouble of agreeing your own, but using them as law imposes one owner's picture on your chain and breaks the blank book.

## The rules, flat

1. Agree words with the appliance in conversation before any work begins.
2. Do not use a form or pre-chosen blanks; arrive at words together.
3. The words restaurant, kitchen, dish, chef, taster in this book are examples only, not required terms.
4. Name exactly these: owner, day-to-day runner, worker, checker, appliance, unit of work.
5. Write the agreed words in the local kitchen record.
6. Never write the agreed words into this book.
7. Once agreed, no competing word for the same thing may be introduced.
8. Once agreed, no agreed word may be stretched to a new meaning.

===== PRINTER-D =====

# 1. The interview

**What this chapter settles:** the six words you and the appliance must agree on before any work begins, and why they are yours to choose.

## Words come before everything else

Two people can agree to a plan in the same room, then walk out and do opposite things —
not because either one lied, but because **they meant different things by the same word.**

One person hears "done" and thinks the dish is plated. The other hears "done" and thinks
it has been tasted, sent back once, and plated again. Both readings are reasonable. Both
are wrong, because neither asked the other what they meant.

**The telephone game begins the moment a word has two meanings.** A recipe that says
"taste the dish" is useless if one side thinks tasting is biting into it and the other
thinks tasting is inspecting the plate. Nothing in this book works until the owner and
the appliance mean the same thing by every word they share.

That is why Part One comes first. No staff are hired in it. No work begins. It is only
language — but language is what every later instruction rests on.

## It is an interview, not a form

You are not filling in blanks that somebody else chose. **The appliance sits with you and
asks questions, and the two of you arrive at the words together.**

The appliance does not hand you a list of approved terms. It asks you what you call the
place, and you answer. It asks you who checks the work, and you give that person a name.
If the word you offer is unclear, the appliance asks again — not because you answered
wrong, but because the two of you have not yet landed on one you both hold the same way.

This matters because **the words will govern every instruction the appliance ever gives
or receives.** If those words were chosen by a stranger — the author of this book, the
maker of the appliance — they would fit a stranger's mind. They need to fit yours.

## The book's words are a worked example, not the law

This book says restaurant, kitchen, dish, chef, taster. Those are one owner's words, and
that owner happened to think in pictures. Another owner might think in workshops, or
studios, or plain blunt terms with no picture in them at all. None of those are wrong.

**If this book published its own words as the only allowed words, it would impose one
mind's habits on every reader.** The words in these pages are evidence that an interview
happened — not instructions for how yours must go. You are free to ignore every one of
them. The only requirement is that you and the appliance agree on what you chose.

## Six things must be named; everything else can wait

Not everything needs a word. Most things do not. Six do, because **every chapter after
this one leans on them:**

1. Who owns the place.
2. Who runs it day to day — who decides what gets worked on and in what order.
3. Who does the work.
4. Who checks the work before anything leaves.
5. The machine everyone works on.
6. One unit of work.

If any of those six is left unnamed, a future chapter will say "hand the dish to the
blank," and nobody will know what the blank is. Everything else — what you call a shift,
whether a failed dish goes back or gets scrapped — can wait until it is needed.

## The words are written down locally, never back into this book

Once you and the appliance agree on the six words, **they are written down in that
kitchen.** Not here. Not in a copy of this book. Not in a note you keep on your own
machine.

The book ships blank on this. It stays blank. That is deliberate. The words belong to
the kitchen they govern, and a kitchen halfway across the city does not need to know
what you call a taster.

## The words are then fixed

Agreement is not the end of it. Drift is the end of it if you let it.

Two things destroy a shared language. The first is **inventing a competing word for the
same thing later** — calling a taster a "reviewer" in one instruction and a "taster" in
another, until nobody can tell whether they are the same job or two different ones. The
second is **stretching an agreed word into a more convenient meaning** — calling anything
that leaves the kitchen a "dish," including things nobody tasted, because it was easier
than saying "untasted dish" and the habit crept in.

Both are how a shared language quietly stops being shared. The fix is simple: **once the
six words are agreed, they are locked.** Nobody renames them. Nobody repurposes them. A
word that no longer fits is replaced openly, by a new conversation — never by slow
erosion.

## The one thing never to do

Do not keep the book's words because they feel official. They are not official. They are
one owner's interview, written down so you could see what an interview looks like — not
so you could skip having your own. **Adopting a stranger's words is still adopting a
stranger's words**, even if they came from a book you trust.

---

## The rules, flat

*The same rules as above, with the explanation removed. This is the part the appliance
obeys.*

1. The interview is a conversation, not a form. The appliance asks; the owner answers.
   Nothing is pre-selected.
2. Six terms must be agreed before any work begins: who owns the place, who runs it day
   to day, who does the work, who checks it, the machine, and one unit of work.
3. The words in this book are a worked example. They are not required, not recommended,
   and not default. Ignore them freely.
4. The agreed words are written down in the kitchen they govern, never in this book.
   The book stays blank.
5. Once agreed, the six words are locked. No competing term may be introduced for the
   same thing. No agreed term may be stretched into a wider meaning.
6. A word that no longer fits is replaced by a new conversation — never by silent
   substitution.
