skill-repair — REPAIR_OK_FIXED

Target: price-alert
Root cause: Timeout risk from 2s sleep delay across multiple API calls
Fix: Reduced sleep from 2s to 1s (still prevents rate-limiting) (risk: LOW)
PR: https://github.com/ildus650-pixel/aeon/pull/18  Issue: ISS-8
Verify: workflow_dispatch skill=price-alert var=dry-run