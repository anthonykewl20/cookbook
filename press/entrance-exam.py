import json, os, sys, time, urllib.request
SP=os.environ.get("PRESS_WORK") or os.path.dirname(os.path.abspath(__file__))
model, tag = sys.argv[1], sys.argv[2]
a=json.load(open(os.path.expanduser('~/.local/share/opencode/auth.json')))['openrouter']
key=a.get('key') or a.get('apiKey') or a.get('api_key')
body=json.dumps({"model":model,"messages":[{"role":"user","content":open(f"{SP}/decomp-{tag}.md").read()}],
                 "temperature":0,"max_tokens":20000}).encode()
t0=time.time()
r=json.load(urllib.request.urlopen(urllib.request.Request(
  "https://openrouter.ai/api/v1/chat/completions", data=body,
  headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}), timeout=900))
out=r["choices"][0]["message"].get("content") or ""
slug=model.split("/")[-1]
open(f"{SP}/exam-{slug}-{tag}.out","w").write(out)
u=r.get("usage",{})
print(f"{slug} {tag}: {round(time.time()-t0,1)}s  ${u.get('cost')}  reasoning={u.get('completion_tokens_details',{}).get('reasoning_tokens')}")
