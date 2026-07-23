# Where the work is tracked — flat files in the repo, or GitHub Issues?

> **About this file.** This is the open hole this book leaves in its own faults record: "Where
> the job list lives for a kitchen with no shared tracker"
> (`KNOWN-HOLES.md`, the self-referential OPEN row whose "where it closes" points at "Part Two,
> ch. 12 — the operations log"). This research IS that open hole. It is the only file I touched,
> and it is left for the host to land.
>
> **Scope.** The question: *where should THIS kitchen track its open work — its tickets, holes and
> corrections — given that it is a public Claude Code plugin repo with a non-programmer owner,
> multiple AI-agent sessions sometimes working it in parallel, and a written doctrine that says
> "every session is a stranger" and "instructions travel, records never do"?* The candidates:
> in-repo flat files (as today), GitHub Issues, a hybrid, and the "issues-as-files" tools (git-bug
> and peers). Every option is weighed against the doctrine, and every option — including the one I
> recommend — is shown where it is wrong.
>
> **Headline finding.** The doctrine decides it, and it decides it cleanly. The work-tracker is a
> **record** ("records never do" travel — `WHERE-WE-ARE.md`, line 218), and a record must be local
> to the restaurant. A GitHub Issue is a record that lives on a third party's servers and **does
> not survive a plain `git clone`** — confirmed against GitHub's own docs — so it breaks the
> project's hardest rule by definition. **The in-repo flat files stay as the system of record.**
> GitHub Issues earn a place only as a **one-way public mailbox** for plugin readers to report
> bugs, triaged into the repo on each session and closed with a pointer — never as a second board.
> And the one thing that has actually cost this repo real work — two parallel sessions colliding —
> is **not fixed by changing the tracker at all**; the evidence says it is fixed by worktree
> isolation, which this repo already mandates.

---

## 1. The options, and the criteria (with what I changed and why)

### The options

1. **In-repo flat files (as today).** `TICKETS.md` is the live plan (claim → work → finish, each
   with a measurable done-condition); `KNOWN-HOLES.md` is the frozen record of evidence; each
   ticket points back to its hole so the two cannot drift apart (`TICKETS.md`, lines 1–14).
2. **GitHub Issues.** Labels, milestones, Projects boards, assignees; one issue per item; auto-link
   to the PR that fixes it.
3. **Hybrid.** GitHub Issues for live per-item state; a thin in-repo pointer file so a stranger
   session finds the work; `KNOWN-HOLES.md` kept as frozen evidence.
4. **"Issues-as-files" in git — git-bug and peers.** Added by me. Distributed, offline-first bug
   trackers that embed issues *inside* the git repository itself.

### The criteria, re-ordered

I re-ordered the eight given criteria and added two, because two of them are not just items on a
list — they have **primary evidence specific to this kitchen**, and the rest are general
preferences. Preferences do not override measured facts.

| # | Criterion | Why its rank |
|---|---|---|
| **C1** | **A stranger session can find and act on the work from the repo ALONE — no network, no login.** (Original 1 + 5, merged: they are the same test.) | **Top.** This is the book's first rule, stated three times: "every session is a stranger; the process lives in the repo, never in a conversation." A tracker that fails this fails the doctrine. |
| **C2** | **Consistency with the doctrine** ("records never travel"; "process lives in the repo"). (Original 7.) | **Top.** The owner named this the governing doctrine and asked every option be weighed against it. |
| **C3** | **NEW — does the option create a second copy of a promise that can drift?** | Added because "two copies of one promise drifting apart" is the single fault this book exists to catch — it appears in roughly a dozen rows of `KNOWN-HOLES.md`. A tracker that manufactures a third copy is a tracker that manufactures the book's named enemy. |
| **C4** | **Two parallel sessions do not collide.** (Original 2.) | High, with a correction below. This repo has recorded **two real collisions**, so the criterion is backed by fact, not preference — but the evidence changes what the criterion actually measures (see §3). |
| **C5** | **A non-programmer owner can read and use it.** (Original 3.) | High. The owner is not a programmer (`CLAUDE.md`). |
| **C6** | **Real lifecycle: claim, close, search, dedup, link to the commit/PR that fixed it.** (Original 4.) | Medium. Real, but the repo already does most of this by hand and at ~18 items it has not strained. |
| **C7** | **Public plugin readers can report bugs into it.** (Original 6.) | Medium. The plugin ships (`.claude-plugin/marketplace.json`), so public readers exist — but this is the *only* criterion the current flat files genuinely fail. |
| **C8** | **Migration + maintenance cost from today.** (Original 8.) | Low-medium. ~18 items already live in `TICKETS.md`; the cost of staying put is ~zero. |

What I **dropped or did not add**: I did not raise "GitHub Projects gives pretty boards/roadmaps" to
a criterion of its own — it is a view on top of Issues, not a separate place to put the record, and
a view is a preference, not a fact about whether the work is findable. I considered "survives the
host disappearing" as a criterion and folded it into C1/C2: it is the same test (is the record in
the repo, or on a server we do not control?).

