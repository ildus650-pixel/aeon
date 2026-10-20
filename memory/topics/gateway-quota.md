---
title: Gateway Quota & Provider Degradation
description: Root cause of Aeon's chronic skill failures — OpenRouter free-tier 50 req/day cap plus GLM 1305 overload leaves the fleet with no working LLM path
tags: [infrastructure, openrouter, glm, rate-limit, root-cause]
resource: https://openrouter.ai/docs/api_reference/limits
timestamp: 2026-10-20T13:27:00Z
---

# Gateway Quota & Provider Degradation

The fleet's chronic failures (digest 0.33, skill-repair 0.38, heartbeat 0.41, token-movers 0.46 success rates) are **not** per-skill code defects. They share one upstream cause: the LLM gateway legs are both degraded simultaneously.

## Verified state (2026-10-20)

| Leg | Role | State | Evidence |
|-----|------|-------|----------|
| `api.z.ai` (GLM-4.7-Flash) | primary | `http-429`, error code `1305` "service may be temporarily overloaded" | live POST to `/api/paas/v4/chat/completions` |
| `openrouter/free` | failover | `http-429`, free tier exhausted | live POST to `/api/v1/chat/completions` |

`GATEWAY_ORDER` is `glm openrouter` — so when GLM returns 1305 the fleet falls through to OpenRouter, which is simultaneously at its cap. Neither leg can carry a run.

## The OpenRouter cap (the real root cause)

`GET https://openrouter.ai/api/v1/key` returns:

```json
{"is_free_tier": true,
 "free_model_daily_requests": {"used": 72, "limit": 50, "remaining": 0}}
```

The cap is **50 requests/day** — the tier for accounts with **under $10 in all-time purchased credits**. Once **$10+** is purchased *at any point*, the daily cap rises to **1,000 requests/day** and stays there even if the balance later drops below $10.

**This is the highest-leverage fix in the fleet**: a one-time $10 purchase multiplies capacity 20× and permanently clears the quota exhaustion behind ISS-8, ISS-11, and the shared root cause of ISS-1.

Check remaining quota at any time:
```bash
./secretcurl -s "https://openrouter.ai/api/v1/key" -H "Authorization: Bearer {OPENROUTER_API_KEY}"
```

## Why the cadence PRs are not the fix

PRs #26 (token-movers retry/backoff) and #27 (price-alert → 2-hourly) reduce *consumption*, but the binding constraint is a 50/day ceiling shared by every skill. Backoff sleeps do not help a hard daily cap. Trimming cadence buys headroom; buying credits raises the ceiling.

## Distinguishing the failure classes

- `429` with `"error_type": "rate_limit_exceeded"` and `free_model_daily_requests.remaining == 0` → **daily cap exhausted**, waits until the UTC reset.
- `429` with code `1305` from Z.AI → **provider overload**, transient, retry may succeed.
- Errors citing `modelUsage.openrouter/free` inside a larger truncated payload → the run died on the failover leg.

## Related

- Tracked token: BTC/WBTC (see [MEMORY.md](/memory/MEMORY.md))
- Open issues: ISS-8, ISS-11 (rate-limit), ISS-1 (gateway-outage)

# Citations

- [OpenRouter — API Credit & Rate Limits](https://openrouter.ai/docs/api_reference/limits)
- [OpenRouter — Pricing](https://openrouter.ai/pricing)
- [OpenRouter — FAQ](https://openrouter.ai/docs/faq)
- [OpenRouter — Help Center: Rate Limits](https://openrouter.zendesk.com/hc/en-us/articles/39501163636379)
