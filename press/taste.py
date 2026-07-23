import json, os, re, sys, time, urllib.request
from brief_contract import BRIEF_FIELDS,BRIEF_LIST_FIELDS
SP=os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__)); CB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root, wherever it is
if len(sys.argv)!=3:
    raise SystemExit("usage: python3 press/taste.py <page-path> <tag>")
page_path, tag = sys.argv[1], sys.argv[2]
r=lambda p: open(f"{CB}/{p}").read()

# Shop rule 8: the taster receives the chapter's brief. Item 4 (is anything asserted that
# nobody established) and item 6 (contradictions, quoted in the brief) cannot be answered
# from the page alone, so this shop was recording straight fives on a question the tool never
# let the taster ask. The chapter is read from the page's own first heading -- the same line
# press/read-for-missing.py trusts -- so a brief is keyed to the page, never to a filename
# that might lie. A present brief that breaks the press/print.py contract is a fault, not a
# missing file: it fails here, before any auth or network access, never as "no brief supplied".
# The exact brief field set lives once in press/brief_contract.py and is shared with the
# producer (prep.py) and the printer (print.py), so the three cannot drift apart.
def page_chapter_and_title(text):
    # "# 8. The money" -> (8, "The money"); a page with no such heading -> (None, None).
    first_line=(text.splitlines() or [""])[0]
    heading=re.fullmatch(r"#\s+(\d+)\.\s+(.*)", first_line)
    if not heading:
        return None, None
    return int(heading.group(1)), heading.group(2).strip()
def damaged_brief(path, problem):
    # A present brief that cannot be loaded or breaks the contract is a fault, not a missing
    # file. Tasting items 4 and 6 need the brief, so a broken one must fail closed here --
    # visibly, on stderr, before any auth or network access -- never as "no brief supplied".
    sys.stderr.write(f"DAMAGED BRIEF: {path}: {problem}\n")
    raise SystemExit(1)
def load_brief(path, chapter, title):
    # None means only one thing: the brief file genuinely does not exist. Any other failure --
    # an unreadable or non-UTF-8 file, invalid JSON, a non-object, the wrong exact fields, the
    # wrong chapter or title, malformed list values, an empty must_cover -- is a present but
    # damaged brief, and fails closed via damaged_brief, never reported as "no brief supplied".
    try:
        with open(path, encoding="utf-8") as handle:
            raw=handle.read()
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as problem:
        damaged_brief(path, f"could not be read ({problem})")
    try:
        data=json.loads(raw)
    except json.JSONDecodeError as problem:
        damaged_brief(path, f"is not valid JSON ({problem.msg})")
    if not isinstance(data, dict):
        damaged_brief(path, "must contain a JSON object")
    if set(data)!=set(BRIEF_FIELDS):
        damaged_brief(path, f"has the wrong fields; "
                            f"missing={sorted(set(BRIEF_FIELDS)-set(data))}, "
                            f"extra={sorted(set(data)-set(BRIEF_FIELDS))}")
    if data["chapter"]!=chapter:
        damaged_brief(path, f"identifies chapter {data['chapter']!r}, expected {chapter}")
    if data["title"]!=title:
        damaged_brief(path, f"title {data['title']!r} does not match this page's title {title!r}")
    for field in BRIEF_LIST_FIELDS:
        entries=data[field]
        if not isinstance(entries, list) or any(not isinstance(e, str) or not e.strip() for e in entries):
            damaged_brief(path, f"field {field!r} must be a list of non-empty strings")
    if not data["must_cover"]:
        damaged_brief(path, "does not name anything the chapter must cover")
    return data
page_text=open(page_path, encoding="utf-8").read()
chapter, title=page_chapter_and_title(page_text)
brief=load_brief(os.path.join(SP, f"brief-{chapter}.json"), chapter, title) if chapter is not None else None
if brief is None:
    reason=("The page carries no chapter heading, so no brief could be attached to it."
            if chapter is None else
            "No brief file was supplied for this chapter.")
    brief_block=("===== NO BRIEF SUPPLIED =====\n"+reason
                 +" Answer item 4 (is anything asserted that nobody established) and item 6 "
                   "(contradictions) from the page and the voice standards alone; the "
                   "must_cover and must_not_contradict lists are not available.")
else:
    brief_block=("===== THE BRIEF THIS CHAPTER WAS PRINTED FROM =====\n"
                 + json.dumps(brief, ensure_ascii=False, indent=2)
                 + "\nItem 4 asks whether anything is asserted that nobody established, and "
                   "item 6 reads every must_not_contradict quotation against the page. The "
                   "brief above is what those two items are judged against.")
if chapter==0:
    voice_standards=("===== VOICE STANDARD: CHAPTER 0 =====\n[WITHHELD: THIS PAGE IS CHAPTER 0, ONE OF THE VOICE-STANDARD CHAPTERS; IT MUST BE JUDGED AGAINST CHAPTER 1, NOT ITSELF.]\n"
                     +"===== VOICE STANDARD: CHAPTER 1 =====\n"+r("book/01-the-interview.md"))
elif chapter==1:
    voice_standards=("===== VOICE STANDARD: CHAPTER 0 =====\n"+r("book/00-opening-the-box.md")+"\n"
                     +"===== VOICE STANDARD: CHAPTER 1 =====\n[WITHHELD: THIS PAGE IS CHAPTER 1, ONE OF THE VOICE-STANDARD CHAPTERS; IT MUST BE JUDGED AGAINST CHAPTER 0, NOT ITSELF.]")
else:
    voice_standards=("===== VOICE STANDARD: CHAPTER 0 =====\n"+r("book/00-opening-the-box.md")+"\n"
                     +"===== VOICE STANDARD: CHAPTER 1 =====\n"+r("book/01-the-interview.md"))
a=json.load(open(os.path.expanduser('~/.local/share/opencode/auth.json')))['openrouter']
key=a.get('key') or a.get('apiKey') or a.get('api_key')
q=f"""You are the taster. Judge one finished chapter against the checklist below. You did not
write it. Judge the page against the checklist below, and against the chapter brief below when one is supplied.

The book teaches a NON-TECHNICAL owner to run a chain of restaurants, where the restaurants
are software projects, the cooks are AI agents and the dishes are units of work.

Apply "The taster's list" — all SEVEN items.

{r("TASTING-CHECKLIST.md")}
{voice_standards}
{brief_block}
===== THE PAGE YOU ARE TASTING =====
{page_text}

Return ONLY valid JSON. Escape quotation marks inside strings.
Every score is 1 to 5, where **5 is best and 1 is worst**. (An earlier version of this
prompt omitted the scale and the scores came back as all zeros and all ones — meaningless.
The verdict and the faults were still sound, but a number with no stated scale is noise.)
{{"verdict":"SERVE" or "SEND BACK","t1_first_read":n,"t2_voice":n,"t3_analogies":n,
"t4_unfounded":n,"t5_length_earned":n,"t6_contradiction":n,"t7_jargon":n,
"faults":[{{"where":"...","what":"..."}}],"why":"one sentence"}}"""
body=json.dumps({"model":"tencent/hy3","messages":[{"role":"user","content":q}],
                 "temperature":0,"max_tokens":20000}).encode()
res=json.load(urllib.request.urlopen(urllib.request.Request(
  "https://openrouter.ai/api/v1/chat/completions", data=body,
  headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}), timeout=900))
open(f"{SP}/hy3taste-{tag}.out","w").write(res["choices"][0]["message"].get("content") or "")
print(tag, res.get("usage",{}).get("cost"))
