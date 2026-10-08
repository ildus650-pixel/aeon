#!/usr/bin/env python3
import json
import re

# Load markets data from the file that WebFetch saved
with open('/home/runner/.claude/projects/-home-runner-work-aeon-aeon/fb7b941e-20e2-4fa5-8c9d-0bcedb077041/tool-results/call_7b48e3c193eb46ed87e135fd.txt', 'r') as f:
    content = f.read()

# Strip markdown code block if present
content = re.sub(r'^```json\s*', '', content)
content = re.sub(r'\s*```$', '', content)
markets = json.loads(content)

trending_data = {
    "coins": [
        {"name": "Super Intelligent Identity", "symbol": "SIMD", "market_cap_rank": 800, "current_price": 0.02280187987576131, "price_change_percentage_24h_in_currency": 20.446275657989066},
        {"name": "Derive", "symbol": "DRV", "market_cap_rank": 124, "current_price": 0.4411759097854263, "price_change_percentage_24h_in_currency": 19.424054291597205},
        {"name": "Quantus", "symbol": "QTC", "market_cap_rank": 502, "current_price": 169.3761579033074, "price_change_percentage_24h_in_currency": 49.442580639813904},
        {"name": "NEAR Protocol", "symbol": "NEAR", "market_cap_rank": 21, "current_price": 4.527094372626781, "price_change_percentage_24h_in_currency": -14.970389737511681},
        {"name": "Pudgy Penguins", "symbol": "PENGU", "market_cap_rank": 114, "current_price": 0.00799028411996631, "price_change_percentage_24h_in_currency": -7.198495182561563},
        {"name": "Pons", "symbol": "PONS", "market_cap_rank": 165, "current_price": 0.3493480144446806, "price_change_percentage_24h_in_currency": -7.91119859146486},
        {"name": "Zcash", "symbol": "ZEC", "market_cap_rank": 10, "current_price": 1183.082839732995, "price_change_percentage_24h_in_currency": -10.450210035133695},
        {"name": "Bitcoin", "symbol": "BTC", "market_cap_rank": 1, "current_price": 81761.11917160737, "price_change_percentage_24h_in_currency": -1.7969764344888168},
        {"name": "Quant", "symbol": "QNT", "market_cap_rank": 34, "current_price": 236.22118994246003, "price_change_percentage_24h_in_currency": -6.093452308281785},
        {"name": "Sui", "symbol": "SUI", "market_cap_rank": 29, "current_price": 1.0506498101515698, "price_change_percentage_24h_in_currency": -6.214812070593754},
        {"name": "Pearl", "symbol": "PRL", "market_cap_rank": 121, "current_price": 1.3513474700151844, "price_change_percentage_24h_in_currency": -3.0244330084297144},
        {"name": "Monad", "symbol": "MON", "market_cap_rank": 153, "current_price": 0.02396069654530129, "price_change_percentage_24h_in_currency": -7.091328994731254},
        {"name": "Jupiter", "symbol": "JUP", "market_cap_rank": 72, "current_price": 0.3373372491261698, "price_change_percentage_24h_in_currency": -4.3482214008659446},
        {"name": "Pyth Network", "symbol": "PYTH", "market_cap_rank": 97, "current_price": 0.08341986615586912, "price_change_percentage_24h_in_currency": 14.612220642924203},
        {"name": "peaq", "symbol": "PEAQ", "market_cap_rank": 285, "current_price": 0.03900426492598408, "price_change_percentage_24h_in_currency": -2.5061136352412148}
    ]
}

# Filter stablecoins
stablecoins = {'tether', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg', 'usdc'}

# Filter and sort by 24h change
filtered = []
for coin in markets:
    if coin['symbol'].lower() in stablecoins:
        continue
    if coin['total_volume'] < 1_000_000:  # <$1M volume
        continue
    filtered.append(coin)

# Sort by 24h % change (descending for winners, ascending for losers)
winners = sorted(filtered, key=lambda x: x['price_change_percentage_24h'], reverse=True)[:10]
losers = sorted(filtered, key=lambda x: x['price_change_percentage_24h'])[:10]

# Trending
trending = trending_data['coins'][:7]

# Tags calculation
trending_set = {t['symbol'].lower() for t in trending}

def get_tags(coin, winning_set, trending_set):
    tags = []
    # Handle both field names
    p24 = coin.get('price_change_percentage_24h_in_currency') or coin.get('price_change_percentage_24h', 0)
    p7 = coin.get('price_change_percentage_7d_in_currency', 0)
    rank = coin.get('market_cap_rank', 999)
    vol = coin.get('total_volume', 0)
    mcap = coin.get('market_cap', 0)

    # TRENDING+UP
    if coin['symbol'].lower() in trending_set and p24 > 0:
        tags.append('[TRENDING+UP]')

    # TRENDING+DOWN
    if coin['symbol'].lower() in trending_set and p24 < 0:
        tags.append('[TRENDING+DOWN]')

    # BREAKOUT
    if p24 > 15 and p7 > 25:
        tags.append('[BREAKOUT]')

    # FADE
    if p24 > 20 and p7 < 0:
        tags.append('[FADE]')

    # CAPITULATION
    if p24 < -10 and vol > mcap * 0.25:
        tags.append('[CAPITULATION]')

    # PUMP-RISK
    if rank > 150 and p24 > 30:
        tags.append('[PUMP-RISK]')

    # MICROCAP
    if mcap < 50_000_000:
        tags.append('[MICROCAP]')

    # MAJOR
    if rank <= 20:
        tags.append('[MAJOR]')

    return tags

# Tag winners
for w in winners:
    w['tags'] = get_tags(w, set(), trending_set)

# Tag losers
for l in losers:
    l['tags'] = get_tags(l, set(), trending_set)

# Trending tags
for t in trending:
    t['tags'] = get_tags(t, set(), trending_set)

# Calculate market pulse
positive_count = sum(1 for c in filtered[:100] if c['price_change_percentage_24h'] > 0)
sorted_changes = [c['price_change_percentage_24h'] for c in filtered[:50]]
median_change = sorted(sorted_changes)[25] if len(sorted_changes) >= 25 else 0

pulse_desc = "Broad risk-on" if positive_count > 60 else "Broad risk-off" if positive_count < 40 else "Mixed tape"

print(json.dumps({
    'winners': winners,
    'losers': losers,
    'trending': trending,
    'pulse': f"{pulse_desc} — {positive_count}/100 top coins are green, median {median_change:+.1f}%",
    'positive_pct': positive_count,
    'median_change': median_change
}, indent=2))