---

## 2. The weighed comparison — and where EACH option is wrong

A summary table first, then the wrongness of each in turn. No option scores flawlessly.

| Criterion | 1. Flat files | 2. GitHub Issues | 3. Hybrid | 4. git-bug |
|---|---|---|---|---|
| **C1** repo-alone, offline | **PASS** | **FAIL** (not in clone) | PARTIAL (pointer yes, live state no) | PARTIAL (in clone, but opaque without the tool) |
| **C2** doctrine (records local) | **PASS** | **FAIL** (record on 3rd-party server) | PARTIAL | PARTIAL |
| **C3** no drifting second copy | PASS (one copy) | PASS (one copy) | **FAIL** (two copies by design) | PASS |
| **C4** parallel sessions don't collide | FAIL* | FAIL* | FAIL* | FAIL* |
| **C5** non-programmer can use | **PASS** (it is a document) | Pass (web UI) but needs a login | Pass (both) | FAIL (CLI/TUI tool) |
| **C6** full lifecycle | Weak (manual, no auto-link) | **PASS** (`closes #N`, search, labels) | Pass (via Issues) | Pass (CLI) |
| **C7** public bug intake | FAIL | **PASS** | **PASS** | FAIL (no hosted web UI) |
| **C8** migration cost | **~zero** | Medium (migrate 18) | Medium-high (migrate + keep two in sync) | High (new tool for every session) |

\*Every option fails C4 — see §3. That is the most important cell in the table and the reason no
tracker choice alone fixes what has actually hurt this repo.

### Where option 1 (flat files) is WRONG

- **No public button.** A plugin reader who hits a bug cannot "file a ticket" without opening a
  pull request against `TICKETS.md`. This is the one criterion the current setup genuinely fails (C7).
- **No auto-link to the fix.** There is no `closes #N`. The repo replaces it with a manual rule —
  "when a ticket is done, strike it here and update its hole in `KNOWN-HOLES.md` **in the same
  commit**" (`TICKETS.md`, line 6) — and that rule is honest labour, not a machine guarantee. A
  forgotten strike is exactly the "record that quietly went stale" the book warns is *worse than one
  nobody wrote down, because it looks handled* (`KNOWN-HOLES.md`, the operations-log row).
- **Search and dedup are human.** Fine at eighteen items; weak at two hundred.

### Where option 2 (GitHub Issues) is WRONG — and this is decisive

- **Issues are not in the repository.** A `git clone` copies commits, branches and tags — not
  issues, which live in GitHub's database. Confirmed by GitHub's own "About issues" page, by a
  direct explanation of what `.git/objects` actually holds, and by the canonical Stack Overflow
  answer. A stranger session that clones this repo and goes offline **cannot see the work at all**.
  That fails C1 outright, and because the work-tracker is a record, it fails the doctrine (C2) too:
  a record on a third-party server is the opposite of "records never travel."
- **It does not fix the collision.** See §3 — two agents will both see an issue as "unassigned" and
  both start it, exactly as they both picked up chapters 9 and 10 here. Assignees help a human notice;
  they do not stop an autonomous session that does not check them.
- **Lock-in.** The record becomes hostage to a platform's terms, API and UI. The book's parked note
  itself frames the harder case — "where the job list lives when a kitchen has no GitHub"
  (`WHERE-WE-ARE.md`, line 204) — and this kitchen answers "we have GitHub today," but a record that
  only exists *because* of GitHub has quietly bet the project's memory on that staying true.

### Where option 3 (hybrid) is WRONG

