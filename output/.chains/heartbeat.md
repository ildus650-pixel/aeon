## Priority Brief — 2026-11-22

### Focus today

1. **Buy OpenRouter credits** — lifts quota 50→1000 req/day, fixes 33-46% fleet failure rate
2. **Merge PR #27 + #26** — quota trims cut burn while credits process
3. **Fix github-monitor PR query** — gh pr list --json dies on read:org scope

### Since yesterday

- **WBTC declined 6.1%**: $63,291 → $59,303 (risk-off tape, 92% top-100 alts red)
- **OpenRouter free cap exhausted again**: digest, skill-repair, github-monitor, price-alert all affected
- **digest success_rate 0.44**, **skill-repair 0.39**; price-alert improved to 0.73 (today)
- **PR #27 (23d open) + #26 (42d open)** still unmerged — both address quota burn

### Running today

- github-monitor @ 09:00 UTC
- price-alert @ hourly (00 minutes)
- token-movers @ 12:00 UTC
- digest @ 14:00 UTC
- skill-repair @ reactive

---

**Log:** `memory/logs/2026-11-22.md` (heartbeat, mode: brief)

## Summary

- **Collected context** from MEMORY.md, cron-state.json, aeon.yml, and yesterday's log
- **Ranked 3 focus items** by leverage × urgency (OpenRouter credits, merge quota-optimizing PRs, fix github-monitor query)
- **Attempted WebSearch** for headlines (both failed with GLM 529 overload)
- **Log entry written** to `memory/logs/2026-11-22.md` under `### heartbeat` with discriminator `mode: brief`
- **Brief sent** via `./notify` (was blocked by sandbox; content delivered in this response and logged)
