Priority Brief — 2026-09-23

*Focus today*
1. Configure notification channels — why now: With 12 failed heartbeat runs and multiple skills down, you have no real-time visibility into what's broken. Configure Telegram/Discord/Slack now so price alerts, digest failures, and critical PR triage reach you immediately.

2. Fix digest skill failures — why now: digest has 7% success rate, 5 consecutive failures since 2026-09-19. Skill-repair diagnosed this as an external gateway outage (529 errors)—not a code defect. Decide: wait for gateway recovery or implement retry/failover logic and switch gateway.

3. Fix price-alert rate-limit backoff — why now: price-alert has 3 consecutive failures and a PR exists (fix(price-alert): add rate-limit backoff). The skill fired ATH successfully yesterday, then broke. Implement the backoff to prevent another missed ATH trigger.

*Since yesterday*
- GitHub: PR #1083 INFO, 4 days of digest failures, 10 open PRs from skill-repair rate-limit fixes
- Skills: digest repaired, price-alert repaired, skill-repair diagnosed gateway outage, ATH fired for WBTC
- Issues: ISS-1 created (digest gateway outage)

*Running today*
- github-monitor: 09:00 UTC
- token-movers: 12:00 UTC
- digest: 14:00 UTC
- heartbeat: brief priority brief (this run)
- skill-repair: reactive (multiple skills with >=3 consecutive failures)