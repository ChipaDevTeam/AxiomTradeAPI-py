---
layout: guide
title: "Trending Tokens V2 Guide"
description: "Guide for the new trending endpoint, normalized response format, and fallback behavior in AxiomTradeAPI-py."
permalink: /trending-tokens-v2/
---

# Trending Tokens V2 Guide

## Overview

AxiomTradeAPI-py now uses the new Axiom trending endpoint:

- Endpoint: https://api3.axiom.trade/new-trending-v2
- Supported periods commonly include 5m, 1h, 6h, 24h, and 7d
- The SDK normalizes the raw array response into a dictionary-based token list for easier use

---

## Basic Usage

```python
from axiomtradeapi import AxiomTradeClient
import os

client = AxiomTradeClient(
    auth_token=os.getenv("AXIOM_ACCESS_TOKEN"),
    refresh_token=os.getenv("AXIOM_REFRESH_TOKEN")
)

trending = client.get_trending_tokens("1h")
print(f"Found {len(trending.get('tokens', []))} tokens")
```

---

## Response Format

The SDK returns a backward-compatible dictionary with these keys:

- tokens: normalized list of token dictionaries
- data: alias of the normalized token list
- timePeriod: actual period returned by the server
- requestedTimePeriod: the period you asked for
- fallbackUsed: whether a safer fallback period was used
- attemptedTimePeriods: the periods tried in order
- endpoint: always set to new-trending-v2

Example:

```python
result = client.get_trending_tokens("24h")

print(result["requestedTimePeriod"])
print(result["timePeriod"])
print(result["fallbackUsed"])
print(result["attemptedTimePeriods"])
```

---

## Why fallback may happen

Axiom occasionally returns transient 500 errors for some time ranges even while authentication is valid. When that happens, the SDK now:

1. Retries the same request automatically
2. Refreshes session state when needed
3. Falls back to the nearest stable period

This makes the call much more reliable for live bots and dashboards.

---

## Common fields in each token

Normalized token entries may include fields such as:

- pairAddress
- tokenAddress
- tokenName
- tokenTicker
- imageUrl
- createdAt
- website
- twitter
- liquidityUsd
- priceUsd
- priceChange5m
- priceChange1h
- priceChange24h
- holderCount
- marketCapUsd

Because the upstream payload is array-based and may evolve, the SDK also preserves the original row under raw.

---

## Automatic session initialization

The client now attempts a browser-style bootstrap automatically before trending calls. This reduces failures in environments where Axiom expects the user to be registered as an active browser session.

You can still call client.connect manually if you want to prewarm the session yourself.

## Best practice

For production bots, prefer checking fallbackUsed before making timeframe-sensitive decisions:

```python
result = client.get_trending_tokens("7d")

if result.get("fallbackUsed"):
    print("Using fallback data due to upstream instability")
```
