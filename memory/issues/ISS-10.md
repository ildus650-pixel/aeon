---
status: open
title: token-movers rate limit exhaustion (429 free-models-per-day)
severity: medium
category: rate-limit
detected: 2026-10-10T04:56:00Z
affected_skills: token-movers
---

## Symptom

Token-movers skill failing with Claude Code API rate limit error:

```
API Error: Request rejected (429) · Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day
```

**Usage at failure:**
- 1725,319 input tokens
- 10,424 output tokens
- 37 tool turns
- Quality score: 4 (good output when successful)
- Failure: 2026-10-10T01:08:57Z

## Diagnosis

- **Failure pattern:** 3 consecutive failures out of 5 recent runs (60% failure rate)
- **Success rate:** 40% (18/45 total runs)
- **Last success:** 2026-10-08T22:43:14Z
- **Last failed:** 2026-10-10T01:08:57Z
- **Regression commits:** ebe47dc - 691 line skill file expansion (full file rewrite)

## Root cause

**Claude Code free model quota exhaustion.** The skill consumed 1.7M+ tokens across 37 turns, exceeding the free daily quota. This is NOT an external API issue (CoinGecko/GeckoTerminal/API are healthy) but a session token budget exhaustion within the run.

The skill file was massively expanded in commit ebe47dc (691 new lines), increasing token consumption through:
- Verbose preamble with detailed rule descriptions (11 parsing rules, each with examples)
- Expanded memory log reading (last 30 days for single-token delta analysis)
- More detailed logging and formatting sections
- Longer examples and inline comments

## Source status

cron_state=ok | issues_index=ok | gh_runs=ok | gh_logs=ok | git_log=ok | check_runs=ok

## Diagnosis Notes

**Skills calling multiple APIs:**
1. CoinGecko (optional API key) - markets, trending endpoints
2. GeckoTerminal (no key) - trending, pools, new_pools endpoints
3. DexScreener (optional) - token endpoint
4. XAI API (optional) - social sentiment
5. Chain RPCs (optional) - treasury balances

**Token consumption hotspots:**
- Preamble: 11 verbose parsing rules with examples
- Log reading: 30 days of history for single-token runs
- Repeated reading of skill file in each tool invocation
- 37 tool turns (max turns before hitting quota)

**Investigation needed:**
- Reduce preamble verbosity (compress rule descriptions)
- Limit log history to 7 days for delta analysis
- Reduce rule examples in preamble
- Use shorter, more direct instructions

## Repair Attempt — 2026-10-10

Apply rate-limit fix by compressing preamble and reducing token consumption:

1. **Compress preamble** — Remove verbose examples from rule descriptions, keep only concise action items
2. **Limit log history** — Reduce single-token delta analysis from 30 days to 7 days
3. **Shorten inline comments** — Condense verbose explanations into brief notes
4. **Consolidate formatting** — Reduce repetition in formatting rules sections

Expected token reduction: ~40-50% (from 1.7M to ~0.8-1M tokens).

**PR:** https://github.com/ildus650-pixel/aeon/pull/26

**Verification:** Manual trigger via workflow_dispatch with `skill=token-movers`.
