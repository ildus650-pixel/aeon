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
print("=== CT LINKS (unique) ===")
seen = set()
for u in re.findall(r"https://cointelegraph\.com/news/[A-Za-z0-9\-]+", d):
    if u not in seen:
        seen.add(u)
        print(u)

print()
print("=== HEAD CHECKS ===")
CANDS = [
    "https://www.coindesk.com/markets/2026/10/19/jpmorgan-s-jpm-coin-representing-dollar-deposits-is-coming-to-ethereum-bloomberg",
    "https://www.coindesk.com/tech/2026/10/19/bitcoin-mining-offshoot-nscale-loses-microsoft-ai-deal-as-power-delay-stretches-into-2030s",
    "https://www.coindesk.com/markets/2026/10/19/crypto-vault-deposits-top-usd10-billion-as-lending-risks-draw-regulatory-scrutiny",
    "https://www.coindesk.com/markets/2026/10/19/live-updates-bitcoin-tags-usd83-000-and-slips-back-as-chip-stocks-lead-a-rebound",
    "https://cointelegraph.com/news/bitcoin-ether-etfs-shed-549m-october-eth-outflows",
    "https://cointelegraph.com/news/qubic-chain-freeze-attacker-drains-wallets-weak-seeds",
    "https://cointelegraph.com/news/jpmorgan-jpm-coin-ethereum-institutional-clients",
    "https://cointelegraph.com/news/three-things-to-know-in-bitcoin-this-week",
]
for u in CANDS:
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=25)
        print(r.status, u)
    except Exception as e:
        print(getattr(e, "code", "?"), u)
