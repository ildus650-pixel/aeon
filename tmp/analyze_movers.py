import json

# Market data
with open('/tmp/movers-data.json', 'r') as f:
    data = json.load(f)

# Trending data
with open('/tmp/trending-data.json', 'r') as f:
    trending = json.load(f)

# Filter stablecoins
stablecoins = {'tether', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg'}

winners = []
losers = []

for coin in data['market_data']:
    symbol = coin['symbol'].lower()
    if symbol in stablecoins:
        continue
    change_24h = coin['price_change_percentage_24h']
    if change_24h > 0:
        winners.append({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'rank': coin['market_cap_rank'],
            'price': coin['current_price'],
            'change_24h': change_24h,
            'change_7d': coin['price_change_percentage_7d'],
            'change_1h': coin['price_change_percentage_1h'],
            'volume': coin['total_volume'],
            'mcap': coin['market_cap']
        })
    else:
        losers.append({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'rank': coin['market_cap_rank'],
            'price': coin['current_price'],
            'change_24h': change_24h,
            'change_7d': coin['price_change_percentage_7d'],
            'change_1h': coin['price_change_percentage_1h'],
            'volume': coin['total_volume'],
            'mcap': coin['market_cap']
        })

# Sort
winners.sort(key=lambda x: x['change_24h'], reverse=True)[:10]
losers.sort(key=lambda x: x['change_24h'], reverse=True)  # negative, so already sorted descending

# Market pulse
if len(winners) + len(losers) > 0:
    pct_positive = len(winners) / (len(winners) + len(losers)) * 100
    # Calculate median of the top 50 coins with change data
    top_coins = [c for c in data['market_data'] if c['symbol'].lower() not in stablecoins][:50]
    top_changes = sorted([c['price_change_percentage_24h'] for c in top_coins])
    median_change = top_changes[len(top_changes)//2]
else:
    pct_positive = 0
    median_change = 0

print(f"Winners: {len(winners)}")
print(f"Losers: {len(losers)}")
print(f"Market pulse: {pct_positive:.0f}% positive, median change {median_change:.1f}%")
print(f"\nTop 10 Winners:")
for w in winners:
    print(f"  {w['symbol']} ({w['name']}) +{w['change_24h']:.2f}%")
print(f"\nTop 10 Losers:")
for l in losers[:10]:
    print(f"  {l['symbol']} ({l['name']}) {l['change_24h']:.2f}%")

print(f"\nTrending (14 coins):")
trending_coins = [t['item']['symbol'].upper() for t in trending['trending_coins']]
for t in trending_coins:
    print(f"  {t}")
