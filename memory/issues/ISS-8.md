---
name: price-alert timeout and rate-limit
description: price-alert skill hitting timeout and rate-limit errors
status: fix-pending
fix_pr: https://github.com/ildus650-pixel/aeon/pull/17
category: timeout
severity: high
---

## Symptoms

price-alert skill hitting timeout errors.

**Error:** `error: harness run exceeded --timeout 1800s`

**Pattern:** 4 consecutive failures in 24h. Last 3 failures show timeout errors; earlier failures showed 429 rate-limit errors.

**Root cause (current):** The cumulative effect of sleep delays (2s per DexScreener call) + multiple API calls per run + state persistence is causing the skill to exceed the 1800s (30 min) timeout.

**Root cause (historical):** The skill was originally hitting Claude API 429 rate limit errors before the 2s sleep was added.

## Diagnosis notes

- Regression source: None in the last week (no commits to price-alert or workflow)
- Consistency: Mixed error pattern (429 errors from ~2026-09-26, then timeout errors after)
- Category: timeout (current) / rate-limit (historical)
- Affected skills: price-alert only (not systemic cluster)
- The fix from PR #17 (2s sleep) resolved the 429 rate-limit errors but introduced a timeout issue

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

## Repair attempt 4 — 2026-09-27 (timeout diagnosis)

**Diagnosis:** The skill now shows timeout errors ("harness run exceeded --timeout 1800s") instead of 429 rate-limit errors. PR #17 already applied a 2s sleep to prevent rate-limiting, but this introduced a timeout issue.

**Root cause:** The cumulative effect of:
- 2s sleep before each DexScreener API call
- Multiple API calls per run (fetching price, checking state)
- State persistence writes
- Logging operations
causes the skill to exceed the 30-minute timeout window.

**PR status:** PR #17 (https://github.com/ildus650-pixel/aeon/pull/17) is still open, has the 2s sleep fix applied, but causes timeout errors.

**Category change:** Changed from `rate-limit` to `timeout` based on current error pattern.

**Risk:** LOW - the sleep is already in place and working for rate-limiting, just need to optimize for timeout.

## Source status

cron_state=ok | issues_index=ok | gh_runs=ok | gh_logs=ok | git_log=ok | check_runs=ok
