## Summary

Executed token-movers skill for 2026-11-27:

**Branch**: Movers (default source = CoinGecko)

**Status**: COINGECKO_MARKETS_OVERLOADED — CoinGecko's markets endpoint returned 529 errors (service overloaded), but trending endpoint returned partial data.

**Report content**:
- **Top winners** (from limited trending list): FIGR HELOC (+1.94%), HYPERLIQUID (+0.94%), XRP (+0.63%), SOL (+0.78%), BTC (+0.11%)
- **Top losers**: ETH (−0.33%), BNB (−0.10%)
- **Trending**: PIPI (+492%), WSTAR (+2587%), RAIN (+15.4%), USDC (0.0%), BTC (+1.3%), PEARL (+1.4%), CHUNKEE (−8.2%)
- **Notable signal**: FIGR HELOC trending + winner on 1.94% 24h move with positive 7d bias

**Key observation**: Mixed tape from limited sample — 3 of 5 winners are mid-cap tokens, BTC flat, ETH slight down.

**Constraints encountered**:
- Notification blocked by permission layer (notify command requires approval)
- CoinGecko markets endpoint unavailable — report based only on trending data (10 coins vs full top 250)

**Files modified**:
- `memory/logs/2026-11-27.md` — Added token-movers entry with full run details
- `memory/MEMORY.md` — Updated Recent Articles and Today's Activity sections

**Follow-up needed**: The CoinGecko markets endpoint is consistently overloaded (529 errors). The skill should retry or fall back to alternative sources when CoinGecko is unavailable.
