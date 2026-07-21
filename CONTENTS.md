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
| **Who you are** | The owner's own preferences. *"I am not a programmer, explain with analogies"* is **this owner's** instruction, not a law of cooking. | The **slot** travels; the answer is personal |
| **Who works here** | The staff, their names, their commands, their file paths | No — filled in locally |

Miss the middle pile and the book patronises every reader who is a programmer, while
claiming to be universal. The book ships a blank owner's card with ours filled in as the
worked example.

A fourth thing came out of the compile that the plan had not accounted for: **some rules are
not words at all.** Three automatic checks already run at every session start on this
machine — one of them is the doorman that stopped this very session and sent it into an
isolated workspace. A book that prints the rule but not the doorman is a book of good
intentions. Part Four exists because of that.

---

# Part One — How we cook

The method. Same in every kitchen. This is the actual book.

1. **Check you are standing in a restaurant.** No handbook and no repository where you are
   means no kitchen — say so and ask, do not proceed. First because everything else assumes it.
2. **The words we use.** Chain, restaurant, kitchen, menu, dish. Owner, head chef, chefs,
   taster. Every later chapter is written in these words, so they come early. Carries the
   correction that *kitchen* must never be used for the portable thing.
3. **Who decides what.** The owner sets direction; one head chef per restaurant runs it.
   Ask when it is a preference, a coin-flip, hard to undo, or a guess. Decide alone when it
   is written down, checkable, cheap to reverse. **Never ask a question you already know the
   best answer to.**
4. **How to explain yourself.** One question at a time, carrying your recommendation, so
   "yes" is a complete reply. When an explanation fails, rewrite it from scratch — adding
   detail is what made it fail.
5. **Every session is a stranger.** Nobody remembers yesterday, so the process lives in the
   repository, never in a conversation. The telephone game: `123456 → 12345 → 12`.
6. **Tracking the work.** Efforts as maps, dishes as tickets, claimed before they are cooked,
   one at a time. Editing a shared map safely when other sessions hold it open.
7. **Cooking without colliding.** Work in an isolated copy, never the main one. Commit as you
   go. How to land cleanly. Never rewrite history someone else is standing on.
8. **Secrets never leave the building.** No keys, no private files, no owner-private material
   sent to any outside worker — checked before the work is handed over, not after.
9. **The tasting rules.** Nothing is finished until: you ran the tests yourself, an
   independent taster who saw the *final* state approved it, you read every line of the change
   and vouch for it, and the taster was asked outright whether it fully does what was asked.
   **The taster is never the cook.** If a check is unavailable, say so — never silently skip it.
10. **A worker never hires a worker.** A chef sent out to cook does not send someone else.
    Stated as a principle here; the local names for it live in Part Three.

# Part Two — Who you are

One short chapter. A card the owner fills in.

11. **The owner's card.** Your expertise, how much detail you want, whether explanations
    should lean on analogies, how you want to be asked. Ships with this owner's card filled
    in as a worked example, clearly marked as an example to overwrite.

# Part Three — Who works here

Forms, not answers. Every kitchen has different staff.

12. **Naming your staff.** Who writes, who analyses, who tastes, who does the small
    mechanical jobs — and which class of work each one is trusted with.
13. **When someone is off sick.** What happens when a worker is unavailable: the stand-in,
    and recording honestly that a stand-in was used rather than relabelling it.
14. **Wiring them up.** Where credentials live on a machine, and why they never live in this
    book.

# Part Four — What the book enforces by itself

The rules that are not words.

15. **The doorman.** The check at every session start that keeps sessions out of each other's
    way.
16. **What ships in the box.** The tools the method depends on. If the book says "track work
    as maps" and the map-making tool does not ship with it, the instruction is empty — a rule
    nobody can follow is exactly the drift this chain exists to prevent.

# Appendix

17. **What we deliberately left out, and why.** So a later reader does not mistake a decision
    for an oversight.

---

## Nothing was dropped in the sort

Every section of the current wall notes, and where it went:

| Wall note section | Goes to |
|---|---|
| Runtime role / recursion ban | Ch. 10 (principle) + Ch. 12 (local names) |
| How to talk to me | Ch. 2, 3, 4, 5 (method) + Ch. 11 (personal) |
| Worktree invariant | Ch. 7 + Ch. 15 |
| Model routing tables | Ch. 12, 13 — all of it local |
| Secrets | Ch. 8 |
| Final validation gate | Ch. 9 |
| Hard constraints | split: method → Ch. 9; runner commands → Ch. 12 |

## Known gaps

- **Chapter 6 depends on a tracker.** Ours is GitHub issues. A stranger may have none. The
  chapter needs a plain fallback, or it becomes a rule nobody can follow.
- **Chapter 16 is unscoped** — see the open question below.
