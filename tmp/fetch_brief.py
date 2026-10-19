import re, html, urllib.request, urllib.parse, gzip

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    })
    r = urllib.request.urlopen(req, timeout=45)
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")

def plain(d, limit=12000):
    d = re.sub(r"(?s)<script.*?</script>", " ", d)
    d = re.sub(r"(?s)<style.*?</style>", " ", d)
    paras = re.findall(r"(?s)<p[^>]*>(.*?)</p>", d)
    out = []
    for p in paras:
        t = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        if len(t) > 40:
            out.append(t)
    s = "\n".join(out)
    if len(s) < 500:
        s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", d)))
    return s[:limit]

print("########## AGENTNEWS 2026-10-19 FULL")
try:
    d = get("https://agentnewsdaily.com/brief/2026-10-19")
    t = plain(d, 14000)
    print(t)
except Exception as e:
    print("ERR", e)

print()
print("########## MOJEEK")
for q in ["OpenAI agent incidents crypto wallet payment disclosure October 2026",
          "JPMorgan JPM Coin Ethereum tokenized deposits"]:
    print("===== Q:", q)
    try:
        d = get("https://www.mojeek.com/search?q=" + urllib.parse.quote(q))
        items = re.findall(r'(?s)<a[^>]+class="ob"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', d)
        snips = re.findall(r'(?s)<p class="s">(.*?)</p>', d)
        for i, (u, ti) in enumerate(items[:6]):
            t = html.unescape(re.sub(r"<[^>]+>", "", ti)).strip()
            s = html.unescape(re.sub(r"<[^>]+>", "", snips[i])).strip()[:280] if i < len(snips) else ""
            print("*", t, "\n  ", u, "\n  ", s)
    except Exception as e:
        print("ERR", e)
    print()
