import json
import subprocess
import sys

# Fetch data
try:
    result = subprocess.run(
        ['curl', '-s', 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h,24h,7d'],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print("curl failed", file=sys.stderr)
        sys.exit(1)
    coins = json.loads(result.stdout)
except Exception as e:
    print(f"Error parsing: {e}", file=sys.stderr)
    sys.exit(1)

# Yesterday's movers
yesterday_winners = {'SIF', 'fluid', 'orca', 'shx', 'night', 'zro', 'cards', 'lit', 'fil', 'sent'}
yesterday_trending = {'SIF', 'EDEL', 'ONDO', 'PUMP', 'LIT', 'PENGU', 'PONS'}

stablecoins = {'tether', 'usd-coin', 'dai', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg', 'usdc', 'usds', 'usdg', 'usyc', 'buidl', 'pyusd', 'usd1', 'usdf', 'bfusd', 'usdgo'}

# Filter
filtered = []
for coin in coins:
    sym = coin['symbol'].lower()
    if sym in stablecoins:
        continue
    if coin['total_volume'] < 1000000:
        continue
    filtered.append({
        'name': coin['name'],
        'symbol': coin['symbol'],
        'rank': coin['market_cap_rank'],
        'price': coin['current_price'],
        'change_24h': coin['price_change_percentage_24h_in_currency'],
        'change_7d': coin.get('price_change_percentage_7d_in_currency', 0),
        'change_1h': coin['price_change_percentage_1h_in_currency'],
        'volume': coin['total_volume'],
        'mcap': coin['market_cap']
    })

# Sort by 24h change
filtered.sort(key=lambda x: x['change_24h'], reverse=True)

# Get unique prices for market pulse
positive_count = sum(1 for c in filtered if c['change_24h'] > 0)
top50 = filtered[:50]
top50_median = sorted([c['change_24h'] for c in top50])[25]

# Get winners/losers excluding yesterday
winners = []
losers = []

for coin in filtered:
    sym = coin['symbol'].lower()
    if sym in yesterday_winners or coin['name'].lower() in yesterday_winners:
        continue
    if len(winners) < 10:
        winners.append(coin)
    elif coin['change_24h'] > winners[-1]['change_24h']:
        winners.append(coin)
        winners.sort(key=lambda x: x['change_24h'], reverse=True)
        winners = winners[:10]

losers = []
for coin in filtered:
    sym = coin['symbol'].lower()
    if sym in yesterday_winners or coin['name'].lower() in yesterday_winners:
        continue
    if len(losers) < 10:
        losers.append(coin)
    elif coin['change_24h'] < losers[-1]['change_24h']:
        losers.append(coin)
        losers.sort(key=lambda x: x['change_24h'])
        losers = losers[:10]

# Trending
try:
    result = subprocess.run(
        ['curl', '-s', 'https://api.coingecko.com/api/v3/search/trending'],
        capture_output=True, text=True, timeout=30
    )
    trending = json.loads(result.stdout)
    trending_coins = [item['item']['symbol'].upper() for item in trending.get('coins', [])[:7]]
except:
    trending_coins = []

# Tags
for coin in winners + losers:
    sym = coin['symbol']
    mcap_rank = coin['rank']
    chg_24h = coin['change_24h']
    chg_7d = coin['change_7d']
    vol = coin['volume']
    mcap = coin['mcap']

    tags = []
    if sym in yesterday_trending:
        tags.append('TRENDING+UP')

    if chg_24h > 15 and chg_7d > 25:
        tags.append('BREAKOUT')
    elif chg_24h > 20 and chg_7d < 0:
        tags.append('FADE')
    elif chg_24h < -10 and vol > 3 * (mcap * 0.25):
        tags.append('CAPITULATION')
    elif mcap_rank > 150 and chg_24h > 30:
        tags.append('PUMP-RISK')
    elif mcap < 50000000:
        tags.append('MICROCAP')
    elif mcap_rank <= 20:
        tags.append('MAJOR')

    coin['tags'] = tags

print(json.dumps({
    'pulse': f'{positive_count}/{len(filtered)} top coins are green, median {top50_median:+.2f}%',
    'winners': winners[:10],
    'losers': losers[:10],
    'trending': trending_coins[:7]
}, indent=2))
