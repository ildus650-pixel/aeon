# Debug movers logic
import json

# Market data (simplified)
market_data = [
    {"name": "Bitcoin", "symbol": "btc", "current_price": 83115, "price_change_percentage_24h": 0.81742, "market_cap_rank": 1},
    {"name": "Ethereum", "symbol": "eth", "current_price": 2503.97, "price_change_percentage_24h": -0.2834, "market_cap_rank": 2},
    {"name": "Tether", "symbol": "usdt", "current_price": 0.999243, "price_change_percentage_24h": 0.0144, "market_cap_rank": 3},
]

stablecoins = {'tether'}

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
            'change_24h': change_24h
        })
    else:
        losers.append({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'rank': coin['market_cap_rank'],
            'price': coin['current_price'],
            'change_24h': change_24h
        })

print("Winners:", winners)
print("Losers:", losers)
