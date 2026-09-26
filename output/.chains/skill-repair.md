*skill-repair — REPAIR_OK_FIXED*
Target: price-alert
Root cause: 0.5s rate-limit backoff insufficient; cumulative tool delays hit Claude API throttling during repeated daily executions
Fix: Increased sleep delay to 2s before DexScreener API call (1-line change) (risk: LOW)
PR: https://github.com/ildus650-pixel/aeon/pull/17
Issue: ISS-8
Verify: workflow_dispatch skill=price-alert