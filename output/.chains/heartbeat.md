Based on the gathered context, here's the priority brief:

**Priority Brief — 2026-11-17**

*Focus today*
1. **Buy OpenRouter credits** — lifts free tier 50→1000 req/day, fixes 33-46% fleet-wide failures that have cascaded into 10+ skill-repair PRs
2. **Restore ambient heartbeat** — regains fleet health visibility (P0/P1 checks + status page dark since 2026-10-14, causing blind spots on skill failures)
3. **Merge PRs #27 & #26** — quota trims for price-alert/token-movers reduce burn; 10 open skill-repair PRs oldest 10d

*Since yesterday*
- **Moving:** digest PR #33 (chore deps for dashboard, mcp-server, webhook) — open 16 days
- **Stuck:** price-alert #27 (2-hourly schedule to ease OpenRouter quota) — open 4 days; token-movers #26 (reduce rate limit throttling) — open 7 days

*Watch*
- Skill-repair queue: 10 PRs, oldest 10 days — multiple ongoing quota- and rate-limit fixes pending merge
- cron-state.json shows mixed health: heartbeat (55% success), token-movers (51%), digest (46%), skill-repair (39%)

*Running today*
- github-monitor at 09:00 UTC
- token-movers at 12:00 UTC
- digest at 14:00 UTC

## Summary

- Generated priority brief for fleet health focus
- Identified 3 top priorities: OpenRouter credits, ambient heartbeat restoration, and PR merging
- Flagged 10 open skill-repair PRs with aging tickets
- Noted 2 stuck PRs (#27, #26) with pending quota/rate-limit fixes
