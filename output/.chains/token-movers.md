## Summary

I've successfully executed the **token-movers** skill with an empty `var` (default movers on CoinGecko). Here's what was accomplished:

### Data Fetched
- **250** coins from CoinGecko markets API
- **7** trending coins from CoinGecko search endpoint
- Applied filters: removed stablecoins and illiquid tokens (< $1M volume)
- **200** coins passed filters

### Key Findings (2026-10-19)

**Top Winners (24h):**
1. BR (+40.4% / 7d +49.3%) — BREAKOUT tag
2. GRX (+32.0% / 7d +0.9%) — PUMP-RISK
3. CARDS (+18.6% / 7d +3.6%) — 
4. S (+15.4% / 7d +2.6%) — 
5. VVV (+13.9% / 7d +5.0%)

**Top Losers (24h):**
1. BTW (-16.4% / 7d +18.7%) — 
2. RAIL (-7.7% / 7d -26.8%)
3. ULTIMA (-3.6% / 7d -8.4%)

**Market Pulse:** Mixed tape — 86/100 top coins are green, median ±2.6%

**Notable:**
- BR extreme microcap pump with BREAKOUT tag
- GRX low liquidity pump (PUMP-RISK)
- Q extreme 7d anomaly (+361.9%)

### Files Created/Modified
- **Report:** `/tmp/token-movers-report.md` (1,907 chars)
- **Log:** `memory/logs/2026-10-19.md` (appended token-movers section)

### Status
- **Notification sent** (requires approval to proceed through workflow)
- **No repeat runners** detected from past 2 days
- **Force-reply offer ready** but skipped (SLEEPY session threshold not met — we had 10 winners, so this is fine)

The skill has completed its primary task of scanning and reporting on crypto movers.
