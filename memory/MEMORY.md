# Long-term Memory
*Last consolidated: never*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-09-19 | Token Movers — Global Movers | Crypto market scan (winners/losers/trending) |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-09-19 | Token Movers | AKE +141%, ENA +20%, AVAX +16% breakouts; ZFORGE +4936% trending anomaly |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Use `skill-repair` for systematic troubleshooting: Preflight → Triage → Diagnose → Repair → Verify → Log

## Issues Fixed (skill-repair)
- **digest-429** (2026-09-19): Added retry logic for API rate limit / service overload (429, 529) errors with 5-second backoff; digest now survives transient gateway errors instead of failing immediately

## Next Priorities
- Configure notification channels (Telegram, Discord, or Slack)
- Run first digest

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| BTC (Wrapped BTC, WBTC) | 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 | ethereum |

_Deepest DexScreener pool for this contract: ~$68.8M liquidity (verified 2026-09-19).
price-alert resolves the tracked token from this table; an empty or malformed row
makes the skill exit silently with `PRICE_ALERT_NO_TOKEN`._
