ℹ️ Aeon Priority Brief — 2026-10-16

*Priority Brief — 2026-10-16*

*Focus today*
1. Merge PR #27 (price-alert schedule cut to 2h) — why now: halves OpenRouter quota share per run, targets the root cause of recent failures
2. Merge PR #26 (token-movers rate limit) — why now: 42% success rate, chronic 429 errors from file expansion consuming quota
3. Configure notification channels — why now: operator blind to fleet health; digest still unconfigured despite aeon.yml enabling it

*Since yesterday*
- [moved]: token-movers recovered from "stuck" status (dispatched 20h ago, now successful)
- [stuck]: PR #27 and #26 still open, blocking fleet stabilization on OpenRouter quota fixes
- [baseline]: price-alert verified WBTC ATH $82,655.15, no alerts triggered

*Watch*
- digest success_rate 0.30 (last 20h) — rate-limiting remains the bottleneck across multiple skills (price-alert, token-movers, digest, skill-repair, github-monitor)

*Running today*
- heartbeat at 08:00 UTC
- token-movers at 12:00 UTC
- digest at 14:00 UTC