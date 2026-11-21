*skill-repair — REPAIR_DIAGNOSED_NO_FIX*
Target: github-monitor (or systemic: skill-repair, heartbeat, github-monitor)
Root cause: OpenRouter free-tier quota exhaustion (429 rate limit, 1000 req/day shared)
Fix: Operator action required — upgrade tier, add alternate gateway key, or reduce fleet frequency (see ISS-11)
Issue: ISS-11
Verify: Wait for quota reset (UTC midnight) or upgrade tier