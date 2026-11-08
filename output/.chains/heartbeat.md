*Priority Brief — 2026-11-08*

*Focus today*
1. Buy OpenRouter credits — why now: one purchase lifts free tier 50→1,000 req/day, fixes 33–46% fleet-wide failure rate (ISS-8/ISS-11 root cause)
2. Restore ambient heartbeat on 08:00 cron — why now: P0/P1 checks and public status page dark since 2026-10-14 (aeon.yml sets var: "brief" instead of "")
3. Merge PR #27 + #26 — why now: quota trims still unmerged 18–21 days while hourly skills burn quota; 10 skill-repair PRs open, oldest 10d

*Since yesterday*
- Unchanged: OpenRouter quota issue persists, ambient heartbeat still on brief mode, quota-trim PRs pending

*Running today*
- heartbeat @ 08:00 UTC (brief mode)
- github-monitor @ 09:00 UTC
- price-alert @ 09:00 UTC
- token-movers @ 12:00 UTC
- digest @ 14:00 UTC