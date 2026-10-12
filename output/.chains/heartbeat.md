## Priority Brief — 2026-10-12

### Focus today

1. Fix OpenRouter free-tier quota exhaustion — why now: systemic 429 errors across heartbeat (failed 3x consecutively), digest (27% success), skill-repair (37%); ISS-11 diagnosis confirms this blocks the entire fleet
2. Fix token-movers intermittent API failures — why now: ISS-10 open with truncated CoinGecko responses; PR #26 pending to address rate-limit throttling; market-moving tokens (STRK +90.5% 7d) at risk of being missed
3. Configure notification channels — why now: MEMORY.md top priority; no digest sent despite aeon.yml enabling it; operator blind to fleet health and alerts

### Since yesterday

- [moved]: Heartbeat rate-limit fix PR #26 created but unresolved; ISS-11 opened tracking OpenRouter quota exhaustion across multiple skills
- [stuck]: token-movers has 49% failure rate despite 10 successful runs; ISS-10 describes truncated CoinGecko API responses
- [pending]: digest skill at 27% success rate — needs either notification config or gateway upgrade
- [flagged]: github-monitor shows 34% failure rate, though consecutive failures at 0

### Watch

(Omitted — WebSearch API overloaded, no meaningful headlines found this run)

### Running today

- 00:00 UTC: price-alert (tracked WBTC +2.5% 24h, ATH unchanged)
- 12:00 UTC: token-movers (global movers scan)
- 14:00 UTC: digest (AI agents, crypto, market news)
- 18:00 UTC: skill-repair (reactive — watches for failing skills)