"""The printer. One brief in, one chapter out.

  PRESS_WORK=<dir> python3 press/print.py 17
  python3 press/print.py --catalog

Reads <PRESS_WORK>/brief-17.json, builds a Codex run directory beside it, and launches
Codex 5.6 Sol at high effort with the chapter template, both voice standards and the
brief. Sol writes exactly one file: the chapter.

Run these two at a time, never six. Six at once came back empty and silent.
"""
import json, os, re, subprocess, sys

from brief_contract import BRIEF_FIELDS, BRIEF_LIST_FIELDS

SP = os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__))
CB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Preserve the one established filename that intentionally abbreviates its CONTENTS title.
FILENAME_OVERRIDES = {19: "19-checking-it.md"}


def r(relative_path):
    with open(os.path.join(CB, relative_path), encoding="utf-8") as handle:
        return handle.read()


def parse_chapter(value):
    if not re.fullmatch(r"(?:1[7-9]|[2-4][0-9]|50)", value):
        raise ValueError("chapter must be a whole number from 17 through 50")
    return int(value)


def chapter_catalog(contents):
    titles = {}
    for line in contents.splitlines():
        match = re.fullmatch(r"(\d+)\.\s+(?:\*\*)?(.+?)(?:\*\*)?\s*", line)
        if not match:
            continue
        number = int(match.group(1))
        if 17 <= number <= 50:
            title = match.group(2).split(" — ", 1)[0].strip().rstrip("*").strip()
            if not title or number in titles:
                raise ValueError(f"CONTENTS.md has an ambiguous title for chapter {number}")
            titles[number] = title
    expected = set(range(17, 51))
    if set(titles) != expected:
        raise ValueError(
            "CONTENTS.md must contain exactly one title for every chapter from 17 to 50; "
            f"missing={sorted(expected - set(titles))}"
        )
    return {
        number: {
            "title": title,
            "filename": FILENAME_OVERRIDES.get(
                number,
                f"{number:02d}-"
                + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
                + ".md",
            ),
        }
        for number, title in titles.items()
    }


def parse_json_document(text, source):
    candidate = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*\n([\s\S]*?)\n```", candidate, re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as error:
        raise ValueError(f"{source} is not valid JSON: {error.msg}") from error


def load_brief(path, chapter, title):
    with open(path, encoding="utf-8") as handle:
        brief = parse_json_document(handle.read(), path)
    if not isinstance(brief, dict):
        raise ValueError(f"{path} must contain a JSON object")
    expected = set(BRIEF_FIELDS)
    if set(brief) != expected:
        raise ValueError(
            f"{path} has the wrong fields; "
            f"missing={sorted(expected - set(brief))}, extra={sorted(set(brief) - expected)}"
        )
    if brief["chapter"] != chapter or brief["title"] != title:
        raise ValueError(
            f"{path} identifies chapter {brief['chapter']!r}, {brief['title']!r}; "
            f"expected chapter {chapter}, {title!r}"
        )
    for field in BRIEF_LIST_FIELDS:
        entries = brief[field]
        if not isinstance(entries, list) or any(
            not isinstance(entry, str) or not entry.strip() for entry in entries
        ):
            raise ValueError(f"{path} field {field!r} must be a list of non-empty strings")
    if not brief["must_cover"]:
        raise ValueError(f"{path} does not name anything the chapter must cover")
    return brief


if len(sys.argv) == 2 and sys.argv[1] == "--catalog":
    print(json.dumps(chapter_catalog(r("CONTENTS.md")), ensure_ascii=False, indent=2))
    raise SystemExit(0)
if len(sys.argv) != 2:
    raise SystemExit("usage: python3 press/print.py CHAPTER (17-50)")
chapter = parse_chapter(sys.argv[1])
ch = str(chapter)
catalog = chapter_catalog(r("CONTENTS.md"))
title = catalog[chapter]["title"]
fname = catalog[chapter]["filename"]
brief_path = os.path.join(SP, f"brief-{chapter}.json")
brief_data = load_brief(brief_path, chapter, title)
brief = json.dumps(brief_data, ensure_ascii=False, indent=2)

# The invariant total is read once from the canonical JSON and counted, never hard-coded, so
# the heading and the review-quality bar below cannot state a number the file does not match.
invariants_source = r("press/core-invariants.json")
invariant_count = len(json.loads(invariants_source))

prompt = f"""[CONTEXT]
Latest user request: write chapter {ch} of a book, from the brief below.

You are the printer in a print shop. The shop is writing a book that teaches a
NON-TECHNICAL owner to run a chain of restaurants — where the restaurants are software
projects, the cooks are AI agents, and the dishes are units of work. The reader has never
written a line of code and never will.

Authoritative sources, in this order of authority:
1. CONTENTS.md — the running order. SETTLED AND CLOSED. It is never reopened, argued with,
   or improved. If it assigns something to this chapter, this chapter carries it.
2. The brief below, written by the prep cook for this chapter specifically.
3. CHAPTER-TEMPLATE.md — what a chapter is.
4. book/00-opening-the-box.md and book/01-the-interview.md — the VOICE STANDARD. Both have
   passed a taster. Every later page is scored against them.

Freshness rule: the brief and the running order win over anything you infer from an
already-written chapter.
Entity boundaries: you are writing chapter {ch} and no other chapter. Do not edit, tidy,
renumber or "fix" any other file in this repository.
Privacy boundaries: nothing outside this repository is needed. Do not reach for the network.
Ignore unless relevant: the press machinery in press/, the logs, and the shop's own notes.
Those describe how the book is MADE. They are not the book.

[TASK]
Write exactly one file: book/{fname}

It is chapter {ch}. Its first line is exactly:

# {ch}. {title}

===== THE BRIEF FOR CHAPTER {ch} =====
{brief}

===== WHAT A CHAPTER IS =====
{r("CHAPTER-TEMPLATE.md")}

===== VOICE STANDARD: CHAPTER 0 (passed the taster) =====
{r("book/00-opening-the-box.md")}

===== VOICE STANDARD: CHAPTER 1 (passed the taster, chosen blind by the owner) =====
{r("book/01-the-interview.md")}

===== THE {invariant_count} CORE INVARIANTS — every chapter is swept against all {invariant_count}, rule by rule =====
{invariants_source}

[CONSTRAINTS]
Scope: one file, book/{fname}. Nothing else.
Non-goals: do not write another chapter's material; the brief says what belongs elsewhere
and names where. Do not reopen the running order. Do not invent mechanisms, commands,
history or numbers — a confident invented fact is worse than an absent one.

Hard limits, each of which a mechanical check will measure before any human reads the page:
- **Body under 700 words**, counting everything above `## The rules, flat`. Count it
  yourself before you hand in. The chapter that won the printer's chair did exactly that.
