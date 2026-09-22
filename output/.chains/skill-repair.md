skill-repair — REPAIR_OK_FIXED

Target: price-alert
Root cause: Claude API 429 rate limit errors from frequent DexScreener calls
Fix: Added 0.5s backoff before API call (LOW risk)
PR: https://github.com/ildus650-pixel/aeon/pull/15
Verify: workflow_dispatch skill=price-alert var=dry-run