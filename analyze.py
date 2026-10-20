import json, math, re

markets = json.load(open('/home/runner/work/aeon/aeon/cg_markets.json'))
trending = json.load(open('/home/runner/work/aeon/aeon/cg_trending.json'))

STABLE = {'tether','usd-coin','dai','first-digital-usd','usde','tusd','usdd','pyusd','fdusd','paxg'}

def is_stable(c):
    sym = c.get('symbol','').upper()
    name = c.get('name','')
    if c.get('id') in STABLE: return True
    if sym.startswith(('USD','EUR','GBP')): return True
    if 'stablecoin' in name.lower(): return True
    return False

filtered = [c for c in markets if not is_stable(c) and (c.get('total_volume') or 0) >= 1000000]
print("total markets:", len(markets), "after filter:", len(filtered))

def pct(c, key):
    return c.get(key) or 0

top100 = sorted(filtered, key=lambda c: -(c.get('market_cap') or 0))[:100]
pos = sum(1 for c in top100 if pct(c,'price_change_percentage_24h_in_currency') > 0)
neg = sum(1 for c in top100 if pct(c,'price_change_percentage_24h_in_currency') < 0)
median24 = sorted(pct(c,'price_change_percentage_24h_in_currency') for c in top100)[len(top100)//2]
print(f"top100 pos={pos} neg={neg} median24={median24:.2f}")

ranked = sorted(filtered, key=lambda c: -pct(c,'price_change_percentage_24h_in_currency'))
winners = ranked[:10]
losers = ranked[-10:][::-1]

def tags(c):
    t = set()
    p24 = pct(c,'price_change_percentage_24h_in_currency')
    p7 = pct(c,'price_change_percentage_7d_in_currency')
    p1 = pct(c,'price_change_percentage_1h_in_currency')
    rank = c.get('market_cap_rank') or 9999
    vol = c.get('total_volume') or 0
    mcap = c.get('market_cap') or 0
    if p24 > 15 and p7 > 25: t.add('BREAKOUT')
    if p24 > 20 and p7 < 0: t.add('FADE')
    if p24 < -10 and (vol/mcap if mcap else 0) > 0.25: t.add('CAPITULATION')
    if rank > 150 and p24 > 30: t.add('PUMP-RISK')
    if mcap < 50000000: t.add('MICROCAP')
    if rank <= 20: t.add('MAJOR')
    return t

print("\n=== WINNERS ===")
for c in winners:
    tg = sorted(tags(c))
    print(f"{c['symbol']:8s} {c['name'][:22]:22s} rank={c.get('market_cap_rank')} price={c['current_price']:.6g} 24h={pct(c,'price_change_percentage_24h_in_currency'):+.2f} 7d={pct(c,'price_change_percentage_7d_in_currency'):+.2f} 1h={pct(c,'price_change_percentage_1h_in_currency'):+.2f} vol={c['total_volume']:.0f} mcap={c['market_cap']:.0f} tags={tg}")

print("\n=== LOSERS ===")
for c in losers:
    tg = sorted(tags(c))
    print(f"{c['symbol']:8s} {c['name'][:22]:22s} rank={c.get('market_cap_rank')} price={c['current_price']:.6g} 24h={pct(c,'price_change_percentage_24h_in_currency'):+.2f} 7d={pct(c,'price_change_percentage_7d_in_currency'):+.2f} 1h={pct(c,'price_change_percentage_1h_in_currency'):+.2f} vol={c['total_volume']:.0f} mcap={c['market_cap']:.0f} tags={tg}")

print("\n=== TRENDING (top 7) ===")
tlist = trending.get('coins', [])[:7]
for item in tlist:
    it = item['item']
    d = it['data']
    print(f"{it['symbol']:8s} {it['name'][:22]:22s} rank={it.get('market_cap_rank')} price={d['price']:.6g} 24h={d['price_change_percentage_24h']['usd']:+.2f}")

trend_syms = {it['item']['symbol'].upper() for it in tlist}
win_syms = {c['symbol'].upper() for c in winners}
lose_syms = {c['symbol'].upper() for c in losers}
print("\nTrending+Up:", sorted(trend_syms & win_syms))
print("Trending+Down:", sorted(trend_syms & lose_syms))