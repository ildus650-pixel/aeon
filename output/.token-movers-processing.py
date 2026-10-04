#!/usr/bin/env python3
import json
from decimal import Decimal, getcontext

getcontext().prec = 10

# Parse the WebFetch JSON responses
markets_data = """[
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "current_price_usd": 85331,
    "price_change_percentage_1h_in_currency": 0.0224,
    "price_change_percentage_24h_in_currency": 0.56919,
    "price_change_percentage_7d_in_currency": 0.2976,
    "total_volume": 14816244820,
    "market_cap": 1714564779662,
    "market_cap_rank": 1
  },
  {
    "id": "ethereum",
    "symbol": "eth",
    "name": "Ethereum",
    "current_price_usd": 2699.32,
    "price_change_percentage_1h_in_currency": -0.0692,
    "price_change_percentage_24h_in_currency": 0.67447,
    "price_change_percentage_7d_in_currency": -0.4464,
    "total_volume": 4817362066,
    "market_cap": 329600588391,
    "market_cap_rank": 2
  },
  {
    "id": "solana",
    "symbol": "sol",
    "name": "Solana",
    "current_price_usd": 121.65,
    "price_change_percentage_1h_in_currency": 0.0684,
    "price_change_percentage_24h_in_currency": 1.66287,
    "price_change_percentage_7d_in_currency": -1.1341,
    "total_volume": 1874430804,
    "market_cap": 71567521978,
    "market_cap_rank": 7
  },
  {
    "id": "near",
    "symbol": "near",
    "name": "NEAR Protocol",
    "current_price_usd": 4.82,
    "price_change_percentage_1h_in_currency": -0.3106,
    "price_change_percentage_24h_in_currency": 3.77426,
    "price_change_percentage_7d_in_currency": -7.4367,
    "total_volume": 517163455,
    "market_cap": 6305391443,
    "market_cap_rank": 22
  },
  {
    "id": "polkadot",
    "symbol": "dot",
    "name": "Polkadot",
    "current_price_usd": 1.2,
    "price_change_percentage_1h_in_currency": 0.3662,
    "price_change_percentage_24h_in_currency": -0.68156,
    "price_change_percentage_7d_in_currency": -3.8318,
    "total_volume": 99744730,
    "market_cap": 2043812510,
    "market_cap_rank": 54
  },
  {
    "id": "cardano",
    "symbol": "ada",
    "name": "Cardano",
    "current_price_usd": 0.2479,
    "price_change_percentage_1h_in_currency": 0.3536,
    "price_change_percentage_24h_in_currency": 1.22095,
    "price_change_percentage_7d_in_currency": -4.2016,
    "total_volume": 275453600,
    "market_cap": 9307001440,
    "market_cap_rank": 17
  },
  {
    "id": "avalanche-2",
    "symbol": "avax",
    "name": "Avalanche",
    "current_price_usd": 11.09,
    "price_change_percentage_1h_in_currency": 0.6762,
    "price_change_percentage_24h_in_currency": 0.11509,
    "price_change_percentage_7d_in_currency": 0.3903,
    "total_volume": 205007684,
    "market_cap": 4915474826,
    "market_cap_rank": 27
  },
  {
    "id": "matic-network",
    "symbol": "matic",
    "name": "Polygon",
    "current_price_usd": 0.10847,
    "price_change_percentage_1h_in_currency": 0.2116,
    "price_change_percentage_24h_in_currency": -0.29754,
    "price_change_percentage_7d_in_currency": -9.4258,
    "total_volume": 45338720,
    "market_cap": 1152581124,
    "market_cap_rank": 75
  },
  {
    "id": "chainlink",
    "symbol": "link",
    "name": "Chainlink",
    "current_price_usd": 14.13,
    "price_change_percentage_1h_in_currency": 0.4928,
    "price_change_percentage_24h_in_currency": 2.1956,
    "price_change_percentage_7d_in_currency": -0.2285,
    "total_volume": 241074097,
    "market_cap": 10570426230,
    "market_cap_rank": 13
  },
  {
    "id": "uniswap",
    "symbol": "uni",
    "name": "Uniswap",
    "current_price_usd": 9.02,
    "price_change_percentage_1h_in_currency": 0.2182,
    "price_change_percentage_24h_in_currency": -0.0866,
    "price_change_percentage_7d_in_currency": -8.4183,
    "total_volume": 288080559,
    "market_cap": 5638752459,
    "market_cap_rank": 23
  },
  {
    "id": "tron",
    "symbol": "trx",
    "name": "TRON",
    "current_price_usd": 0.335735,
    "price_change_percentage_1h_in_currency": 0.0652,
    "price_change_percentage_24h_in_currency": -0.28867,
    "price_change_percentage_7d_in_currency": 0.5923,
    "total_volume": 199728562,
    "market_cap": 31885432042,
    "market_cap_rank": 8
  },
  {
    "id": "stellar",
    "symbol": "xlm",
    "name": "Stellar",
    "current_price_usd": 0.21808,
    "price_change_percentage_1h_in_currency": 0.5825,
    "price_change_percentage_24h_in_currency": 1.81345,
    "price_change_percentage_7d_in_currency": 0.1434,
    "total_volume": 98824373,
    "market_cap": 7644603305,
    "market_cap_rank": 20
  },
  {
    "id": "dogecoin",
    "symbol": "doge",
    "name": "Dogecoin",
    "current_price_usd": 0.094311,
    "price_change_percentage_1h_in_currency": 0.4608,
    "price_change_percentage_24h_in_currency": 1.2686,
    "price_change_percentage_7d_in_currency": -3.9303,
    "total_volume": 397286227,
    "market_cap": 14729239977,
    "market_cap_rank": 12
  },
  {
    "id": "litecoin",
    "symbol": "ltc",
    "name": "Litecoin",
    "current_price_usd": 71.79,
    "price_change_percentage_1h_in_currency": 1.5308,
    "price_change_percentage_24h_in_currency": 3.08239,
    "price_change_percentage_7d_in_currency": 1.2213,
    "total_volume": 301238936,
    "market_cap": 5573840342,
    "market_cap_rank": 24
  },
  {
    "id": "internet-computer",
    "symbol": "icp",
    "name": "Internet Computer",
    "current_price_usd": 3.37,
    "price_change_percentage_1h_in_currency": 1.0349,
    "price_change_percentage_24h_in_currency": 2.54611,
    "price_change_percentage_7d_in_currency": 7.119,
    "total_volume": 72611178,
    "market_cap": 1876583348,
    "market_cap_rank": 57
  },
  {
    "id": "render",
    "symbol": "render",
    "name": "Render",
    "current_price_usd": 1.97,
    "price_change_percentage_1h_in_currency": 0.9817,
    "price_change_percentage_24h_in_currency": -2.32274,
    "price_change_percentage_7d_in_currency": -3.1561,
    "total_volume": 45510564,
    "market_cap": 1022002811,
    "market_cap_rank": 79
  },
  {
    "id": "cosmos",
    "symbol": "atom",
    "name": "Cosmos Hub",
    "current_price_usd": 1.77,
    "price_change_percentage_1h_in_currency": 1.0238,
    "price_change_percentage_24h_in_currency": 2.76298,
    "price_change_percentage_7d_in_currency": -3.0001,
    "total_volume": 53009985,
    "market_cap": 946162445,
    "market_cap_rank": 82
  },
  {
    "id": "aptos",
    "symbol": "apt",
    "name": "Aptos",
    "current_price_usd": 0.808635,
    "price_change_percentage_1h_in_currency": 1.3973,
    "price_change_percentage_24h_in_currency": -0.4624,
    "price_change_percentage_7d_in_currency": -4.4796,
    "total_volume": 39388617,
    "market_cap": 704411687,
    "market_cap_rank": 97
  },
  {
    "id": "aave",
    "symbol": "aave",
    "name": "Aave",
    "current_price_usd": 178.81,
    "price_change_percentage_1h_in_currency": 0.071,
    "price_change_percentage_24h_in_currency": -0.24491,
    "price_change_percentage_7d_in_currency": 15.6808,
    "total_volume": 237482730,
    "market_cap": 2759951057,
    "market_cap_rank": 42
  },
  {
    "id": "injective-protocol",
    "symbol": "inj",
    "name": "Injective",
    "current_price_usd": 7.52,
    "price_change_percentage_1h_in_currency": 0.3861,
    "price_change_percentage_24h_in_currency": -2.22916,
    "price_change_percentage_7d_in_currency": -2.5204,
    "total_volume": 62301019,
    "market_cap": 751904068,
    "market_cap_rank": 91
  },
  {
    "id": "stacks",
    "symbol": "stx",
    "name": "Stacks",
    "current_price_usd": 0.39178,
    "price_change_percentage_1h_in_currency": 0.5376,
    "price_change_percentage_24h_in_currency": 3.27202,
    "price_change_percentage_7d_in_currency": 12.46,
    "total_volume": 35555437,
    "market_cap": 733356348,
    "market_cap_rank": 94
  },
  {
    "id": "blockstack",
    "symbol": "stx",
    "name": "Stacks",
    "current_price_usd": 0.39178,
    "price_change_percentage_1h_in_currency": 0.5376,
    "price_change_percentage_24h_in_currency": 3.27202,
    "price_change_percentage_7d_in_currency": 12.46,
    "total_volume": 35555437,
    "market_cap": 733356348,
    "market_cap_rank": 94
  },
  {
    "id": "ether-fi",
    "symbol": "ethfi",
    "name": "Ether.fi",
    "current_price_usd": 0.750605,
    "price_change_percentage_1h_in_currency": 1.4708,
    "price_change_percentage_24h_in_currency": 7.1052,
    "price_change_percentage_7d_in_currency": 3.9843,
    "total_volume": 35789137,
    "market_cap": 723711329,
    "market_cap_rank": 95
  }
]"""

