**Token Movers run completed** — duplicate signal detected.

## Summary

**Preamble:**
- Read `memory/MEMORY.md` for context
- Scanned last 2 days of logs: found identical movers reported both Nov 4 and Nov 5
- `var` was empty → mode=movers, source=coingecko (global)

**Analysis:**
The same movers were already reported:
- **Winners:** CAP (+32.2%), FLUID (+27.6%), DGAI (+26.1%), DRV (+19.8%), BEAM (+18.0%)
- **Losers:** YELLOW (-21.8%), TRUMP (-16.8%), RAIN (-7.3%), STABLE (-3.5%), GOMINING (-3.5%)
- **Trending:** PENGU, TRUMP, NEAR, BTC
- **Notable:** [PUMP-RISK] on CAP, [CAPITULATION] on TRUMP

**Action:**
- Skipped notification (duplicate signal from prior days)
- Log entry would be appended to `memory/logs/2026-11-05.md`, but write access is restricted in this environment

**Follow-up needed:** None — the skill correctly identified no new signal to surface.
