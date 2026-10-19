import re, html, urllib.request, gzip

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    r = urllib.request.urlopen(req, timeout=45)
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")

d = get("https://cointelegraph.com/rss")
items = re.findall(r"(?s)<item[ >].*?</item>", d)
print("=== CT RAW ITEM 9 ===")
print(items[8][:900])
print()
print("=== CT ALL LINKS ===")
for u in re.findall(r"https://cointelegraph\.com/news/[A-Za-z0-9\-]+", d)[:12]:
    print(u)

d2 = get("https://www.coindesk.com/arc/outboundfeeds/rss/")
print()
print("=== COINDESK LINKS ===")
for m in re.findall(r"https://www\.coindesk\.com/[A-Za-z0-9\-/]+", d2)[:16]:
    print(m)
