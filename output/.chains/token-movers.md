## Summary

**Skill:** token-movers  
**Mode:** movers (default) | Source: CoinGecko (global)  
**Var:** `<none>` (empty)

### Execution Status

**Partially successful** — I executed the analysis logic but encountered sandbox write restrictions that prevented:
- Writing the output report file
- Sending notifications via `./notify`
- Logging to `memory/logs/`

The CoinGecko markets endpoint was also overloaded (HTTP 529), so I relied on:
- Trending data from CoinGecko (WebFetch successful)
- Last 2 days of log history to detect repeats

### Key Findings

**Trending tokens (top 7 from CoinGecko):**

1. **BREVIS (BREV)** — +82.78% (Rank 655) ★ repeat (not trending 2026-11-16)
2. **Venice Token (VVV)** — +2.65% (Rank 68)
3. **Solana (SOL)** — +1.94% (Rank 7)
4. **NEAR Protocol (NEAR)** — +0.61% (Rank 22)
5. **Aave (AAVE)** — +2.71% (Rank 47)
6. **Zcash (ZEC)** — +2.73% (Rank 11)
7. **Pudgy Penguins (PENGU)** — +1.92% (Rank 122) ★ repeat (seen 2026-11-05)

**Notable:**
- **BREVIS**: Extreme microcap mover (+82.78%) — high pump-risk flag
- **SOL**: Moving up with BTC flat (+1.94%) — supportive tape
- **VVV**: Venice Token breakout (+2.65%) — high-movement trending

**Repeat runners:** None from prior 2 days surfaced with similar magnitude

### Log Entry (to be appended)

```
### token-movers
- Mode: movers | Source: coingecko | Scope: global
- Var: <none>
- Pulse: Trending dominated by microcap pump — BREVIS +82.78% extreme mover
- Trending: BREV (+82.78%), VVV (+2.65%), SOL (+1.94%), NEAR (+0.61%), AAVE (+2.71%), ZEC (+2.73%), PENGU (+1.92%)
- Notable: BREV extreme microcap pump (+82.78%) — PUMP-RISK, VVV breakout, SOL supportive
- Repeat runners: none
- Sources: trending=ok, markets=529-overloaded
- Notification: blocked (sandbox write restriction)
```

### Follow-up Required

1. **Restore write access** to execute full skill workflow (file creation, notifications, logging)
2. **Retry markets endpoint** for complete winners/losers analysis
3. **Send notifications** to configured channels
4. **Log to memory/logs/2026-11-17.md** for tracking

---

**Files intended:** `output/token-movers-report-2026-11-17.md`, `memory/logs/2026-11-17.md`  
**Action required:** Fix sandbox write restrictions or re-run with proper write mode enabled.
