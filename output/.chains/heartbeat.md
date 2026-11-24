*Priority Brief — 2026-11-24*

*Focus today*
1. Buy OpenRouter credits — ISS-8/ISS-11: lifts free tier 50→1000 req/day, fixes 33-46% fleet success rates
2. Merge PR 27 and 26 — quota trims for price-alert (2-hourly) and token-movers (reduced quota burn); 10 skill-repair PRs open, oldest 44d
3. Fix github-monitor PR query — gh pr list --json fails on read:org scope (ISS-4); repair PR ready, just waiting for merge

*Since yesterday*
- [moved]: PR 27 merged to reduce price-alert quota burn (cut from hourly to 2-hourly)
- [stuck]: skill-repair still dispatched with 1 completed run (warming up)
- [stalled]: 4 dependency bump PRs (32, 31, 30, 29) open since Nov 1

*Running today*
- digest @ 14:00 UTC
- skill-repair @ reactive trigger (consecutive_failures >= 3)