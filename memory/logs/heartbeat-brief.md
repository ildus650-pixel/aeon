## Priority Brief — 2026-09-30

### Focus today

1. Merge token-movers retry PR (#19) — why now: chronic failures (35% success rate, 17 failures), CoinGecko/GeckoTerminal timeout/rate-limit is systemic
2. Merge digest retry fixes (#13, #11, #10) — why now: chronic failures (15% success rate, 29 failures), same 529 gateway overload affecting all skills via api.z.ai
3. Configure notification channels — why now: no alerts have been sent in days; operator unaware of issues until they surface in logs

### Since yesterday

- GitHub PRs: 10 open (5 PRs fix the same rate-limit/gateway issues across digest, price-alert, token-movers)
- Open issues: 3 (ISS-1 gateway overload [High], ISS-8 rate-limit throttling [High], ISS-10 truncated API responses [Medium])
- Skills with low success rates but no consecutive_failures yet: digest (15%), token-movers (35%), price-alert (43%)
- GLM Gateway overloaded (529 errors) — causing chronic API failures across multiple skills

### Running today

- heartbeat at 08:00 UTC
