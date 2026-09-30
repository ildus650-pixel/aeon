Priority Brief — 2026-09-30

*Focus today*
1. Merge token-movers retry PR (#19) — why now: chronic 35% success rate, gateway overload systemic
2. Merge digest retry PRs (#13, #11, #10) — why now: 15% success rate, 529 gateway kills all skills
3. Configure notification channels — why now: silent failures, operator blind for days

*Since yesterday*
- All skills recovered from failure streaks but chronic rates persist (digest 15%, token-movers 35%, skill-repair 32%)
- 7 open PRs fix the same rate-limit/gateway issues — not merged
- Chain dev-loop dispatched 24h+ ago, never completed (scheduler may not be wired)
- Issues: ISS-1 High (digest 529), ISS-8 High (price-alert rate-limit), ISS-10 Medium (token-movers truncated)

*Running today*
- heartbeat @ 08:00 UTC (completed)
- github-monitor @ 09:00 UTC (due)
- price-alert hourly @ ~10:00 UTC
- token-movers @ 12:00 UTC
- digest @ 14:00 UTC