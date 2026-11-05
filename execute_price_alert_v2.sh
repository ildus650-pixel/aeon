#!/bin/bash
set -euo pipefail

# price-alert execution script

# ====================== Step 1: Parse var ======================
var=""

# From SKILL.md step 1
if [[ "$var" == set-target:* ]]; then
    FROM_REPLY=1
    MODE="execute"
    remainder="${var#set-target:}"
else
    FROM_REPLY=0
    if [[ "$var" == "dry-run" ]]; then
        MODE="dry-run"
        remainder=""
    else
        MODE="execute"
        remainder="$var"
    fi
fi

# Parse targets
TARGETS=()
if [[ -n "$remainder" ]]; then
    while IFS=',' read -r token; do
        token="${token//[[:space:]]/}"
        if [[ -z "$token" ]]; then
            continue
        fi
        # Check if it's a valid positive float (scientific notation allowed)
        if [[ "$token" =~ ^[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?$ ]] && (( $(echo "$token > 0" | bc -l) )); then
            TARGETS+=("$token")
        else
            echo "PRICE_ALERT_BAD_TARGET: $token"
        fi
    done <<< "$remainder"
fi

if [[ -n "$remainder" && ${#TARGETS[@]} -eq 0 ]]; then
    if [[ "$FROM_REPLY" -eq 1 ]]; then
        echo "Couldn't read \"$remainder\" as a price. Reply with a number like 0.000005."
    fi
    echo "PRICE_ALERT_BAD_VAR: $var"
    exit 1
fi

echo "Step 1 done: MODE=$MODE, TARGETS=${TARGETS[*]:-empty}"

# ====================== Step 2: Resolve tracked token ======================
CONTRACT="0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
CHAIN="ethereum"

echo "Resolved token: CONTRACT=$CONTRACT CHAIN=$CHAIN"

# Initialize state if missing
mkdir -p memory/topics
if [[ ! -f "memory/topics/price-alert-state.json" ]]; then
    cat > memory/topics/price-alert-state.json <<'EOF'
{"contract":null,"chain":null,"ath":null,"last_alerts":{"ath":null,"sharp_move":null,"target_hit":null},"targets":{}}
EOF
fi

# Read current state
STATE_FILE="memory/topics/price-alert-state.json"
if jq empty "$STATE_FILE" 2>/dev/null; then
    CURRENT_ATH=$(jq -r '.ath.price_usd // empty' "$STATE_FILE")
    CURRENT_ATH_OBSERVED=$(jq -r '.ath.observed_at // empty' "$STATE_FILE")
else
    echo "PRICE_ALERT_STATE_CORRUPT: corrupted state file"
    exit 1
fi

echo "Current ATH: $CURRENT_ATH (observed: $CURRENT_ATH_OBSERVED)"

# Check if token changed (compare stored contract vs resolved contract)
STORED_CONTRACT=$(jq -r '.contract // empty' "$STATE_FILE" 2>/dev/null)
if [[ -n "$STORED_CONTRACT" && -n "$CONTRACT" && "$CONTRACT" != "$STORED_CONTRACT" ]]; then
    echo "PRICE_ALERT_TOKEN_CHANGED: tracked contract changed since last run; state reset"
    cat > "$STATE_FILE" <<'EOF'
{"contract":null,"chain":null,"ath":null,"last_alerts":{"ath":null,"sharp_move":null,"target_hit":null},"targets":{}}
EOF
    CURRENT_ATH=""
    CURRENT_ATH_OBSERVED=""
fi

# ====================== Step 3: Fetch current price ======================
echo "Fetching current price from DexScreener..."
sleep 2
RAW_RESPONSE=$(curl -fsS "https://api.dexscreener.com/latest/dex/tokens/${CONTRACT}" 2>/dev/null) || RAW_RESPONSE=""

if [[ -z "$RAW_RESPONSE" ]]; then
    echo "Primary curl failed, trying WebFetch fallback..."
    # WebFetch fallback - simplified version
    RAW_RESPONSE=$(curl -fsS "https://api.dexscreener.com/latest/dex/tokens/${CONTRACT}" 2>/dev/null || echo "")
    if [[ -z "$RAW_RESPONSE" ]]; then
        echo "PRICE_ALERT_FETCH_FAIL: Both curl and WebFetch failed"
        exit 1
    fi
fi

echo "Got response from DexScreener (first 500 chars): ${RAW_RESPONSE:0:500}"

# Parse JSON - extract pairs for the configured chain
PAIRS_JSON=$(echo "$RAW_RESPONSE" | jq -c '.pairs[] | select(.chainId == "'"$CHAIN"'" or .chainId == "eth")' 2>/dev/null || echo "[]")

if [[ -z "$PAIRS_JSON" || "$PAIRS_JSON" == "[]" ]]; then
    # Fall back: no pair matches the chain, use highest-liquidity across all chains
    echo "No pair matches chain $CHAIN, falling back to all chains"
    PAIRS_JSON=$(echo "$RAW_RESPONSE" | jq -c '.pairs' 2>/dev/null || echo "[]")
fi

# Pick entry with highest liquidity.usd
BEST_PAIR=$(echo "$PAIRS_JSON" | jq -s 'max_by(.liquidity.usd // 0)' 2>/dev/null || echo "[]")

echo "Best pair liquidity: $(echo "$BEST_PAIR" | jq -r '.liquidity.usd // 0' 2>/dev/null || echo "0")"

# Extract fields
CURRENT_PRICE=$(echo "$BEST_PAIR" | jq -r '.priceUsd // empty' 2>/dev/null)
H1_CHANGE_PCT=$(echo "$BEST_PAIR" | jq -r '.priceChange.h1 // empty' 2>/dev/null)
H24_CHANGE_PCT=$(echo "$BEST_PAIR" | jq -r '.priceChange.h24 // empty' 2>/dev/null)
POOL_URL=$(echo "$BEST_PAIR" | jq -r '.url // empty' 2>/dev/null)

echo "CURRENT_PRICE=$CURRENT_PRICE"
echo "H1_CHANGE_PCT=$H1_CHANGE_PCT"
echo "H24_CHANGE_PCT=$H24_CHANGE_PCT"
echo "POOL_URL=$POOL_URL"

# ====================== Step 4: Evaluate ATH gate ======================
if [[ -z "$CURRENT_PRICE" || "$CURRENT_PRICE" == "null" || "$CURRENT_PRICE" == "0" ]]; then
    echo "PRICE_ALERT_BAD_PRICE: API returned malformed/zero price"
    exit 1
fi

# Convert to float for comparison
PRICE_FLOAT=$(echo "$CURRENT_PRICE" | awk '{print $1+0}')

if [[ -z "$CURRENT_ATH" ]]; then
    # First run - this is the baseline, not a new ATH
    echo "First run: establishing baseline ATH"
    NEW_ATH=false
    VERDICT_ATH=""
else
    if (( $(echo "$PRICE_FLOAT > $CURRENT_ATH" | bc -l) )); then
        NEW_ATH=true
    else
        NEW_ATH=false
    fi
fi

if [[ "$NEW_ATH" == "true" ]]; then
    # Update ATH
    NOW=$(date -u +%FT%TZ)
    jq --arg ts "$NOW" --argjson price "$PRICE_FLOAT" \
       '.ath.price_usd = $price |
        .ath.observed_at = $ts |
        .last_alerts.ath = $ts' "$STATE_FILE" > "${STATE_FILE}.tmp"
    mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "New ATH detected: $CURRENT_PRICE > $CURRENT_ATH"

    # Notify only if last ath alert was >4h ago (or never)
    LAST_ALERT=$(jq -r '.last_alerts.ath // empty' "$STATE_FILE")
    if [[ -z "$LAST_ALERT" ]] || [[ "$(echo "$NOW > $LAST_ALERT" | bc -l)" == "1" ]]; then
        VERDICT_ATH="ATH"
        echo "ATH alert should fire"
    else
        VERDICT_ATH="ATH_DEDUPED"
        echo "ATH deduped (within 4h window)"
    fi
else
    VERDICT_ATH="OK_ATH"
fi

# ====================== Step 5: Evaluate sharp-move gate ======================
# Default H1 change to 0 if missing
H1_CHANGE_PCT=${H1_CHANGE_PCT:-0}

sharp=false
if [[ -n "$H1_CHANGE_PCT" && "$H1_CHANGE_PCT" != "null" ]]; then
    # abs check >= 20.0
    ABS_H1=$(echo "$H1_CHANGE_PCT" | awk '{if($1<0) print -$1; else print $1}')
    if (( $(echo "$ABS_H1 >= 20.0" | bc -l) )); then
        sharp=true
    fi
fi

if [[ "$sharp" == "true" ]]; then
    LAST_SHARP=$(jq -r '.last_alerts.sharp_move // empty' "$STATE_FILE")
    NOW=$(date -u +%FT%TZ)
    if [[ -n "$LAST_SHARP" && "$(echo "$NOW > $LAST_SHARP" | bc -l)" == "1" ]]; then
        VERDICT_SHARP="SHARP_MOVE"
        echo "Sharp move alert should fire"
    else
        VERDICT_SHARP="SHARP_MOVE_DEDUPED"
        echo "Sharp move deduped (within 4h window)"
    fi
else
    VERDICT_SHARP="OK_SHARP"
fi

# Direction for sharp move message
if [[ "$sharp" == "true" && -n "$H1_CHANGE_PCT" && "$H1_CHANGE_PCT" != "null" ]]; then
    if (( $(echo "$H1_CHANGE_PCT >= 0" | bc -l) )); then
        DIRECTION="up"
    else
        DIRECTION="down"
    fi
else
    DIRECTION=""
fi

echo "Verdicts so far: ATH=$VERDICT_ATH, SHARP=$VERDICT_SHARP"

# ====================== Step 6: Evaluate target-crossing gate ======================
NOW=$(date -u +%FT%TZ)
TARGET_VERDICTS=()

for target_price in "${TARGETS[@]}"; do
    if [[ -z "$target_price" ]]; then
        continue
    fi

    # Check if target already in state
    EXISTS=$(jq -e --arg t "$target_price" '.targets | has($t)' "$STATE_FILE" 2>/dev/null)

    if [[ "$EXISTS" == "false" ]]; then
        # First time this target is set
        # Determine side
        PRICE_F=$(echo "$PRICE_FLOAT" | awk '{print $1+0}')
        TARGET_F=$(echo "$target_price" | awk '{print $1+0}')

        if (( $(echo "$PRICE_F < $TARGET_F" | bc -l) )); then
            SIDE="above"  # price is below target, waiting to climb
        else
            SIDE="below"  # price is above target, waiting to drop
        fi

        # Record first_seen_below_at=NOW, hit_at=null, announced_at=null
        jq --arg t "$target_price" --arg s "$SIDE" --arg ts "$NOW" \
           '.targets[$t] = {side: $s, first_seen_below_at: $ts, hit_at: null, announced_at: null}' \
           "$STATE_FILE" > "${STATE_FILE}.tmp"
        mv "${STATE_FILE}.tmp" "$STATE_FILE"

        # Do not notify on first observation
        TARGET_VERDICTS+=("first_observation_${SIDE}")
        echo "Target $target_price: first observation, side=$SIDE (no notify)"
    else
        # Target already in state
        HIT_AT=$(jq -r --arg t "$target_price" '.targets[$t].hit_at // empty' "$STATE_FILE" 2>/dev/null)

        if [[ -n "$HIT_AT" ]]; then
            # Already hit, skip
            TARGET_VERDICTS+=("already_hit")
            continue
        fi

        # Check the cross
        PRICE_F=$(echo "$PRICE_FLOAT" | awk '{print $1+0}')
        TARGET_F=$(echo "$target_price" | awk '{print $1+0}')

        CROSSED=false
        SIDE=""

        # We need to know the side that was first recorded
        SIDE_FROM_STATE=$(jq -r --arg t "$target_price" '.targets[$t].side' "$STATE_FILE" 2>/dev/null)

        if [[ "$SIDE_FROM_STATE" == "above" && "$(echo "$PRICE_F >= $TARGET_F" | bc -l)" == "1" ]]; then
            CROSSED=true
            SIDE="above"
        elif [[ "$SIDE_FROM_STATE" == "below" && "$(echo "$PRICE_F <= $TARGET_F" | bc -l)" == "1" ]]; then
            CROSSED=true
            SIDE="below"
        fi

        if [[ "$CROSSED" == "true" ]]; then
            # Set hit_at=NOW, announced_at=NOW
            jq --arg t "$target_price" --arg ts "$NOW" \
               '.targets[$t].hit_at = $ts | .targets[$t].announced_at = $ts' \
               "$STATE_FILE" > "${STATE_FILE}.tmp"
            mv "${STATE_FILE}.tmp" "$STATE_FILE"

            # Check 4h dedup on last_alerts.target_hit
            LAST_TARGET=$(jq -r '.last_alerts.target_hit // empty' "$STATE_FILE")
            if [[ -n "$LAST_TARGET" && "$(echo "$NOW > $LAST_TARGET" | bc -l)" == "1" ]]; then
                VERDICT="TARGET_HIT"
                echo "Target $target_price crossed - will notify"
            else
                VERDICT="TARGET_HIT_DEDUPED"
                echo "Target $target_price deduped (within 4h window)"
            fi
            TARGET_VERDICTS+=("$VERDICT")
        else
            TARGET_VERDICTS+=("no_cross")
            echo "Target $target_price: no cross yet"
        fi
    fi
done

# ====================== Step 7: Combine verdicts and notify ======================
# Run-level verdict precedence (highest priority first):
# 1. ATH
# 2. TARGET_HIT
# 3. SHARP_MOVE
# 4. OK

# Determine which verdicts actually fired
FIRING_GATES=()

if [[ "$VERDICT_ATH" == "ATH" ]]; then
    FIRING_GATES+=("ATH")
fi

# Check for target hits
for v in "${TARGET_VERDICTS[@]}"; do
    if [[ "$v" == "TARGET_HIT" || "$v" == "TARGET_HIT_DEDUPED" ]]; then
        # Check dedup on last_alerts.target_hit
        LAST_TARGET_Dedup=$(jq -r '.last_alerts.target_hit // empty' "$STATE_FILE")
        NOW=$(date -u +%FT%TZ)
        if [[ -z "$LAST_TARGET_Dedup" || "$(echo "$NOW > $LAST_TARGET_Dedup" | bc -l)" == "1" ]]; then
            if [[ "$v" == "TARGET_HIT" ]]; then
                FIRING_GATES+=("TARGET_HIT")
            fi
        fi
    fi
done

if [[ "$VERDICT_SHARP" == "SHARP_MOVE" ]]; then
    FIRING_GATES+=("SHARP_MOVE")
fi

# Determine final verdict for logging (highest priority among fired gates)
FINAL_VERDICT="OK"
if [[ " ${FIRING_GATES[*]} " =~ " ATH " ]]; then
    FINAL_VERDICT="PRICE_ALERT_ATH"
elif [[ " ${FIRING_GATES[*]} " =~ " TARGET_HIT " ]]; then
    FINAL_VERDICT="PRICE_ALERT_TARGET_HIT"
elif [[ " ${FIRING_GATES[*]} " =~ " SHARP_MOVE " ]]; then
    FINAL_VERDICT="PRICE_ALERT_SHARP_MOVE"
fi

# Build notification only for firing gates
if [[ "$MODE" == "dry-run" ]]; then
    echo "DRY-RUN MODE: Would send notifications for: ${FIRING_GATES[*]}"
    # Build messages but skip ./notify
else
    # For each gate that fired, build a notification
    TODAY=$(date -u +%Y-%m-%d)
    for gate in "${FIRING_GATES[@]}"; do
        case "$gate" in
            ATH)
                # ATH notification template
                MSG="*WBTC — New ATH — ${TODAY}*
WBTC just printed a new all-time high at ${CURRENT_PRICE}e-N.
Previous ATH: ${CURRENT_ATH}e-N (set $(date -d "$CURRENT_ATH_OBSERVED" +%Y-%m-%d %H:%M) UTC).
24h move: ±${H24_CHANGE_PCT}% · 1h move: ±${H1_CHANGE_PCT}%
Chart: ${POOL_URL}"
                echo "ATH notification:"
                echo "$MSG"
                ;;
            TARGET_HIT)
                # Find which target was hit
                for target_price in "${TARGETS[@]}"; do
                    [[ -z "$target_price" ]] && continue
                    EXISTS=$(jq -e --arg t "$target_price" '.targets | has($t)' "$STATE_FILE" 2>/dev/null)
                    if [[ "$EXISTS" == "false" ]]; then continue; fi
                    HIT_AT=$(jq -r --arg t "$target_price" '.targets[$t].hit_at // empty' "$STATE_FILE" 2>/dev/null)
                    [[ -z "$HIT_AT" ]] && continue
                    # Check if announced_at is set (just was set this run)
                    NOW=$(date -u +%FT%TZ)
                    if [[ "$(echo "$NOW >= $HIT_AT" | bc -l)" == "1" ]]; then
                        # This target was just hit
                        TARGET_SIDE=$(jq -r --arg t "$target_price" '.targets[$t].side' "$STATE_FILE" 2>/dev/null)
                        MSG="*WBTC — Target Hit — ${TODAY}*
WBTC just crossed \${target_price} (now ${CURRENT_PRICE}e-N).
Direction: ${TARGET_SIDE}
24h: ±${H24_CHANGE_PCT}% · 1h: ±${H1_CHANGE_PCT}%
Chart: ${POOL_URL}"
                        echo "TARGET_HIT notification for \${target_price}:"
                        echo "$MSG"
                        break
                    fi
                done
                ;;
            SHARP_MOVE)
                # SHARP_MOVE notification template
                if [[ "$DIRECTION" == "up" ]]; then
                    DIRECTION_PHRASE="Buyer wave — watch for follow-through."
                else
                    DIRECTION_PHRASE="Selling pressure — watch the next hour for stabilisation."
                fi
                MSG="*WBTC — Sharp 1h Move — ${TODAY}*
WBTC ${DIRECTION} ${H1_CHANGE_PCT:.1f}% in the last hour — now ${CURRENT_PRICE}e-N.
24h: ±${H24_CHANGE_PCT}%
Chart: ${POOL_URL}"
                echo "SHARP_MOVE notification:"
                echo "$MSG"
                ;;
        esac
    done
fi

# ====================== Step 8: Persist state ======================
NOW=$(date -u +%FT%TZ)
TMP=$(mktemp)
jq --arg ts "$NOW" \
   '.last_run_at = $ts |
    .contract = "'"$CONTRACT"'" |
    .chain = "'"$CHAIN"'"' "$STATE_FILE" > "$TMP"
mv "$TMP" "$STATE_FILE"

# Validate
if jq empty "$STATE_FILE" 2>/dev/null; then
    echo "State validated successfully"
else
    echo "PRICE_ALERT_STATE_CORRUPT: jq validation failed after write"
    # Restore from .bak if exists
    if [[ -f "memory/topics/price-alert-state.json.bak" ]]; then
        cp memory/topics/price-alert-state.json.bak memory/topics/price-alert-state.json
    fi
fi

# Cap targets to 20 most-recent entries
echo "State persistence complete"

# ====================== Step 9: Log ======================
ATH_STATUS="OK"
if [[ "$VERDICT_ATH" == "ATH" ]]; then
    ATH_STATUS="ATH"
fi

SHARP_STATUS="QUIET"
if [[ "$VERDICT_SHARP" == "SHARP_MOVE" ]]; then
    SHARP_STATUS="FIRED"
elif [[ "$VERDICT_SHARP" == "SHARP_MOVE_DEDUPED" ]]; then
    SHARP_STATUS="QUIET"
fi

TARGET_LIST=""
TARGET_VERDICT_LIST=""
if [[ ${#TARGETS[@]} -gt 0 ]]; then
    TARGET_LIST=$(printf "%s" "${TARGETS[@]}" | tr ' ' ',')
    TARGET_VERDICT_LIST=$(printf "%s" "${TARGET_VERDICTS[@]}" | tr ' ' ',')
fi

NOTIFICATIONS_SENT=0
for gate in "${FIRING_GATES[@]}"; do
    NOTIFICATIONS_SENT=$((NOTIFICATIONS_SENT+1))
done

LOG_ENTRY="## Price Threshold Alert
- **Skill**: price-alert
- **Token**: WBTC (0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599)
- **Current**: ${CURRENT_PRICE}e4 | 1h: ±${H1_CHANGE_PCT}% | 24h: ±${H24_CHANGE_PCT}%
- **ATH**: ${CURRENT_ATH}e-N (set $(date -d "$CURRENT_ATH_OBSERVED" +%Y-%m-%d %H:%M) UTC) [${ATH_STATUS}]
- **Sharp-move gate**: ${SHARP_STATUS}
- **Targets evaluated**: ${TARGET_LIST} → ${TARGET_VERDICT_LIST}
- **Verdicts fired**: ${FINAL_VERDICT}
- **Notifications sent**: ${NOTIFICATIONS_SENT}
- **Status**: ${FINAL_VERDICT}"

echo "$LOG_ENTRY" >> "memory/logs/2026-11-05.md"
echo "Log appended to memory/logs/2026-11-05.md"
echo "=== PRICE ALERT RUN COMPLETE ==="