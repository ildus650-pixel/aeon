I've read the token-movers skill. This skill supports multiple modes controlled by the `${var}` parameter:

1. **Movers scan** (default) — Top winners, losers, trending from CoinGecko OR on-chain runners from GeckoTerminal
2. **Single-token deep report** — Verdict-first deep analysis of one token

To execute the skill, I need to know what you'd like me to run. Please specify one of:

- **Empty or unspecified** → Global movers scan on CoinGecko (top 250, winners/losers/trending)
- `coingecko` → Global movers scan on CoinGecko
- `geckoterminal` → On-chain runners scan across all major networks (Solana, Ethereum, Base, BSC, Arbitrum)
- `geckoterminal:<chain>` (e.g., `geckoterminal:base`, `geckoterminal:solana`) → Runners on that specific chain
- `category:<name>` (e.g., `category:layer-2`, `category:meme`) → CoinGecko movers scoped to that category
- `<contract>` (e.g., `0xabc…`) or `<contract>:<chain>` → Single-token deep report
- `<SYMBOL>` (e.g., `WIF`, `SOL`) → Single-token deep report (will resolve symbol to contract)
- `token` or `single-token` → Single-token report on the token configured in `memory/token-report.md`
- `deep-dive:<text>` → Single-token report (from Telegram force-reply)

What would you like me to run?
