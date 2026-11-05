#!/usr/bin/env python3

import json
from datetime import date

# Load markets data
with open('/home/runner/.claude/projects/-home-runner-work-aeon-aeon/4375ca3a-b87b-49bf-9aac-5a9de30db681/tool-results/bnnmxivbj.txt', 'r') as f:
    markets_data = json.load(f)

# Load trending data
with open('/home/runner/.claude/projects/-home-runner-work-aeon-aeon/4375ca3a-b87b-49bf-9aac-5a9de30db681/tool-results/b9zlyq8mj.txt', 'r') as f:
    trending_data = json.load(f)

# Filter out stablecoins (case-insensitive check)
def is_stablecoin(coin):
    symbol_lower = coin['symbol'].lower()
    name_lower = coin['name'].lower()
    stable_ids = {'tether', 'usdc', 'usdt', 'dai', 'busd', 'gemini', 'frax',
                  'pax', 'wusdt', 'usd-coin', 'usd', 'first-digital-usd',
                  'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg'}
    if symbol_lower in stable_ids:
        return True
    if symbol_lower.startswith('usd') or symbol_lower.startswith('eur') or symbol_lower.startswith('gbp'):
        return True
    stable_keywords = ['stablecoin', 'tether', 'usd coin', 'binance usd']
    for keyword in stable_keywords:
        if keyword in name_lower:
            return True
    return False

# Filter markets data
filtered_markets = []
for coin in markets_data:
    if is_stablecoin(coin):
        continue
    if coin.get('total_volume', 0) < 1000000:
        continue
    filtered_markets.append(coin)

# Sort by 24h change
filtered_markets.sort(key=lambda x: x.get('price_change_percentage_24h', 0) or 0, reverse=True)

top_10_winners = filtered_markets[:10]
top_10_losers = filtered_markets[-10:][::-1]  # Reverse so lowest first

# Format numbers
def fmt_price(num):
    if num is None:
        return 'N/A'
    if num >= 1:
        return f'${num:,.4f}'.rstrip('0').rstrip('.')
    elif num >= 0.000001:
        return f'${num:.4f}'
    else:
        return f'${num:.6f}'

def fmt_pct(num):
    if num is None:
        return 'N/A'
    return f'{num:+.1f}%'

def fmt_vol(num):
    if num is None:
        return 'N/A'
    if num >= 1_000_000_000:
        return f'${num/1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'${num/1_000_000:.1f}M'
    else:
        return f'${num:,.0f}'

def fmt_mcap(num):
    if num is None:
        return 'N/A'
    if num >= 1_000_000_000:
        return f'${num/1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'${num/1_000_000:.1f}M'
    else:
        return f'${num:,.0f}'

# Process trending coins
trending_coins = []
for item in trending_data['coins']:
    trending_coins.append({
        'symbol': item['item']['symbol'],
        'name': item['item']['name'],
        'rank': item['item']['market_cap_rank'],
        'price': item['item']['data']['price'],
        '24h_change': item['item']['data']['price_change_percentage_24h']['usd']
    })

top_7_trending = trending_coins[:7]

# Compute tags for each coin
def compute_tags(coin, trending_symbols):
    tags = []
    change_24h = coin.get('price_change_percentage_24h', 0) or 0
    change_7d = coin.get('price_change_percentage_7d', 0) or 0
    change_1h = coin.get('price_change_percentage_1h_in_currency', 0) or 0
    volume = coin.get('total_volume', 0) or 0
    market_cap = coin.get('market_cap', 0) or 0
    rank = coin.get('market_cap_rank', 999)
    symbol = coin['symbol']

    # Check trending
    is_trending = symbol in trending_symbols

    if is_trending and change_24h > 0:
        tags.append('[TRENDING+UP]')
        return tags
    if is_trending and change_24h < 0:
        tags.append('[TRENDING+DOWN]')
        return tags
    if change_24h > 15 and change_7d > 25:
        tags.append('[BREAKOUT]')
        return tags
    if change_24h > 20 and change_7d < 0:
        tags.append('[FADE]')
        return tags
    volume_proxy_ratio = volume / market_cap if market_cap > 0 else 0
    if change_24h < -10 and volume_proxy_ratio > 0.25:
        tags.append('[CAPITULATION]')
        return tags
    if rank > 150 and change_24h > 30:
        tags.append('[PUMP-RISK]')
        return tags
    if market_cap < 50_000_000:
        tags.append('[MICROCAP]')
        return tags
    if rank <= 20:
        tags.append('[MAJOR]')
    return tags

trending_symbols = {tc['symbol'] for tc in top_7_trending}

for coin in top_10_winners:
    coin['tags'] = compute_tags(coin, trending_symbols)

for coin in top_10_losers:
    coin['tags'] = compute_tags(coin, trending_symbols)

