# Long-term Memory
*Last consolidated: never*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-10-17 | India rogue AI agents, Replit ends Anthropic partnership | AI agents, AI partnerships |
| 2026-10-01 | Token Movers — Global Movers | Bitcoin $83,842 (+0.05%) |
| 2026-09-19 | Token Movers — Global Movers | Crypto market scan (winners/losers/trending) |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-10-21 | Digest | PHP2Shell RCE, LiteLLM PyPI compromise, eMudhra CA keys, PAN-OS CVE-2026-0257, Qwen3-Coder bias |
| 2026-10-20 | Digest | Meta Muse 10M downloads, TorchTPU open source, Rust AI gateway Respan |
| 2026-10-19 | Digest | Linux KVM PwnEscape guest-host escape, ConnectWise Cloud Backup breach, Anthropic 5% benefit fund, JPM Coin on Ethereum, Mistral Timestral |
| 2026-10-18 | Digest | Character.AI Disney acquisition, zero-click spyware ads, bankruptcy court cyberattack |
| 2026-10-17 | Digest | India rogue AI agents, Replit Anthropic partnership, self-driving companies, Waymo Canada |
| 2026-10-16 | Digest | Bank of America Mythos patches, password policy resistance |
| 2026-10-15 | Digest | Meta Muse Spark Open model, Rivian AI agents, zero-click spyware via ads |
| 2026-10-14 | Digest | Linux AI-assisted patches, ASML chip demand, AI tells research, Graphicle Rust agents |
| 2026-10-10 | Digest | Anthropic AI control issues, AWS AgentCore security, Shai-Hulud worm targeting AI infrastructure, Chinese hacking tools disrupted |
| 2026-10-09 | Digest | Google agentic AI, OpenAI revenue, Goodfire agent monitors |
| 2026-10-08 | Digest | Nous Research $1.5B, Meta Muse iPad, Microsoft AI PCs, Mecka AI $60M, HealthLeap $38M |
| 2026-10-06 | Digest | Anthropic startup credits, LibreOffice no-AI stance, Wajo agent market |
| 2026-10-04 | Digest | Trump Super Intelligence Force, Japan Garantex sanctions, El Salvador IMF $138M, Russia digital rubles |
| 2026-10-03 | Digest | OpenAI culture crisis, AI czar appointment, Bitcoin surges |
| 2026-10-02 | Digest | Pope AI stance, $300M Nvidia export probe, OpenAI subpoena, FortiMail zero-day |
| 2026-10-01 | Digest | Photon $4.5M agents, Zimbra exploit, RAM shortage |
| 2026-09-30 | Digest | ElevenLabs $22B valuation, Reddit RSS kill, DoorDash AI agent |
| 2026-09-29 | Digest | AMD World Labs acquisition, Bitget hack, Bitcoin Q3 gains |
| 2026-09-28 | Digest | Ember-1, SpaceX Starship, Parley |
| 2026-10-11 | Digest | AI infrastructure attacks, Chromium typosquatting, $111B media merger, Apple HomeView |
| 2026-09-25 | Digest (empty) | Gateway overload, no candidates |
| 2026-09-21 | Digest | Grok 4.7, NASA Mars Sample Return cancelled, CI bottleneck, OpenAI math advisory group |
| 2026-09-19 | Token Movers | AKE +141%, ENA +20%, AVAX +16% breakouts; ZFORGE +4936% trending anomaly |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|

## Lessons Learned
- Digest format: Markdown with clickable links, under 3000 chars
- Always save files AND commit before logging

## Next Priorities
- Buy $10+ OpenRouter credits — one-time purchase lifts the free tier 50→1000 req/day; root cause of ISS-8/ISS-11 and the fleet's 33-46% success rates (see [Gateway Quota](/memory/topics/gateway-quota.md))
- Restore the ambient heartbeat branch on the 08:00 cron — `aeon.yml` sets `var: "brief"`, so P0/P1 checks and the public status page have been dark since 2026-10-14
- Merge PR #27 + #26 — quota trims for price-alert and token-movers; 10 skill-repair PRs open, oldest 10d
- Add `XAI_API_KEY` repo secret (missing; xAI Responses API returns http-400 on every run, meaning the key is present but unusable) — and note that WebSearch also hit the free-models-per-day cap on Oct 21, so RSS/Atom feeds are now the primary source class.

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| BTC (Wrapped BTC, WBTC) | 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 | ethereum |

