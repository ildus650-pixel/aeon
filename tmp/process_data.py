import json

STABLECOINS = {'tether', 'usdt', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg'}
MIN_VOLUME = 1000000

data = json.load(open('/tmp/coingecko-full.json'))
tokens = []
for coin in data:
    symbol = coin['symbol'].lower()
    if symbol in STABLECOINS:
        continue
    volume = coin.get('total_volume', 0)
    if volume < MIN_VOLUME:
        continue
    change_24h = coin.get('price_change_percentage_24h')
    if change_24h is not None:
        tokens.append({
            'symbol': coin['symbol'].upper(),
            'name': coin['name'],
            'price': coin['current_price'],
            'rank': coin['market_cap_rank'],
            'change_24h': change_24h,
            'volume': volume,
            'market_cap': coin['market_cap']
        })

tokens.sort(key=lambda x: x['change_24h'], reverse=True)
winners = tokens[:10]
losers = tokens[-10:][::-1]

# Market pulse
top100 = tokens[:100]
positive = sum(1 for t in top100 if t['change_24h'] > 0)
median = tokens[49]['change_24h'] if len(tokens) >= 50 else None

pulse_sentence = f"Quiet — median move under 1% either way; {positive}/100 top coins green."

print(f'Market pulse: {positive}/100 top coins green, median change {median:.2f}%')
print()
print('Top 10 Winners:')
for i, t in enumerate(winners[:10], 1):
    vol_m = t['volume'] / 1_000_000
    mc_m = t['market_cap'] / 1_000_000_000
    print(f'{i}. {t["symbol"]} ({t["name"]}) — ${t["price"]:.2f} +{t["change_24h"]:.2f}% | ${vol_m:.1f}M | #{t["rank"]}')

print()
print('Top 10 Losers:')
for i, t in enumerate(losers[:10], 1):
    vol_m = t['volume'] / 1_000_000
    mc_m = t['market_cap'] / 1_000_000_000
    print(f'{i}. {t["symbol"]} ({t["name"]}) — ${t["price"]:.2f} {t["change_24h"]:.2f}% | ${vol_m:.1f}M | #{t["rank"]}')
