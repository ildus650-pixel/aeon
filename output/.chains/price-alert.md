I've read the `skills/price-alert/SKILL.md` skill file. Here's a summary of what it does:

**Price Alert Skill** — Fires a same-day notification when a tracked token makes a significant move. Three trigger classes:
1. **New all-time high (ATH)** — logs the new ATH regardless of size
2. **Sharp 1h move (±20%)** — detects a large hourly price swing
3. **Operator-set target crossing** — fires when price hits user-specified USD levels

**How it works:**
- Reads the tracked token from `memory/MEMORY.md`
- Fetches the current price via DexScreener API (with WebFetch fallback)
- Evaluates three gates against stored state in `memory/topics/price-alert-state.json`
- Sends notifications via `./notify` only when gates fire
- Dedupes alerts to one per event type per 4 hours
- One-shot target alerts per side (won't refire if price wobbles back)
- Baseline alert suppressed on first run after token init or state reset
- Atomic, validated state writes with backups; rolling log entries per run

**Key constraints:**
- Liquid-pool selection only (deepest liquidity pair on configured chain is canonical mark)
- Absolute USD for targets (not percentages)
- Sign of H1 change is interpreted literally ("buyer wave" vs "selling pressure") — no external TA commentary
- State writes are atomic + validated; corrupt writes restore from `.bak`

**Configuration option:** The `${var}` frontmatter field accepts comma-separated `target_price` levels (e.g., `0.000005`), or `dry-run` to suppress notifications while still updating state, or `set-target:<price>` for force-reply targeting.

This skill appears to be the crypto price alert capability within the Aeon agent framework. Would you like me to adjust anything about this skill's configuration, or is there a specific task you'd like me to perform using this skill?
