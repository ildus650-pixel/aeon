import json, subprocess, time

ids = {'the-sandbox':'the-sandbox','arbitrum':'arbitrum','ultima':'ultima','crclb':'circle-internet-group-bstock','memecore':'memecore','beam':'beam-2','geodnet':'geodnet','celestia':'celestia','curve-dao-token':'curve-dao-token','theta-token':'theta-token','collector-crypt':'collector-crypt','basic-attention-token':'basic-attention-token','worldcoin-wld':'worldcoin-wld','vaulta':'vaulta','stable-2':'stable-2','bedrock-token':'bedrock-token'}

for sym, cid in ids.items():
    u = f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=7&interval=daily"
    raw = subprocess.run(['./secretcurl','-s',u], capture_output=True, text=True).stdout
    try:
        d = json.loads(raw)
        vols = [v for _, v in d.get('total_volumes', [])]
        if len(vols) >= 2:
            prior = vols[:-1]
            avg = sum(prior)/len(prior)
            print(f"{sym:8s} today=${vols[-1]:>14,.0f} avg7d=${avg:>14,.0f} ratio={vols[-1]/avg:.2f}x")
        else:
            print(f"{sym:8s} insufficient data: {raw[:120]}")
    except Exception as e:
        print(f"{sym:8s} ERR {raw[:100]}")
    time.sleep(1.2)
