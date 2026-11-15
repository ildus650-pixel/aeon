**Priority Brief — 2026-11-15**

*Focus today*

1. **Buy $10+ OpenRouter credits** — why now: 4 weeks unresolved; quota still exhausted daily; every skill 40-60% failure rate persists.

2. **Merge PR #27 + #26 (and the 10 skill-repair PRs)** — why now: quota binds; consumption trims (price-alert → 2-hourly) needed while cap is binding.

3. **Reset the scheduler (token-movers + digest)** — why now: both dispatched 19h ago without outcome; today's 12:00/14:00 dispatches will confirm or clear.

*Since yesterday*

- **price-alert**: WBTC $64,965, no new gates; ATH $67,958 unchanged.
- **token-movers + digest**: dispatched 2026-11-14 15:01 UTC, never reported back (19h); next run at 12:00/14:00 UTC today.
- **BTC market**: ~$62K (4-month low), ETH -19.5% weekly, ETFs $1.07B outflows, DXY >103, Fed hike priced (88% Dec 25bp) — extreme fear.
- **OpenRouter**: quota exhausted (70/50 used), fleet running with no working LLM path for another day.
- **SC operations**: github-monitor PR #32-29 (dependabot) and #27-26 (skill-repair) stalled >24h; 10 open skill-repair PRs, oldest 26d.
- **Heart of the issue**: gateway-quota 2026-10-20 root cause: OpenRouter free tier cap 50/day, $10+ credits permanently lift to 1,000.

*Watch*

- Fed Dec hike (88% chance) + DXY >103 → risk-off tape; token-movers at 12:00 UTC scans into a falling market; price-alert gates matter.

*Running today*

- github-monitor @ 09:00 UTC
- token-movers @ 12:00 UTC
- price-alert @ hourly (00 minutes)
- digest @  sampled 14:00 UTC
- skill-repair @ reactive
- heartbeat @ 08:00 UTC (brief) 

The admin pause is resolved — the skill runs completed.
