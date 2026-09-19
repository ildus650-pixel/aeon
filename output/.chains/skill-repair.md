*skill-repair — REPAIR_OK_FIXED*
Target: digest (systemic: none — per-skill fix)
Root cause: API gateway rate limit / service overload errors (429, 529) when fetching X signal
Fix: Added 5-second backoff retry for 429/529 errors with fallback to Path B on retry failure (risk: LOW)
PR: https://github.com/ildus650-pixel/aeon/pull/10
Issue: digest-429
Verify: workflow_dispatch skill=digest

🔗 https://github.com/ildus650-pixel/aeon/pull/10