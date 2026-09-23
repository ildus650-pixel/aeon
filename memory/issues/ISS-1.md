---
title: digest skill failing with 529 gateway overload errors
severity: High
category: gateway-outage
status: open
created: 2026-09-23
affected_skills:
  - digest
---

## Symptom

The digest skill has failed on 13/14 runs (7% success rate) with **529 gateway overload errors** from api.z.ai.

## Diagnosis

**Error signature**: `api_error_status":529,"duration_ms":281586,"duration_api_ms":99686,"num_turns":2,"result":"API Error: 529 [1305][The service may be temporarily overloaded, please try again later]`

**Root cause**: Z.AI inference gateway is experiencing temporary service overload, preventing the skill from completing. This is a transient infrastructure issue, not a code defect.

**Evidence**:
- cron-state: `success_rate: 0.07`, `consecutive_failures: 5`, `last_quality_score: 4`
- Recent failed runs: 3 runs all returning 529 errors from `api.z.ai`
- git history: No code changes to digest since 2026-09-19 (no regression)
- No prior issues filed for this skill

**Error pattern**: Consistent 529 errors across all recent runs → **deterministic** (gateway overload affecting all invocations)

**Recent runs**:
- Run 35882431951 (failed) - 529 gateway overload
- Run 35882415237 (failed) - 529 gateway overload
- Run 35854824031 (failed) - 529 gateway overload

## Repair Attempt — 2026-09-23

**Attempted**: 0 (diagnostic only — issue filed for operator action)

**Reason**: Root cause is external gateway service overload, not fixable via code changes. The skill code is correct; it requires either:
1. Gateway provider retry/backoff logic (not implemented in current skill)
2. Multiple gateway failover (skill currently pins to Z.AI)
3. Operator coordination with gateway provider

## Recommendations

**Immediate**:
- Do not retry this skill automatically — gateway is overloaded, additional attempts will likely fail
- Operator should monitor gateway status and retry after service recovers
- Consider enabling `enabled: false` in aeon.yml temporarily until gateway is stable

**Long-term**:
- Implement gateway failover in skill code: when Z.AI fails, retry with alternative gateway (e.g., openai/gpt-5-mini fallback)
- Add exponential backoff + circuit breaker before giving up
- Monitor gateway status and surface as health issue when unavailable

## Verification

To verify when the issue is resolved:
1. Wait for gateway to return 2xx responses for digest skill runs
2. Run skill-repair with `var=digest` after successful run
3. Verify cron-state `success_rate` improves to >0.5 and `consecutive_failures` resets to 0

## Diagnosis Notes

**Regression suspect**: None in skill code since 2026-09-19 (only commit touches github-monitor)

**Error pattern**:
- 529 errors are **consistent** across 3 recent runs → likely gateway overload affecting all invocations
- HTTP 529 = "Service Temporarily Unavailable" (Cloudflare-style overload)
- Duration: ~281 seconds per run (slow, likely waiting for gateway to recover)

**Source status**:
- cron_state: ok (has detailed error data)
- issues_index: ok (issue file created)
- gh_runs: ok (3 recent failed runs verified with 529 errors)
- gh_logs: ok (error log confirms gateway overload)
- git_log: ok (no code regressions)
- check_runs: N/A (no associated GitHub check runs)

