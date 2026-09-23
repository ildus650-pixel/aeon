ℹ️ skill-repair — REPAIR_DIAGNOSED_NO_FIX

## skill-repair — REPAIR_DIAGNOSED_NO_FIX

Target: price-alert

Root cause: Claude API 429 rate limit errors from frequent DexScreener API calls

Fix: Open PR #15 adds 0.5s rate-limit backoff — operator must review and merge (risk: MED — fix exists but not applied yet)

PR: https://github.com/ildus650-pixel/aeon/pull/15  Issue: ISS-8

Verify: Review and merge PR #15, then re-run workflow_dispatch skill=price-alert