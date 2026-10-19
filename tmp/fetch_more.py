import re, html, urllib.request, urllib.parse, json, gzip, io

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

def text(d, limit=3000):
    d = re.sub(r"(?s)<script.*?</script>", " ", d)
    d = re.sub(r"(?s)<style.*?</style>", " ", d)
    paras = re.findall(r"(?s)<p[^>]*>(.*?)</p>", d)
    out = []
    for p in paras:
        t = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        if len(t) > 55:
            out.append(t)
    s = "\n".join(out)
    if len(s) < 300:
        s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", d)))
    return s[:limit]

TARGETS = [
    ("neuron", "https://www.theneuron.ai/digest/everything-that-happened-in-ai-today-monday-october-19-2026/"),
    ("agentnews", "https://agentnewsdaily.com/brief/2026-10-19"),
    ("opsin", "https://fintech.global/2026/10/19/opsin-raises-21m-as-ai-agents-outpace-legacy-security/"),
    ("sweet", "https://www.globenewswire.com/news-release/2026/10/19/3383504/0/en/sweet-security-launches-virtual-patching-to-protect-production-before-permanent-fixes-are-deployed.html"),
]

for name, url in TARGETS:
    print("#####", name, url)
    try:
        d = get(url)
    except Exception as e:
        print("ERR", e); print(); continue
    t = text(d)
    print(t[:limit] if False else t[:3000])
    print()

# DuckDuckGo html search for primary sources
QUERIES = [
    "Schwab JPMorgan block third-party AI agents client accounts Wurster",
    "EU AI Office information requests OpenAI Anthropic agents October 2026",
    "OpenAI four unauthorized agent incidents crypto wallet 147451 rows",
    "Perplexity open sources SPACE microVM sandbox computer agent",
]
print("########## SEARCHES")
for q in QUERIES:
    print("===== Q:", q)
    try:
        d = get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    except Exception as e:
        print("ERR", e); continue
    res = re.findall(r'(?s)<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', d)
    snip = re.findall(r'(?s)<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', d)
    for i, (u, ti) in enumerate(res[:6]):
        t = html.unescape(re.sub(r"<[^>]+>", "", ti)).strip()
        u = html.unescape(u)
        if "uddg=" in u:
            u = urllib.parse.unquote(u.split("uddg=")[1].split("&")[0])
        s = ""
        if i < len(snip):
            s = html.unescape(re.sub(r"<[^>]+>", "", snip[i])).strip()[:260]
        print("*", t)
        print("  ", u)
        print("  ", s)
    print()
