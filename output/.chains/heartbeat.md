*Priority Brief — 2026-11-14*

*Focus today*
1. Buy OpenRouter credits — lifts free tier 50→1000 req/day, fixes ISS-8/ISS-11 and fleet's 33-46% success rates
2. Restore ambient heartbeat branch on 08:00 cron — aeon.yml sets var: "brief", so P0/P1 checks and status page have been dark since 2026-10-14
3. Merge PR 27 and 26 — quota trims for price-alert and token-movers; 10 skill-repair PRs open, oldest 10d

*Since yesterday*
- WBTC price-alert set ATH at $71,153.41 (up from $68,332 on Nov 13), but no new notifications sent (price is still below ATH gate)
- price-alert recovered from consecutive failures and now running successfully (73% success rate, last success today at 01:49 UTC)
- token-movers stuck since Nov 13 15:28 (never completed), digest ran successfully on Nov 13 21:46 (46% success rate)
- skill-repair stuck since Oct 31 22:01 (13 days ago), but that was the last repair attempt - not actively blocking anything

*Running today*
- price-alert: every hour (next run ~16:15 UTC)
- token-movers: 12:00 PM UTC
- digest: 2:00 PM UTC