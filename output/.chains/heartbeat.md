Priority Brief — 2026-10-22

Focus today
1. Restore ambient heartbeat on the 08:00 cron — the fleet's core monitoring has been dark since 2026-10-14; without it, P0/P1/P2/P3 checks don't run and the public status page stays stale
2. Buy $10+ OpenRouter credits — lifts the free tier 50→1000 req/day, which is the root cause of the 33-46% skill success rates (ISS-8/ISS-11); especially impacts digest (35%), token-movers (48%), heartbeat (43%)
3. Merge PR #27 + #26 — both address quota exhaustion (price-alert 2-hourly, token-movers backoff) and are the direct fix for the ongoing rate-limit issues; 10 skill-repair PRs are open, oldest 10 days

Since yesterday
- WBTC set a new ATH at $84,712.99 (four times yesterday alone)
- Heartbeat itself has only 43% success rate (last_success 2026-10-21 09:41:50Z)
- digest dropped TorchTPU, DeepSeek DeepInfer, etc. after 36h+ dedup window
- 7 skill-repair PRs are still open (oldest: 2026-09-27 fix(price-alert) timeout)

Running today
- heartbeat at 08:00 UTC
- github-monitor at 09:00 UTC
- token-movers at 12:00 UTC
- digest at 14:00 UTC
- price-alert runs hourly
- skill-repair triggers on consecutive failures