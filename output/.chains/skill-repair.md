skill-repair — REPAIR_DIAGNOSED_NO_FIX

Target: heartbeat (systemic)
Root cause: OpenRouter free-tier quota exhaustion — shared 1000 req/day budget exceeded across fleet (price-alert, digest, heartbeat, skill-repair). Error signature: openrouter/free quota exceeded (truncated JSON in last_error).
Fix: Operator action required — upgrade OpenRouter tier, add alternate gateway key, or reduce fleet frequency. No code changes needed — skill is correctly using the gateway.
Issue: ISS-11
Verify: Wait for UTC midnight quota reset or upgrade tier, then re-run skill-repair