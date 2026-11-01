I see you've invoked the price-alert skill, but I'm currently in **read-only mode**. The skill requires write access to:

1. Read and write the `memory/topics/price-alert-state.json` file
2. Create log entries in `memory/logs/${today}.md`
3. Send notifications via `./notify`

Would you like me to switch to **write mode** so I can execute this skill properly? The skill will:

- Monitor the tracked token (WBTC on Ethereum)
- Check for new ATH, sharp 1h moves (±20%), and target crossings
- Send notifications only when gates fire
- Update state to avoid duplicate alerts

Or if you have a specific task in mind (like parsing a special `var` value), please let me know what you'd like me to do!
