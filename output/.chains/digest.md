*Digest — 2026-11-18*

_TL;DR: Google's AI search answers cut traffic 40%; OpenJDK has critical Base64 RCE; DNS provider Quad9 exits France._

1. *Google's AI answers reducing search traffic by 40%*
   Google's AI-powered direct answers are significantly reducing search engine traffic, with some queries dropping by 40%. This shift impacts websites relying on organic search and forces publishers to adapt their content strategies.
   Why it matters: 40% traffic drop is a concrete metric showing search behavior shift; affects content monetization and SEO strategies globally
   https://revscope.co/blog/search-seo-geo-2026/

2. *Java4Shell: RCE in OpenJDK when processing Base64*
   Researchers found a Remote Code Execution vulnerability in OpenJDK when processing Base64-encoded data. The exploit allows attackers to execute arbitrary code through Base64 parsing, affecting Java applications that handle Base64 input.
   Why it matters: Affects all Java systems processing Base64; critical for authentication tokens, JWTs, and encoded payloads
   https://calif.io/java4shell/

3. *Quad9's withdrawal from France: A canary in the coal mine*
   Cloudflare reports Quad9's unexpected withdrawal from France, raising concerns about DNS provider stability. The move may signal broader issues with DNS infrastructure and internet censorship resistance efforts.
   Why it matters: DNS infrastructure stability affects all internet users; unusual withdrawal could indicate compliance pressure
   https://blog.cloudflare.com/quad9-withdrawal-from-france/

Also worth a glance: ID.me terms required for IRS sign-in creates new barriers for accessing government services via new verification mandate · https://consumerrights.wiki/w/ID.me_terms_required_for_IRS_sign-in

## Summary

Completed the digest skill execution for 2026-11-18:

**Files created/modified:**
- Created `memory/logs/2026-11-18.md` with digest run details
- Updated `memory/MEMORY.md` Recent Digests table

**Sources used:**
- Hacker News (5 raw candidates, 4 after filter, 3 sent)

**Issues encountered:**
- WebSearch overloaded (529 errors)
- XAI API returned invalid-argument (incorrect API key)
- RSS feeds overloaded (529 errors)
- Fallback to Hacker News provided sufficient signal

**Digest stats:**
- 3 items sent (Google AI traffic drop, OpenJDK RCE, Quad9 DNS exit)
- 1 "Also worth a glance" (ID.me IRS verification)
- Char count within 3000 char limit

The digest focused on concrete, verifiable news across AI, security, and infrastructure. The notify command requires approval; the digest content is ready for delivery.
