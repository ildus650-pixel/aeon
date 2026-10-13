import json

# Market data (from WebFetch result)
market_data = [
    {
      "name": "Bitcoin",
      "symbol": "btc",
      "current_price": 83115,
      "price_change_percentage_24h": 0.81742,
      "price_change_percentage_7d": -3.0348,
      "price_change_percentage_1h": -0.3966,
      "total_volume": 32725726894,
      "market_cap": 1670430712996,
      "market_cap_rank": 1
    },
    {
      "name": "Ethereum",
      "symbol": "eth",
      "current_price": 2503.97,
      "price_change_percentage_24h": -0.2834,
      "price_change_percentage_7d": -7.3282,
      "price_change_percentage_1h": -0.5354,
      "total_volume": 14853796670,
      "market_cap": 305809865856,
      "market_cap_rank": 2
    },
    {
      "name": "Tether",
      "symbol": "usdt",
      "current_price": 0.999243,
      "price_change_percentage_24h": 0.0144,
      "price_change_percentage_7d": -0.0725,
      "price_change_percentage_1h": -0.0077,
      "total_volume": 63239964582,
      "market_cap": 184053350378,
      "market_cap_rank": 3
    },
    {
      "name": "BNB",
      "symbol": "bnb",
      "current_price": 740.79,
      "price_change_percentage_24h": -0.44543,
      "price_change_percentage_7d": -5.4459,
      "price_change_percentage_1h": -0.547,
      "total_volume": 803574380,
      "market_cap": 98637724212,
      "market_cap_rank": 4
    },
    {
      "name": "XRP",
      "symbol": "xrp",
      "current_price": 1.37,
      "price_change_percentage_24h": 0.60405,
      "price_change_percentage_7d": -9.2039,
      "price_change_percentage_1h": -0.3339,
      "total_volume": 2217101474,
      "market_cap": 86295064109,
      "market_cap_rank": 5
    },
    {
      "name": "USDC",
      "symbol": "usdc",
      "current_price": 0.999836,
      "price_change_percentage_24h": 0.01484,
      "price_change_percentage_7d": -0.0158,
      "price_change_percentage_1h": -0.0032,
      "total_volume": 19949424663,
      "market_cap": 72639564330,
      "market_cap_rank": 6
    },
    {
      "name": "Solana",
      "symbol": "sol",
      "current_price": 107.62,
      "price_change_percentage_24h": -0.00488,
      "price_change_percentage_7d": -10.9904,
      "price_change_percentage_1h": -0.3513,
      "total_volume": 4135164385,
      "market_cap": 63410885820,
      "market_cap_rank": 7
    },
    {
      "name": "TRON",
      "symbol": "trx",
      "current_price": 0.327957,
      "price_change_percentage_24h": -0.64773,
      "price_change_percentage_7d": -2.623,
      "price_change_percentage_1h": 0.0968,
      "total_volume": 375972788,
      "market_cap": 31153812790,
      "market_cap_rank": 8
    },
    {
      "name": "Figure Heloc",
      "symbol": "figr_heloc",
      "current_price": 1.05,
      "price_change_percentage_24h": -1.31187,
      "price_change_percentage_7d": 3.3072,
      "price_change_percentage_1h": -0.1566,
      "total_volume": 12360670,
      "market_cap": 24962976556,
      "market_cap_rank": 9
    },
    {
      "name": "Zcash",
      "symbol": "zec",
      "current_price": 1202.99,
      "price_change_percentage_24h": -2.52662,
      "price_change_percentage_7d": -11.0575,
      "price_change_percentage_1h": -0.196,
      "total_volume": 1093843549,
      "market_cap": 20436141058,
      "market_cap_rank": 10
    },
    {
      "name": "Hyperliquid",
      "symbol": "hype",
      "current_price": 81.27,
      "price_change_percentage_24h": -2.60082,
      "price_change_percentage_7d": -11.6726,
      "price_change_percentage_1h": -0.0911,
      "total_volume": 940919342,
      "market_cap": 18073171464,
      "market_cap_rank": 11
    },
    {
      "name": "Dogecoin",
      "symbol": "doge",
      "current_price": 0.084129,
      "price_change_percentage_24h": -0.6685,
      "price_change_percentage_7d": -11.6386,
      "price_change_percentage_1h": -0.4969,
      "total_volume": 770436597,
      "market_cap": 13151452288,
      "market_cap_rank": 12
    },
    {
      "name": "USDS",
      "symbol": "usds",
      "current_price": 1.0,
      "price_change_percentage_24h": 0.04994,
      "price_change_percentage_7d": 0.0285,
      "price_change_percentage_1h": -0.0058,
      "total_volume": 116986643,
      "market_cap": 10340433314,
      "market_cap_rank": 13
    },
    {
      "name": "Monero",
      "symbol": "xmr",
      "current_price": 531.42,
      "price_change_percentage_24h": -0.11734,
      "price_change_percentage_7d": -5.2536,
      "price_change_percentage_1h": -0.3259,
      "total_volume": 91491488,
      "market_cap": 9999948786,
      "market_cap_rank": 14
    },
    {
      "name": "Chainlink",
      "symbol": "link",
      "current_price": 12.92,
      "price_change_percentage_24h": 0.4688,
      "price_change_percentage_7d": -7.1083,
      "price_change_percentage_1h": -0.2718,
      "total_volume": 399342988,
      "market_cap": 9911382754,
      "market_cap_rank": 15
    },
    {
      "name": "WhiteBIT Coin",
      "symbol": "wbt",
      "current_price": 81.66,
      "price_change_percentage_24h": 0.59499,
      "price_change_percentage_7d": -4.6104,
      "price_change_percentage_1h": -0.4289,
      "total_volume": 133628570,
      "market_cap": 9699628606,
      "market_cap_rank": 16
    },
    {
      "name": "Cardano",
      "symbol": "ada",
      "current_price": 0.236093,
      "price_change_percentage_24h": -2.32591,
      "price_change_percentage_7d": -13.7442,
      "price_change_percentage_1h": -0.32,
      "total_volume": 495547286,
      "market_cap": 8867933359,
      "market_cap_rank": 17
    },
    {
      "name": "LEO Token",
      "symbol": "leo",
      "current_price": 8.9,
      "price_change_percentage_24h": 0.17203,
      "price_change_percentage_7d": 0.1065,
      "price_change_percentage_1h": -0.003,
      "total_volume": 96003,
      "market_cap": 8183758611,
      "market_cap_rank": 18
    },
    {
      "name": "Rain",
      "symbol": "rain",
      "current_price": 0.00999325,
      "price_change_percentage_24h": -3.1972,
      "price_change_percentage_7d": -11.2841,
      "price_change_percentage_1h": -0.202,
      "total_volume": 18619725,
      "market_cap": 7082236910,
      "market_cap_rank": 19
    },
    {
      "name": "Stellar",
      "symbol": "xlm",
      "current_price": 0.191499,
      "price_change_percentage_24h": -2.13491,
      "price_change_percentage_7d": -10.6238,
      "price_change_percentage_1h": -0.2819,
      "total_volume": 170804164,
      "market_cap": 6715192893,
      "market_cap_rank": 20
    },
    {
      "name": "NEAR Protocol",
      "symbol": "near",
      "current_price": 5.0,
      "price_change_percentage_24h": -7.96083,
      "price_change_percentage_7d": -1.9843,
      "price_change_percentage_1h": 0.0492,
      "total_volume": 1336431161,
      "market_cap": 6549197088,
      "market_cap_rank": 21
    },
    {
      "name": "Bitcoin Cash",
      "symbol": "bch",
      "current_price": 272.65,
      "price_change_percentage_24h": -0.13029,
      "price_change_percentage_7d": -13.4718,
      "price_change_percentage_1h": -0.3764,
      "total_volume": 185487429,
      "market_cap": 5480739197,
      "market_cap_rank": 22
    }
]

