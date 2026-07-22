import json, os, sys, time, urllib.request, glob
SP=os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__))
CB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root, wherever it is
# The ruler is the canonical repo file, read directly so two copies of one promise
# can never drift apart inside the checker built to catch exactly that. It is never read
# from PRESS_WORK and callers never stage a copy.
rules=json.load(open(f"{CB}/press/core-invariants.json"))
a=json.load(open(os.path.expanduser('~/.local/share/opencode/auth.json')))['openrouter']
key=a.get('key') or a.get('apiKey') or a.get('api_key')
path=sys.argv[1]; name=os.path.basename(path)
q=("You are checking ONE page against a list of rules, one rule at a time. This is not an "
   "overall judgement and you must not give one.\n\nFor EACH rule below, in order:\n"
   "- Search the page for any sentence that would make that rule untrue, or that a reader "
   "could follow INSTEAD of the rule.\n- If you find one, QUOTE IT VERBATIM.\n"
   "- If there is genuinely none, write NONE.\n\nDo not summarise. Do not judge the page "
   "overall. Do not comment on style. Work rule by rule. A sentence that sounds sensible and "
   "helpful can still break a rule — those are the ones that matter, so read for MEANING, not "
   "tone. Most pages will be NONE for most rules; do not invent violations.\n\nTHE RULES:\n"
   + "\n".join(f"RULE {i+1}: {r}" for i,r in enumerate(rules))
   + f"\n\nTHE PAGE ({name}):\n\n{open(path).read()}\n\n"
   + 'Return ONLY JSON: {"rule_1":{"violating_quote":"..." or "NONE"}, ... through rule_%d}' % len(rules))
body=json.dumps({"model":"tencent/hy3","messages":[{"role":"user","content":q}],
                 "temperature":0,"max_tokens":20000}).encode()
t0=time.time()
r=json.load(urllib.request.urlopen(urllib.request.Request(
  "https://openrouter.ai/api/v1/chat/completions", data=body,
  headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}), timeout=900))
out=r["choices"][0]["message"].get("content") or ""
open(f"{SP}/sweep-{name}.json","w").write(out)
print(name, round(time.time()-t0,1), r.get("usage",{}).get("cost"))
