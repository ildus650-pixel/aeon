import re, html, urllib.request, urllib.parse

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    })
    return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")

def ddg(q, n=6):
    d = get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    res = re.findall(r'(?s)<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', d)
    snip = re.findall(r'(?s)<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', d)
    out = []
    for i, (u, ti) in enumerate(res[:n]):
        t = html.unescape(re.sub(r"<[^>]+>", "", ti)).strip()
        u = html.unescape(u)
        if "uddg=" in u:
            u = urllib.parse.unquote(u.split("uddg=")[1].split("&")[0])
        s = html.unescape(re.sub(r"<[^>]+>", "", snip[i])).strip()[:300] if i < len(snip) else ""
        out.append((t, u, s))
    return out

QUERIES = [
    "OpenAI disclosed unauthorized agent incidents crypto wallet payment rows report",
    "JPMorgan JPM Coin Ethereum tokenized deposits Bloomberg",
    "October 19 2026 tech news announcement today",
]

for q in QUERIES:
    print("===== Q:", q)
    try:
        for t, u, s in ddg(q):
            print("*", t)
            print("  ", u)
            print("  ", s)
    except Exception as e:
        print("ERR", e)
    print()
