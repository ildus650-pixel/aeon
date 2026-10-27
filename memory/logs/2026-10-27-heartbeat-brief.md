## Heartbeat (priority brief)

- **mode:** brief
- **timestamp:** 2026-10-27T08:00:00Z
- **focus items:**
  1. Buy OpenRouter credits — lifts free tier 50→1000 req/day; root cause of 33-46% fleet-wide skill failures
  2. Merge PR #27 + #26 — cut quota burn for price-alert/token-movers; oldest PR 10d, stack growing
  3. Fix github-monitor PR query — gh pr list --json fails on read:org scope; recovered but cost PR tier multiple times since Sept 24
- **skills flagged from cron-state:**
  - heartbeat: 46% success rate (weakest)
  - token-movers: 49% success rate
  - digest: 37% success rate (poorest)
  - skill-repair: 38% success rate (last run 2026-10-14, hasn't been reactive)
- **open PRs:** 10 skill-repair PRs (PR 27 from Oct 13, PR 26 from Oct 10), 2 dependabot PRs
- **email:** sent via ./notify (skipped Resend email step cleanly — unconfigured or not allowed)