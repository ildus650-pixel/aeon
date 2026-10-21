import urllib.request, ssl, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://www.wiz.io/blog/php2shell-php-rce",
    "https://www.php.net/index.php",
    "https://news-web.php.net/php.announce/509",
    "https://patchtheplanet.org/",
    "https://safedep.io/litellm-pypi-compromise-credential-stealer-backdoor/",
    "https://emudhra.we-have-a-problem.com/",
    "https://www.theregister.com/security/2026/10/20/indian-certification-authority-emudhras-private-keys-compromised-one-of-them-was-the-number-4/5304312",
    "https://www.theregister.com/cyber-crime/2026/10/20/palo-altos-firewall-os-has-been-under-attack-from-multiple-ransomware-groups-since-june/5304226",
    "https://techcrunch.com/2026/10/20/anthropic-pitches-ai-safety-bill-that-may-block-a-model-if-50-people-could-be-killed/",
    "https://mistral.ai/news/voxtral-3/",
    "https://www.hirundo.io/blog/qwen3-coder-vulnerabilities",
    "https://www.theregister.com/security/2026/10/20/deepseek-deep-sixed-at-all-us-federal-civilian-agencies/5304010",
    "https://github.com/deepseek-ai/DeepInfer",
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (compatible; aeon-digest)"})
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            print(r.status, u)
    except Exception as e:
        code = getattr(e, "code", None)
        print(code if code else "ERR", u, str(e)[:80])
