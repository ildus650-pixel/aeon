*Priority Brief — 2026-11-06*

*Focus today*
1. Buy OpenRouter credits — why now: $10 purchase lifts free tier 50→1,000 req/day, fixes 33–46% fleet-wide quota failures
2. Merge PR 27 + 26 — why now: quota trims still unmerged (10–13d old), price-alert runs hourly, token-movers daily
3. Restore ambient heartbeat on 08:00 cron — why now: P0/P1 checks and status page dark since 2026-10-14 (17 days stale)

*Since yesterday*
- price-alert: 6× successful overnight runs (hourly), WBTC $76,036 (ATH $81,858 unchanged)
- token-movers: mixed alt rotation — CAP +32.2% PUMP-RISK, FLUID +27.6% BREAKOUT, TRUMP -16.8% CAPITULATION
- digest: completed, github-monitor: completed, heartbeat brief: sent
- No PRs merged, no issues closed; 10 skill-repair PRs still open (oldest 10d)

*Watch*
- OpenRouter free tier confirmed: 50 req/day → 1,000/day after $10 credit purchase (failed requests count toward cap) — [OpenRouter docs](https://openrouter.ai/docs/api_reference/limits) → reinforces focus #1
- BTC swung $75.5k–$80.5k this week; $430M ETF outflows Nov 6, $1B+ liquidations; DeFi tokens outperformed — [CoinDesk](https://www.coindesk.com) → contextual for token-movers, no priority shift

*Running today*
- github-monitor @ 09:00 UTC
- token-movers @ 12:00 UTC
- price-alert @ hourly
- digest @ 14:00 UTC
- skill-repair @ reactive
- heartbeat @ 08:00 UTC (var=brief)

*Background:* Fix github-monitor PR query — gh pr list --json dies on read:org scope; working GraphQL shape in memory/topics/gh-cli-scope-workaround.md