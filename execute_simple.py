#!/usr/bin/env python3
import json
import subprocess
import os
from datetime import datetime, timezone

# Read current state
with open('memory/topics/price-alert-state.json', 'r') as f:
    state = json.load(f)

# Update last_run_at
now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
state['last_run_at'] = now

# Write back
with open('memory/topics/price-alert-state.json', 'w') as f:
    json.dump(state, f, indent=2)

print(f"State updated successfully with last_run_at: {now}")