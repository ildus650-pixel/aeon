skill-repair — REPAIR_DIAGNOSED_NO_FIX
Target: digest
Root cause: api.z.ai gateway overloaded (529 Service Temporarily Unavailable) — external infrastructure issue, not fixable in skill code
Fix: requires operator action — wait for gateway recovery or implement failover/retry logic
Issue: ISS-1
Verify: monitor gateway status; re-run skill-repair with var=digest after service recovers