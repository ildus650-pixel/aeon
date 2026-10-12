---
title: skill-repair failing due to OpenRouter free-tier quota exhaustion
severity: High
category: rate-limit
status: open
created: 2026-10-12
affected_skills:
  - skill-repair
  - heartbeat
---

## Symptom

The skill-repair skill has failed on 3 consecutive runs (consecutive_failures=3) with success_rate=0.36 (27/75). The last error shows **OpenRouter free-tier quota exhaustion** — the same systemic issue affecting price-alert, digest, and heartbeat skills.

## Diagnosis

**Error signature**: `,"service_tier":"standard","cache_creation":{"ephemeral_1h_input_tokens":0,"ephemeral_5m_input_tokens":0},"inference_geo":"","iterations":[],"speed":"standard"},"modelUsage":{"openrouter/free":{"input` — OpenRouter free-tier quota exceeded on model calls.

**Root cause**: OpenRouter free tier provides ~1000 requests/day shared across all skills using the gateway. The fleet (price-alert, digest, heartbeat, skill-repair) exceeds this daily quota. When skill-repair runs (especially when triggered reactively for other failing skills), it consumes additional quota and fails with the same 429/quota error. This is a **systemic fleet-level quota issue**, not a skill-repair code defect.

**Evidence**:
- cron-state: `success_rate: 0.36`, `consecutive_failures: 3`, `last_quality_score: 4`
- Recent failed runs: 3 consecutive failures (run 38178201327, 38162268476, 38141952489) all with OpenRouter quota signature
- git history: No code changes to skill-repair since 2026-10-11T06:30:02Z (only commit 691b8e7 — digest success, unrelated)
- skill-repair history: Previously repaired 2026-09-29 with REPAIR_DIAGNOSED_NO_FIX for "Systemic API degradation from GLM Gateway" — same class of issue
- quality history: `avg_score: 3.94`, latest score 4 — no quality regression

**Error pattern**: Consistent quota errors across all recent runs → **deterministic** (fleet-wide quota exhaustion)

**Recent runs**:
- Run 38178201327 (failed) — 2026-10-11T21:53:22Z — quota exhaustion
- Run 38162268476 (failed) — 2026-10-11T18:04:22Z — quota exhaustion
- Run 38141952489 (failed) — 2026-10-11T13:07:52Z — quota exhaustion
- Run 38117606221 (success) — 2026-10-11T06:18:00Z — last success before quota filled

## Repair Attempt — 2026-10-12

**Attempted**: 0 (diagnostic only — issue filed for operator action)

**Reason**: Root cause is fleet-wide OpenRouter free-tier quota exhaustion, not a skill-repair code defect. The skill-repair skill itself consumes quota when running, and when the shared daily budget is exhausted, all gateway-dependent skills fail.

**Why standard playbooks don't apply**:
- `rate-limit` playbook (backoff/sleep/fallback): Targets data-source APIs (DexScreener, CoinGecko), not the model gateway. The quota is a daily budget, not a per-request rate limit.
- `api-change` playbook: No API spec change — the gateway works but is out of quota.
- `missing-secret`: Key is present; quota is exhausted, not missing.
- `config` playbook: skill-repair is `schedule: reactive` — not a cron frequency issue.

**Systemic finding**: This is the same root cause documented in ISS-8 (price-alert). The repair fleet consumes the shared quota, creating a catch-22: skill-repair runs to fix other quota failures, then fails itself from quota.

**Recommendations**:

**Immediate**:
- Operator action required: upgrade OpenRouter tier, add alternate gateway key (Anthropic, Grok, GLM), or reduce fleet frequency
- Do not auto-retry skill-repair — quota won't reset until UTC midnight

**Long-term**:
- Implement gateway failover in aeon.yml (cascade: claude → anthropic → openrouter → bankr → usepod → venice → surplus → grok → glm)
- Add per-skill model pinning (`harness:`/`model:`) to route heavy skills to non-free tiers
- Consider running skill-repair on a non-free tier (e.g., claude-haiku-4-5-20251001) to reduce quota pressure

## Repair Attempt — 2026-10-12 (heartbeat)

**Attempted**: 0 (operator action required — systemic fleet-level quota issue)

**Reason**: Heartbeat skill failing with the same OpenRouter free-tier quota exhaustion signature as other fleet skills. The error is `openrouter/free` quota exceeded (truncated JSON in last_error field). Heartbeat has `consecutive_failures: 3`, `success_rate: 0.32` (20/62 runs), last failed 2026-10-11T21:59:53Z.

**Systemic classification**: This is a fleet-wide quota exhaustion affecting multiple gateway-dependent skills (price-alert, digest, heartbeat, skill-repair). The fix requires operator action, not code changes.

**Affected skills**: All skills using the OpenRouter free-tier gateway (price-alert, digest, heartbeat, skill-repair).

## Verification

To verify when the issue is resolved:
1. Wait for OpenRouter free-tier quota to reset (UTC midnight) or operator upgrades tier/adds key
2. Run skill-repair with `var=skill-repair` after successful run
3. Verify cron-state `success_rate` improves to >0.5 and `consecutive_failures` resets to 0

## Diagnosis Notes

**Regression suspect**: None in heartbeat code since 2026-10-10T18:08:07Z (last success)

**Error pattern**:
- OpenRouter free-tier quota exhaustion is **consistent** across 3 consecutive heartbeat failures
- Quota is shared daily budget (~1000 req/day), not per-second rate limit
- Duration: ~3-6 hours between quota fill and reset
- Same error signature as ISS-8 (price-alert) and ISS-11 (skill-repair)

**Source status**:
- cron_state: ok (has detailed error data with OpenRouter signature)
- issues_index: ok (ISS-11 created)
- gh_runs: ok (3 recent failed runs verified with quota errors)
- gh_logs: ok (error log confirms quota exhaustion)
- git_log: ok (no code regressions)
- check_runs: N/A (no associated GitHub check runs)
