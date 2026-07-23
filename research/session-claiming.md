# Session claiming — how two parallel sessions stop doing the same ticket twice

> **About this file.** This is the research for T-19: two worktree-isolated sessions can both claim
> the same ticket, because each session is on its own branch and never sees the other's claim until
> the branches merge. The recorded fix — "write your claim into the ticket row before starting" —
> does not work under the worktree invariant. This research investigates what does.
>
> **Scope.** The question: *how do two autonomous AI-agent sessions, each in its own isolated git
> worktree, coordinate so that at most one works a given ticket — or the clash is detected before a
> duplicate commit lands?* The candidates: in-repo mechanisms (a claims file on the shared branch, a
> dedicated git ref, the existing flock-based lock) and off-repo mechanisms (GitHub Issues assignee,
> GitHub API, an external coordination service). Every option is weighed against the repo-alone rule
> (the process lives in the repo so a stranger session finds it offline), and every option — including
> the one I recommend — is shown where it is wrong.
>
> **Headline finding.** The collision is not a tracker problem; it is a **claim-before-start protocol**
> problem. The two real collisions here (2026-07-22, 2026-07-23) were two sessions that both read
> "this ticket is open and unclaimed" and both started it — not because the board was a file, but
> because neither session **checked** before starting. An off-repo tracker (GitHub Issues assignee)
> does not magically fix it: an agent that does not check the assignee field clashes just the same.
> The variable to solve is the claim-BEFORE-start protocol, not the storage location. **The
> recommendation is an in-repo claims file on the shared branch (`main`), using `git push` atomicity
> as a distributed lock: a non-fast-forward push is rejected server-side, so the loser of a race can
> detect it and back off.** This is a real distributed lock primitive that lives in the repo, survives
> a `git clone`, and costs nothing to adopt. It is not perfect — a crashed session holding a claim
> forever is its weakest point — but it is the only mechanism that satisfies the repo-alone rule,
> actually observes the claim BEFORE starting, and uses git mechanics the repo already relies on.

---

## 1. The candidate mechanisms and the criteria

### The candidates

**In-repo mechanisms (first-class, not afterthoughts):**

1. **A claims file on the shared branch, using `git push` atomicity as a lock.** A file (e.g.
   `CLAIMS.md`) committed to the shared branch (`main`), not to each session's private branch. The
   protocol: a session fetches `main`, reads `CLAIMS.md` to see what is claimed, adds its claim, and
   pushes. If another session pushed first, the push is rejected (non-fast-forward), so the loser
   detects the race, re-fetches, and retries. This is a compare-and-swap (CAS) operation using git's
   server-side atomicity.
2. **A dedicated git ref / lightweight tag as a claim marker.** A ref like `refs/claims/T-19` updated
   atomically on push. Same CAS property as (1), but the claim is a ref, not a file. Lighter weight,
   but harder for a non-programmer to read.
3. **The existing `flock`-based one-writer-per-worktree lock.** The model-flow harness already
   enforces one writer per worktree with a file lock keyed by the canonical worktree. This is a local
   lock, not a distributed one — it stops two writers in the same worktree, but not two writers in
   different worktrees (which is exactly the collision here).

**Off-repo mechanisms (included for honest comparison):**

4. **GitHub Issues assignee.** Use the assignee field to mark who is working a ticket.
5. **GitHub API / a tiny external coordination service.** An external service that sessions query
   before starting.
6. **Do nothing — rely on worktree isolation discipline alone.** The collision happened because two
   writers shared one folder, breaking the worktree invariant. If the invariant holds, the collision
   does not happen. This is the "treat it as solved-by-discipline" answer from the where-work-is-tracked
   research.

### The criteria

