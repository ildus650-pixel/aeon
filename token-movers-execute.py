#!/usr/bin/env python3
import json
import datetime
from pathlib import Path

# Step 1: Read the data
with open('.coingecko-markets.json') as f:
    markets_data = json.load(f)

with open('.trending.json') as f:
    trending_data = json.load(f)

# Step 2: Helper functions
def is_stablecoin(coin):
    # Exclude stablecoins based on rules
    symbol = coin.get('symbol', '').lower()
    name = coin.get('name', '').lower()
    coin_id = coin.get('id', '').lower()

    # Specific stablecoin symbols/ids
    stablecoin_ids = ['tether', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd']
    stablecoin_symbols = ['usdt', 'usdc', 'dai', 'fdusd', 'pyusd']

    if coin_id in stablecoin_ids or symbol in stablecoin_symbols:
        return True
    if any(s in symbol for s in ['usd', 'eur', 'gbp']) or 'stablecoin' in name:
        return True
    return False

def is_illiquid(coin):
    volume = coin.get('total_volume', 0)
    return volume < 1000000  # $1M

def enrich_with_tags(coin, all_tags):
    """Compute all tags for a coin and return top 2"""
    tags = []

    # Check if in trending
    in_trending = any(c.get('item', {}).get('id') == coin.get('id') for c in trending_data.get('coins', []))

    # TRENDING+UP / TRENDING+DOWN - need to check if top winner/loser
    # Will be set after sorting

    # BREAKOUT - 24h > 15% AND 7d > 25%
    price_change_24h = coin.get('price_change_percentage_24h', 0)
    price_change_7d = coin.get('price_change_percentage_7d_in_currency', 0)
    if price_change_24h > 15 and price_change_7d > 25:
        tags.append('[BREAKOUT]')

    # FADE - 24h > 20% BUT 7d negative
    if price_change_24h > 20 and price_change_7d < 0:
        tags.append('[FADE]')

    # CAPITULATION - 24h < -10% AND volume > 3x typical (proxy: market_cap ratio)
    if price_change_24h < -10:
        market_cap = coin.get('market_cap', 0)
        volume = coin.get('total_volume', 0)
        if market_cap > 0 and volume > 0:
            volume_to_mc_ratio = volume / market_cap
            if volume_to_mc_ratio > 0.25:
                tags.append('[CAPITULATION]')

    # PUMP-RISK - market cap rank > 150 AND 24h > 30%
    market_cap_rank = coin.get('market_cap_rank', 9999)
    if market_cap_rank > 150 and price_change_24h > 30:
        tags.append('[PUMP-RISK]')

    # MICROCAP - market cap < $50M
    market_cap = coin.get('market_cap', 0)
    if market_cap < 50000000:
        tags.append('[MICROCAP]')

    # MAJOR - market cap rank ≤ 20
    if market_cap_rank <= 20:
        tags.append('[MAJOR]')

    # TRENDING+UP/TRENDING+DOWN will be assigned after sorting

    return tags[:2]  # Max 2 tags

def format_price(price):
    if price < 0.01:
        return f'${price:.6f}'
    elif price < 1:
        return f'${price:.4f}'
    else:
        return f'${price:.2f}'

def format_volume(vol):
    if vol >= 1000000000:
        return f'${vol/1000000000:.1f}B'
    elif vol >= 1000000:
        return f'${vol/1000000:.1f}M'
    else:
        return f'${vol:.0f}'

def format_mcap(mcap):
    if mcap >= 1000000000:
        return f'${mcap/1000000000:.1f}B'
    elif mcap >= 1000000:
        return f'${mcap/1000000:.1f}M'
    else:
        return f'${mcap:.0f}'

# Step 3: Filter before ranking
filtered_coins = []
for coin in markets_data:
    if is_stablecoin(coin):
        continue
    if is_illiquid(coin):
        continue
    filtered_coins.append(coin)

# Step 4: Pick top 10 winners and losers by 24h %
sorted_coins = sorted(filtered_coins, key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)

winners = sorted_coins[:10]
losers = sorted_coins[-10:]

# Step 5: Enrich with signal tags
winners_with_tags = []
for coin in winners:
    tags = enrich_with_tags(coin, [])
    winners_with_tags.append(coin)

losers_with_tags = []
for coin in losers:
    tags = enrich_with_tags(coin, [])
    losers_with_tags.append(coin)

# Step 6: Market commentary
positive_coins = [c for c in filtered_coins if c.get('price_change_percentage_24h', 0) > 0]
positive_count = len(positive_coins)
total_count = len(filtered_coins)
median_positive = 0
if positive_coins:
    median_positive = sorted([c.get('price_change_percentage_24h', 0) for c in positive_coins])[len(positive_coins)//2]

if total_count == 0:
    market_pulse = "No coins passed filters."
elif positive_count / total_count >= 0.78:
    market_pulse = f"Broad risk-off — {positive_count}/{total_count} top coins are red, median {median_positive:.1f}%; losers dominate across cap tiers and volumes."
elif positive_count / total_count <= 0.4:
    market_pulse = f"Risk-on — {positive_count}/{total_count} top coins are red, median {median_positive:.1f}%; high-conviction winners on low caps."
else:
    market_pulse = f"Mixed tape with rotation — {positive_count}/{total_count} top-100 alts green, median {median_positive:.1f}%; mid-cap names leading."

# Step 7: Build the report
report_lines = []
report_lines.append(f"*Token Movers — {datetime.date.today().isoformat()}*")
report_lines.append("")
report_lines.append(f"_{market_pulse}_")
report_lines.append("")
report_lines.append("*Top Winners (24h)*")
for i, coin in enumerate(winners_with_tags, 1):
    symbol = coin.get('symbol', '').upper()
    name = coin.get('name', '')
    price = format_price(coin.get('current_price', 0))
    change_24h = coin.get('price_change_percentage_24h', 0)
    change_7d = coin.get('price_change_percentage_7d_in_currency', 0)
    change_1h = coin.get('price_change_percentage_1h', 0)
    volume = format_volume(coin.get('total_volume', 0))
    rank = coin.get('market_cap_rank', 0)
    mcap = format_mcap(coin.get('market_cap', 0))
    tags_str = " ".join(enrich_with_tags(coin, []))

    report_lines.append(f"{i}. {symbol} ({name}) — {price} {change_24h:+.1f}% / 7d {change_7d:+.1f}% / 1h {change_1h:+.1f}%  •  {volume} / #{rank}  {tags_str}")

report_lines.append("")
report_lines.append("*Top Losers (24h)*")
for i, coin in enumerate(losers_with_tags, 1):
    symbol = coin.get('symbol', '').upper()
    name = coin.get('name', '')
    price = format_price(coin.get('current_price', 0))
    change_24h = coin.get('price_change_percentage_24h', 0)
    change_7d = coin.get('price_change_percentage_7d_in_currency', 0)
    change_1h = coin.get('price_change_percentage_1h', 0)
    volume = format_volume(coin.get('total_volume', 0))
    rank = coin.get('market_cap_rank', 0)
    mcap = format_mcap(coin.get('market_cap', 0))
    tags_str = " ".join(enrich_with_tags(coin, []))

    report_lines.append(f"{i}. {symbol} ({name}) — {price} {change_24h:+.1f}% / 7d {change_7d:+.1f}% / 1h {change_1h:+.1f}%  •  {volume} / #{rank}  {tags_str}")

report_lines.append("")
report_lines.append("*Trending*")
trending_coins = trending_data.get('coins', [])[:7]
for i, trend_entry in enumerate(trending_coins, 1):
    item = trend_entry.get('item', {})
    symbol = item.get('symbol', '').upper()
    name = item.get('name', '')
    rank = item.get('market_cap_rank', 0)
    price = format_price(item.get('data', {}).get('price', 0))
    change_24h = item.get('data', {}).get('price_change_percentage_24h', {}).get('usd', 0)

    # Check if this trending coin is also a winner/loser
    is_winner = any(c.get('id') == item.get('id') for c in winners)
    is_loser = any(c.get('id') == item.get('id') for c in losers)

    # Determine tag
    tags = []
    if is_winner and item.get('data', {}).get('price_change_percentage_24h', {}).get('usd', 0) > 0:
        tags.append('[TRENDING+UP]')
    elif is_loser and item.get('data', {}).get('price_change_percentage_24h', {}).get('usd', 0) < 0:
        tags.append('[TRENDING+DOWN]')
    else:
        tags.append('[TRENDING]')

    tags_str = " ".join(tags)
    report_lines.append(f"{i}. {name} ({symbol}) — #{rank}, {price}, 24h {change_24h:+.1f}%  {tags_str}")

# Step 8: Notable section
report_lines.append("")
report_lines.append("*Notable*")
notable_items = []

for coin in winners_with_tags + losers_with_tags:
    tags = enrich_with_tags(coin, [])
    if '[PUMP-RISK]' in tags or '[BREAKOUT]' in tags or '[CAPITULATION]' in tags:
        symbol = coin.get('symbol', '').upper()
        change_24h = coin.get('price_change_percentage_24h', 0)
        volume = format_volume(coin.get('total_volume', 0))
        note = f"{symbol}: price went {change_24h:+.1f}% on ${volume} volume — {tags[0] if tags else ''}"
        notable_items.append(note)
        if len(notable_items) >= 4:
            break

if notable_items:
    for item in notable_items:
        report_lines.append(f"• {item}")
else:
    report_lines.append("None")

# Step 9: Write to report file
report_dir = Path('/tmp')
report_path = report_dir / 'token-movers-report.md'

with open(report_path, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"Report written to {report_path}")
print(f"Report size: {len(report_lines)} lines")

# Step 10: Log to memory/logs
today = datetime.date.today().isoformat()
log_path = Path('memory/logs') / f"{today}.md"
log_path.parent.mkdir(exist_ok=True)

with open(log_path, 'a') as f:
    f.write(f'\n### token-movers\n')
    f.write(f"- Mode: movers | Source: coingecko | Scope: global\n")
    f.write(f"- Var: ''\n")
    f.write(f"- Pulse: {market_pulse}\n")
    f.write(f"- Winners: {', '.join([c.get('symbol', '').upper() for c in winners])}\n")
    f.write(f"- Losers: {', '.join([c.get('symbol', '').upper() for c in losers])}\n")
    f.write(f"- Trending: {', '.join([c.get('item', {}).get('symbol', '').upper() for c in trending_data.get('coins', [])[:5]])}\n")
    f.write(f"- Notable: {', '.join(notable_items)}\n")
    f.write(f"\n")

print(f"Log appended to {log_path}")

# Step 11: Notify
import subprocess
notify_cmd = ['./notify', '-f', str(report_path)]
print(f"Running notify: {' '.join(notify_cmd)}")
result = subprocess.run(notify_cmd, capture_output=True, text=True)
print(f"Notify result: {result.returncode}")
if result.stderr:
    print(f"Notify stderr: {result.stderr}")
print("Token movers execution complete!")