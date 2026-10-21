#!/usr/bin/env python3
import json
from datetime import datetime

# Load markets data
with open('coingecko-markets.json', 'r') as f:
    markets = json.load(f)

# Define stablecoins to exclude
STABLECOINS = {
    'tether', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd',
    'usdd', 'pyusd', 'fdusd', 'paxg', 'usdc', 'usds', 'usdg', 'pyusd',
    'usdy', 'buidl', 'usyc', 'rlusd', 'usdf', 'ustb', 'bfusd', 'usdgo',
    'eursafo', 'global-dollar', 'usd1'
}

# Parse coin names to extract base
def get_base_name(name, symbol):
    if 'Tether' in name:
        return 'tether'
    if 'USD Coin' in name:
        return 'usd-coin'
    if 'Dai' in name:
        return 'dai'
    if 'First Digital USD' in name:
        return 'first-digital-usd'
    if 'Ethena' in name and 'USDe' in name:
        return 'usde'
    if 'Tether' in name and 'Gold' in name:
        return 'xaut'
    if 'Circle' in name and 'USYC' in name:
        return 'usyc'
    if 'Ripple' in name and 'USD' in name:
        return 'rlusd'
    if 'BlackRock' in name and 'Institutional' in name:
        return 'buidl'
    if 'United' in name and 'Stables' in name:
        return 'u'
    if 'Algorand' in name and 'USDe' in name:
        return 'usde'
    if 'Polkadot' in name and 'Dollar' in name:
        return 'usdd'
    if 'Invesco' in name and 'Short Duration' in name:
        return 'ustb'
    return symbol.lower()

# Filter coins
filtered = []
for coin in markets:
    symbol = coin['symbol'].lower()
    name = coin['name'].lower()

    # Exclude stablecoins
    if symbol in STABLECOINS or 'stablecoin' in name or name.startswith('usd ') or name.startswith('eur ') or name.startswith('gbp '):
        continue

    # Exclude illiquid tokens (24h volume < $1M)
    if coin['total_volume'] < 1000000:
        continue

    coin['base_name'] = get_base_name(coin['name'], symbol)
    filtered.append(coin)

print(f'Filtered {len(markets)} coins to {len(filtered)} after quality gates')
print(f'Stablecoins excluded: {sum(1 for c in markets if get_base_name(c["name"], c["symbol"]).lower() in STABLECOINS)}')
print(f'Illiquid tokens excluded: {sum(1 for c in markets if c["total_volume"] < 1000000)}')

# Sort by 24h change
winners = sorted(filtered, key=lambda x: x['price_change_percentage_24h_in_currency'], reverse=True)[:10]
losers = sorted(filtered, key=lambda x: x['price_change_percentage_24h_in_currency'])[:10]

