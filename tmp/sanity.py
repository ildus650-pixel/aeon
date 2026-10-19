import re, urllib.request, sys

p = "/home/runner/work/aeon/aeon/tmp/digest-final.md"
s = open(p, encoding="utf-8").read()

print("CHARS:", len(s), "->", "OK (<=3000)" if len(s) <= 3000 else "OVER")
print("EMOJI:", [c for c in s if ord(c) > 0x2100 and c not in "—·’‘“”"] or "none")
hedge = ["could potentially", "it remains to be seen", "may be significant", "watch this space",
         "arguably", "some might say", "potentially", "may ", "might ", "seems to", "appears to",
         "exciting", "game-chang", "revolutionary", "groundbreaking"]
hits = [h for h in hedge if h.lower() in s.lower()]
print("HEDGING/HYPE HITS:", hits or "none")
print("PLACEHOLDERS:", [w for w in ["TBD", "[link]", "TODO", "http://"] if w in s] or "none")
print("ITEMS:", len(re.findall(r"^\d+\. \*", s, re.M)))
print("WHYS:", len(re.findall(r"^   Why it matters:", s, re.M)))

urls = re.findall(r"https?://[^\s)]+", s)
print("\nLINK CHECKS:")
for u in urls:
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=25)
        print(" ", r.status, u)
    except Exception as e:
        print(" ", getattr(e, "code", "?"), u)