- **Zero words that only mean something to a programmer**, anywhere on the page — body AND
  flat rules. The flat rules are the part the appliance obeys, so jargon matters MORE there.
  A page went back for one such word in its flat rules.
- **Every heading makes a statement, not a label.** "The book is installed, not read" —
  never "Installation". A heading of three words or fewer is a label suspect unless it is
  an imperative.
- **Every flat rule traces to something explained in the body.** The flat rules are the
  same rules with the reasoning removed — the shopping list printed from the recipe. A flat
  rule with nothing above it explaining it is a promise nobody argued for.
- **Analogies come from the agreed set only**: the chain, a restaurant, its kitchen, a
  dish, the cooks, the taster, the appliance, the recipe and the shopping list, the
  telephone game, a building with doors, a photograph and a diary. Anything from outside
  that world is a fault however good it is — and so is one of these stretched past where it
  fits, which is the commoner failure. The restaurant itself is the SETTING, not an
  analogy: waiters, ovens, safes and plates are simply furniture of this world.
- **Point back at another chapter only where a reader would otherwise be lost, and NEVER in
  the opening line.** An earlier batch opened three chapters the same way and it became a
  formula. Two independent readers caught it. Do not restart it.

If the brief assigns this chapter more than 700 words can hold, do NOT pad and do NOT
silently drop something. Fit what you can, and name plainly in the page what it does not
cover and which chapter handles it instead. A chapter that says what it leaves out is
honest; a chapter that quietly leaves it out is a hole.

Permissions: full access, but you write one file.
Review quality bar: the page is read by a taster on seven questions and then swept against
all {invariant_count} invariants above, rule by rule, with any violating sentence quoted verbatim. Write
as though that has already happened.

[VALIDATION]
Commands: run this before you finish, and act on what it says —

    python3 press/head-chef-check.py book/{fname}

Read its output. `A4_within_700` must be true. `A5_jargon_hits` and
`A5_jargon_in_flat_rules` must both be empty. `A1_label_suspects` must be empty, or every
entry in it must genuinely be an imperative. `A1_settles_line` and `A1_flat_rules` must be
true. If any of those is wrong, fix the page and run it again.

Expected artifacts: book/{fname} exists, and final.json records the body word count you
measured and the check's output.
Stop condition: the file exists, the check passes on every item above, and you have read
the finished page once from the top as a reader who has never written code.
If blocked: say so in final.json open_issues with the exact obstacle. Do not hand in a page
you know is faulty and hope it is caught.

