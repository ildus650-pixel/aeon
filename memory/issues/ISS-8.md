---
name: price-alert rate-limit throttling
description: price-alert skill hits Claude API 429 errors during execution
status: fix-pending
fix_pr: https://github.com/ildus650-pixel/aeon/pull/15
category: rate-limit
severity: high
---

## Symptoms

price-alert skill failing with Claude API 429 rate limit errors.

**Error:** `API Error: Request rejected (429) · Rate limit reached for requests`

**Pattern:** 4 consecutive failures in 24h with 58% success rate. Each failure shows 43,969 input tokens and high cache read volume, indicating repeated tool executions triggering throttling.

## Root cause

The skill makes frequent DexScreener API calls without sufficient delay between requests, hitting Claude's rate limit thresholds during repeated workflow executions. The cumulative effect of tool delays across 10+ calls per run pushes Claude into rate limit territory.

## Diagnosis notes

- Regression source: None in the last week (no commits to price-alert or workflow)
- Consistency: All 5 recent failures show the same 429 error pattern
- Category: rate-limit
- Affected skills: price-alert only (not systemic cluster)

## Repair attempt — 2026-09-22

**Fix applied:** Added 0.5s sleep before DexScreener API call to reduce rate of requests.

**PR:** https://github.com/ildus650-pixel/aeon/pull/15

**Verification plan:**
1. Run skill with `var=dry-run` to verify completion without 429 errors
2. Check that price-alert state file updates successfully
3. Confirm no `rate limit` strings in run logs

**If still failing:** Increase backoff to 1-2 seconds or implement exponential backoff.

## Repair attempt 2 — 2026-09-22 (skill-repair diagnosis fix)

**Diagnosis:** The price-alert skill itself completed successfully (PRICE_ALERT_OK), but skill-repair failed when trying to diagnose it, consuming 25454+ input tokens with GLM-4.7 flash.

**Root cause:** skill-repair's diagnosis phase fetches 5 failed runs and full logs, causing token exhaustion.

**Fix applied:** Reduced diagnosis verbosity:
- Limit failed runs from 5 to 3
- Add `--max-log-lines 500` to log fetch commands

**PR:** https://github.com/ildus650-pixel/aeon/pull/15 (updated with both fixes)

**Verification plan:**
1. Run skill-repair with `var=price-alert` to verify diagnosis completes without token exhaustion
2. Confirm diagnosis uses < 5000 input tokens

**If still failing:** Increase `--max-log-lines` to 300 or reduce runs to 2.

## Repair attempt 3 — 2026-09-23 (fresh diagnosis)

**Diagnosis:** The skill is still failing with 3 consecutive failures. The PR #15 is still open and has not been merged.

**Root cause:** Rate-limiting is still occurring; the fix has not been applied to the working directory yet.

**PR status:** Open, created 2026-09-22, last updated 2026-09-22T20:21:04Z, no reviews yet.

**Action required:** Operator must review and merge PR #15 to apply the rate-limit backoff fix.

## Source status

cron_state=ok | issues_index=ok | gh_runs=ok | gh_logs=ok | git_log=ok | check_runs=ok