# Trending data
trending = [
    {
      "name": "WISP",
      "symbol": "WISP",
      "market_cap_rank": 817,
      "current_price": 0.021965386106061507
    },
    {
      "name": "DOPE",
      "symbol": "DOPE",
      "market_cap_rank": 820,
      "current_price": 0.020681600241017024
    },
    {
      "name": "CRAWLER",
      "symbol": "CRAWLER",
      "market_cap_rank": 958,
      "current_price": 0.01603834627622648
    },
    {
      "name": "AERO",
      "symbol": "AERO",
      "market_cap_rank": 84,
      "current_price": 0.9005467712999387
    },
    {
      "name": "PRL",
      "symbol": "PRL",
      "market_cap_rank": 104,
      "current_price": 1.8289973684191714
    },
    {
      "name": "ZYLO",
      "symbol": "ZYLO",
      "market_cap_rank": 843,
      "current_price": 0.023189759949685834
    },
    {
      "name": "QTC",
      "symbol": "QTC",
      "market_cap_rank": 592,
      "current_price": 126.16826252341605
    },
    {
      "name": "PENGU",
      "symbol": "PENGU",
      "market_cap_rank": 121,
      "current_price": 0.007759096686687658
    },
    {
      "name": "STRK",
      "symbol": "STRK",
      "market_cap_rank": 102,
      "current_price": 0.0847484904204059
    },
    {
      "name": "INJ",
      "symbol": "INJ",
      "market_cap_rank": 87,
      "current_price": 8.291745413947325
    },
    {
      "name": "SUI",
      "symbol": "SUI",
      "market_cap_rank": 30,
      "current_price": 1.0467444402788764
    },
    {
      "name": "ZEC",
      "symbol": "ZEC",
      "market_cap_rank": 10,
      "current_price": 1203.4939266582455
    },
    {
      "name": "S",
      "symbol": "S",
      "market_cap_rank": 178,
      "current_price": 0.05603763782743573
    },
    {
      "name": "QNT",
      "symbol": "QNT",
      "market_cap_rank": 38,
      "current_price": 211.16428771374737
    },
    {
      "name": "LIT",
      "symbol": "LIT",
      "market_cap_rank": 85,
      "current_price": 3.3734951337512262
    }
]

