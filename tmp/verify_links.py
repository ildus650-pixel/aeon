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
print("items", len(items))
for it in items[:10]:
    t = re.search(r"<title>(.*?)</title>", it, re.S)
    l = re.search(r"<link>(.*?)</link>", it, re.S)
    dt = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
    cl = lambda m: html.unescape(re.sub("<[^>]+>", "", m.group(1))).strip() if m else ""
    print(cl(dt)[:32], "|", cl(t)[:90], "|", cl(l))

print()
print("##### HEAD CHECKS")
LINKS = [
    "https://www.theregister.com/virtualization/2026/10/19/linux-kvm-guest-host-escape-rated-critical-may-represent-a-new-way-to-attack-penguin-powered-networking/5303744",
    "https://www.theregister.com/security/2026/10/19/connectwise-turns-off-its-saas-y-backup-security-and-management-services-to-probe-security-snafu/5303758",
    "https://techcrunch.com/2026/10/18/anthropic-says-its-committing-5-of-its-shares-to-a-public-benefit-fund/",
    "https://techcrunch.com/2026/10/19/apple-updates-guidelines-to-ban-nudify-apps-masquerading-as-regular-apps-to-pass-review/",
    "https://techcrunch.com/2026/10/19/musk-pledges-to-give-every-kid-in-america-one-of-his-spacex-shares/",
    "https://mistral.ai/news/timestral/",
    "https://lwn.net/Articles/1101143/",
    "https://fintech.global/2026/10/19/opsin-raises-21m-as-ai-agents-outpace-legacy-security/",
    "https://www.coindesk.com/markets/2026/10/19/jpmorgan-s-jpm-coin-representing-dollar-deposits-is-coming-to-ethereum-report",
    "https://cointelegraph.com/news/jpmorgan-jpm-coin-ethereum-institutional-clients-report",
    "https://cointelegraph.com/news/bitcoin-ether-etfs-shed-549m-october-eth-outflows-near-1b",
]
for u in LINKS:
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=25)
        print(r.status, u)
    except Exception as e:
        code = getattr(e, "code", "?")
        print(code, u, "|", str(e)[:70])