Latest user request, restated: write book/{fname} — chapter {ch}, "{title}" — from the
brief above, in the voice of chapters 0 and 1, body under 700 words, no programmer words,
every flat rule earned by the body. One file. Nothing else.
"""

run_dir = os.path.join(SP, f"run-{ch}")
os.makedirs(run_dir, exist_ok=True)
with open(os.path.join(run_dir, "prompt.txt"), "w", encoding="utf-8") as handle:
    handle.write(prompt)
with open(os.path.join(run_dir, "run.spec.json"), "w", encoding="utf-8") as handle:
    json.dump({
    "objective": f"Write book/{fname} — chapter {ch}, '{title}' — from its brief, to the template and the voice standard.",
    "mode": "implementation",
    "model": "gpt-5.6-sol",
    "effort": "high",
    "sandbox": "danger-full-access",
    "ephemeral": False,
    "timeout_seconds": 0,
    "heartbeat_seconds": 30,
    "idle_timeout_seconds": 0,
    "observability": {"version": 1, "log_level": "warn", "allow_sensitive_logs": False,
                      "doctor": "never", "doctor_timeout_seconds": 15,
                      "max_file_bytes": 0, "max_capture_bytes": 0,
                      "retention": {"enabled": False, "max_age_days": 14,
                                    "max_runs": 100, "max_bytes": 1073741824}},
    "owned_paths": [f"book/{fname}"],
    "context_policy": {
        "authoritative_sources": ["CONTENTS.md", f"{SP}/brief-{ch}.json",
                                  "CHAPTER-TEMPLATE.md", "book/00-opening-the-box.md",
                                  "book/01-the-interview.md", "press/core-invariants.json"],
        "freshness_rule": "The brief and CONTENTS.md outrank anything inferred from an already-written chapter.",
        "entity_boundaries": [f"chapter {ch} only", f"book/{fname} only"],
        "privacy_boundaries": ["repository-local only; no network"],
        "ignore_unless_relevant": ["press/", "PRESS-LOG.md", "THE-PRINT-SHOP.md", "SHOWDOWN.md"],
        "latest_request_wins": True},
    "verification": [f"python3 press/head-chef-check.py book/{fname}"],
    "stop_condition": f"book/{fname} exists, body under 700 words, no jargon anywhere, every flat rule traced to the body.",
    # This list is checked as an EXACT set, not a minimum. With observability declared it
    # must also carry the seven lifecycle artifacts, or the run is rejected before launch.
    "expected_artifacts": ["run.spec.json", "spec.validated.json", "prompt.txt", "owner.json",
                           "final.schema.json", "events.jsonl", "stderr.log", "heartbeat.jsonl",
                           "last-progress.json", "final.json", "pid", "watchdog.pid", "exit-code",
                           ".codex-run-v1.json", ".run.lock", "debug.jsonl", "diagnostics.json",
                           "manifest.sha256", "terminal-state.json", "retention.json"],
    "blocking_gates": ["exit-code", "timeout", "liveness", "artifacts", "jsonl", "final",
                       "scope", "context", "verification"],
    }, handle, indent=2)
    handle.write("\n")

page_path = os.path.join(CB, "book", fname)
before = None
try:
    with open(page_path, "rb") as handle:
        before = handle.read()
except FileNotFoundError:
    pass

completed = subprocess.run(["codex-exec", run_dir], cwd=CB, check=False)
if completed.returncode != 0:
    raise SystemExit(f"chapter {ch}: codex-exec failed with rc={completed.returncode}")

try:
    with open(page_path, "rb") as handle:
        after = handle.read()
except FileNotFoundError as error:
    raise RuntimeError(f"codex-exec returned success but did not create book/{fname}") from error
if before == after:
    raise RuntimeError(
        f"codex-exec returned success but book/{fname} was unchanged; refusing false success"
    )

page_text = after.decode("utf-8")
expected_heading = f"# {chapter}. {title}"
if page_text.splitlines()[:1] != [expected_heading]:
    actual = page_text.splitlines()[:1]
    raise RuntimeError(
        f"book/{fname} has heading {actual!r}; expected {expected_heading!r}"
    )

check = subprocess.run(
    [sys.executable, "press/head-chef-check.py", f"book/{fname}"],
    cwd=CB,
    capture_output=True,
    text=True,
    check=False,
)
if check.returncode != 0:
    raise RuntimeError(f"head-chef-check failed with rc={check.returncode}")
try:
    reports = json.loads(check.stdout)
    report = reports[0]
except (json.JSONDecodeError, IndexError, KeyError, TypeError) as error:
    raise RuntimeError("head-chef-check returned an unreadable report") from error
required = {
    "A1_chapter_number": str(chapter),
    "A1_settles_line": True,
    "A1_flat_rules": True,
    "A1_flat_rules_numbered": True,
    "A4_within_700": True,
    "A5_jargon_hits": {},
    "A5_jargon_in_flat_rules": {},
    "A1_label_suspects": [],
}
failed = {key: report.get(key) for key, expected in required.items() if report.get(key) != expected}
if failed:
    raise RuntimeError(f"book/{fname} failed head-chef-check requirements: {failed}")

print(f"chapter {ch}: wrote book/{fname}; body_words={report['A4_body_words']}")
