#!/usr/bin/env python3
import json
import requests

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h,24h,7d"

try:
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        with open('/home/runner/work/aeon/aeon/.coingecko-markets.json', 'w') as f:
            json.dump(resp.json(), f, indent=2)
        print(f"markets fetched: {len(resp.json())} coins")
    else:
        print(f"markets: HTTP {resp.status_code}")
except Exception as e:
    print(f"markets: ERROR - {e}")
