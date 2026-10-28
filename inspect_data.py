import json

with open('.coingecko-markets.json') as f:
    data = json.load(f)

print(f'Number of coins: {len(data)}')
if data:
    first = data[0]
    print('First coin keys:', sorted(first.keys()))
    print('Sample:', {k: first[k] for k in ['id','symbol','name','current_price','market_cap_rank','total_volume','market_cap','price_change_percentage_1h','price_change_percentage_24h','price_change_percentage_7d'] if k in first})
    print()

# Also inspect trending
with open('.trending.json') as f:
    trend = json.load(f)
print(f'Trending type: {type(trend)}')
if isinstance(trend, dict) and 'coins' in trend:
    print(f'Trending coins count: {len(trend["coins"])}')
    for i, c in enumerate(trend['coins'][:3]):
        item = c.get('item', c)
        print(f'  {i}: {item.get("name")} ({item.get("symbol")}) rank={item.get("market_cap_rank")} price={item.get("data",{}).get("price")} 24h%={item.get("data",{}).get("price_change_percentage_24h",{}).get("usd")}')