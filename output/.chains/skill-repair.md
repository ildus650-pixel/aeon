⚠️ skill-repair: token-movers rate-limit diagnosis

skill-repair — REPAIR_DIAGNOSED_NO_FIX
Target: token-movers (open PR #26 exists for rate-limit)
Root cause: OpenRouter free-tier daily quota exhaustion (rate-limit) — NOT XAI API truncation
Fix: Requires operator action — upgrade OpenRouter tier, reduce fleet frequency, or switch model provider
PR: #26 (fix/skill-repair-token-movers-rate-limit-2026-10-10) already addresses correct diagnosis
Issue: ISS-10 updated to category rate-limit
Verify: operator must act on infrastructure level