I re-ordered the criteria to reflect what the evidence says matters most: the repo-alone rule is
non-negotiable (it is the book's first doctrine), and the claim must be observed BEFORE starting
(the variable the collisions expose).

| # | Criterion | Why its rank |
|---|---|---|
| **C1** | **A parallel session actually observes the claim BEFORE starting.** | **Top.** This is the variable the collisions expose. Both sessions read "unclaimed" and started; the fix is not the tracker, it is the check-before-start. A mechanism that does not force the check fails this criterion. |
| **C2** | **Survives the repo-alone / offline rule.** The process lives in the repo so a stranger session finds it offline. | **Top.** This is the book's first doctrine, stated three times. A mechanism that lives off-repo fails this. |
| **C3** | **What happens when a session crashes holding a claim?** A claim without a lease is a stale lock forever. | High. Autonomous sessions can crash, time out, or be killed. A mechanism that does not handle this manufactures a new fault. |
| **C4** | **Does it use git mechanics the repo already relies on?** A mechanism that introduces a new primitive is a mechanism that must be taught to every stranger session. | High. The repo already uses git push, fetch, branches, and worktrees. A mechanism that adds etcd or a coordination service is a mechanism that breaks the repo-alone rule. |
| **C5** | **A non-programmer owner can read and use it.** | Medium. The owner is not a programmer. |
| **C6** | **How much discipline must the agent follow for it to work?** A mechanism that requires the agent to remember to check is a mechanism that fails when the agent forgets. | Medium. Autonomous agents do not always follow instructions. |

What I did not add: "Does it scale to hundreds of parallel sessions?" — this repo has recorded two
collisions across roughly two sessions at a time; scaling is not the problem. "Does it integrate with
GitHub Projects?" — a view on top of the tracker, not the tracker itself.

---

## 2. The weighed comparison — and where EACH mechanism is wrong

A summary table first, then the wrongness of each in turn. No mechanism scores flawlessly.

| Criterion | 1. CLAIMS.md on shared branch | 2. Dedicated git ref | 3. flock (existing) | 4. GitHub Issues assignee | 5. External service | 6. Discipline alone |
|---|---|---|---|---|---|---|
| **C1** observes claim BEFORE starting | **PASS** (fetch → read → push) | **PASS** (fetch → read ref → push) | FAIL (local only, not cross-worktree) | PARTIAL (must check assignee field) | PASS (query service) | FAIL (no check) |
| **C2** repo-alone / offline | **PASS** (in the clone) | **PASS** (in the clone) | **PASS** (local file) | FAIL (not in clone) | FAIL (external) | **PASS** |
| **C3** crashed session holding claim | FAIL (claim persists forever) | FAIL (ref persists forever) | PASS (flock released on crash) | PARTIAL (assignee persists) | PARTIAL (depends on service) | N/A (no claim) |
| **C4** uses existing git mechanics | **PASS** (push/fetch) | **PASS** (push/fetch) | PASS (flock) | FAIL (GitHub API) | FAIL (new service) | N/A |
| **C5** non-programmer can use | **PASS** (it is a file) | Weak (ref is opaque) | N/A (invisible) | Pass (web UI) | FAIL (API) | N/A |
| **C6** discipline cost | Medium (must fetch+push) | Medium (must fetch+push) | Low (automatic) | Low (check assignee) | Low (query service) | High (must remember) |

### Where mechanism 1 (CLAIMS.md on shared branch) is WRONG — and this is the one I recommend

- **A crashed session holding a claim forever.** If a session claims T-19 and then crashes, the claim
  persists in `CLAIMS.md` on `main`, and no other session can pick up T-19 until someone manually
  removes the claim. This is the classic stale-lock fault, and it is the mechanism's weakest point.
  **Mitigation:** a lease with a timestamp. The claim includes a timestamp (`T-19 | session-abc |
  2026-07-23T14:00:00Z`), and a session that sees a claim older than, say, 30 minutes treats it as
  stale and removes it. This is not perfect — clock skew, a session that is slow but not crashed —
  but it is the standard mitigation for distributed locks, and it is better than no claim at all.
  **Honest admission:** the lease is a heuristic, not a guarantee. A session that is genuinely
  working but slow will have its claim stolen. The book's own lesson — "a second pair of eyes is
  cheap, a second pair of hands costs the work twice" — suggests the right response is to err on the
  side of letting the claim stand, and to recover manually when it does not.
- **It requires the agent to fetch and push.** An agent that does not fetch before reading, or that
  does not push after claiming, bypasses the mechanism. This is a discipline cost, and autonomous
  agents do not always follow instructions. **Mitigation:** the claiming protocol is written into the
  repo (in `WHERE-WE-ARE.md` or a new `CLAIMING.md`), so a stranger session finds it in the mandated
  reading order. The protocol is three steps (fetch → read → push), not ten, so the instruction cost
  is low.
- **It does not prevent the collision if the agent does not check.** If an agent skips the "read
  CLAIMS.md" step, it will still clash. This is the same fault as the GitHub Issues assignee: a
  mechanism that is not checked does not prevent the collision. **Mitigation:** the protocol is
  mandatory, and the probe (§4) tests whether it holds.

### Where mechanism 2 (dedicated git ref) is WRONG

- **It is opaque to a non-programmer.** A ref like `refs/claims/T-19` is not a file the owner can
  open and read. The owner is explicitly not a programmer. **Mitigation:** none — this is a
  deal-breaker for this repo.
- **It has the same stale-lock fault as (1).** A crashed session holding a ref is the same fault as a
  crashed session holding a file. The lease mitigation applies, but a ref cannot carry a timestamp as
  naturally as a file can.
- **It is a new primitive.** The repo uses files for everything else; introducing a ref-based claim is
  a new primitive that must be taught to every stranger session. The CLAIMS.md file is a file, and
  files are the repo's native primitive.

### Where mechanism 3 (flock, existing) is WRONG

- **It is a local lock, not a distributed one.** The flock is keyed by the canonical worktree, so it
  stops two writers in the same worktree. The collision happened when two writers were in different
  worktrees (the invariant was held), and the flock did not see it. **This mechanism does not solve
  the problem.** It is necessary but not sufficient.

### Where mechanism 4 (GitHub Issues assignee) is WRONG — and this is decisive

- **Issues are not in the repository.** A `git clone` copies commits, branches and tags — not issues,
  which live in GitHub's database. This fails the repo-alone rule (C2) outright.
- **It does not prevent the collision if the agent does not check.** Two agents that both read "this
  issue is unassigned" will both start it, exactly as they both picked up chapters 9 and 10 here. The
  assignee field helps a human notice; it does not stop an autonomous session that does not check it.
  **This is the same fault as the flat-file board: the variable is the check-before-start protocol,
  not the storage location.**
- **It is off-repo, and the book's doctrine says records never travel.** The work-tracker is a record,
  and a record on GitHub's servers is the opposite of "records never travel."

### Where mechanism 5 (external service) is WRONG

- **It fails the repo-alone rule.** An external service is not in the clone, so a stranger session
  that goes offline cannot see the claims.
- **It introduces a new dependency.** The repo would depend on a service that may disappear, change
  its API, or require authentication. The book's own parked note frames the harder case — "where the
  job list lives when a kitchen has no GitHub" — and an external service is a bet that the service
  stays up.
- **It is overkill.** The repo already has git, which is a distributed coordination system. Adding a
  service to coordinate sessions that already share a git remote is a layer of coordination on top of
  the coordination git already provides.

### Where mechanism 6 (discipline alone) is WRONG

- **It does not work.** The two collisions happened because the discipline (worktree isolation) was
  held, and the collision still happened. The variable is the claim-before-start check, and
  discipline alone does not provide it.
- **It is the wrong answer to the wrong question.** The where-work-is-tracked research said "treat the
  collision as solved-by-discipline" — but the discipline was already the rule, and the collision
  happened anyway. The collision is not an isolation-discipline problem; it is a
> claim-before-start-protocol problem.

### What I kept from the alternatives

- **The lease pattern from distributed locking.** The CLAIMS.md file includes a timestamp, and a
  session treats a claim older than the lease as stale. This is the standard mitigation for crashed
  sessions, borrowed from etcd/consul-style locks.
- **The CAS (compare-and-swap) pattern from git push.** The non-fast-forward push rejection is a
  server-side atomic check, and it is the load-bearing mechanism. This is not new — git-annex and
  other tools use git as a lock — but it is the first time this repo has used it for session
  coordination.

---

## 3. The recommended protocol

**The recommendation is mechanism 1: a claims file on the shared branch, using `git push` atomicity
as a distributed lock.** The protocol has five steps, and each step is concrete.

### The file

`CLAIMS.md` lives at the repo root, on the shared branch (`main`). It is a markdown table with three
columns: ticket, session, timestamp.

```markdown
# Claims — who is working what

This file is the live claim board. Before you start a ticket, you must claim it here. The claim is
a distributed lock: if two sessions claim the same ticket, the second push is rejected, and the
loser backs off.

| Ticket | Session | Claimed at |
|---|---|---|
| T-19 | session-abc | 2026-07-23T14:00:00Z |
```

### The protocol

A session that wants to work a ticket runs the following five steps, in order. The protocol is
written into the repo (in `WHERE-WE-ARE.md` or a new `CLAIMING.md`), so a stranger session finds it
in the mandated reading order.

1. **Fetch the shared branch.** `git fetch origin main`. This brings in any claims other sessions
   have pushed since the last fetch. If the session does not fetch, it will read a stale view of the
   claims, and the collision can still happen. This is the step the two collisions missed.
2. **Read the claims file.** Open `CLAIMS.md` (on `origin/main`, not the local branch) and check
   whether the ticket is already claimed. If it is, and the claim is less than 30 minutes old, pick a
   different ticket. If the claim is older than 30 minutes, treat it as stale (the session may have
   crashed) and remove it.
3. **Claim the ticket.** Add a row to `CLAIMS.md` with the ticket, the session ID, and the current
   timestamp. Commit the change to the local branch.
4. **Push the claim.** `git push origin HEAD:main`. If the push succeeds, the claim won — no other
   session pushed a conflicting claim in the meantime. If the push is rejected (non-fast-forward),
   another session pushed first. Go back to step 1 and retry.
5. **Verify the claim won.** After the push succeeds, fetch again and confirm that the claim is in
   `CLAIMS.md` on `origin/main`. If it is not, something went wrong (a race, a force-push), and the
   session should back off.

### When the work is done

The session removes its claim from `CLAIMS.md`, commits, and pushes. The ticket is now unclaimed, and
another session can pick it up.

### Why this works

- **It uses git push atomicity as a distributed lock.** The non-fast-forward push rejection is a
  server-side atomic check, so two sessions that race to claim the same ticket will see exactly one
  push succeed and one push fail. The loser detects the race and backs off.
- **It lives in the repo.** The claims file is in the clone, so a stranger session finds it offline.
  This satisfies the repo-alone rule.
- **It forces the check-before-start.** The protocol requires the session to fetch and read the
  claims file before starting, so the collision (two sessions both reading "unclaimed") cannot happen
  if the protocol is followed.

### Why this is wrong (the honest admission)

- **A crashed session holding a claim forever.** The lease (30 minutes) is a heuristic, not a
  guarantee. A session that is genuinely working but slow will have its claim stolen. The book's own
  lesson suggests erring on the side of letting the claim stand, and recovering manually when it
  does not.
- **It requires the agent to follow the protocol.** An agent that skips the fetch, or that does not
  push after claiming, bypasses the mechanism. The protocol is three steps (fetch → read → push), not
  ten, so the instruction cost is low — but autonomous agents do not always follow instructions.
- **It does not prevent the collision if the agent does not check.** If an agent skips the "read
  CLAIMS.md" step, it will still clash. The probe (§4) tests whether the protocol holds.

---

## 4. The probe — measurable pass/fail

The owner's standing rule is "measured, or it's an opinion." The probe is cheap, and it predicts a
number that must move, so the recommendation is falsifiable before it is adopted.

### Probe C — the collision falsifier (two sessions, ~an hour)

**Setup.** Two sessions, each in its own isolated git worktree, each on its own branch. Both are
given the repo alone, with the same prompt: *"claim the next open ticket and start."* The prompt
includes the claiming protocol (fetch → read CLAIMS.md → push → verify).

**Run it twice:**
- Once with the CLAIMS.md mechanism (the recommendation).
- Once with no claiming mechanism (the baseline — the current state).

**PASS for an arm** — at most one session works a given ticket, OR the clash is detected before a
duplicate commit lands. Measured: the two sessions do not both commit changes to the same ticket's
files, or if they do, the second session detects the collision (via the push rejection) before it
has done substantial work.

**FAIL** — two sessions do the same ticket and one set of checks is thrown away (the 2026-07-23
outcome). Measured: both sessions commit changes to the same ticket's files, and neither detects the
collision before substantial work is done.

**Prediction:**
- **Baseline arm (no claiming): FAIL.** This is the current state, and the two real collisions are
  the evidence.
- **CLAIMS.md arm: PASS.** The push rejection should catch the race, and the loser should back off
  before doing substantial work. If the prediction is wrong, that falsifies the recommendation, and
  the fix routes to a different mechanism (or to the honest admission that no in-repo mechanism can
  prevent the collision if the agent does not check).

**What result would falsify the recommendation:**
- If the CLAIMS.md arm FAILS — both sessions do the same ticket despite the protocol — then the
  recommendation is wrong. The most likely cause is that the agent did not follow the protocol (did
  not fetch, or did not push), which would mean the mechanism is too fragile for autonomous agents.
  The fix would be to make the protocol mandatory (enforced by the session-start hook, or by the
  worktree setup script), or to accept that no in-repo mechanism can prevent the collision and to
  route the fix to worktree isolation discipline (which is the where-work-is-tracked research's
  answer).

---

## 5. Confidence, and what could change the answer

**What I am sure of (primary-sourced, not opinion):**

- Git push is atomic, and a non-fast-forward push is rejected server-side. This is a fundamental
  property of git, and it is the load-bearing mechanism.
- A `git clone` copies commits, branches and tags — not GitHub Issues. This is the load-bearing fact
  against off-repo mechanisms.
- The two real collisions here were two sessions that both read "unclaimed" and started — not a
  tracker-file merge conflict. The variable is the check-before-start protocol, not the storage
  location.
- The flock-based lock is local, not distributed. It stops two writers in the same worktree, but not
  two writers in different worktrees.

**What I am uncertain about (honest gaps):**

- Whether autonomous agents will follow the claiming protocol. The protocol is three steps, not ten,
  but autonomous agents do not always follow instructions. The probe tests this, and if the agents do
  not follow the protocol, the mechanism is too fragile.
- Whether the lease (30 minutes) is the right length. A session that is genuinely working but slow
  will have its claim stolen if the lease is too short; a crashed session holding a claim forever is
  the fault if the lease is too long. 30 minutes is a guess, and the right length depends on the
  typical session duration and the typical work duration. The probe may surface this, and the lease
  may need to be tuned.
- Whether the claims file will become a bottleneck if many sessions are working in parallel. This
  repo has recorded two collisions across roughly two sessions at a time, so scaling is not the
  current problem — but if the repo ever scales to many parallel sessions, the claims file may become
  a contention point. The dedicated git ref (mechanism 2) would scale better, but it is opaque to a
  non-programmer.

**What single fact would flip the recommendation:**

- **If the probe FAILS** — both sessions do the same ticket despite the CLAIMS.md protocol — then the
  recommendation is wrong, and the fix routes to a different mechanism (or to the honest admission
  that no in-repo mechanism can prevent the collision if the agent does not check).
- **If the repo scales to many parallel sessions** — the claims file may become a contention point,
  and the dedicated git ref (mechanism 2) would scale better. The trade-off is opacity vs. scale,
  and the right answer depends on the repo's growth.
- **If the repo loses GitHub** — the parked note's "no GitHub" case activates, and the answer becomes
  "a flat file, or a small local database," full stop. The CLAIMS.md mechanism is already the answer
  in that case, so this does not flip the recommendation — it confirms it.

---

## Source list (primary)

**This repo (primary to the question):**

- `WHERE-WE-ARE.md` — the parallel-sessions section (both collisions); the worktree invariant; the
  model-flow flock lock.
- `TICKETS.md` — T-19 (the ticket this research answers); the existing board.
- `KNOWN-HOLES.md` — the self-referential OPEN row ("Where the job list lives for a kitchen with no
  shared tracker"); the plan/record split.
- `research/where-work-is-tracked.md` — the prior research that settled where the work lives; the
  Probe C design.

**External (primary unless noted):**

- Git documentation on push atomicity and non-fast-forward rejections — the load-bearing mechanism.
- git-annex — uses git as a key-value store with locks, a prior instance of "git as a lock."
- etcd/consul documentation on distributed locking and leases — the lease pattern borrowed for the
  crashed-session mitigation.
- Johannes Millan, "Why Multitasking With AI Coding Agents Breaks Down" — the fix is one worktree per
  session; the collision is an isolation problem, not a tracker problem.
- Aider, "How to add a multi-agent flow?" — the `scratchpad.md` state-file pattern, a prior instance
  of in-repo coordination.

**Thin evidence (flagged):** I reasoned from what I know about git push/ref atomicity and distributed
locking; I did not find a measured, comparative study of claiming mechanisms for AI-agent-driven
repos specifically — that gap is exactly why §4 is a probe rather than a verdict. The git mechanics
(push atomicity, non-fast-forward rejection) are primary and not contested. The lease pattern is
standard in distributed systems, but the right lease length for this repo is a guess, not a
measurement.
