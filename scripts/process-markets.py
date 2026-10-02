#!/usr/bin/env python3
import json
import math

# Read the markets data
with open('/home/runner/work/aeon/aeon/.coingecko-markets.json', 'r') as f:
    markets = json.load(f)

# Stablecoins to exclude
stablecoins = ['tether', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg']

# Filter out stablecoins
filtered = [c for c in markets if c['symbol'].lower() not in stablecoins and 'stablecoin' not in c['name'].lower()]

# Filter by 24h volume (minimum $1M)
filtered = [c for c in filtered if c.get('total_volume', 0) >= 1_000_000]

# Sort by 24h change
filtered.sort(key=lambda x: x['price_change_percentage_24h'], reverse=True)

# Get top 10 winners and losers
winners = filtered[:10]
losers = filtered[-10:] if len(filtered) >= 10 else []

# Read the trending data with nested structure
with open('/home/runner/work/aeon/aeon/.trending.json', 'r') as f:
    trending_raw = json.load(f)

# Extract the nested coins
trending = [t['item'] for t in trending_raw['coins']][:7]  # Get top 7 trending

# Compute market pulse
top_100 = filtered[:100]
positive_count = sum(1 for c in top_100 if c.get('price_change_percentage_24h', 0) > 0)
median_change = 0
if top_50 := top_100[:50]:
    changes = [c.get('price_change_percentage_24h', 0) for c in top_50]
    changes.sort()
    median_change = changes[25]  # 25th percentile = median

market_pulse = f"Broad risk-on — {positive_count}/100 top coins are green, median +{median_change:.1f}%"

# Helper to format currency
def fmt_currency(val):
    if val is None:
        return "N/A"
    if val >= 1_000_000_000:
        return f"${val/1_000_000_000:.1f}B"
    elif val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif val >= 1_000:
        return f"${val/1_000:.1f}K"
    else:
        return f"${val:.2f}"

# Helper to format percentage
def fmt_pct(val):
    sign = '+' if val >= 0 else ''
    return f"{sign}{val:.1f}%"

# Helper to format number (for ranks, counts)
def fmt_num(num):
    if num is None:
        return "N/A"
    return f"#{num:,}" if num >= 1_000 else f"#{num}"

# Helper to convert value to float for percentage
def float_pct(val):
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        return float(val.replace('%', ''))
    return 0.0

# Build output structure
output = {
    'market_pulse': market_pulse,
    'winners': [
        {
            'symbol': w['symbol'].upper(),
            'name': w['name'],
            'rank': fmt_num(w.get('market_cap_rank')),
            'price': fmt_currency(w.get('current_price')),
            'change_24h': fmt_pct(w.get('price_change_percentage_24h', 0)),
            'change_7d': fmt_pct(w.get('price_change_percentage_7d', 0)),
            'change_1h': fmt_pct(w.get('price_change_percentage_1h', 0)),
            'volume': fmt_currency(w.get('total_volume')),
            'market_cap': fmt_currency(w.get('market_cap')),
        }
        for w in winners
    ],
    'losers': [
        {
            'symbol': l['symbol'].upper(),
            'name': l['name'],
            'rank': fmt_num(l.get('market_cap_rank')),
            'price': fmt_currency(l.get('current_price')),
            'change_24h': fmt_pct(l.get('price_change_percentage_24h', 0)),
            'change_7d': fmt_pct(l.get('price_change_percentage_7d', 0)),
            'change_1h': fmt_pct(l.get('price_change_percentage_1h', 0)),
            'volume': fmt_currency(l.get('total_volume')),
            'market_cap': fmt_currency(l.get('market_cap')),
        }
        for l in losers
    ],
    'trending': [
        {
            'name': t['name'],
            'symbol': t['symbol'].upper(),
            'rank': fmt_num(t.get('market_cap_rank')),
            'price': fmt_currency(t.get('price')),
            'change_24h': fmt_pct(float_pct(t.get('price_change_percentage_24h', {}).get('usd', 0) if isinstance(t.get('price_change_percentage_24h'), dict) else t.get('price_change_percentage_24h', 0))),
        }
        for t in trending
    ]
}

# Apply tags to winners
tagged_winners = []
for w in output['winners']:
    tags = []

    # TRENDING+UP
    trending_symbol = next((t['symbol'].upper() for t in trending if t['symbol'].upper() == w['symbol']), None)
    change_val = float_pct(w.get('price_change_percentage_24h', 0))
    if trending_symbol and change_val > 0:
        tags.append('TRENDING+UP')

    # BREAKOUT
    change_24h = float_pct(w.get('price_change_percentage_24h', 0))
    change_7d = float_pct(w.get('price_change_percentage_7d', 0))
    if change_24h > 15 and change_7d > 25:
        tags.append('BREAKOUT')

    # PUMP-RISK
    rank = w.get('rank', 'N/A')
    try:
        rank = int(rank.replace('#', '').replace(',', '').strip()) if rank != 'N/A' else 999
    except (ValueError, AttributeError):
        rank = 999
    if rank > 150 and change_24h > 30:
        tags.append('PUMP-RISK')

    # MICROCAP
    market_cap = output['winners'].index(w) + 1
    if market_cap >= 150:  # Rough estimate
        tags.append('MICROCAP')

    # MAJOR
    try:
        rank = int(w['rank'].replace('#', '').replace(',', '').strip())
    except (ValueError, AttributeError):
        rank = 999
    if rank <= 20:
        tags.append('MAJOR')

    w['tags'] = tags
    tagged_winners.append(w)

output['winners'] = tagged_winners

# Apply tags to losers
tagged_losers = []
for l in output['losers']:
    tags = []

    # TRENDING+DOWN
    trending_symbol = next((t['symbol'].upper() for t in trending if t['symbol'].upper() == l['symbol']), None)
    change_val = float_pct(l.get('price_change_percentage_24h', 0))
    if trending_symbol and change_val < 0:
        tags.append('TRENDING+DOWN')

    # CAPITULATION
    change_24h = float_pct(l.get('price_change_percentage_24h', 0))
    volume_str = l.get('volume', 'N/A')
    if volume_str != 'N/A':
        volume = float(volume_str.replace('$', '').replace('M', 'e6').replace('K', 'e3').replace('B', 'e9'))
    else:
        volume = 0
    if change_24h < -10 and volume > 3_000_000:
        tags.append('CAPITULATION')

    # PUMP-RISK (reversal case)
    rank = l.get('rank', 'N/A')
    try:
        rank = int(rank.replace('#', '').replace(',', '').strip()) if rank != 'N/A' else 999
    except (ValueError, AttributeError):
        rank = 999
    if rank > 150 and change_24h < -30:
        tags.append('PUMP-RISK')

    l['tags'] = tags
    tagged_losers.append(l)

output['losers'] = tagged_losers

# Identify notable moves
notable = []

# TRENDING+UP or TRENDING+DOWN
for t in trending:
    change_val = float_pct(t.get('price_change_percentage_24h', {}).get('usd', 0) if isinstance(t.get('price_change_percentage_24h'), dict) else t.get('price_change_percentage_24h', 0))
    trending_symbol = t['symbol'].upper()
    # Check if trending
    in_winners = any(w['symbol'] == trending_symbol and float_pct(w.get('price_change_percentage_24h', 0)) > 0 for w in winners)
    in_losers = any(l['symbol'] == trending_symbol and float_pct(l.get('price_change_percentage_24h', 0)) < 0 for l in losers)

    if in_winners and change_val > 5:
        notable.append(f"{trending_symbol}: trending +{change_val:.1f}%")
    elif in_losers and change_val < -5:
        notable.append(f"{trending_symbol}: trending -{abs(change_val):.1f}%")

# BREAKOUT
for w in winners:
    change_24h = float_pct(w.get('price_change_percentage_24h', 0))
    change_7d = float_pct(w.get('price_change_percentage_7d', 0))
    if change_24h > 15 and change_7d > 25:
        notable.append(f"{w['symbol']}: {change_24h:.1f}% 24h, {change_7d:.1f}% 7d — BREAKOUT")

# PUMP-RISK
for w in winners:
    change_24h = float_pct(w.get('price_change_percentage_24h', 0))
    rank = w.get('rank', 'N/A')
    try:
        rank = int(rank.replace('#', '').replace(',', '').strip()) if rank != 'N/A' else 999
    except (ValueError, AttributeError):
        rank = 999
    if rank > 150 and change_24h > 30:
        notable.append(f"{w['symbol']}: #{rank} rank up {change_24h:.1f}% — PUMP-RISK, low liquidity")

# CAPITULATION
for l in losers:
    change_24h = float_pct(l.get('price_change_percentage_24h', 0))
    volume_str = l.get('volume', 'N/A')
    if volume_str != 'N/A':
        volume = float(volume_str.replace('$', '').replace('M', 'e6').replace('K', 'e3').replace('B', 'e9'))
    else:
        volume = 0
    if change_24h < -10 and volume > 3_000_000:
        notable.append(f"{l['symbol']}: {change_24h:.1f}% 24h on {volume_str} — CAPITULATION")

output['notable'] = notable[:4]  # Top 4 notable moves

print(json.dumps(output, indent=2))
