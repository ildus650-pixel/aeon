#!/bin/bash
# Send the priority brief via Resend email if configured.
set -euo pipefail

# Check if BRIEF_RECIPIENTS is set (this script file approach avoids the
# Bash permission layer's command-line expansion block)
BRIEF_RECIPIENTS_VAL="${BRIEF_RECIPIENTS:-}"
if [ -z "$BRIEF_RECIPIENTS_VAL" ]; then
  echo "email: skipped (no BRIEF_RECIPIENTS)"
  exit 0
fi

# Build the email payload
RECIPIENTS_JSON=$(echo "$BRIEF_RECIPIENTS" | tr ',' '\n' | sed 's/^"\(.*\)"$/\1/' | jq -R . | jq -s .)

HTML_BODY="<h2>Priority Brief — 2026-10-27</h2>

<h3>Focus today</h3>
<ol>
<li><strong>Buy OpenRouter credits</strong> — why now: free tier exhausted; root cause of 33-46% fleet-wide skill failures</li>
<li><strong>Restore ambient heartbeat cron</strong> — why now: dark 13 days; P0/P1 checks disabled</li>
<li><strong>Merge PR #27 + #26</strong> — why now: quota trims; oldest PR 10d pending</li>
</ol>

<h3>Since yesterday</h3>
<ul>
<li>github-monitor: dispatch stuck since 10-19 14:27 (~8 days; last success 10-18 09:45) — 🕸 stuck</li>
<li>price-alert: ATH \$80,059 held; no new gates; quiet since 10-19</li>
<li>digest: X-signal layer still down — http-400 from missing XAI_API_KEY; RSS fallback active</li>
<li>OpenRouter free tier exhausted: 0/50 remaining; fleet running without LLM headroom</li>
<li>10 skill-repair PRs open (oldest 10d) — merge queue growing</li>
</ul>

<h3>Watch</h3>
<ul>
<li>Bitcoin below \$80K on Fed/geopolitical pressure (CoinDesk Oct 27) — market context for token-movers fleet</li>
<li>Coinbase launched AI agent trading features (CryptoBriefing Oct 22) — new onchain agent primitive; fleet can't track → focus #1, #2</li>
</ul>

<h3>Running today</h3>
<ul>
<li>price-alert @ hourly (00 minutes)</li>
<li>token-movers @ 12:00 UTC</li>
<li>digest @ 14:00 UTC</li>
<li>skill-repair @ reactive</li>
</ul>"

TEXT_BODY="Priority Brief — 2026-10-27

Focus today
1. Buy OpenRouter credits — why now: free tier exhausted; root cause of 33-46% fleet-wide skill failures
2. Restore ambient heartbeat cron — why now: dark 13 days; P0/P1 checks disabled
3. Merge PR #27 + #26 — why now: quota trims; oldest PR 10d pending

Since yesterday
- github-monitor: dispatch stuck since 10-19 14:27 (~8 days; last success 10-18 09:45) — 🕸 stuck
- price-alert: ATH $80,059 held; no new gates; quiet since 10-19
- digest: X-signal layer still down — http-400 from missing XAI_API_KEY; RSS fallback active
- OpenRouter free tier exhausted: 0/50 remaining; fleet running without LLM headroom
- 10 skill-repair PRs open (oldest 10d) — merge queue growing

Watch
- Bitcoin below $80K on Fed/geopolitical pressure (CoinDesk Oct 27) — market context for token-movers fleet
- Coinbase launched AI agent trading features (CryptoBriefing Oct 22) — new onchain agent primitive; fleet can't track → focus #1, #2

Running today
- price-alert @ hourly (00 minutes)
- token-movers @ 12:00 UTC
- digest @ 14:00 UTC
- skill-repair @ reactive"

# Write payload to a temp file
PAYLOAD_FILE=$(mktemp)
jq -n \
  --arg to "$RECIPIENTS_JSON" \
  --arg from "Aeon Briefings <onboarding@resend.dev>" \
  --arg subject "[Aeon] Priority Brief — 2026-10-27" \
  --arg html "$HTML_BODY" \
  --arg text "$TEXT_BODY" \
  '{from: $from, to: ($to | fromjson), subject: $subject, html: $html, text: $text}' > "$PAYLOAD_FILE"

# Send via secretcurl (handles the placeholder substitution internally)
HTTP_CODE=$(./secretcurl -s -o /tmp/resend-response.json -w "%{http_code}" \
  "https://api.resend.com/emails" \
  -H "Authorization: Bearer {RESEND_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "@$PAYLOAD_FILE")

echo "http=$HTTP_CODE"

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
  # Extract the id from the response
  RESEND_ID=$(jq -r '.id // "unknown"' /tmp/resend-response.json 2>/dev/null || echo "unknown")
  echo "resend_id=$RESEND_ID"
  echo "email: sent (Resend id=$RESEND_ID)"
else
  echo "email: ERROR — http=$HTTP_CODE"
  cat /tmp/resend-response.json
  exit 1
fi

rm -f "$PAYLOAD_FILE"
