import re, html, urllib.request, gzip

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    r = urllib.request.urlopen(req, timeout=45)
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")

# try candidate slugs
slugs = [
    "https://cointelegraph.com/news/bitcoin-ether-etfs-shed-549m-october-eth-outflows-near-1b",
    "https://cointelegraph.com/news/bitcoin-ether-etfs-shed-549-million-october-outflows",
    "https://cointelegraph.com/news/spot-bitcoin-etf-outflows-october",
]
for u in slugs:
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
        print("OK", r.status, u)
    except Exception as e:
        print(getattr(e, "code", "?"), u)

print()
print("=== check 'what happened in crypto today' for ETF figure ===")
try:
    d = get("https://cointelegraph.com/news/what-happened-in-crypto-today")
    d = re.sub(r"(?s)<script.*?</script>", " ", d)
    d = re.sub(r"(?s)<style.*?</style>", " ", d)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", d))
    txt = re.sub(r"\s+", " ", txt)
    for m in re.finditer(r"[^.]{0,260}(?:549|ETF outflow|outflow)[^.]{0,260}\.", txt):
        s = m.group(0).strip()
        if "ETF" in s or "549" in s:
            print("*", s[:420], "\n")
except Exception as e:
    print("ERR", e)
