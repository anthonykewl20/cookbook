"""The reader. One complete batch in, a list of what is ABSENT out. No verdict.

  PRESS_WORK=<dir> python3 press/read-for-missing.py 17 18 19 20 21

Every requested chapter must resolve to exactly one correctly labelled page. A missing,
ambiguous, or failed read produces no report and returns non-zero.
"""

import glob
import os
import re
import subprocess
import sys
import tempfile


PRESS_WORK = os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_repo(relative_path):
    path = os.path.join(REPO_ROOT, relative_path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def parse_chapters(values):
    if not values:
        raise ValueError("at least one chapter is required")
    chapters = []
    for value in values:
        if not re.fullmatch(r"(?:1[7-9]|[2-4][0-9]|50)", value):
            raise ValueError(f"invalid chapter {value!r}; expected a whole number from 17 to 50")
        chapters.append(int(value))
    if chapters != sorted(set(chapters)):
        raise ValueError("chapters must be unique and in increasing order")
    return chapters


def load_pages(chapters):
    pages = []
    for chapter in chapters:
        pattern = os.path.join(REPO_ROOT, "book", f"{chapter:02d}-*.md")
        matches = sorted(path for path in glob.glob(pattern) if os.path.isfile(path))
        if len(matches) != 1:
            names = [os.path.basename(path) for path in matches]
            raise FileNotFoundError(
                f"chapter {chapter} must match exactly one book/{chapter:02d}-*.md; found {names}"
            )
        path = matches[0]
        with open(path, encoding="utf-8") as handle:
            page = handle.read()
        heading = re.match(r"^#\s+(\d+)\.\s+", page)
        if not heading or int(heading.group(1)) != chapter:
            actual = page.splitlines()[:1]
            raise ValueError(
                f"{os.path.relpath(path, REPO_ROOT)} has heading {actual!r}, "
                f"not chapter {chapter}"
            )
        pages.append(f"===== CHAPTER {chapter}: {os.path.basename(path)} =====\n{page}")
    return pages


def write_atomically(path, text):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    descriptor, temporary_path = tempfile.mkstemp(prefix=".reader-", dir=directory, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            if not text.endswith("\n"):
                handle.write("\n")
        os.replace(temporary_path, path)
    except BaseException:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise


def main(argv):
    chapters = parse_chapters(argv[1:])
    pages = load_pages(chapters)
    contents = read_repo("CONTENTS.md")

    task = f"""You are the reader. You do NOT give a verdict. You cannot send a page back and
you are not being asked whether these pages are good.

Answer one question only: **what is MISSING?**

The book teaches a NON-TECHNICAL owner to run a chain of restaurants, where the restaurants
are software projects, the cooks are AI agents and the dishes are units of work. The reader
has never written a line of code.

These {len(pages)} chapters were just printed as one batch. Read them together, against the
running order that assigned them.

For the batch as a whole, answer:

1. **What did the running order give these chapters that no page actually delivers?** Quote
   the running order's words, then say which chapter should have carried it.
2. **What would confuse someone who has never done this?** A step assumed, a word used
   before it is settled, an order of events that is never stated.
3. **What falls in the GAP between two of these chapters** — something no chapter claims,
   because each assumed the other had it?
4. **What does a reader need before they can act on these pages, that is nowhere on them?**

Do not comment on style, voice, length or quality. Do not say a page is good or bad. Do not
list things that are present and correct. Only what is absent.

If a chapter is genuinely complete against the running order, say so in one line and move on.

===== THE RUNNING ORDER =====
{contents}

===== THE PAGES =====
{chr(10).join(pages)}
"""
    completed = subprocess.run(
        [
            # --variant and --pure are NOT ocask options. An earlier version passed
            # them because they appear as shorthand in the routing notes, and the
            # reader failed with an unknown-option error before it ever reached the
            # model. Check the tool's own help before copying a flag out of prose.
            "ocask", "--model", "deepseek-v4-pro",
            "--task", "-", "--lens", "general", "--temperature", "0",
            "--timeout-ms", "300000",
        ],
        input=task,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"reader model failed with rc={completed.returncode}; no report written")
    report = completed.stdout.strip()
    if not report:
        raise RuntimeError("reader model returned no report; no report written")

    output_path = os.path.join(
        PRESS_WORK, f"reader-batch-{chapters[0]}to{chapters[-1]}.md"
    )
    write_atomically(output_path, report)
    print(f"reader -> {output_path} rc=0 bytes={os.path.getsize(output_path)}")


if __name__ == "__main__":
    main(sys.argv)
