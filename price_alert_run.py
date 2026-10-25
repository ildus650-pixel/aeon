import json
import requests
from datetime import datetime, timezone
import os
import sys

with open('memory/MEMORY.md', 'r') as f:
    memory_content = f.read()

lines = memory_content.split('\n')
in_token_table = False
contract = None
chain = None

for i, line in enumerate(lines):
    if line.strip() == '## Tracked Token':
        in_token_table = True
        continue
    elif in_token_table and line.strip() and '|' in line:
        if 'Token' in line or '---' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            contract = parts[2]
            chain = parts[3].lower()
            break

print('Token contract: ' + str(contract))
print('Chain: ' + str(chain))

state_path = 'memory/topics/price-alert-state.json'
if os.path.exists(state_path):
    with open(state_path, 'r') as f:
        state = json.load(f)
else:
    state = {
        "contract": contract,
        "chain": chain,
        "ath": {"price_usd": 0.0, "observed_at": "", "announced_at": ""},
        "last_alerts": {"ath": None, "sharp_move": None, "target_hit": None},
        "targets": {}
    }

print('State contract: ' + str(state.get('contract')))

if state.get('contract') and state.get('contract') != contract:
    print('PRICE_ALERT_TOKEN_CHANGED')
    state = {
        "contract": contract,
        "chain": chain,
        "ath": {"price_usd": 0.0, "observed_at": "", "announced_at": ""},
        "last_alerts": {"ath": None, "sharp_move": None, "target_hit": None},
        "targets": {}
    }
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
    print('State reset for new contract')

