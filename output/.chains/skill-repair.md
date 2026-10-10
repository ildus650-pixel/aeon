*skill-repair — REPAIR_OK_FIXED*

Target: token-movers

Root cause: Claude Code free model quota exhaustion (429 free-models-per-day) after 37 turns, 1.7M input tokens

Fix: Compressed preamble (removed verbose examples), reduced log history from 30 days to 7 days, condensed formatting rules, shortened inline comments. Expected token reduction: ~40-50% (1.7M → ~0.8-1M tokens).

PR: https://github.com/ildus650-pixel/aeon/pull/26

Verify: workflow_dispatch skill=token-movers