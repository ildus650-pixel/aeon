*skill-repair — REPAIR_OK_FIXED*
Target: price-alert
Root cause: DexScreener API backoff (`sleep 2`) insufficient to prevent Claude API 429 rate-limit throttling during repeated workflow executions; PR #15 (0.5s) unmerged
Fix: Increased DexScreener backoff from `sleep 2` to `sleep 5` in `skills/price-alert/SKILL.md` line 98 (risk: LOW)
PR: https://github.com/ildus650-pixel/aeon/pull/25 | Issue: ISS-8 updated (status: fix-pending)
Verify: workflow_dispatch skill=price-alert