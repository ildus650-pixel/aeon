import json, os, shutil
from datetime import datetime, timezone, timedelta

STATE = "/home/runner/work/aeon/aeon/memory/topics/price-alert-state.json"
LOG = "/home/runner/work/aeon/aeon/memory/logs/2026-11-15.md"
NOW = datetime.now(timezone.utc)
NOW_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")

# Fetched data (deepest ethereum pool by liquidity: Curve crvUSD, $64.68M)
CURRENT_PRICE = 64432.057
H1_CHANGE_PCT = 0.0      # missing in API response -> treat as 0
H24_CHANGE_PCT = -0.45
POOL_URL = "https://dexscreener.com/ethereum/0x313698667d7fdd6789a9bc70821309ff891e729a"
SYMBOL = "WBTC"
CONTRACT = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
CHAIN = "ethereum"
TARGETS = []  # var empty -> no operator targets

with open(STATE) as f:
    state = json.load(f)

# --- Step 4: ATH gate ---
prior_ath = state["ath"]["price_usd"] if state.get("ath") else None
new_ath = (prior_ath is None) or (CURRENT_PRICE > prior_ath)
ath_verdict = None
if new_ath:
    prior_observed = state["ath"]["observed_at"] if state.get("ath") else NOW_ISO
    state["ath"] = {"price_usd": CURRENT_PRICE, "observed_at": NOW_ISO,
                    "announced_at": state["ath"]["announced_at"] if state.get("ath") else None}
    last_ath_alert = state["last_alerts"].get("ath")
    if prior_ath is None:
        ath_verdict = "ATH_BASELINE"   # suppress notify on first run
        state["ath"]["announced_at"] = NOW_ISO
    elif last_ath_alert is None or (NOW - datetime.fromisoformat(last_ath_alert.replace("Z", "+00:00"))) > timedelta(hours=4):
        ath_verdict = "ATH"
        state["ath"]["announced_at"] = NOW_ISO
        state["last_alerts"]["ath"] = NOW_ISO
    else:
        ath_verdict = "ATH_DEDUPED"
    prior_observed = prior_observed
else:
    prior_observed = state["ath"]["observed_at"] if state.get("ath") else NOW_ISO

# --- Step 5: Sharp-move gate ---
sharp = abs(H1_CHANGE_PCT) >= 20.0
sharp_verdict = "QUIET"
if sharp:
    lsm = state["last_alerts"].get("sharp_move")
    if lsm and (NOW - datetime.fromisoformat(lsm.replace("Z", "+00:00"))) <= timedelta(hours=4):
        sharp_verdict = "SHARP_MOVE_DEDUPED"
    else:
        sharp_verdict = "SHARP_MOVE"
        state["last_alerts"]["sharp_move"] = NOW_ISO

# --- Step 6: Target-crossing gate ---
target_verdicts = []
for t in TARGETS:
    key = str(t)
    if key not in state["targets"]:
        state["targets"][key] = {"side": "above" if CURRENT_PRICE < t else "below",
                                 "first_seen_below_at": NOW_ISO, "hit_at": None, "announced_at": None}
        target_verdicts.append(str(key) + ":REGISTERED")
    elif state["targets"][key].get("hit_at"):
        target_verdicts.append(str(key) + ":SKIP_HIT")
    else:
        side = state["targets"][key]["side"]
        crossed = (side == "above" and CURRENT_PRICE >= t) or (side == "below" and CURRENT_PRICE <= t)
        if crossed:
            state["targets"][key]["hit_at"] = NOW_ISO
            state["targets"][key]["announced_at"] = NOW_ISO
            target_verdicts.append(str(key) + ":TARGET_HIT")
        else:
            target_verdicts.append(str(key) + ":PENDING")

# --- Step 7: verdict precedence ---
fired = []
if ath_verdict == "ATH":
    fired.append("ATH")
if any(v.endswith("TARGET_HIT") for v in target_verdicts):
    fired.append("TARGET_HIT")
if sharp_verdict == "SHARP_MOVE":
    fired.append("SHARP_MOVE")
status = "PRICE_ALERT_OK"
if "ATH" in fired:
    status = "PRICE_ALERT_ATH"
elif "TARGET_HIT" in fired:
    status = "PRICE_ALERT_TARGET_HIT"
elif "SHARP_MOVE" in fired:
    status = "PRICE_ALERT_SHARP_MOVE"
notif_count = len(fired)

# --- Step 8: persist state atomically ---
state["last_run_at"] = NOW_ISO
state["contract"] = CONTRACT
state["chain"] = CHAIN

shutil.copyfile(STATE, STATE + ".bak")
tmp = STATE + ".tmp"
with open(tmp, "w") as f:
    json.dump(state, f, indent=2)
os.replace(tmp, STATE)
try:
    with open(STATE) as f:
        json.load(f)
    print("state validated OK")
except Exception as e:
    shutil.copyfile(STATE + ".bak", STATE)
    print("PRICE_ALERT_STATE_CORRUPT restored:", e)
    status = "PRICE_ALERT_STATE_CORRUPT"

# --- Step 9: log ---
def sci(x):
    return "%.4e" % x

def pct(x):
    return "%+.1f" % x if x else "+0.0"

ath_observed = state["ath"]["observed_at"]
ath_dt = datetime.fromisoformat(ath_observed.replace("Z", "+00:00"))
ath_set_str = ath_dt.strftime("%Y-%m-%d %H:%M")
ath_marker = "NEW" if new_ath else "UNCHANGED"
ath_price = CURRENT_PRICE if new_ath else prior_ath

lines = []
lines.append("## Price Threshold Alert")
lines.append("- **Skill**: price-alert")
lines.append("- **Token**: " + SYMBOL + " (" + CONTRACT + ")")
lines.append("- **Current**: $" + sci(CURRENT_PRICE) + " | 1h: " + pct(H1_CHANGE_PCT) + "% | 24h: " + pct(H24_CHANGE_PCT) + "%")
lines.append("- **ATH**: $" + sci(ath_price) + " (set " + ath_set_str + " UTC) [" + ath_marker + "]")
lines.append("- **Sharp-move gate**: " + sharp_verdict)
lines.append("- **Targets evaluated**: () → ()")
lines.append("- **Verdicts fired**: " + (", ".join(fired) if fired else "NONE"))
lines.append("- **Notifications sent**: " + str(notif_count))
lines.append("- **Status**: " + status)
log_block = "\n" + "\n".join(lines) + "\n"

with open(LOG, "a") as f:
    f.write(log_block)

print("---")
print("CURRENT_PRICE=" + str(CURRENT_PRICE) + " prior_ath=" + str(prior_ath) + " new_ath=" + str(new_ath) + " sharp=" + str(sharp))
print("verdicts=" + str(fired) + " status=" + status)
print(log_block)
