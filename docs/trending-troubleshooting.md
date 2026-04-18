---
layout: guide
title: "Trending Endpoint Troubleshooting"
description: "Fixes for 404 and 500 errors when calling get_trending_tokens in AxiomTradeAPI-py."
permalink: /trending-troubleshooting/
---

# Trending Endpoint Troubleshooting

## Common error: 500 Internal Server Error

You may see an error like this:

```python
Exception: Failed to get trending tokens: 500 Server Error
```

This is usually caused by temporary instability in the upstream Axiom trending service for a specific time range.

### What changed in the SDK

The latest release adds:

- automatic retries
- session reinitialization when needed
- fallback to a working time period

---

## Common error: 404 Not Found

If you were using an older version of the package, the client may still have been pointing to the retired trending endpoint.

### Fix

Upgrade to the latest version:

```bash
pip install -U axiomtradeapi
```

---

## Recommended usage

```python
from axiomtradeapi import AxiomTradeClient
import os

client = AxiomTradeClient(
    auth_token=os.getenv("AXIOM_ACCESS_TOKEN"),
    refresh_token=os.getenv("AXIOM_REFRESH_TOKEN")
)

result = client.get_trending_tokens("1h")
print(result.get("count", len(result.get("tokens", []))))
```

---

## How to inspect fallback behavior

```python
result = client.get_trending_tokens("24h")

print("requested:", result.get("requestedTimePeriod"))
print("actual:", result.get("timePeriod"))
print("fallback:", result.get("fallbackUsed"))
print("attempted:", result.get("attemptedTimePeriods"))
```

---

## If issues continue

1. Verify your access token and refresh token are valid
2. Upgrade to the latest package release
3. Try 1h or 5m first to confirm upstream availability
4. Retry after a short delay if the Axiom API is unstable

If your bot depends on strict timeframe fidelity, check fallbackUsed and handle that case explicitly.
