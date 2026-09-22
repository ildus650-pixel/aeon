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

## Source status

cron_state=ok | issues_index=ok | gh_runs=ok | gh_logs=ok | git_log=ok | check_runs=ok
