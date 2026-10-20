import json, urllib.request, time

ids = {'bitway':'bitway','stacks':'blockstack','near':'near','aioz':'aioz-network','starknet':'starknet','nubatoken':'non-playable-coin','the-sandbox':'the-sandbox','arbitrum':'arbitrum','ultima':'ultima','crclb':'circle-internet-group-bstock','memecore':'memecore','beam':'beam-2','geodnet':'geodnet','celestia':'celestia','curve-dao-token':'curve-dao-token','theta-token':'theta-token','collector-crypt':'collector-crypt','basic-attention-token':'basic-attention-token','worldcoin-wld':'worldcoin-wld','vaulta':'vaulta','stable-2':'stable-2','bedrock-token':'bedrock-token'}

out = {}
for sym, cid in ids.items():
    u = f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=7&interval=daily"
    try:
        req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
        d = json.loads(urllib.request.urlopen(req, timeout=30).read())
        vols = [v for _, v in d.get('total_volumes', [])]
        if len(vols) >= 2:
            # last entry = today's partial 24h window; prior 7 full days
            prior = vols[:-1]
            avg = sum(prior) / len(prior)
            out[sym] = {'today_vol': vols[-1], 'avg7': avg, 'ratio': (vols[-1]/avg if avg else 0), 'days': len(prior)}
    except Exception as e:
        out[sym] = {'error': str(e)}
    time.sleep(0.6)

for k, v in out.items():
    if 'error' in v:
        print(f"{k:8s} ERROR {v['error'][:60]}")
    else:
        print(f"{k:8s} today=${v['today_vol']:>14,.0f} avg7d=${v['avg7']:>14,.0f} ratio={v['ratio']:.2f}x")
