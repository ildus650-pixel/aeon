# Summary

## What I did

Executed the **token-movers** skill (mode: **movers / coingecko / global**, var empty) as defined in `skills/token-movers/SKILL.md`. The full run:

1. **Fetched data** — CoinGecko markets (250 coins, top-by-market-cap with 1h/24h/7d changes) and search trending, via `./secretcurl` (keyless public endpoints, `{COINGECKO_API_KEY:+x}` placeholder pattern).

2. **Filtered** — excluded 15 fiat-pegged stablecoins (`tether`, `usd-coin`, `dai`, etc.), symbols starting with USD/EUR/GBP, and coins with 24h total_volume < $1M. Result: 135 coins passed the filter from 250 listed.

3. **Ranked** — sorted filtered coins by 24h % change:
   - **Top 10 winners** (highest 24h %): ICNT +28.4%, BTW +22.2%, LUNC +10.9%, SN51 +4.0%, GRASS +3.8%, USELESS +3.6%, AKT +3.5%, GENIUS +3.5%, SENT +3.2%, PUMP +2.8%
   - **Top 10 losers** (lowest 24h %): BP −15.7%, PIEVERSE −13.0%, BR −7.7%, ZRO −7.1%, KMNO −6.6%, SKY −6.6%, M −6.5%, ENA −6.0%, PI −5.8%, BDX −5.4%
   - **Top 7 trending**: BTC, PEARL, ZEC, VVV, BP, ETH, XRP

4. **Tagged** each entry with at most 2 tags per coin per the skill's rule set: [BREAKOUT], [FADE], [TRENDING+UP], [TRENDING+DOWN], [CAPITULATION], [PUMP-RISK], [MICROCAP], [MAJOR]. ICNT earned [BREAKOUT]; BP and PIEVERSE earned [TRENDING+DOWN]; VVV earned [TRENDING+UP].

5. **Market pulse** — one sentence: "Risk-off tape — only 30 of top 100 coins green, median top-50 move −0.69%; large-cap DeFi and L1 names (ZRO, ENA, KMNO, SKY) lead the slide." (This reflects the flip from yesterday's 60% green / risk-on to today's 30% green / risk-off.)

6. **Notable section** (qualified: ICNT [BREAKOUT] + VVV [TRENDING+UP] tags present):
   - ICNT: [BREAKOUT] +28.4% with 7d +55.6% on $36M vol — sustained small-cap move; not a flash pump
   - PIEVERSE: yesterday's trending PUMP-RISK leader (+61%) reversed to −13% today on $109M vol — the pump faded
   - PEARL: trending again but now −4% (was +22% yesterday) — momentum reversed across the board
   - VVV: only green name in trending (+0.9%) — a rare spot of bid on a red tape

7. **Sent digest** via `./notify -f /home/runner/work/aeon/aeon/tmp_tm_report.md` (queued to all configured channels: Telegram, Discord, Slack, Buzz, Resend email; json-render feed pending).

8. **Sent deep-dive offer** via `./notify "Want a deep-dive report on a mover? Reply with a ticker or contract." --force-reply --placeholder "e.g. WIF" --context "token-movers::deep-dive"` (dedup check: no prior FORCE_REPLY_OFFERED: deep-dive marker dated 2026-11-19, so offer sent).

9. **Appended log** to `memory/logs/2026-11-19.md` under `### token-movers` entry with all structured fields (mode, source, var, pulse, winners/losers/trending, notable, FORCE_REPLY_OFFERED: deep-dive marker).

10. **Updated MEMORY.md** — added token-movers (2026-11-19) to Today's Activity section.

## Files created/modified

| File | Action |
|------|--------|
| `tmp_tm_scan.py` | Created (helper script for data processing) |
| `tmp_tm_report.md` | Created (movers digest markdown report) |
| `memory/logs/2026-11-19.md` | Appended `### token-movers` entry |
| `memory/MEMORY.md` | Added token-movers (2026-11-19) to Today's Activity |
| `output/summary.md` | Created summary artifact |

Note: `tmp_tm_scan.py` and `tmp_tm_report.md` are in the working directory and are temporary artifacts. They are not committed to the repo.

## Follow-up actions

- **Deep-dive offer** is live on Telegram/Discord/Slack — operator can reply with a ticker or contract for a single-token deep report (this skill re-dispatches via rule 0).
- **Monitor runners** (GeckoTerminal branch) on future 2026-11-20 run if cron resumes — today was coingecko movers only.
- **Deep-dive dedup** — next token-movers run (tomorrow) will skip the force-reply offer since FORCE_REPLY_OFFERED: deep-dive marker will already be dated 2026-11-19.
- **Skills cleanup** — the `tmp_tm_scan.py` and `tmp_tm_report.md` can be left as temp artifacts; they do not persist between runs (read-only skills revert stray writes, but these are write-mode artifacts).
- **XAI_API_KEY** — currently set but returns http-400 on every run; noted in MEMORY.md for context (xAI Responses API unusable, so xai=skip in future token reports).
- **OpenRouter credits** — still needed to lift fleetwide quota from 50→1000 req/day (ISS-8/ISS-11, 33-46% success rates); tracked in heartbeat brief.