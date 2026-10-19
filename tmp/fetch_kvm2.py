import re, html, urllib.request

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
chunks = re.findall(r'(?s)<div[^>]*(?:id="body"|article_body|entry-content)[^>]*>(.*)', d)
body = max(chunks, key=len) if chunks else d
# paragraph-level extraction
paras = re.findall(r"(?s)<p[^>]*>(.*?)</p>", body)
out = []
for p in paras:
    t = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
    t = re.sub(r"\s+", " ", t)
    if len(t) > 50:
        out.append(t)
for i, p in enumerate(out):
    print(i, "|", p[:400])
print()
print("CVE mentions:", set(re.findall(r"CVE-\d{4}-\d+", body)))
print("CVSS mentions:", re.findall(r"\b\d\.\d\b(?=[^\d]{0,30}(?:CVSS|rated|score))", body)[:10])