- **It builds the book's named enemy on purpose.** A thin in-repo pointer plus a live GitHub board
  are, by construction, two copies of the same promise. `KNOWN-HOLES.md` records this fault roughly
  a dozen times — two copies of the ruler, of the brief, of the running order — and every one of them
  drifted. Adding a third place for the same facts is the one move this book's own evidence argues
  against most loudly (C3).
- **Maintenance doubles.** Every state change must be made in two places or the pointer rots — and a
  rotted pointer is precisely the "stale where-it-closes" fault `KNOWN-HOLES.md` calls worse than
  nothing. The hybrid is only defensible if the pointer is kept deliberately thin and reconciled on
  every landing, which is a discipline cost forever.

### Where option 4 (git-bug) is WRONG — and why I dropped it

git-bug is real, maintained (about 10,000 stars, releases through 2025), and genuinely clever: it
"embeds issues, comments, and more as objects in a git repository (*not files!*)" so they survive a
clone and merge like code. In theory it gives the offline survival of flat files with the per-item
structure of Issues.

It is the wrong fit here, for three reasons that the evidence makes plain:

- **It fails C1 anyway.** git-bug data rides inside the clone, yes — but as git *objects*, not as
  readable documents. A stranger session without the git-bug binary sees opaque blobs, not a board it
  can read. This repo's whole philosophy is that a stranger reads the repo with **no setup**; git-bug
  demands a tool install first.
- **It fails C5.** It is a CLI/TUI (and an optional local web UI), not a document a non-programmer
  owner opens and reads. The owner is explicitly not a programmer.
- **It fails C7, decisively.** The clearest primary source on this whole family is a survey by Jelmer
  Vernooĳ, a long-standing free-software contributor, who tried every distributed bug tracker and
  concluded they "fail to even provide the basic functionality I would want in a bug tracker,"
  because "regular users interact with a bug tracker. They report bugs, provide comments and
  feedback on fixes. All of the systems I tried make these actions a lot harder than with your
  average bugzilla or mantis instance — they provide a limited web UI or no web interface at all."
  That is a direct failure of the one thing a public plugin needs: a place a reader can file a bug
  without installing anything. git-bug's bridges to GitHub exist, but at that point GitHub Issues is
  doing the public work anyway.

So git-bug is **dropped**: it buys the offline property the flat files already have, loses the
readability the flat files already have, and fails the public-intake property that is the only real
gap. It solves a problem this kitchen does not have (distributed tracking with no host) because this
kitchen *has* a host.

### What I kept from the alternatives (the refinement, not a fifth option)

Two ideas from the wider landscape are worth borrowing into option 1 rather than adopting whole:

- **The ADR pattern for the frozen record.** Architecture Decision Records are markdown files kept
  in the repo, each with a **Status** field (proposed / accepted / **superseded**). The decisive
  property is that a decision is never silently edited — when it changes, its status flips to
  *superseded* and the new one is written beside it, leaving the original readable. That is already
  this repo's discipline: `KNOWN-HOLES.md` strikes a closed hole with `~~~~` and keeps the original
  text, "because a record that quietly corrects itself is the failure this book is about." The ADR
  literature is the published validation of exactly that practice — its originator, Michael Nygard,
  framed the same five-part shape (Title, Status, Context, Decision, Consequences) in 2011. Naming
  what `KNOWN-HOLES.md` already does — "these are ADRs, and the Status field is the strike-through"
  — costs nothing and makes the convention teachable to a stranger.
- **The kernel's split between inline and structured.** The Linux kernel does not keep one big
  `TODO.md`. It uses thousands of small `TODO`/`FIXME` notes *inline at the code*, plus structured
  TODO pages under `Documentation/` rendered into the published docs, plus the mailing list for
  larger work. The transferable lesson: small, local, in-the-page notes and one structured in-repo
  list are not in tension — they are the two layers the kernel has used for decades, all of it in the
  tree. This repo already runs the same shape: per-page notes live in the chapters, and the
  structured list is `TICKETS.md`.

---

## 3. The collision criterion — why the tracker choice does not decide it

This deserves its own section because it is the one place the evidence most cleanly contradicts the
obvious story ("move to GitHub Issues so parallel sessions stop colliding"). The story is wrong, and
this kitchen's own record proves it.

