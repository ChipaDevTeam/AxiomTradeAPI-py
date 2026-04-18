---
layout: guide
title: "Release Notes 1.1.3"
description: "Release notes for AxiomTradeAPI-py 1.1.3 with stronger trending endpoint error handling and fallback behavior."
permalink: /release-1-1-3/
---

# Release Notes 1.1.3

## Highlights

Version 1.1.3 strengthens trending token reliability even when the upstream Axiom service is unstable.

### Included improvements

- multi-host failover across Axiom API domains
- smarter retries for transient server and rate-limit issues
- structured error payloads instead of opaque crashes
- cached response fallback when live data is temporarily unavailable
- improved diagnostics including attempted periods, attempted URLs, failing status code, and failing URL

---

## Upgrade

```bash
pip install -U axiomtradeapi
```

---

## Example

```python
result = client.get_trending_tokens("1h")

if result.get("success"):
    print(result.get("count"))
else:
    print(result.get("error"))
```

---

## Related pages

- Trending guide: https://chipadevteam.github.io/AxiomTradeAPI-py/trending-tokens-v2/
- Troubleshooting: https://chipadevteam.github.io/AxiomTradeAPI-py/trending-troubleshooting/
