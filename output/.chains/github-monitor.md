

## Summary

**Skill:** github-monitor — `monitor` view (empty var → all watched repos)

**Watched repos:** `aeonfun/aeon` (from `memory/watched-repos.md`)

**Data collected:**
- **Open PRs:** #1181 `feat(plugin): 0.2.0 - connect to the hosted Aeon MCP server` — draft, opened 2026-10-07 (6d ago), no reviews, no CI failures
- **Open issues:** none (the only open item is the draft PR itself, outside the 24h window)
- **Releases:** `v0.1.0` published 2026-07-09 — outside the 24h window

**Tiers:** ACT_NOW=0, REVIEW=0, INFO=0 — the draft PR is 6 days old (not yet >7d, so it doesn't even reach INFO), and no issues/releases fall in the 24h window.

**Notification:** none sent (silence is the correct signal when every tier is empty).

**Log:** appended to `memory/logs/2026-10-13.md`:
```
### github-monitor
- view: monitor (var="")
ACT_NOW=0 REVIEW=0 INFO=0
sources: aeonfun/aeon=ok
GITHUB_MONITOR_OK repos=1
```

**Note:** `gh` in this environment lacks the `read:org` scope, so `gh pr/issue list --json author` fails on the `login` field. I worked around it by using the REST API (`gh api repos/.../pulls`) which returned the same data. The releases list endpoint also rejected the `url`/`htmlUrl` JSON field names — used `gh api` instead. If the watchlist grows, this scope gap will bite on the `issues` view's `gh search issues` path too; worth adding `read:org` to the token.
