#!/usr/bin/env python3
import json
import requests

url = "https://api.coingecko.com/api/v3/search/trending"

try:
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        with open('/home/runner/work/aeon/aeon/.trending.json', 'w') as f:
            json.dump(resp.json(), f, indent=2)
        print("trending fetched")
    else:
        print(f"trending: HTTP {resp.status_code}")
except Exception as e:
    print(f"trending: ERROR - {e}")