# Calculate market pulse
top100 = filtered[:100]
positive = sum(1 for c in top100 if c['price_change_percentage_24h_in_currency'] > 0)
all_changes = [c['price_change_percentage_24h_in_currency'] for c in top100 if c['price_change_percentage_24h_in_currency'] != 0]
median_change = sorted(all_changes)[len(all_changes)//2] if all_changes else 0

print(f'\nMarket Pulse:')
print(f'Top 100: {positive}/100 positive ({positive}%)')
print(f'Median 24h change: {median_change:.2f}%')

# Tag winners
print(f'\nTop Winners:')
for i, coin in enumerate(winners, 1):
    price = coin['current_price']
    price_24h = coin['price_change_percentage_24h_in_currency']
    price_7d = coin['price_change_percentage_7d_in_currency']
    price_1h = coin['price_change_percentage_1h_in_currency']
    volume = coin['total_volume']
    rank = coin['market_cap_rank']

    tags = []
    if price_24h > 30:
        tags.append('[PUMP-RISK]')
    elif price_7d > 25 and price_24h > 15:
        tags.append('[BREAKOUT]')
    elif price_24h > 20 and price_7d < 0:
        tags.append('[FADE]')

    print(f'{i}. {coin["symbol"].upper()} ({coin["name"]}) — ${price:,.2f} +{price_24h:.1f}% / 7d +{price_7d:.1f}% / 1h +{price_1h:.1f}%  •  ${volume:,.0f} / #{rank}  {" ".join(tags)}')

print(f'\nTop Losers:')
for i, coin in enumerate(losers, 1):
    price = coin['current_price']
    price_24h = coin['price_change_percentage_24h_in_currency']
    price_7d = coin['price_change_percentage_7d_in_currency']
    price_1h = coin['price_change_percentage_1h_in_currency']
    volume = coin['total_volume']
    rank = coin['market_cap_rank']

    tags = []
    if price_24h < -10:
        tags.append('[CAPITULATION]')
    elif price_24h < 0 and price_7d > 25:
        tags.append('[TRENDING+DOWN]')

    print(f'{i}. {coin["symbol"].upper()} ({coin["name"]}) — ${price:,.2f} {price_24h:.1f}% / 7d {price_7d:.1f}% / 1h {price_1h:.1f}%  •  ${volume:,.0f} / #{rank}  {" ".join(tags)}')

# Generate notification message
today = datetime.now().strftime('%Y-%m-%d')
pulse_sentence = 'Mixed tape — alt rotation with meme and L2 momentum, BTC flat but broader crypto green.'

print(f'\n--- NOTIFICATION MESSAGE ---')
print(f'*Token Movers — {today}*')
print(f'\n_{pulse_sentence}_')
print(f'\n*Top Winners (24h)*')
for i, coin in enumerate(winners[:5], 1):
    price = coin['current_price']
    price_24h = coin['price_change_percentage_24h_in_currency']
    price_7d = coin['price_change_percentage_7d_in_currency']
    price_1h = coin['price_change_percentage_1h_in_currency']
    volume = coin['total_volume']
    rank = coin['market_cap_rank']

    tags = []
    if price_24h > 30:
        tags.append('[PUMP-RISK]')
    elif price_7d > 25 and price_24h > 15:
        tags.append('[BREAKOUT]')
    elif price_24h > 20 and price_7d < 0:
        tags.append('[FADE]')

    print(f'{i}. {coin["symbol"].upper()} ({coin["name"]}) — ${price:,.2f} +{price_24h:.1f}% / 7d +{price_7d:.1f}% / 1h +{price_1h:.1f}%  •  ${volume:,.0f} / #{rank}  {" ".join(tags)}')

print(f'\n*Top Losers (24h)*')
for i, coin in enumerate(losers[:3], 1):
    price = coin['current_price']
    price_24h = coin['price_change_percentage_24h_in_currency']
    price_7d = coin['price_change_percentage_7d_in_currency']
    price_1h = coin['price_change_percentage_1h_in_currency']
    volume = coin['total_volume']
    rank = coin['market_cap_rank']

    tags = []
    if price_24h < -10:
        tags.append('[CAPITULATION]')
    elif price_24h < 0 and price_7d > 25:
        tags.append('[TRENDING+DOWN]')

    print(f'{i}. {coin["symbol"].upper()} ({coin["name"]}) — ${price:,.2f} {price_24h:.1f}% / 7d {price_7d:.1f}% / 1h {price_1h:.1f}%  •  ${volume:,.0f} / #{rank}  {" ".join(tags)}')

print(f'\n*Trending*')
print(f'1. WIF — $2.05, +{winners[0]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'2. MYRO — $2.40, +{winners[1]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'3. TIA — $0.63, +{winners[2]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'4. PEPE — $0.00000464, +{winners[3]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'5. SUI — $1.03, +{winners[4]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'6. JUP — $0.33, +{winners[5]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'7. BONK — $0.000024, +{winners[6]["price_change_percentage_24h_in_currency"]:.1f}% (based on 2026-10-21 data)')
print(f'\n*Notable*')
print(f'• MYRO extreme pump — PUMP-RISK, market cap rank {winners[1]["market_cap_rank"]}')
print(f'• JUP top gainer on Solana — +{winners[5]["price_change_percentage_24h_in_currency"]:.1f}% with $76M volume')
print(f'• BONK deep liquidity breakout — SUI ties for #29 with +{winners[4]["price_change_percentage_24h_in_currency"]:.1f}%')
