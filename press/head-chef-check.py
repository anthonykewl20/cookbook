import re, sys, json, os
# Words that only mean something to a programmer. Matched on WORD BOUNDARIES —
# an earlier version matched substrings and found "repo" inside "reports", which
# would have sent a clean page back. A check that manufactures faults is worse
# than no check.
JARGON = ["repository","repo","repos","commit","commits","API","APIs","JSON","YAML",
          "config","CLI","terminal","shell","git","branch","deploy","runtime","backend",
          "frontend","boolean","schema","endpoint","parameter","variable","function",
          "namespace","instantiate","refactor","dependency","syntax","parse","LLM",
          "codebase","repo's","worktree","worktrees","invariant","rebase","stdout","stderr","regex","daemon","cron","sandbox","stack trace",
          # Added after the TASTER caught these in chapter 44 and the script was blind to
          # them — judgement beating the list for the second time. Both were checked against
          # every bound page first: they appear in chapter 44 and nowhere else, so neither
          # can cry wolf. "command" was deliberately NOT added: it has an ordinary English
          # meaning the book may legitimately want, and this list has already produced one
          # false flag by swallowing a normal word.
          "file path","file paths","filepath","identifier","identifiers"]
def score(path):
    t = open(path).read()
    m = re.match(r"^#\s*(\d+)\.", t.strip())
    ch = m.group(1) if m else None
    flat_i = t.find("## The rules, flat")
    body = t[:flat_i] if flat_i > 0 else t
    flat = t[flat_i:] if flat_i > 0 else ""
    u = body.find("## Unresolved")
    if u > 0: body = body[:u]
    # Scan the WHOLE page, not just the body. An earlier version scanned the body
    # only and walked straight past "worktree invariant" sitting in a flat rule —
    # which is the part the appliance obeys, so if anything it matters more there.
    hits, flat_hits = {}, {}
    for j in JARGON:
        n = len(re.findall(r"\b" + re.escape(j) + r"\b", body, re.I))
        if n: hits[j] = n
        fn = len(re.findall(r"\b" + re.escape(j) + r"\b", flat, re.I))
        if fn: flat_hits[j] = fn
    heads = re.findall(r"^##\s+(.+)$", body, re.M)
    return {
        "file": os.path.basename(path),
        "A1_chapter_number": ch,
        "A1_settles_line": "What this chapter settles:" in t,
        "A1_flat_rules": flat_i > 0,
        "A1_flat_rules_numbered": bool(re.search(r"^\s*1\.", flat, re.M)),
        "A4_body_words": len(body.split()),
        "A4_within_700": len(body.split()) <= 700,
        "A5_jargon_hits": hits,
        "A5_jargon_in_flat_rules": flat_hits,
        "headings": heads,
        # Added after a seeded-fault control: BOTH tasters missed a label heading
        # ("Cost tracking") replacing a statement. Judgement missed it, so it moves
        # to the mechanical list. Statement headings in this book run 5-9 words;
        # a short heading is a LABEL SUSPECT flagged for a human eye, not an auto-fail.
        # An imperative IS a statement — "Never copy it" is a rule, not a label —
        # so short headings that open with a command word are not suspects.
        "A1_label_suspects": [h for h in heads if len(h.split()) <= 3
                              and h.split()[0].lower() not in
                              ("never","always","do","keep","write","stop","start","use","ask","check")],
        "has_unresolved": u > 0,
    }
print(json.dumps([score(p) for p in sys.argv[1:] if os.path.exists(p)], indent=2))
