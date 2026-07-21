# The Cookbook — table of contents

**Status: draft, nothing written yet.** This page decides what belongs in the book. It is
the running order, not the book.

## Where this comes from

Compiled from everything the chain currently knows, not from memory:

- the chain's standards, the wall notes themselves — `~/.claude/CLAUDE.md`, 123 lines
- the restaurant's own local rules and vocabulary — `opencode-verify/CLAUDE.md`
- the reasons and corrections behind the vocabulary — the `restaurant-vocabulary` memory
- the automatic checks that run at every session start — 3 hooks in `~/.claude/settings.json`
- the skills the standards actually lean on — `wayfinder`, `model-flow`, `handoff`, and others

## The sort: three piles, not two

The plan said the notes split in two — the portable method, and the machine-specific staff.
Reading them properly, there is a third pile, and it is the one that would have ruined the
book if it went unnoticed.

| Pile | What it is | Travels? |
|---|---|---|
| **How we cook** | True in any kitchen, whoever owns it, whoever staffs it | Yes — this is the book |
| **What we call things** | Our cooking words are *this owner's* way of seeing. Another owner may think in workshops, or in plain blunt terms. | The **interview** travels; the words are personal |
| **Who works here** | The staff, their names, their commands, their file paths | No — filled in locally |

Miss the middle pile and the book forces its own metaphor on every reader and claims to be
universal while doing it. **The book teaches how to cook; the interview decides what
language you cook in.** The recipes are unchanged either way.

A fourth thing came out of the compile that the plan had not accounted for: **some rules are
not words at all.** Three automatic checks already run at every session start on this
machine — one of them is the doorman that stopped this very session and sent it to its own
prep bench. A book that prints the rule but not the doorman is a book of good intentions.
Part Four exists because of that.

---

# Part One — How we cook

The method. Same in every kitchen, whatever it calls itself. This is the actual book.

1. **Check you are standing somewhere real.** No handbook and no repository where you are
   means no kitchen — say so and ask, do not proceed. First because everything else assumes it.
2. **The words we use.** The roles: the owner, the one head chef who runs a place, the chefs
   who cook, the taster who is never the cook. The things: a place, its setup, what it is
   building, one job of work. And **the appliance** — the machine the chefs cook on; ours is
   Claude Code. Carries the correction that one word must never do two jobs.
3. **Who decides what.** The owner sets direction; one head chef per place runs it. Ask when
   it is a preference, a coin-flip, hard to undo, or a guess. Decide alone when it is written
   down, checkable, cheap to reverse. **Never ask a question you already know the best answer to.**
4. **How to explain yourself.** One question at a time, carrying your recommendation, so
   "yes" is a complete reply. When an explanation fails, rewrite it from scratch — adding
   detail is what made it fail.
5. **Every session is a stranger.** Nobody remembers yesterday, so the process lives where
   the work lives, never in a conversation. The telephone game: `123456 → 12345 → 12`.
6. **One job at a time, and claiming it.** A job being cooked wears a tag; nobody touches a
   tagged job. One job, one chef, start to finish — who may call in specialists, and whose
   work is always tasted by someone else. This is what stops two chefs reaching into one bowl.
7. **Charting when you are lost — and only then.** A map is for fog: a goal too big to see
   the way to. You stop mapping the moment the way is clear, and then you just cook. **A
   recipe is not a map.** Most work needs no map at all, and drawing one anyway is ceremony.
8. **Cooking without colliding.** Two chefs on two different jobs is normal; each gets their
   own prep bench, never the shared counter. Save your work as you go. How to hand a finished
   job back cleanly. Never rewrite history someone else is standing on.
9. **Secrets never leave the building.** No keys, no private files, no owner-private material
   sent to any outside worker — checked before the work is handed over, not after.
10. **The tasting rules.** Nothing is finished until: you ran the tests yourself, an
    independent taster who saw the *final* state approved it, you read every line of the change
    and vouch for it, and the taster was asked outright whether it fully does what was asked.
    **The taster is never the cook.** If a check is unavailable, say so — never silently skip it.
11. **A worker never hires a worker.** A chef sent out to cook does not send someone else.
    Stated as a principle here; the local names for it live in Part Three.

# Part Two — Agreeing on words

The book's first act in a new kitchen, before any cooking.

12. **The interview.** The appliance sits down with its new owner and agrees a shared set of
    words, together — how they see the work, how much they want explained, whether pictures
    help or get in the way, how they want to be asked. The output is written down where the
    work lives, so every later session inherits it instead of re-inventing it. Ships with
    **this** kitchen's interview filled in as a complete worked example — restaurants, dishes,
    tasters and all — clearly marked as one answer, not the answer.

# Part Three — Who works here

Forms, not answers. Every kitchen has different staff.

13. **Naming your staff.** Who writes, who analyses, who tastes, who does the small
    mechanical jobs — and which class of work each one is trusted with.
14. **When someone is off sick.** What happens when a worker is unavailable: the stand-in,
    and recording honestly that a stand-in was used rather than relabelling it.
15. **Wiring them up.** Where credentials live on a machine, and why they never live in this
    book.

# Part Four — What the book enforces by itself

The rules that are not words.

16. **The doorman.** The check at every session start that gives each chef their own prep
    bench and keeps them out of each other's way.
17. **What ships in the box.** *Decided: batteries included.* The book carries the handful of
    tools its own rules depend on — roughly six. If the book says "chart it when you are lost"
    and no map-making tool ships with it, the instruction is empty, and a rule nobody can
    follow is exactly the drift this chain exists to prevent. The owner's other tools stay
    private.

# Appendix

18. **What we deliberately left out, and why.** So a later reader does not mistake a decision
    for an oversight.

---

## Nothing was dropped in the sort

Every section of the current wall notes, and where it went:

| Wall note section | Goes to |
|---|---|
| Runtime role / recursion ban | Ch. 11 (principle) + Ch. 13 (local names) |
| How to talk to me | Ch. 2, 3, 4, 5 (method) + Ch. 12 (the interview) |
| Worktree invariant | Ch. 8 + Ch. 16 |
| Model routing tables | Ch. 13, 14 — all of it local |
| Secrets | Ch. 9 |
| Final validation gate | Ch. 10 |
| Hard constraints | split: method → Ch. 10; runner commands → Ch. 13 |

## Settled while drafting

- **Batteries included** (Ch. 17) — the book carries the tools its rules depend on.
- **A map is only for fog** (Ch. 7) — the map-making tool says so about itself. Recipes,
  jobs and maps are three different things and were previously blurred into one chapter.
- **One job, one chef** (Ch. 6) — plus an independent taster. Two chefs on one job is
  prevented by *claiming*; two chefs on different jobs is normal and handled by the doorman.
- **The appliance** (Ch. 2) — the machine the chefs cook on. Ours is Claude Code.

## Open

- **Where the job list lives** when a kitchen has no GitHub. Candidates weighed: plain
  documents, a structured file, or a small database. Undecided — see the recommendation
  put to the owner.
