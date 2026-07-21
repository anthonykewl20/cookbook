"""The prep cook. One chapter in, one validated brief out.

  python3 press/prep.py 17          -> <PRESS_WORK>/brief-17.json

The brief is what the printer writes from AND what the taster reads beside the page.
Invalid or mislabelled model output is refused and never replaces an existing brief.
"""

import glob
import json
import os
import re
import sys
import tempfile
import time
import urllib.request


PRESS_WORK = os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIEF_LIST_FIELDS = (
    "must_cover",
    "must_not_cover",
    "must_not_contradict",
    "known_holes",
    "traps",
    "hooks",
)


def read_repo(relative_path):
    path = os.path.join(REPO_ROOT, relative_path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def parse_chapter(value):
    if not re.fullmatch(r"(?:1[7-9]|[2-4][0-9]|50)", value):
        raise ValueError("chapter must be a whole number from 17 through 50")
    return int(value)


def chapter_titles(contents):
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
        missing = sorted(expected - set(titles))
        extra = sorted(set(titles) - expected)
        raise ValueError(
            f"CONTENTS.md chapter catalogue is incomplete or ambiguous; "
            f"missing={missing}, extra={extra}"
        )
    return titles


def parse_json_reply(text):
    candidate = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*\n([\s\S]*?)\n```", candidate, re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as error:
        raise ValueError(f"model reply is not valid JSON: {error.msg}") from error


def validate_brief(value, chapter, title):
    if not isinstance(value, dict):
        raise ValueError("brief must be a JSON object")
    expected = {"chapter", "title", *BRIEF_LIST_FIELDS}
    if set(value) != expected:
        raise ValueError(
            f"brief fields do not match the required shape; "
            f"missing={sorted(expected - set(value))}, extra={sorted(set(value) - expected)}"
        )
    if value["chapter"] != chapter:
        raise ValueError(
            f"brief identifies chapter {value['chapter']!r}, not requested chapter {chapter}"
        )
    if value["title"] != title:
        raise ValueError(
            f"brief title {value['title']!r} does not match CONTENTS.md title {title!r}"
        )
    for field in BRIEF_LIST_FIELDS:
        entries = value[field]
        if not isinstance(entries, list) or any(
            not isinstance(entry, str) or not entry.strip() for entry in entries
        ):
            raise ValueError(f"brief field {field!r} must be a list of non-empty strings")
    if not value["must_cover"]:
        raise ValueError("brief must name at least one thing the chapter must cover")
    return value


def write_json_atomically(path, value):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    descriptor, temporary_path = tempfile.mkstemp(prefix=".brief-", dir=directory, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary_path, path)
    except BaseException:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise


def load_openrouter_key():
    auth_path = os.path.expanduser("~/.local/share/opencode/auth.json")
    with open(auth_path, encoding="utf-8") as handle:
        auth = json.load(handle)
    openrouter = auth.get("openrouter")
    if not isinstance(openrouter, dict):
        raise ValueError(f"OpenRouter credentials are missing from {auth_path}")
    key = openrouter.get("key") or openrouter.get("apiKey") or openrouter.get("api_key")
    if not isinstance(key, str) or not key.strip():
        raise ValueError(f"OpenRouter key is missing from {auth_path}")
    return key


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: python3 press/prep.py CHAPTER (17-50)")
    chapter = parse_chapter(argv[1])
    contents = read_repo("CONTENTS.md")
    title = chapter_titles(contents)[chapter]

    written_paths = sorted(glob.glob(os.path.join(REPO_ROOT, "book", "*.md")))
    if not written_paths:
        raise FileNotFoundError("no already-written chapters found in book/")
    written_sections = []
    for path in written_paths:
        with open(path, encoding="utf-8") as handle:
            written_sections.append(
                f"===== ALREADY WRITTEN: {os.path.basename(path)} =====\n{handle.read()}"
            )
    neighbours = "\n\n".join(written_sections)

    prompt = f"""You are the prep cook for a print shop that is writing a book. You do not write
chapters. You gather what goes into ONE chapter before the printer starts, so the printer
spends its effort writing rather than searching.

The book teaches a NON-TECHNICAL owner to run a chain of restaurants, where the restaurants
are software projects, the chefs are AI agents and the dishes are units of work.

Prepare the brief for **CHAPTER {chapter}: {title}** and no other chapter.

===== THE RUNNING ORDER (settled, closed, not reopened) =====
{contents}

===== WHAT A CHAPTER IS =====
{read_repo("CHAPTER-TEMPLATE.md")}

===== KNOWN HOLES =====
{read_repo("KNOWN-HOLES.md")}

===== THE TEN CORE INVARIANTS every chapter is swept against =====
{read_repo("press/core-invariants.json")}

{neighbours}

===== YOUR JOB =====
Return ONLY valid JSON, no prose around it, in exactly this shape:

{{
  "chapter": {chapter},
  "title": {json.dumps(title)},
  "must_cover": ["..."],
  "must_not_cover": ["... (belongs to chapter N)"],
  "must_not_contradict": ["QUOTED VERBATIM from the running order or an already-written chapter"],
  "known_holes": ["a hole from KNOWN-HOLES.md that touches this chapter, and what the printer should do about it"],
  "traps": ["..."],
  "hooks": ["a settled decision in the running order this chapter must carry"]
}}

Rules for the brief itself:
- Keep "chapter" and "title" exactly as shown. They prevent a brief being handed to the
  wrong printer under a plausible filename.
- **must_not_contradict entries are QUOTATIONS.** Copy the sentence exactly. A paraphrase
  cannot be checked against the page later, and this list is what the taster reads.
- **must_not_cover names the chapter the material belongs to instead.** "Not this" without
  "it is over there" makes the printer guess.
- Do not invent material the running order never assigned to this chapter.
- If the running order gives this chapter something that CONTRADICTS an already-written
  chapter or a core invariant, say so plainly in "known_holes". Finding that before the
  printer trips over it is the whole point of prep.
"""

    body = json.dumps(
        {
            "model": "tencent/hy3",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 20000,
        }
    ).encode()
    key = load_openrouter_key()
    started = time.time()
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=900) as response:
        result = json.load(response)
    try:
        reply = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("OpenRouter response has no model reply") from error
    if not isinstance(reply, str) or not reply.strip():
        raise ValueError("OpenRouter returned an empty model reply")

    brief = validate_brief(parse_json_reply(reply), chapter, title)
    output_path = os.path.join(PRESS_WORK, f"brief-{chapter}.json")
    write_json_atomically(output_path, brief)
    print(
        chapter,
        round(time.time() - started, 1),
        result.get("usage", {}).get("cost"),
        os.path.getsize(output_path),
    )


if __name__ == "__main__":
    main(sys.argv)
