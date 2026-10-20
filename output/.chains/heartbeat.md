⚠️ Priority Brief — 2026-10-20

*Priority Brief — 2026-10-20*

*Focus today*
1. Restore ambient heartbeat on the 08:00 cron — why now: P0 checks and status page dark since 10-14; fleet issues unobserved
2. Buy $10+ OpenRouter credits — why now: free cap exhausted 72/50, zero gateway headroom today
3. Merge PR #27 + #26 — why now: cut quota burn now while credits purchase is processed

*Since yesterday*
- github-monitor: 10-19 14:27 dispatch never reported back (23h; last success 10-18 09:45) — stuck 🕸; a fresh dispatch has been in flight since 12:56 today
- price-alert: ATH $82,901.12 held, no new gates; quiet since the 10-19 14:43 alert
- digest: X-signal layer still down — http-400 because XAI_API_KEY is absent from repo secrets; RSS fallback carried 5 headlines
- OpenRouter free cap: 72 used of 50, 0 remaining — the fleet ran with no working LLM path today

*Watch*
- OpenRouter free tier: under $10 lifetime credits = 50 req/day; $10+ = 1,000 req/day, permanent — one-time $10 clears ISS-8 and ISS-11 at the root
- GLM (primary gateway) returning code 1305 overload — with OpenRouter at 0, both legs are degraded simultaneously

*Running today*
- heartbeat @ 08:00 UTC
- github-monitor @ 09:00 UTC
- price-alert @ hourly (00 minutes)
- token-movers @ 12:00 UTC
- digest @ 14:00 UTC
- skill-repair @ reactive