import json

STABLECOINS = {'tether', 'usdt', 'usd', 'usd-coin', 'dai', 'usde', 'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg', 'usdc', 'usds', 'usdf'}
MIN_VOLUME = 1000000

# The data from WebFetch
coins = [
  {"symbol": "btc", "name": "Bitcoin", "price": 85498, "rank": 1, "change_24h": -0.36635, "volume": 26728052661},
  {"symbol": "eth", "name": "Ethereum", "price": 2696.76, "rank": 2, "change_24h": -0.60397, "volume": 10977860379},
  {"symbol": "usdt", "name": "Tether", "price": 0.99994, "rank": 3, "change_24h": 0.00094, "volume": 50489774587},
  {"symbol": "bnb", "name": "BNB", "price": 778.42, "rank": 4, "change_24h": -1.02056, "volume": 685922267},
  {"symbol": "xrp", "name": "XRP", "price": 1.5, "rank": 5, "change_24h": -0.63484, "volume": 1509595024},
  {"symbol": "usdc", "name": "USDC", "price": 0.999942, "rank": 6, "change_24h": -0.00155, "volume": 15673828667},
  {"symbol": "sol", "name": "Solana", "price": 120.51, "rank": 7, "change_24h": -0.30912, "volume": 2447497173},
  {"symbol": "trx", "name": "TRON", "price": 0.335408, "rank": 8, "change_24h": -0.23737, "volume": 291955554},
  {"symbol": "figr_heloc", "name": "Figure Heloc", "price": 1.038, "rank": 9, "change_24h": 0.52601, "volume": 45693242},
  {"symbol": "zec", "name": "Zcash", "price": 1366.22, "rank": 10, "change_24h": 1.25114, "volume": 693851269},
  {"symbol": "hype", "name": "Hyperliquid", "price": 92.17, "rank": 11, "change_24h": -2.4687, "volume": 928815253},
  {"symbol": "doge", "name": "Dogecoin", "price": 0.093724, "rank": 12, "change_24h": -1.5964, "volume": 735916661},
  {"symbol": "xmr", "name": "Monero", "price": 559.54, "rank": 13, "change_24h": -0.19935, "volume": 107800702},
  {"symbol": "link", "name": "Chainlink", "price": 13.97, "rank": 14, "change_24h": 0.92438, "volume": 264125558},
  {"symbol": "wbt", "name": "WhiteBIT Coin", "price": 85.38, "rank": 15, "change_24h": -0.41153, "volume": 68981647},
  {"symbol": "usds", "name": "USDS", "price": 0.999782, "rank": 16, "change_24h": 0.00113, "volume": 163708305},
  {"symbol": "ada", "name": "Cardano", "price": 0.267095, "rank": 17, "change_24h": -0.95054, "volume": 667462518},
  {"symbol": "rain", "name": "Rain", "price": 0.01155067, "rank": 18, "change_24h": 1.0392, "volume": 13847282},
  {"symbol": "leo", "name": "LEO Token", "price": 8.9, "rank": 19, "change_24h": -0.23618, "volume": 151872},
  {"symbol": "xlm", "name": "Stellar", "price": 0.21195, "rank": 20, "change_24h": -1.84325, "volume": 125955567}
]

tokens = []
for coin in coins:
    if coin['symbol'].lower() in STABLECOINS:
        continue
    if coin['volume'] < MIN_VOLUME:
        continue
    if coin['change_24h'] is not None:
        tokens.append({
            'symbol': coin['symbol'].upper(),
            'name': coin['name'],
            'price': coin['price'],
            'rank': coin['rank'],
            'change_24h': coin['change_24h'],
            'volume': coin['volume']
        })

tokens.sort(key=lambda x: x['change_24h'], reverse=True)
winners = tokens[:10]
losers = tokens[-10:][::-1]

# Market pulse
top100 = tokens[:100]
positive = sum(1 for t in top100 if t['change_24h'] > 0)
median = tokens[49]['change_24h'] if len(tokens) >= 50 else None

pulse_sentence = f"Broad risk-on — {positive}/100 top coins are green, median +0.0%"

print("MARKET PULSE:")
print(pulse_sentence)
print()
print("TOP WINNERS (24h):")
for i, t in enumerate(winners[:10], 1):
    vol_m = t['volume'] / 1_000_000
    print(f"{i}. {t['symbol']} ({t['name']}) — ${t['price']:.2f} +{t['change_24h']:.2f}% | ${vol_m:.1f}M | #{t['rank']}")

print()
print("TOP LOSERS (24h):")
for i, t in enumerate(losers[:10], 1):
    vol_m = t['volume'] / 1_000_000
    print(f"{i}. {t['symbol']} ({t['name']}) — ${t['price']:.2f} {t['change_24h']:.2f}% | ${vol_m:.1f}M | #{t['rank']}")
