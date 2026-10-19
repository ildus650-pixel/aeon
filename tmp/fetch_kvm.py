import re, html, urllib.request, urllib.parse

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")

url = "https://www.theregister.com/virtualization/2026/10/19/linux-kvm-guest-host-escape-rated-critical-may-represent-a-new-way-to-attack-penguin-powered-networking/5303744"
d = get(url)
d = re.sub(r"(?s)<script.*?</script>", " ", d)
d = re.sub(r"(?s)<style.*?</style>", " ", d)
d = re.sub(r"(?s)<nav.*?</nav>", " ", d)
d = re.sub(r"(?s)<aside.*?</aside>", " ", d)
d = re.sub(r"(?s)<footer.*?</footer>", " ", d)
chunks = re.findall(r"(?s)<div[^>]*(?:id=\"body\"|article_body|entry-content)[^>]*>(.*)", d)
body = max(chunks, key=len) if chunks else d
txt = html.unescape(re.sub(r"<[^>]+>", "\n", body))
lines = [re.sub(r"\s+", " ", l).strip() for l in txt.split("\n")]
lines = [l for l in lines if len(l) > 40]
full = "\n".join(lines)
print("LEN", len(full))
print(full[2000:6000])