trending_data = """{
  "trending_coins": [
    {
      "name": "Super Iguana",
      "symbol": "SI",
      "market_cap_rank": 953,
      "current_price": 0.01759308310333197,
      "24h_price_change_percentage": 45.34398897573468
    },
    {
      "name": "Fetch.ai",
      "symbol": "FET",
      "market_cap_rank": 110,
      "current_price": 0.24718986613352353,
      "24h_price_change_percentage": 7.877745252826639
    },
    {
      "name": "Starknet",
      "symbol": "STRK",
      "market_cap_rank": 125,
      "current_price": 0.05709290249522787,
      "24h_price_change_percentage": 15.690382052260423
    },
    {
      "name": "Pump.fun",
      "symbol": "PUMP",
      "market_cap_rank": 40,
      "current_price": 0.00646309068892092,
      "24h_price_change_percentage": 12.246684698906286
    },
    {
      "name": "Quant",
      "symbol": "QNT",
      "market_cap_rank": 33,
      "current_price": 257.9944973810481,
      "24h_price_change_percentage": 3.5335756721862674
    },
    {
      "name": "Sui",
      "symbol": "SUI",
      "market_cap_rank": 25,
      "current_price": 1.2567018417788363,
      "24h_price_change_percentage": 6.846105498778653
    },
    {
      "name": "Pudgy Penguins",
      "symbol": "PENGU",
      "market_cap_rank": 106,
      "current_price": 0.009232130087802378,
      "24h_price_change_percentage": 0.0900997094956827
    },
    {
      "name": "NEAR Protocol",
      "symbol": "NEAR",
      "market_cap_rank": 22,
      "current_price": 4.820466234849891,
      "24h_price_change_percentage": 3.8212603776165683
    },
    {
      "name": "Solana",
      "symbol": "SOL",
      "market_cap_rank": 7,
      "current_price": 121.64524768357711,
      "24h_price_change_percentage": 1.658523222540069
    },
    {
      "name": "Bittensor",
      "symbol": "TAO",
      "market_cap_rank": 34,
      "current_price": 303.6848292351036,
      "24h_price_change_percentage": 3.966546857487806
    },
    {
      "name": "Grass",
      "symbol": "GRASS",
      "market_cap_rank": 120,
      "current_price": 0.6881103952052038,
      "24h_price_change_percentage": -7.67672033552014
    },
    {
      "name": "Canton",
      "symbol": "CC",
      "market_cap_rank": 26,
      "current_price": 0.1267338853266777,
      "24h_price_change_percentage": 3.728450717900534
    },
    {
      "name": "Aerodrome Finance",
      "symbol": "AERO",
      "market_cap_rank": 85,
      "current_price": 0.8586382514604504,
      "24h_price_change_percentage": 8.080819843610856
    }
  ]
}"""