resp = requests.get('https://api.dexscreener.com/latest/dex/tokens/' + contract, timeout=5)
if resp.status_code == 200:
    data = resp.json()
    print('DexScreener response received')

    pairs = []
    for pair in data.get('pairs', []):
        if pair.get('chainId', '').lower() == chain:
            pairs.append(pair)

    if not pairs:
        print('No pairs found for chain, using fallback to highest liquidity')
        for pair in data.get('pairs', []):
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            if liquidity > 0:
                pair['fallback'] = True
                pairs.append(pair)
        pairs.sort(key=lambda p: p.get('liquidity', {}).get('usd', 0), reverse=True)

    if not pairs:
        print('ERROR: No pairs found for this token')
        sys.exit(1)

    deepest = pairs[0]
    current_price = float(deepest.get('priceUsd', 0))
    h1_change = float(deepest.get('priceChange', {}).get('h1', 0))
    h24_change = float(deepest.get('priceChange', {}).get('h24', 0))
    pool_url = deepest.get('url', '')

    print('Price: ' + str(current_price) + ', 1h: ' + str(h1_change) + '%, 24h: ' + str(h24_change) + '%')

    if not current_price or current_price <= 0:
        print('ERROR: Invalid price from API')
        sys.exit(1)

    results = []
    prior_ath = state.get('ath', {}).get('price_usd', 0)
    new_ath = (prior_ath == 0) or (current_price > prior_ath)
    ath_verdict = ''
    if new_ath:
        state['ath']['price_usd'] = current_price
        state['ath']['observed_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        last_ath_alert = state.get('last_alerts', {}).get('ath')
        current_time = datetime.now(timezone.utc)
        if last_ath_alert:
            last_alert_time = datetime.fromisoformat(last_ath_alert.replace('Z', '+00:00'))
            hours_since = (current_time - last_alert_time).total_seconds() / 3600
            if hours_since > 4:
                state['last_alerts']['ath'] = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                ath_verdict = 'ATH'
                results.append({'gate': 'ATH', 'verdict': 'ATH', 'new_price': current_price})
            else:
                ath_verdict = 'ATH_DEDUPED'
        else:
            state['ath']['announced_at'] = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            ath_verdict = 'ATH_BASELINE'

    sharp = abs(h1_change) >= 20.0
    sharp_verdict = ''
    if sharp:
        last_sharp_alert = state.get('last_alerts', {}).get('sharp_move')
        current_time = datetime.now(timezone.utc)
        if last_sharp_alert:
            last_alert_time = datetime.fromisoformat(last_sharp_alert.replace('Z', '+00:00'))
            hours_since = (current_time - last_alert_time).total_seconds() / 3600
            if hours_since > 4:
                state['last_alerts']['sharp_move'] = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                direction = 'up' if h1_change >= 0 else 'down'
                sharp_verdict = 'SHARP_MOVE'
                results.append({'gate': 'SHARP_MOVE', 'verdict': 'SHARP_MOVE', 'direction': direction, 'change': h1_change})
            else:
                sharp_verdict = 'SHARP_MOVE_DEDUPED'
        else:
            state['last_alerts']['sharp_move'] = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            direction = 'up' if h1_change >= 0 else 'down'
            sharp_verdict = 'SHARP_MOVE'
            results.append({'gate': 'SHARP_MOVE', 'verdict': 'SHARP_MOVE', 'direction': direction, 'change': h1_change})

    for target_price_str, target_data in state.get('targets', {}).items():
        if target_data.get('hit_at'):
            continue
        target_price = float(target_price_str)
        crossed = False
        if target_data.get('side') == 'above':
            if current_price >= target_price:
                crossed = True
        else:
            if current_price <= target_price:
                crossed = True
        if crossed:
            state['last_alerts']['target_hit'] = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            results.append({'gate': 'TARGET_HIT', 'verdict': 'TARGET_HIT', 'target': target_price})
            target_data['hit_at'] = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    if os.path.exists(state_path):
        os.rename(state_path, state_path + '.bak')
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
    try:
        with open(state_path, 'r') as f:
            json.load(f)
        print('State validation successful')
    except Exception as e:
        if os.path.exists(state_path + '.bak'):
            os.rename(state_path + '.bak', state_path)
        print('ERROR: State corrupted: ' + str(e))
        sys.exit(1)

    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    current_str = '{:.2f}'.format(current_price)
    h1_str = '{:+.1f}'.format(h1_change)
    h24_str = '{:+.1f}'.format(h24_change)
    ath_price_str = '{:.2f}'.format(state['ath']['price_usd'])
    new_ath_str = 'NEW' if new_ath else 'UNCHANGED'
    if 'SHARP_MOVE' in sharp_verdict and 'DEDUPED' not in sharp_verdict:
        sharp_str = 'FIRED'
    elif not sharp:
        sharp_str = 'QUIET'
    else:
        sharp_str = 'DEDUPED'
    targets_str = str(list(state.get('targets', {}).keys()))

    log_entry = (
        '## Price Threshold Alert\n'
        '- **Skill**: price-alert\n'
        '- **Token**: WBTC (' + str(contract) + ')\n'
        '- **Current**: $' + current_str + ' | 1h: ' + h1_str + '% | 24h: ' + h24_str + '%\n'
        '- **ATH**: $' + ath_price_str + ' (set ' + str(state['ath']['observed_at']) + ' UTC) [' + new_ath_str + ']\n'
        '- **Sharp-move gate**: ' + sharp_str + '\n'
        '- **Targets evaluated**: ' + targets_str + ' -> ' + targets_str + '\n'
        '- **Verdicts fired**: ' + str(len(results)) + '\n'
        '- **Notifications sent**: ' + str(len(results)) + '\n'
    )

    if 'ATH' in ath_verdict and 'BASELINE' not in ath_verdict:
        log_entry += '- **Status**: PRICE_ALERT_ATH\n'
    elif 'SHARP_MOVE' in sharp_verdict:
        log_entry += '- **Status**: PRICE_ALERT_SHARP_MOVE\n'
    else:
        log_entry += '- **Status**: PRICE_ALERT_OK\n'

    print('LOG ENTRY:')
    print(log_entry)

    if results:
        print('SUCCESS: ' + str(len(results)) + ' gates fired')
        for result in results:
            print('  - ' + str(result))
    else:
        print('SUCCESS: No gates fired (OK)')

    sys.exit(0)
else:
    print('ERROR: Failed to fetch from DexScreener, status: ' + str(resp.status_code))
    sys.exit(1)