# Compute market pulse: top 100 by mcap
top_100_markets = [c for c in filtered_markets if (c.get('market_cap_rank', 0) or 999) <= 100]
if top_100_markets:
    total_100 = len(top_100_markets)
    positive_count = sum(1 for c in top_100_markets if (c.get('price_change_percentage_24h', 0) or 0) > 0)
    positive_pct = round((positive_count / total_100) * 100, 0)

    top_50_changes = [c.get('price_change_percentage_24h', 0) for c in top_100_markets[:50] if c.get('price_change_percentage_24h') is not None]
    median_change = sorted(top_50_changes)[len(top_50_changes)//2] if top_50_changes else 0

    if positive_pct <= 40:
        pulse_sentence = f"Broad risk-off — {int(positive_pct)}/{total_100} top coins are red, median {median_change:+.1f}%; losers dominate across L1s and DeFi."
    elif positive_pct >= 60:
        pulse_sentence = f"Mixed tape with alt rotation — {int(positive_pct)}% of top-100 alts green, median {median_change:+.1f}%; meme and AI-coin names leading."
    else:
        pulse_sentence = f"Quiet — median move under 1% either way; trending is dominated by new listings rather than price action."
else:
    pulse_sentence = "No market data available."

# Notable section: any coin with TRENDING+UP, BREAKOUT, CAPITULATION, PUMP-RISK
notable_signals = []
for coin in top_10_winners + top_10_losers:
    if any(t in coin.get('tags', []) for t in ['[TRENDING+UP]', '[BREAKOUT]', '[CAPITULATION]', '[PUMP-RISK]']):
        notable_signals.append(coin)

# Build the notification message
lines = []
today = date.today().strftime('%b %-d, %Y')
lines.append(f"*Token Movers — {today}*")
lines.append("")
lines.append(f"_{pulse_sentence}_")
lines.append("")
lines.append("*Top Winners (24h)*")

for i, coin in enumerate(top_10_winners, 1):
    symbol = coin['symbol'].upper()
    name = coin['name']
    price = fmt_price(coin.get('current_price'))
    chg_24h = fmt_pct(coin.get('price_change_percentage_24h'))
    chg_7d = fmt_pct(coin.get('price_change_percentage_7d'))
    chg_1h = fmt_pct(coin.get('price_change_percentage_1h_in_currency'))
    vol = fmt_vol(coin.get('total_volume'))
    rank = coin.get('market_cap_rank', 'N/A')
    tags = ' '.join(coin.get('tags', []))
    lines.append(f"{i}. {symbol} ({name}) — {price}  {chg_24h} / 7d {chg_7d} / 1h {chg_1h}  •  {vol} / #{rank}  {tags}")

lines.append("")
lines.append("*Top Losers (24h)*")

for i, coin in enumerate(top_10_losers, 1):
    symbol = coin['symbol'].upper()
    name = coin['name']
    price = fmt_price(coin.get('current_price'))
    chg_24h = fmt_pct(coin.get('price_change_percentage_24h'))
    chg_7d = fmt_pct(coin.get('price_change_percentage_7d'))
    chg_1h = fmt_pct(coin.get('price_change_percentage_1h_in_currency'))
    vol = fmt_vol(coin.get('total_volume'))
    rank = coin.get('market_cap_rank', 'N/A')
    tags = ' '.join(coin.get('tags', []))
    lines.append(f"{i}. {symbol} ({name}) — {price}  {chg_24h} / 7d {chg_7d} / 1h {chg_1h}  •  {vol} / #{rank}  {tags}")

lines.append("")
lines.append("*Trending*")

for i, tc in enumerate(top_7_trending, 1):
    sym = tc['symbol'].upper()
    name = tc['name']
    price = fmt_price(tc['price'])
    rank = tc['rank']
    chg_24h = fmt_pct(tc['24h_change'])
    lines.append(f"{i}. {name} ({sym}) — #{rank}, {price}, 24h {chg_24h}")

lines.append("")
lines.append("*Notable*")

if notable_signals:
    for coin in notable_signals[:4]:
        symbol = coin['symbol'].upper()
        name = coin['name']
        change_24h = coin.get('price_change_percentage_24h', 0) or 0
        tags_str = ' '.join(coin.get('tags', []))
        # Generate a brief reason
        if '[PUMP-RISK]' in tags_str:
            take = f"low-cap {change_24h:+.1f}% spike — manipulation warning"
        elif '[BREAKOUT]' in tags_str:
            take = f"sustained +{change_24h:.1f}% with strong 7d momentum"
        elif '[CAPITULATION]' in tags_str:
            take = f"{change_24h:+.1f}% down on heavy volume — relief bounce unlikely"
        elif '[TRENDING+UP]' in tags_str:
            take = f"trending with +{change_24h:.1f}% — strong signal"
        else:
            take = f"{change_24h:+.1f}% on watch"
        lines.append(f"• {symbol}: {tags_str} — {take}")
else:
    lines.append("No standout signals this session.")

lines.append("")

# Write notification message
notification_text = '\n'.join(lines)
print(notification_text)

# Save to file
with open('/tmp/token-movers-report.md', 'w') as f:
    f.write(notification_text)

print(f"\n--- Saved to /tmp/token-movers-report.md ({len(notification_text)} chars) ---")

# Log entry
log_lines = []
log_lines.append("### token-movers")
log_lines.append(f"- Mode: movers | Source: coingecko | Scope: global")
log_lines.append(f"- Var: <none>")
log_lines.append(f"- Pulse: {pulse_sentence}")
winners_str = ', '.join(f"{c['symbol'].upper()} (+{c.get('price_change_percentage_24h', 0):.1f}%)" for c in top_10_winners[:3])
losers_str = ', '.join(f"{c['symbol'].upper()} ({c.get('price_change_percentage_24h', 0):.1f}%)" for c in top_10_losers[:3])
trending_str = ', '.join(tc['symbol'].upper() for tc in top_7_trending[:4])
notable_tags = []
for coin in notable_signals:
    notable_tags.extend(coin.get('tags', []))
notable_str = ', '.join(set(notable_tags)) if notable_tags else 'none'

log_lines.append(f"- Winners: {winners_str}, ...")
log_lines.append(f"- Losers: {losers_str}, ...")
log_lines.append(f"- Trending: {trending_str}")
log_lines.append(f"- Notable: {notable_str}")

log_entry = '\n'.join(log_lines)
print("\n--- Log Entry ---")
print(log_entry)
print("\n--- Saved log to /tmp/token-movers-log.md ---")
with open('/tmp/token-movers-log.md', 'w') as f:
    f.write(log_entry + '\n')