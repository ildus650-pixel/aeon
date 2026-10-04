import json

data = json.load(open('tmp/dex.json'))
pairs = [p for p in data.get('pairs', []) if p.get('chainId') == 'ethereum']
if not pairs:
    pairs = data.get('pairs', [])
    print('NO_ETH_FALLBACK')
else:
    print('ETH_CHAIN_OK')

deepest = max(pairs, key=lambda p: p.get('liquidity', {}).get('usd', 0))
p = deepest['priceUsd']
h1 = deepest.get('priceChange', {}).get('h1', 0)
h24 = deepest.get('priceChange', {}).get('h24', 0)
url = deepest.get('url', '')
liq = deepest.get('liquidity', {}).get('usd', 0)
print(f'CONTRACT={deepest["baseToken"]["address"]}')
print(f'PRICE={p}')
print(f'H1={h1}')
print(f'H24={h24}')
print(f'LIQ={liq}')
print(f'URL={url}')
print(f'SYMBOL={deepest["baseToken"]["symbol"]}')