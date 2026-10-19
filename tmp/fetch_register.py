import re, html, urllib.request

URLS = [
    "https://www.theregister.com/virtualization/2026/10/19/linux-kvm-guest-host-escape-rated-critical-may-represent-a-new-way-to-attack-penguin-powered-networking/5303744",
    "https://www.theregister.com/security/2026/10/19/connectwise-turns-off-its-saas-y-backup-security-and-management-services-to-probe-security-snafu/5303758",
    "https://lwn.net/Articles/1101143/",
]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")

for url in URLS:
    print("#####", url)
    try:
        d = get(url)
    except Exception as e:
        print("ERR", e); print(); continue
    d = re.sub(r"(?s)<script.*?</script>", " ", d)
    d = re.sub(r"(?s)<style.*?</style>", " ", d)
    d = re.sub(r"(?s)<nav.*?</nav>", " ", d)
    d = re.sub(r"(?s)<aside.*?</aside>", " ", d)
    d = re.sub(r"(?s)<footer.*?</footer>", " ", d)
    # Register article bodies live in divs with class containing 'article_body' or id 'body'
    chunks = re.findall(r"(?s)<div[^>]*(?:id=\"body\"|article_body|entry-content|post_body)[^>]*>(.*)", d)
    body = max(chunks, key=len) if chunks else d
    text = html.unescape(re.sub(r"<[^>]+>", "\n", body))
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.split("\n")]
    lines = [l for l in lines if len(l) > 55]
    print("\n".join(lines)[:3000])
    print()