**What actually collided here.** The two recorded collisions (`WHERE-WE-ARE.md`, "Two sessions
worked this repository at once") were **not** merge conflicts on `TICKETS.md`. They were two sessions
that **picked up the same ticket** and did the same work — chapters 30/31 on 2026-07-22, and
chapters 9/10 on 2026-07-23, the second one "committing into the same folder minute by minute, each
mostly re-finding what the other had already found." The fault the page names is a coordination
fault: "neither session could tell it was happening until commits appeared under its feet."

**Why no static tracker fixes that.** Whether the board is a file or a website, two autonomous
sessions that both read "this ticket is open and unclaimed" will both start it. A human glances at
the assignee field; an agent session does not, unless its instructions tell it to. GitHub Issues
therefore buys nothing here that the flat file does not — and the page's own conclusion is the
sharpest line in the repo: *"That is an argument for a second pair of EYES. It is not an argument
for a second pair of HANDS."*

**What the wider evidence says fixes it.** The people running many AI coding agents in parallel
report the same thing: the breakdown is not the tracker, it is the lack of *isolation*. The fix they
converge on is one git worktree per session — "each AI session should behave like an isolated feature
branch — automatically… its own git worktree" — because, in that author's words, "layout is not
workflow." This repo **already mandates** exactly that: the worktree invariant in `CLAUDE.md`
requires every writer to move into an isolated worktree before touching a file, and the model-flow
harness enforces one writer per worktree with a file lock. The collision on 2026-07-23 happened
because *two writers shared one folder*, breaking that invariant — not because the board was a file.

**The honest upshot.** The collision is an isolation-discipline problem, and changing the tracker is
a misdiagnosis that would spend a migration to fix nothing. The recommendation in §4 leaves the
tracker alone and treats the collision as already-solved-by-a-rule-that-was-bent-once. That is the
non-rubber-stamp answer the owner asked for: I am not endorsing flat files because they are
familiar, I am endorsing them because the one rival argument for Issues (parallelism) does not
survive the evidence.

---

## 4. Recommendation

**Keep the in-repo flat files as the system of record, and open GitHub Issues only as a one-way
public mailbox for plugin readers — not as a second tracker.**

Concretely:

1. **`TICKETS.md` stays the live plan; `KNOWN-HOLES.md` stays the frozen record.** They are records,
   the doctrine says records never travel, and a record on GitHub's servers does not survive a clone.
   This passes C1, C2 and C8 (~zero migration) at the cost of C6's manual linking and C7's missing
   public button.
2. **Name `KNOWN-HOLES.md` as ADRs** (Status = the strike-through). Costs nothing, makes the
   convention legible to the next stranger, and aligns the repo with a published practice rather
   than a private one.
3. **Open GitHub Issues as an intake mailbox only.** Plugin readers file bugs there; each session
   triages any open issue into `KNOWN-HOLES.md` (the evidence) and `TICKETS.md` (the plan), then
   **closes the issue with a comment pointing at the commit and the ticket row**. The issue never
   holds the live state — it is a letterbox, not a board. This closes C7 (the one real gap) while
   keeping a single source of truth, so C3 holds.
4. **Do not move the live board to GitHub Issues, and do not build the hybrid.** Both fail C2 or C3,
   and neither fixes C4 (§3). The hybrid in particular manufactures the two-copies-of-one-promise
   fault this book exists to catch.
5. **Treat the collision as solved-by-discipline, not by tooling.** The worktree invariant already
   exists; the fix for "two chefs cooked the same ticket" is one writer per worktree (already the
   rule) plus a claiming convention — a session writes its claim into the ticket row before starting,
   so a second reader sees it. No tracker migration is involved.

**The citations that back this recommendation:**

- A GitHub Issue is not in the clone — GitHub, "About issues"; Julia Evans, "In a git repository,
  where do your files live?"; Stack Overflow #19938579. This is the load-bearing fact against option 2.
- `closes #N` / `fixes #N` auto-close the issue **only** when the PR or commit lands on the default
  branch — GitHub, "Linking a pull request to an issue." This is what makes the mailbox's
  "close-with-a-pointer" step automatic and cheap.
- ADRs use a Status field and are never silently edited — Nygard, "Documenting Architecture Decisions"
  (2011); the ADR templates portal. This validates the strike-through convention already in
  `KNOWN-HOLES.md`.
- Parallel-agent collisions are fixed by worktree isolation, not by the tracker — Johannes Millan,
  "Why Multitasking With AI Coding Agents Breaks Down."
- Distributed bug trackers fail at public intake — Jelmer Vernooĳ, "The state of distributed bug
  trackers." This is the load-bearing fact against option 4.
- The doctrine itself, and the two real collisions, are primary to this kitchen — `WHERE-WE-ARE.md`
  (line 218 for "records never do"; the parallel-sessions section for both collisions; line 204 for
  the parked "no GitHub" note) and `KNOWN-HOLES.md` (the self-referential open row that is this hole).

---

## 5. The probe — measurable pass/fail, so the owner can prove it before committing

The owner's standing rule is "measured, or it's an opinion." Three cheap probes, cheapest first.
Each predicts a number that must move, so the recommendation is **falsifiable** before it is adopted.

### Probe A — the stranger-finds-the-work test (tests C1, the doctrine core; ~zero cost)

Migrate nothing. Clone the repo fresh. Hand it to a brand-new session that has never seen it, with
only the prompt *"this is a cookbook plugin repo; pick up the next open job and tell me what 'done'
means for it."* No mention of GitHub.

- **PASS** — the session, reading only files in the clone (`WHERE-WE-ARE.md` → `TICKETS.md` →
  `KNOWN-HOLES.md`), correctly names the next P1 ticket, its measurable done-condition, and its
  evidence row in `KNOWN-HOLES.md`.
- **FAIL** — it cannot find the work, or names a ticket that is already closed/stale.

Prediction: **PASS today**, because the reading order is already wired and the self-referential hole
this research fills is the only gap in it. The point of running it is to *measure* that the doctrine
is satisfied before touching anything — which is itself the argument against moving the live board
off-repo.

### Probe B — the mailbox round-trip (tests C7 + that the mailbox stays one-way; one issue)

From a second account, file ONE real GitHub Issue labelled `intake` (simulate a plugin reader
reporting a bug). The next session must triage it.

- **PASS** — within one session: (a) if the report is real, it is written into `KNOWN-HOLES.md`
  (evidence) **and** given a row in `TICKETS.md` (plan), and the GitHub issue is **closed with a
  comment pointing to the commit and the ticket number**; (b) if not real, it is closed with the
  reason; and (c) the closed issue and the repo record **do not contradict each other**.
- **FAIL** — the issue stays open and un-mirrored (the mailbox has become a second, drifting board),
  OR the repo record disagrees with the issue.

This is the probe that could change the add-on. If the mailbox keeps drifting across a few real
intakes, drop it and accept C7 as an honest limit (readers open a PR instead) rather than carry a
second tracker.

### Probe C — the collision falsifier (tests C4; two sessions, ~an hour)

Give two sessions the repo alone, each told *"pick the next open ticket and start."* Run it twice:
once with the flat-file board only; once with the same two tickets mirrored as GitHub Issues (so the
assignee field is available).

- **PASS for an arm** — at most one session works a given ticket, OR the collision is detected
  before any duplicate commit lands.
- **FAIL** — two sessions do the same ticket and one set of checks is thrown away (the 2026-07-23
  outcome).

Prediction: **both arms FAIL the strict test**, because detection needs live coordination no static
tracker gives an autonomous agent. If confirmed, that **falsifies** "moving to GitHub Issues fixes
collisions" — the claim most worth testing — and the fix routes to worktree isolation (§3) instead.
If, against expectation, the Issues arm's assignee field lets the second session back off, that is
the one finding that would weaken the recommendation.

---

## 6. Confidence, and what could change the answer

**What I am sure of (primary-sourced, not opinion):**

- GitHub Issues are absent from a `git clone` (GitHub's own docs; Julia Evans; Stack Overflow). They
  live on GitHub's servers. This is not contested.
- `closes`/`fixes`/`resolves` + `#N` auto-closes an issue when the change lands on the default
  branch, and works in a commit message as well as a PR description (GitHub docs).
- git-bug stores issues as git objects, not working-tree files, and needs its own binary to read
  them (git-bug README). It is real and maintained, not theoretical.
- The "issues-as-files" family fails public bug intake — the people who have actually tried them say
  so, and say it has not improved (Vernooĳ's survey; "TL;DR: Not much has changed since").
- ADRs carry a Status field and are not silently rewritten (Nygard; adr.github.io).
- This repo's two collisions were two sessions picking the same ticket — a coordination fault, not a
  tracker-file merge conflict (`WHERE-WE-ARE.md`).

**What I am uncertain about (honest gaps):**

- Whether plugin readers would actually use a GitHub Issues mailbox, or just open a PR. No data on
  this repo's readership exists yet — Probe B is the cheap way to find out.
- Whether the one-way-mailbox discipline holds over time. It is the single drift risk in the
  recommendation, and Probe B exists specifically to catch it failing.
- The owner's tolerance for requiring a GitHub login to file or comment on a bug (C5's edge). That
  is a preference, so it is the owner's to decide, not mine to assert.

**What single fact would flip the recommendation:**

- **If this kitchen ever loses GitHub** — moves to a host without it — then the parked note's "no
  GitHub" case activates and the answer becomes "a flat file, or a small local database," full stop.
  The book's own parked row already frames this exact contingency.
- **If the ticket count grows into the hundreds**, flat-file search and dedup weaken enough that a
  structured live board is worth its clone cost — which is the moment the hybrid earns its keep
  despite C3. At ~18 items, that threshold is nowhere near.
- **If Probe C surprises me** and GitHub Issues' assignee field actually prevents the collision, that
  is the one result that would reopen option 2/3 for live state.

---

## Source list (primary)

**This repo (primary to the question):**

- `WHERE-WE-ARE.md` — line 218 ("Instructions travel, records never do"); the parallel-sessions
  section (both collisions); line 204 (the parked "no GitHub" note).
- `KNOWN-HOLES.md` — the self-referential OPEN row ("Where the job list lives for a kitchen with no
  shared tracker"); the plan/record split (lines 11–14); the "stale where-it-closes is worse than
  unwritten" pattern (operations-log row).
- `TICKETS.md` — the existing board, its columns, its measurable done-conditions, and the
  "strike the row and update the hole in the same commit" rule (line 6).
- `README.md` and `.claude-plugin/marketplace.json` — the plugin ships; public readers exist.

**External (primary unless noted):**

- GitHub, "About issues" — `https://docs.github.com/issues/tracking-your-work-with-issues/about-issues`
- GitHub, "Linking a pull request to an issue" — `https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue`
- GitHub, "About Projects" — `https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects`
- Julia Evans, "In a git repository, where do your files live?" — `https://jvns.ca/blog/2023/09/14/in-a-git-repository--where-do-your-files-live-/`
- Stack Overflow, "Is possible to store repository issues in the git repository?" — `https://stackoverflow.com/questions/19938579/is-possible-to-store-repository-issues-in-the-git-repository`
- git-bug README — `https://github.com/git-bug/git-bug` (issues as git objects, not files; ~10k stars; bridges to GitHub/GitLab)
- Jelmer Vernooĳ, "The state of distributed bug trackers" — `https://jelmer.uk/distributed-bug-trackers.html` (the "fail to provide basic functionality / no web UI for reporters" finding)
- Michael Nygard, "Documenting Architecture Decisions" (2011), and the ADR templates portal — `https://adr.github.io/adr-templates/` (Status field; never silently edited)
- Linux kernel, DRM TODO list — `https://docs.kernel.org/gpu/todo.html` (in-tree structured TODO under `Documentation/`); inline TODO-comment convention noted via `https://news.ycombinator.com/item?id=21910391`
- Johannes Millan, "Why Multitasking With AI Coding Agents Breaks Down (And How I Fixed It)" — `https://dev.to/johannesjo/why-multitasking-with-ai-coding-agents-breaks-down-and-how-i-fixed-it-2lm0` (the fix is one worktree per session)
- Aider, "How to add a multi-agent flow?" — `https://github.com/Aider-AI/aider/issues/1839` (the `scratchpad.md` state-file pattern)
- Josef, "Migrating Content from Markdown to GitHub" — `https://josef.dev/posts/migrating-content-from-markdown-to-github/` (a firsthand markdown↔issues migration; the migration is bounded work; files are universally readable, issues require the platform)

**Thin evidence (flagged):** I read the primary docs and the two firsthand accounts (Millan, Josef)
in full; the kernel and ADR material via the official pages. I did not find a measured, comparative
study of flat-file vs. issue-tracker *for AI-agent-driven repos specifically* — that gap is exactly
why §5 is a probe rather than a verdict. The doctrine and the two collisions, which carry the
decision, are primary to this kitchen and need no external source.
