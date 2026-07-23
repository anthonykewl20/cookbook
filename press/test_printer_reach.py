#!/usr/bin/env python3
"""Acceptance test for print.py's chapter-completeness check.

Host-authored (head chef), not written by the fix's author. It drives the REAL
`press/print.py --catalog` CLI against throwaway fixture repositories, so it tests the
tool's actual behaviour rather than a copy of its logic.

Three requirements, and any correct fix must satisfy all three:

  A. On the true running order, the catalog covers every chapter 0..50 (max is 50).
  B. THE DEFECT: if the LAST chapter falls off CONTENTS.md while its book/NN-*.md page
     still exists on disk, the tool must RAISE, not silently return a short catalog.
     (Before the fix this returned a 0..49 catalog with exit 0.)
  C. THE CONSTRAINT: the tool must still work for a chapter whose page does not exist
     yet. Removing a mid-range chapter's page while it stays in CONTENTS must NOT break
     the catalog — otherwise a printer could never be launched to write a missing page.

Run: python3 press/test_printer_reach.py   (exit 0 = pass, nonzero = fail)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PRESS_FILES = ["print.py", "brief_contract.py"]


def build_fixture(root, contents_text, book_numbers):
    """Create a minimal repo: <root>/press/*.py, <root>/CONTENTS.md, <root>/book/NN-*.md."""
    os.makedirs(os.path.join(root, "press"), exist_ok=True)
    for name in PRESS_FILES:
        shutil.copy(os.path.join(HERE, name), os.path.join(root, "press", name))
    with open(os.path.join(root, "CONTENTS.md"), "w", encoding="utf-8") as fh:
        fh.write(contents_text)
    book = os.path.join(root, "book")
    os.makedirs(book, exist_ok=True)
    for n in book_numbers:
        # Filenames only need the NN- prefix; the title suffix is irrelevant to the catalog anchor.
        open(os.path.join(book, f"{n:02d}-fixture-chapter.md"), "w").close()


def run_catalog(root):
    """Return (exit_code, parsed_json_or_None)."""
    proc = subprocess.run(
        [sys.executable, "press/print.py", "--catalog"],
        cwd=root, capture_output=True, text=True,
    )
    data = None
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            data = None
    return proc.returncode, data, proc.stderr.strip()


def real_contents():
    with open(os.path.join(REPO, "CONTENTS.md"), encoding="utf-8") as fh:
        return fh.read()


def book_numbers_on_disk():
    nums = []
    for name in os.listdir(os.path.join(REPO, "book")):
        m = re.match(r"(\d+)-.*\.md$", name)
        if m:
            nums.append(int(m.group(1)))
    return sorted(nums)


FAILURES = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        FAILURES.append(name)


def main():
    contents = real_contents()
    all_books = book_numbers_on_disk()
    max_book = max(all_books)

    with tempfile.TemporaryDirectory() as tmp:
        # A. Baseline: true running order, all pages present.
        a = os.path.join(tmp, "a")
        build_fixture(a, contents, all_books)
        code, data, err = run_catalog(a)
        check("A: baseline catalog exits 0", code == 0, err)
        check("A: baseline catalog covers 0..50",
              data is not None and max(int(k) for k in data) == max_book and 0 in {int(k) for k in data},
              f"got {sorted(int(k) for k in data) if data else None}")

        # B. Terminal chapter removed from CONTENTS, its page still on disk -> must RAISE.
        b = os.path.join(tmp, "b")
        truncated = "\n".join(
            l for l in contents.splitlines() if not re.match(rf"{max_book}\.\s", l.strip())
        )
        build_fixture(b, truncated, all_books)
        code, data, err = run_catalog(b)
        check("B: terminal-chapter drop is REJECTED (nonzero exit)", code != 0,
              f"exit={code}, catalog={sorted(int(k) for k in data) if data else None}")

        # C. Mid-range page absent but chapter kept in CONTENTS -> must still succeed.
        c = os.path.join(tmp, "c")
        mid = 30
        books_missing_mid = [n for n in all_books if n != mid]
        build_fixture(c, contents, books_missing_mid)
        code, data, err = run_catalog(c)
        check("C: missing mid-range page still yields a full catalog", code == 0, err)
        check("C: catalog still lists the unwritten chapter and full 0..50",
              data is not None and mid in {int(k) for k in data}
              and max(int(k) for k in data) == max_book,
              f"got {sorted(int(k) for k in data) if data else None}")

    if FAILURES:
        print(f"\n{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
