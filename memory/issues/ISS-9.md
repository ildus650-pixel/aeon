---
name: digest
title: fix: add retry logic for API rate limits (429, 529) with 5-second backoff
status: fix-pending
severity: medium
category: rate-limit
detected: 2026-09-20T23:42:00Z
affected_skills:
  - digest
---

## Repair Attempt — 2026-09-20

**Root cause:** The xAI API curl command had no retry logic for HTTP 429 (rate limit) and 529 (service overload) errors, which are temporary and often resolve within seconds.

**Fix applied:** Added retry logic with 5-second backoff. If HTTP=429 or HTTP=529, the skill now retries once before falling back to WebSearch/WebFetch.

**PR:** https://github.com/ildus650-pixel/aeon/pull/11

**Source status:** cron_state=ok | issues_index=ok | gh_runs=ok | gh_logs=ok | git_log=ok | check_runs=ok
