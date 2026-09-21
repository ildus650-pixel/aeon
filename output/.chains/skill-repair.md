skill-repair — REPAIR_DIAGNOSED_NO_FIX

Target: price-alert (systemic cluster affecting 4 skills)
Root cause: 529 Gateway Overload from api.z.ai (provider infrastructure)
Fix: Requires operator action — contact api.z.ai support, adjust schedules to reduce concurrent load, or implement fallback provider. Retry logic won't solve the gateway capacity issue.
Issue: https://github.com/ildus650-pixel/aeon/issues/14
Verify: Contact api.z.ai support to address gateway capacity; adjust schedules to spread hourly runs (e.g., :15 instead of :00)
