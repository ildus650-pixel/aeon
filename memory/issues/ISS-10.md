---
status: open
title: token-movers intermittent failures with truncated API responses
severity: medium
category: rate-limit
detected: 2026-09-25T20:00:00Z
affected_skills: token-movers
---

## Symptom

Token-movers skill failing with truncated JSON error messages in `memory/cron-state.json`:

```
"last_error": "a9730\",\"total_cost_usd\":0,\"usage\":{\"input_tokens\":0,\"cache_creation_input_tokens\":0,\"cache_read_input_tokens\":0,\"output_tokens\":0,\"server_tool_use\":{\"web_search_requests\":0,\"web_fetch_requests\":0},\"s"
```

## Diagnosis

- **Failure pattern:** 3 consecutive failures out of 16 runs (19% failure rate) — updated: 5 consecutive failures in recent runs (100%)
- **Success rate:** 38% (6/16 runs successful) — updated: 48% (35/73 total)
- **Last success:** 2026-09-24T15:31:57Z — updated: 2026-10-29T16:21:22Z
- **Last failed:** 2026-09-25T19:59:13Z — updated: 2026-10-30T22:59:01Z
- **Quality score:** Last successful run had score 5 (good output when successful) — updated: last_quality_score=1 (empty output)
- **Regression commits:** None in the 24h window since last success — updated: a957c8c (XAI truncation fix) is the only commit in window
- **API health:** Manual tests show CoinGecko and GeckoTerminal responding successfully

## Root cause

**OpenRouter free-tier daily quota exhaustion (rate-limit category)** — NOT api-change or XAI truncation.

The skill fails at the LLM gateway level BEFORE any skill code executes:
- Gateway cascade: GLM → OpenRouter (both hit 429 rate limits)
- Error: "Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day"
- Consistent 5/5 recent failures with identical OpenRouter 429 signature
- Skill never reaches CoinGecko, GeckoTerminal, XAI, or any API calls

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

**Corrected analysis (2026-10-31):**
- The truncated error message contains OpenRouter modelUsage data, confirming LLM provider failure
- XAI API truncation fix (commit a957c8c) addresses WRONG issue — skill fails at gateway, never reaches XAI
- This is a SYSTEMIC issue affecting multiple skills: token-movers, price-alert, digest, heartbeat, skill-repair
- Requires operator action: upgrade OpenRouter tier, reduce fleet frequency, or switch model provider

## Repair Attempt — 2026-09-25

Diagnostic phase only. No fix applied. Issue filed to allow operator review before attempting fix.

## Repair Attempt — 2026-10-31

**Diagnostic finding:** Root cause is OpenRouter free-tier daily quota exhaustion (rate-limit), NOT XAI API truncation (api-change). 

**Prior repair attempt (commit a957c8c):** Added XAI retry/validation logic but this fix is MISDIRECTED — the skill fails at the LLM gateway (OpenRouter/GLM 429 rate limits) before any skill API calls execute. The XAI code path is never reached.

**Existing PR #26** (fix/skill-repair-token-movers-rate-limit-2026-10-10) already addresses the correct rate-limit diagnosis. No new PR needed.

**Exit code:** REPAIR_BLOCKED (open PR exists for correct diagnosis) / REPAIR_DIAGNOSED_NO_FIX (systemic operator action required)
