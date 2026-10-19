import re, html, urllib.request, urllib.parse, gzip

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    r = urllib.request.urlopen(req, timeout=45)
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")

print("########## ARS TECHNICA")
try:
    d = get("https://feeds.arstechnica.com/arstechnica/technology-lab")
    items = re.findall(r"(?s)<item[ >].*?</item>", d)
    for it in items[:15]:
        t = re.search(r"<title>(.*?)</title>", it, re.S)
        l = re.search(r"<link>(.*?)</link>", it, re.S)
        dt = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        cl = lambda m: html.unescape(re.sub("<[^>]+>", "", m.group(1))).strip() if m else ""
        print(cl(dt)[:32], "|", cl(t)[:80], "|", cl(l))
except Exception as e:
    print("ERR", e)

print()
print("########## COINDESK RSS")
for u in ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss"]:
    print("=== ", u)
    try:
        d = get(u)
        items = re.findall(r"(?s)<item[ >].*?</item>", d)
        for it in items[:14]:
            t = re.search(r"<title>(.*?)</title>", it, re.S)
            l = re.search(r"<link>(.*?)</link>", it, re.S)
            dt = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
            cl = lambda m: html.unescape(re.sub("<[^>]+>", "", m.group(1))).strip() if m else ""
            print(cl(dt)[:32], "|", cl(t)[:95], "|", cl(l)[:100])
    except Exception as e:
        print("ERR", e)
    print()