# Filter stablecoins
stablecoins = {'tether', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg'}

winners = []
losers = []

for coin in market_data:
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
    top_coins = [c for c in market_data if c['symbol'].lower() not in stablecoins][:50]
    top_changes = sorted([c['price_change_percentage_24h'] for c in top_coins])
    median_change = top_changes[len(top_changes)//2]
else:
    pct_positive = 0
    median_change = 0

# Check repeat runners from prior days
repeat_runners = []
prior_logs = []

# Read logs from last 2 days
import os
logs_dir = '/home/runner/work/aeon/aeon/memory/logs'
today = '2026-10-13'
yesterday = '2026-10-12'
two_days_ago = '2026-10-11'

prior_runner_names = set()
for log_file in [yesterday, two_days_ago]:
    log_path = os.path.join(logs_dir, log_file)
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            content = f.read()
            # Extract token names from "Winners:" and "Losers:" sections
            for line in content.split('\n'):
                if 'Winners:' in line or 'Losers:' in line:
                    # Extract symbols
                    parts = line.split(':')
                    if len(parts) > 1:
                        symbols = parts[1].strip()
                        if symbols:
                            for s in symbols.split(','):
                                prior_runner_names.add(s.strip())

print(f"Winners: {len(winners)}")
print(f"Losers: {len(losers)}")
print(f"Market pulse: {pct_positive:.0f}% positive, median change {median_change:.1f}%")
print(f"\nTop 10 Winners:")
for w in winners:
    repeat = " ★ repeat" if w['symbol'] in prior_runner_names else ""
    print(f"  {w['symbol']} ({w['name']}) +{w['change_24h']:.2f}%{repeat}")
print(f"\nTop 10 Losers:")
for l in losers[:10]:
    repeat = " ★ repeat" if l['symbol'] in prior_runner_names else ""
    print(f"  {l['symbol']} ({l['name']}) {l['change_24h']:.2f}%{repeat}")

print(f"\nTrending (14 coins):")
trending_coins = [t['item']['symbol'].upper() for t in trending]
for t in trending_coins:
    repeat = " ★ repeat" if t in prior_runner_names else ""
    print(f"  {t}{repeat}")

# Compute tags
tags = []
for w in winners:
    tags.append(f"[TRENDING+UP]" if w['symbol'].lower() in [t['item']['symbol'].lower() for t in trending] else "")

# Notable signals
notable = []
for w in winners:
    if w['change_24h'] > 10:
        notable.append(f"{w['symbol']} {w['change_24h']:.1f}% 24h — strong signal")
    if w['change_24h'] > 20:
        notable.append(f"{w['symbol']} {w['change_24h']:.1f}% 24h — extreme pump")
    if w['change_7d'] > 25 and w['change_24h'] > 15:
        notable.append(f"{w['symbol']} {w['change_24h']:.1f}% / {w['change_7d']:.1f}% 7d — BREAKOUT")

for l in losers:
    if l['change_24h'] < -10:
        notable.append(f"{l['symbol']} {l['change_24h']:.1f}% 24h — capitulation")
    if l['change_7d'] < -20:
        notable.append(f"{l['symbol']} {l['change_24h']:.1f}% / {l['change_7d']:.1f}% 7d — deep drawdown")

print(f"\nNotable:")
for n in notable[:5]:
    print(f"  {n}")
