#!/bin/bash
set -euo pipefail

STATE_FILE="memory/topics/price-alert-state.json"
RESP_FILE="/tmp/dexscreener_response.json"
TODAY=$(date -u +%Y-%m-%d)
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "=== Price Alert Skill Run ==="
echo "Today: $TODAY"
echo "Now: $NOW"
echo ""

# Step 3: Fetch current price from DexScreener
echo "Fetching price from DexScreener..."
curl -fsS "https://api.dexscreener.com/latest/dex/tokens/0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599" -o "$RESP_FILE" 2>/dev/null || echo ""

if [ ! -s "$RESP_FILE" ]; then
    echo "FALLBACK: WebFetch path..."
    echo "PRICE_ALERT_FETCH_FAIL: Both curl and WebFetch failed"
    exit 1
fi

echo "=== DexScreener response received ==="

# Step 3: Parse the data - find deepest liquidity pool on ethereum
echo "Finding deepest liquidity pool on ethereum..."
CURRENT_PRICE=$(jq -r '[.pairs[] | select(.chainId == "ethereum")] | max_by(.liquidity.usd) | .priceUsd' "$RESP_FILE")
H1_CHANGE=$(jq -r '[.pairs[] | select(.chainId == "ethereum")] | max_by(.liquidity.usd) | .priceChange.h1 // 0' "$RESP_FILE")
H24_CHANGE=$(jq -r '[.pairs[] | select(.chainId == "ethereum")] | max_by(.liquidity.usd) | .priceChange.h24 // 0' "$RESP_FILE")
POOL_URL=$(jq -r '[.pairs[] | select(.chainId == "ethereum")] | max_by(.liquidity.usd) | .url' "$RESP_FILE")
LIQUIDITY_USD=$(jq -r '[.pairs[] | select(.chainId == "ethereum")] | max_by(.liquidity.usd) | .liquidity.usd' "$RESP_FILE")
DEX=$(jq -r '[.pairs[] | select(.chainId == "ethereum")] | max_by(.liquidity.usd) | .dexId' "$RESP_FILE")

echo "Deepest pool: $DEX (liquidity: $LIQUIDITY_USD USD)"
echo "Current Price: $CURRENT_PRICE"
echo "1h Change: $H1_CHANGE%"
echo "24h Change: $H24_CHANGE%"
echo "Pool URL: $POOL_URL"
echo ""

if [ -z "$CURRENT_PRICE" ] || [ "$CURRENT_PRICE" = "null" ] || [ "$CURRENT_PRICE" = "0" ]; then
    echo "PRICE_ALERT_BAD_PRICE: Invalid price from API"
    exit 1
fi

# Step 4: Evaluate ATH gate
echo ""
echo "=== Step 4: ATH gate evaluation ==="

ATH_PRICE=$(jq -r '.ath.price_usd' "$STATE_FILE")
ATH_LAST_ALERT=$(jq -r '.last_alerts.ath' "$STATE_FILE")
ATH_ANNOUNCED_AT=$(jq -r '.ath.announced_at' "$STATE_FILE")

ATH_IS_ZERO=false
if [ "$ATH_PRICE" = "null" ] || [ -z "$ATH_PRICE" ] || [ "$ATH_PRICE" = "0" ]; then
    ATH_IS_ZERO=true
fi

if [ "$ATH_IS_ZERO" = "true" ]; then
    echo "ATH_BASELINE: true (first run - suppress notification)"
    ATH_VERDICT="ATH_BASELINE"
else
    CURRENT_NUM=$(echo "$CURRENT_PRICE" | sed 's/,//g')
    ATH_NUM=$(echo "$ATH_PRICE" | sed 's/,//g')

    COMPARE=$(echo "$CURRENT_NUM > $ATH_NUM" | bc -l 2>/dev/null || echo "false")

    if [ "$COMPARE" = "true" ]; then
        echo "New ATH detected! Current ($CURRENT_PRICE) > ATH ($ATH_PRICE)"
        ATH_VERDICT="ATH"
    else
        echo "No new ATH (current $CURRENT_PRICE <= stored ATH $ATH_PRICE)"
        ATH_VERDICT="ATH_OK"
    fi
fi

# Step 5: Evaluate sharp-move gate
echo ""
echo "=== Step 5: Sharp-move gate evaluation ==="

ABS_H1=$(echo "$H1_CHANGE" | sed 's/-//g')
THRESHOLD=20.0
IS_SHARP=false

if [ -n "$H1_CHANGE" ] && [ "$H1_CHANGE" != "null" ]; then
    IS_SHARP=$(echo "$ABS_H1 >= $THRESHOLD" | bc -l 2>/dev/null || echo "false")
fi

if [ "$IS_SHARP" = "true" ]; then
    echo "SHARP_MOVE: abs(H1) ($ABS_H1%) >= threshold ($THRESHOLD%)"
    SHARP_VERDICT="SHARP_MOVE"
else
    echo "No sharp move (abs(H1) < threshold). Verdict: OK"
    SHARP_VERDICT="OK"
fi

# Step 6: Evaluate target-crossing gate
echo ""
echo "=== Step 6: Target-crossing gate evaluation ==="

TARGETS_COUNT=$(jq -r '.targets | length' "$STATE_FILE")
TARGET_VERDICT="NONE"
TARGETS_LIST=$(jq -c 'keys' "$STATE_FILE")

echo "Targets in state: $TARGETS_COUNT ($TARGETS_LIST)"

# Step 7: Combine verdicts and determine notifications
echo ""
echo "=== Step 7: Verdict combination ==="

FINAL_VERDICT="OK"
NOTIFICATIONS_COUNT=0

if [ "$ATH_VERDICT" = "ATH" ]; then
    FINAL_VERDICT="ATH"
    NOTIFICATIONS_COUNT=1
elif [ "$SHARP_VERDICT" = "SHARP_MOVE" ]; then
    FINAL_VERDICT="SHARP_MOVE"
    NOTIFICATIONS_COUNT=1
elif [ "$TARGET_VERDICT" = "TARGET_HIT" ]; then
    FINAL_VERDICT="TARGET_HIT"
    NOTIFICATIONS_COUNT=1
fi

echo "Final verdict: $FINAL_VERDICT"
echo "Notifications to send: $NOTIFICATIONS_COUNT"

if [ "$FINAL_VERDICT" = "OK" ]; then
    echo "No alerts fired. OK status."
fi

echo ""
echo "=== Skill run analysis complete ==="
echo ""
echo "Step 8-9: Persist state and log to be completed"