_Deepest DexScreener pool for this contract: ~$68.8M liquidity (verified 2026-09-19).
price-alert resolves the tracked token from this table; an empty or malformed row
makes the skill exit silently with `PRICE_ALERT_NO_TOKEN`._

- [github-monitor (2026-09-28)](memory/logs/2026-09-28.md) — 1 repo scanned, 1 issue logged
- [github-monitor (2026-10-05)](memory/logs/2026-10-05.md) — 1 repo scanned, no alerts

## Today's Activity
- [token-movers (2026-10-21)](memory/logs/2026-10-21.md) — Global movers: GRX +45.2% (PUMP-RISK), CVX +20.1% (BREAKOUT), PEARL +16.4% (BREAKOUT), ZBCN +11.2%, UB +11.0%; BAT -18.9% (CAPITULATION), BR -13.3% (CAPITULATION), BTW -11.1% (CAPITULATION)
- [price-alert (2026-10-19)](memory/logs/2026-10-19.md) — WBTC new ATH $82,901.12 (prev $82,714.69, 7h47m earlier); ATH alert + set-target prompt sent
- [token-movers (2026-10-16)](memory/logs/2026-10-16.md) — Global movers: tia +16.9% (BREAKOUT), inj +13.5%, fil +9.9%, dot +7.1%; pyth -13.1% (CAPITULATION)
- [price-alert (2026-10-15)](memory/logs/2026-10-15.md) — WBTC ATH observed (baseline), no alerts fired
- [token-movers (2026-10-11)](memory/logs/2026-10-11.md) — Global movers scan: STRK +39.7% (BREAKOUT, 7d +90.5%), AERO +17.1%, INJ +11.3%, NIGHT +10.4%, WLD +8.6%, NEAR +6.6%, APT +6.2%
- [token-movers (2026-10-06)](memory/logs/2026-10-06.md) — Global movers scan: SIF +418.36% (extreme microcap pump, PUMP-RISK), LIT +8.69% (TRENDING+UP), ZRO +10.10% (TRENDING+UP), fluid +22.51%
- [token-movers (2026-10-04)](memory/logs/2026-10-04.md) — Global movers scan: ETHFI +7.11% (top gainer), SI +45.3% (TRENDING+UP microcap), STRK +15.7% (TRENDING+UP L2 breakout)
- [token-movers (2026-10-03)](memory/logs/2026-10-03.md) — Global movers scan: STRK +20.3% (top gainer), SAND +15.6% (metaverse momentum), PUMP +11.3% (meme platform liquid)
- [token-movers (2026-10-02)](memory/logs/2026-10-02.md) — Global movers scan: SUPER CAT +248% (TRENDING+UP extreme pump), SAND +43% (BREAKOUT metaverse), GRX +62% (BREAKOUT deep liquidity)

## Today's Activity
- [price-alert (2026-10-21)](memory/logs/2026-10-21.md) — WBTC new ATH $83,990.54 (prev $83,288.33, 7h50m earlier); ATH alert + set-target prompt sent
- [price-alert (2026-10-21)](memory/logs/2026-10-21.md) — WBTC new ATH $83,220.16 (prev $82,830.98, ~4h earlier); ATH alert sent
- [price-alert (2026-10-21)](memory/logs/2026-10-21.md) — WBTC new ATH $82,830.98 (prev $82,807.77, 163d4h earlier); ATH alert sent
- [price-alert (2026-10-20)](memory/logs/2026-10-20.md) — WBTC current: $8.2808e4 | no gates fired
- [price-alert (2026-10-20)](memory/logs/2026-10-20.md) — WBTC current: $8.2901e4 | ATH announced
- [price-alert (2026-10-20)](memory/logs/2026-10-20.md) — WBTC current: $8.1918e4 | no gates fired
- [heartbeat (2026-10-20)](memory/logs/2026-10-20.md) — Priority brief; root-caused fleet failures to OpenRouter 50/day cap (0 remaining) + GLM 1305 overload; regenerated the 6-day-stale status page
