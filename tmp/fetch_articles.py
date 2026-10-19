import sys, re, html, urllib.request

URLS = [
    "https://www.theregister.com/virtualization/2026/10/19/linux-kvm-guest-host-escape-rated-critical-may-represent-a-new-way-to-attack-penguin-powered-networking/5303744",
    "https://www.theregister.com/security/2026/10/19/connectwise-turns-off-its-saas-y-backup-security-and-management-services-to-probe-security-snafu/5303758",
    "https://techcrunch.com/2026/10/18/anthropic-says-its-committing-5-of-its-shares-to-a-public-benefit-fund/",
    "https://techcrunch.com/2026/10/19/apple-updates-guidelines-to-ban-nudify-apps-masquerading-as-regular-apps-to-pass-review/",
    "https://techcrunch.com/2026/10/19/musk-pledges-to-give-every-kid-in-america-one-of-his-spacex-shares/",
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
    paras = re.findall(r"(?s)<p[^>]*>(.*?)</p>", d)
    out = []
    for p in paras:
        t = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        if len(t) > 60:
            out.append(t)
    body = "\n".join(out)
    if len(body) < 400:
        # fallback: strip all tags
        body = re.sub(r"<[^>]+>", " ", d)
        body = re.sub(r"\s+", " ", html.unescape(body))
    print(body[:2400])
    print()
