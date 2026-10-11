import json
import subprocess

fd = subprocess.run(["date", "-u", "-d", "yesterday", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
td = "2026-10-11"
prompt = f"Search X for substantive, recent posts about: the most notable technology, AI, and crypto stories today. Date range: {fd} to {td}. Return up to 10 high-signal posts - prioritize verifiable claims, launches, funding, releases, exploits, or hard data over hot takes. For EACH post return: @handle, the full text, date posted, exact engagement counts (likes, retweets, replies; 0 if unknown), and the direct link https://x.com/handle/status/ID. Return a numbered list."
payload = {"model":"grok-4.6","input":[{"role":"user","content":prompt}],"tools":[{"type":"x_search","from_date":fd,"to_date":td}]}
with open("/tmp/xai-digest-payload.json","w") as f:
    json.dump(payload,f)
print("bytes:",len(json.dumps(payload)))