import json, os, sys, time, urllib.request
SP=os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__)); CB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root, wherever it is
page_path, tag = sys.argv[1], sys.argv[2]
r=lambda p: open(f"{CB}/{p}").read()
a=json.load(open(os.path.expanduser('~/.local/share/opencode/auth.json')))['openrouter']
key=a.get('key') or a.get('apiKey') or a.get('api_key')
q=f"""You are the taster. Judge one finished chapter against the checklist below. You did not
write it. Judge only what is on the page.

The book teaches a NON-TECHNICAL owner to run a chain of restaurants, where the restaurants
are software projects, the chefs are AI agents and the dishes are units of work.

Apply "The taster's list" — all SEVEN items.

{r("TASTING-CHECKLIST.md")}
===== VOICE STANDARD: CHAPTER 0 =====
{r("book/00-opening-the-box.md")}
===== VOICE STANDARD: CHAPTER 1 =====
{r("book/01-the-interview.md")}
===== THE PAGE YOU ARE TASTING =====
{open(page_path).read()}

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
