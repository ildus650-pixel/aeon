#!/bin/bash
NOW="2026-11-04T22:17:52Z"
STATE_FILE="/home/runner/work/aeon/aeon/memory/topics/price-alert-state.json"

# Update last_run_at and reset other fields that might have drifted
jq --arg now "$NOW" \
  '.last_run_at = $now |
   .contract = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599" |
   .chain = "ethereum"' \
  "$STATE_FILE" > /tmp/state-updated.json

# Validate the JSON
if jq empty /tmp/state-updated.json 2>/dev/null; then
  mv /tmp/state-updated.json "$STATE_FILE"
  echo "State updated successfully"
else
  echo "State validation failed, restore from backup"
  cp "${STATE_FILE}.bak" "$STATE_FILE"
fi