markets = json.loads(markets_data)
trending = json.loads(trending_data)["trending_coins"]

# Stablecoins to exclude (case-insensitive symbol check, plus known names)
stablecoins = {
    "tether", "usdt", "usd-coin", "usdc", "usde", "dai", "usds", "usdg", "usd1", "usdy",
    "buidl", "pyusd", "fdusd", "usdg", "usdgo", "usd1", "usdy", "bfusd", "usdgo", "gho",
    "ousd", "eutbl", "jaaa", "ustb", "xaut", "usds", "usdd", "global-dollar", "usdg",
    "paypal-usd", " united-stables", "usds", "usdd", "bfusd", "usdgo", "gho", "ousd",
    "eutbl", "jaaa", "ustb", "hashnote-usyc"
}

# Filter and convert to dicts
tokens = []
for coin in markets:
    symbol = coin["symbol"].lower()
    name = coin["name"].lower()

    # Skip stablecoins
    if symbol in stablecoins:
        continue
    if name in stablecoins:
        continue
    if symbol.startswith("usd") or symbol.startswith("eur") or symbol.startswith("gbp"):
        continue
    if "stablecoin" in name:
        continue

    # Skip illiquid tokens (< $1M volume)
    volume = Decimal(str(coin["total_volume"]))
    if volume < Decimal("1000000"):
        continue

    tokens.append({
        "id": coin["id"],
        "symbol": coin["symbol"],
        "name": coin["name"],
        "price": float(Decimal(str(coin["current_price_usd"]))),
        "change_1h": float(Decimal(str(coin["price_change_percentage_1h_in_currency"]))),
        "change_24h": float(Decimal(str(coin["price_change_percentage_24h_in_currency"]))),
        "change_7d": float(Decimal(str(coin["price_change_percentage_7d_in_currency"]))),
        "volume": float(volume),
        "market_cap": float(Decimal(str(coin["market_cap"]))),
        "rank": coin["market_cap_rank"]
    })

