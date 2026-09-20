---
name: fix(digest): add retry logic for API rate limits (429, 529) with 5-second backoff
description: Digest skill failed 4 consecutive runs with API Error 529 (service temporarily overloaded)
severity: HIGH
category: rate-limit
affected_skills: digest
status: fix-pending
fix_pr: https://github.com/ildus650-pixel/aeon/pull/13
---

## Symptom
Digest skill failed 4 consecutive runs (100% failure rate):
- 2026-09-19T20:49:35Z: API Error 529 (service temporarily overloaded)
- 2026-09-20T00:22:20Z: API Error 529 (service temporarily overloaded)
- 2026-09-20T05:10:07Z: API Error 529 (service temporarily overloaded)
- 2026-09-20T05:16:13Z: API Error 529 (service temporarily overloaded)

All failures occur early in execution (within 2 API turns) via xAI API Gateway, consistently returning HTTP 529 for "service temporarily overloaded".

## Root Cause
Transient API Gateway rate limiting / service overload from xAI (Grok x_search). The skill lacked retry logic for HTTP 429 (rate limit) and 529 (service overload) errors, which are often temporary and resolve within seconds.

## Fix Applied
Added retry logic for HTTP 429 and 529 errors with a 5-second backoff:
1. Make initial xAI API curl request
2. If HTTP=429 or HTTP=529, log retry attempt and sleep 5s
3. Retry the same request once
4. After retry, continue with the same parsing logic; if retry also fails, fall back to Path B

See PR #13 for full details.

## Verification
**Manual trigger:** [Run skill](https://github.com/ildus650-pixel/aeon/actions/workflows/aeon.yml) with `skill=digest` and `var=`.

**Expected result:**
- Workflow conclusion: `success` (or `failure` only if rate limit persists across retries and fallback also fails)
- On 429/529 errors: log shows `xai rate-limit detected, retrying after 5s...` followed by retry attempt
- On retry success: uses the retried response as primary X signal
- On retry failure: falls back to WebSearch/WebFetch for X signal, logging the true reason
- If X signal ultimately unavailable: skill continues with web + RSS sources, logging the reason in run notes

**If still failing after this PR:** delete `memory/state/skill-repair-history.json[digest]` to remove the cooldown, then re-dispatch `skill-repair` with `var=digest` for a second pass.

## Repair Attempt — 2026-09-20
Exit: REPAIR_OK_FIXED
Target: digest
Category: rate-limit
Diagnosis: xAI API Gateway returning HTTP 529 (service temporarily overloaded) on all 4 consecutive runs
Fix: Added retry logic for HTTP 429/529 with 5-second backoff before falling back to WebFetch/WebSearch (12 lines added)
Risk: LOW
PR: https://github.com/ildus650-pixel/aeon/pull/13
