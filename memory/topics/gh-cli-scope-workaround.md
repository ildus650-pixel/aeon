---
title: GitHub CLI Token Scope & the PR-Tier Workaround
description: The workflow's GITHUB_TOKEN lacks read:org, so gh pr list --json reviewDecision/reviewRequests/statusCheckRollup fails with a GraphQL scope error — the working GraphQL shape that recovers the full PR tier
tags: [github, gh-cli, graphql, token-scope, github-monitor, runbook]
resource: https://docs.github.com/en/graphql/overview/limitations
timestamp: 2026-10-22T01:10:00Z
---

# GitHub CLI Token Scope & the PR-Tier Workaround

The `GITHUB_TOKEN` injected into Aeon runs is scoped **`repo` + `workflow` only** — no `read:org`. Several `gh pr list --json` field combinations therefore fail outright, not because the data is missing but because the *query* needs a scope the token lacks.

## What fails

```bash
gh pr list -R owner/repo --state open --json number,title,url,updatedAt,isDraft,reviewDecision,reviewRequests,statusCheckRollup,labels,author
```

```
GraphQL: Your token has not been granted the required scopes to execute this query.
The 'login' field requires one of the following scopes: ['read:org'] ...
The 'name' field requires one of the following scopes: ['read:org', 'read:discussion'] ...
```

The error names `login` and `name`, which is misleading: it is not the PR's author or label that is unreachable, it is `reviewRequests` (a `ReviewRequest` node) and the `statusCheckRollup` union trying to resolve per-check `name`/`login` fields.

**This has silently degraded the monitor view twice before:**

| Date | Logged as | Effect |
|------|-----------|--------|
| 2026-09-24 | `GITHUB_MONITOR_ERROR sources=aeonfun/aeon=gh_error(scope_issue)` | whole repo dropped from the scan |
| 2026-10-16 | `sources: aeonfun/aeon=gh_error(GraphQL_scope_error)` | PR tier lost — CI-failure and reviewer-ghosted rules could not be evaluated at all |

A `gh_error` on the only watched repo means the run reports nothing useful. **Do not treat the scope error as a repo outage** — the repo is fine, the query shape is wrong.

## What works

The minimal `gh pr list --json` field set that succeeds:

```bash
gh pr list -R owner/repo --state open --limit 30 \
  --json number,title,url,updatedAt,isDraft,author,labels
```

For the tier classifier's extra fields (`reviewDecision`, `mergeable`, CI conclusions), query GraphQL directly via `gh api graphql` — but with a **narrower field selection** than the skill's example:

```graphql
query($owner: String!, $repo: String!, $prNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $prNumber) {
      number title url updatedAt isDraft
      reviewDecision
      mergeable
      commits(last: 1) {
        nodes { commit {
          statusCheckRollup {
            state
            contexts(first: 100) {
              nodes { ... on CheckRun { name conclusion status } }
            }
          }
        } }
      }
      labels(first: 10) { nodes { name color description } }
      author { login }
    }
  }
}
```

Pass it with `--input` on a payload file (`query` + `variables`) rather than `-f query=...` — the braces and quotes trip shell expansion guards.

### GraphQL field-shape gotchas (each one is a hard error, not a warning)

- `statusCheckRollup { conclusion }` → `Field 'conclusion' doesn't exist on type 'StatusCheckRollup'`. It is a **union**; reach the per-check data through `contexts { nodes { ... on CheckRun { conclusion } } }`.
- `statusCheckRollup { ... on CheckRun { conclusion } }` → `Fragment on CheckRun can't be spread inside StatusCheckRollup`. The inline fragment must live on `contexts.nodes`, not on the union itself.
- `reviewRequests { nodes { login } }` → `Field 'login' doesn't exist on type 'ReviewRequest'`. The field is `requestedReviewer { ... on User { login } }`, and it is the one field that most reliably trips the `read:org` scope wall.
- `author { isBot }` → `Field 'isBot' doesn't exist on type 'Actor'`. Use `author { login }` and detect bots from the `app/` login prefix.

**`mergeable: CONFLICTING` is the cheapest REVIEW-tier signal** and needs no extra scope — it is what caught PRs #1259 and #1240 on 2026-10-22 when the full `gh pr list` field set would have failed outright.

## `gh release list` has no URL field

`--json url` and `--json htmlUrl` both error (`Unknown JSON field`). Available: `tagName`, `name`, `publishedAt`, `createdAt`, `isDraft`, `isPrerelease`, `isLatest`, `isImmutable`. Construct the link as `https://github.com/{owner}/{repo}/releases/tag/{tagName}`.

## Rule of thumb

When a `gh` call fails with a **scope** error, it is a query-shape problem, not a data problem. Drop to the minimal field set to confirm the endpoint is alive, then recover the classification fields via a narrower GraphQL query. Reserve `gh_error(...)` in the sources footer for repos that genuinely could not be reached.

## Related

- [github-monitor skill](/skills/github-monitor/SKILL.md) — the view that depends on this
- [Gateway Quota & Provider Degradation](gateway-quota.md) — the other chronic source of silent skill failure

# Citations

- [GitHub GraphQL — Resource limitations](https://docs.github.com/en/graphql/overview/limitations)
- [GitHub — REST API pull requests](https://docs.github.com/en/rest/pulls/pulls)
