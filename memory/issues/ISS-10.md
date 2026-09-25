---
status: open
title: token-movers intermittent failures with truncated API responses
severity: medium
category: api-change
detected: 2026-09-25T20:00:00Z
affected_skills: token-movers
---

## Symptom

Token-movers skill failing with truncated JSON error messages in `memory/cron-state.json`:

```
"last_error": "a9730\",\"total_cost_usd\":0,\"usage\":{\"input_tokens\":0,\"cache_creation_input_tokens\":0,\"cache_read_input_tokens\":0,\"output_tokens\":0,\"server_tool_use\":{\"web_search_requests\":0,\"web_fetch_requests\":0},\"s"
```

## Diagnosis

- **Failure pattern:** 3 consecutive failures out of 16 runs (19% failure rate)
- **Success rate:** 38% (6/16 runs successful)
- **Last success:** 2026-09-24T15:31:57Z
- **Last failed:** 2026-09-25T19:59:13Z
- **Quality score:** Last successful run had score 5 (good output when successful)
- **Regression commits:** None in the 24h window since last success
- **API health:** Manual tests show CoinGecko and GeckoTerminal responding successfully

## Root cause

Intermittent API responses returning malformed/empty JSON that isn't being properly caught by current error handling. The truncated error message suggests partial API response data, possibly from:
- CoinGecko markets endpoint
- GeckoTerminal endpoints
- Or another third-party API used by the skill

## Source status

cron_state=ok | issues_index=ok | gh_runs=ok | gh_logs=ok | git_log=ok | check_runs=ok

## Diagnosis Notes

**Skills calling multiple APIs:**
1. CoinGecko (optional API key) - markets, trending endpoints
2. GeckoTerminal (no key) - trending, pools, new_pools endpoints
3. DexScreener (optional) - token endpoint
4. XAI API (optional) - social sentiment
5. Chain RPCs (optional) - treasury balances

**Current error handling:**
- WebFetch fallback when curl fails or returns empty JSON
- Graceful degradation for missing config/data

**Investigation needed:**
- Check if CoinGecko or GeckoTerminal have recently changed their response format
- Verify if rate-limiting is causing partial responses
- Review the specific error message source in the skill's execution path

## Repair Attempt — 2026-09-25

Diagnostic phase only. No fix applied. Issue filed to allow operator review before attempting fix.
