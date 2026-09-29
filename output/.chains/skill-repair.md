skill-repair — REPAIR_DIAGNOSED_NO_FIX
Target: skill-repair
Root cause: Systemic API degradation from GLM Gateway (HTTP 529 service overload)
Fix: Requires operator action — API instability is upstream, not a code problem. Open PRs (#19 token-movers, #18 price-alert) exist but require manual merge to reduce failure rates.
Issue: #12