# Sort by 24h change
tokens_sorted = sorted(tokens, key=lambda x: x["change_24h"], reverse=True)

# Top 10 winners and losers
winners = tokens_sorted[:10]
losers = tokens_sorted[-10:]

# Top 7 trending
trending_coins = trending[:7]

# Market pulse: count green/red among top 100 by mcap
green_count = 0
total_in_top100 = 0
for coin in markets:
    symbol = coin["symbol"].lower()
    name = coin["name"].lower()

    # Same filters
    if symbol in stablecoins or name in stablecoins or symbol.startswith("usd") or symbol.startswith("eur") or symbol.startswith("gbp") or "stablecoin" in name:
        continue
    if Decimal(str(coin["total_volume"])) < Decimal("1000000"):
        continue
    if coin["market_cap_rank"] > 100:
        continue
    total_in_top100 += 1
    if coin["price_change_percentage_24h_in_currency"] > 0:
        green_count += 1

median_change = 0
if len(tokens_sorted) >= 50:
    median_change = tokens_sorted[49]["change_24h"]

# Calculate percentages
green_pct = green_count / total_in_top100 if total_in_top100 > 0 else 0

# Build result
result = {
    "tokens": tokens_sorted,
    "winners": winners,
    "losers": losers,
    "trending": trending_coins,
    "pulse": {
        "green_count": green_count,
        "green_pct": float(green_pct),
        "median_change": float(median_change)
    },
    "market_cap_rank_limit": 100
}

print(json.dumps(result, indent=2))
