*skill-repair — REPAIR_DIAGNOSED_NO_FIX*

Target: price-alert
Root cause: Systemic OpenRouter free-tier quota exhaustion (1000 req/day shared across price-alert, digest, skill-repair, heartbeat). Sleep backoff fixes ineffective — error is from Claude RUN hitting model quota, not DexScreener rate limits.
Fix: — (requires operator action: upgrade tier, reduce frequency to 2h, or switch to Haiku)
PR: —
Issue: ISS-8 (updated with diagnosis)
Verify: —