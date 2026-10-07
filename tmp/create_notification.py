import json

# Movers data from earlier
winners_data = [
    ("ZEC", "Zcash", 1366.22, 10, 1.25114, 693851269),
    ("RAIN", "Rain", 0.01155067, 18, 1.0392, 13847282),
    ("LINK", "Chainlink", 13.97, 14, 0.92438, 264125558),
    ("FIGR_HELOC", "Figure Heloc", 1.038, 9, 0.52601, 45693242),
    ("XMR", "Monero", 559.54, 13, -0.19935, 107800702),
    ("TRX", "TRON", 0.335408, 8, -0.23737, 291955554),
    ("SOL", "Solana", 120.51, 7, -0.30912, 2447497173),
    ("BTC", "Bitcoin", 85498, 1, -0.36635, 26728052661),
    ("WBT", "WhiteBIT Coin", 85.38, 15, -0.41153, 68981647),
    ("ETH", "Ethereum", 2696.76, 2, -0.60397, 10977860379)
]

losers_data = [
    ("HYPE", "Hyperliquid", 92.17, 11, -2.4687, 928815253),
    ("XLM", "Stellar", 0.21195, 20, -1.84325, 125955567),
    ("DOGE", "Dogecoin", 0.093724, 12, -1.5964, 735916661),
    ("BNB", "BNB", 778.42, 4, -1.02056, 685922267),
    ("ADA", "Cardano", 0.267095, 17, -0.95054, 667462518),
    ("XRP", "XRP", 1.5, 5, -0.63484, 1509595024),
    ("ETH", "Ethereum", 2696.76, 2, -0.60397, 10977860379),
    ("WBT", "WhiteBIT Coin", 85.38, 15, -0.41153, 68981647),
    ("BTC", "Bitcoin", 85498, 1, -0.36635, 26728052661),
    ("SOL", "Solana", 120.51, 7, -0.30912, 2447497173)
]

# Apply tags
tags = []
for sym, name, price, rank, change, vol in winners_data + losers_data:
    tag = ""
    if change > 0:
        # Check for TRENDING+UP (trending and top winner)
        tag = "[TRENDING+UP]" if sym in ["ZEC", "RAIN", "LINK"] else ""
        # Check for BREAKOUT
        if change > 15 and change < 25:
            tag = "[BREAKOUT]"
        # Check for PUMP-RISK
        if rank > 150 and change > 30:
            tag = "[PUMP-RISK]"
    else:
        # Losers
        tag = "[TRENDING+DOWN]" if sym in ["HYPE", "XLM", "DOGE"] else ""

    vol_m = vol / 1_000_000
    tags.append(f"{sym} (Name: {name}) — ${price:.2f} {change:+.2f}% | ${vol_m:.1f}M | #{rank} {tag}")

today = "2026-10-07"
pulse = "Broad risk-on — 4/100 top coins are green, median +0.0%"

print(f"*Token Movers — {today}*")
print()
print(f"_{pulse}_")
print()
print("*Top Winners (24h)*")
for t in winners_data[:10]:
    sym, name, price, rank, change, vol = t
    vol_m = vol / 1_000_000
    print(f"1. {sym} ({name}) — ${price:.2f} {change:+.2f}% | ${vol_m:.1f}M | #{rank}")

print()
print("*Top Losers (24h)*")
for t in losers_data[:10]:
    sym, name, price, rank, change, vol = t
    vol_m = vol / 1_000_000
    print(f"1. {sym} ({name}) — ${price:.2f} {change:+.2f}% | ${vol_m:.1f}M | #{rank}")
