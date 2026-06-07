---
layout: guide
title: "Release Notes — v1.1.5"
description: "Cloudflare bypass via Chrome TLS impersonation, automatic token refresh, and WebSocket reliability improvements."
permalink: /release-1-1-5/
---

# Release Notes — v1.1.5

> **Trade on Axiom:** [axiom.trade/@chipadev](https://axiom.trade/@chipadev)  
> **Build bots faster with [ChipaEditor](https://chipaeditor.com/?utm_source=github&utm_medium=docs&utm_campaign=axiomtradeapi&utm_term=release&utm_content=release_1_1_5)** — the AI-powered IDE for DeFi developers.

---

## What's New

### 🛡️ Chrome TLS Impersonation (Cloudflare bypass)

**Problem:** Axiom Trade's WebSocket endpoints sit behind Cloudflare's Bot Management. Python's standard `ssl`/`websockets` stack has a different TLS ClientHello fingerprint (JA3) from Chrome. Cloudflare was rejecting all WebSocket connection attempts with HTTP 502 regardless of cookies or headers.

**Fix:** The WebSocket client now uses [`curl_cffi`](https://github.com/yifeikong/curl-cffi) — a Python binding to libcurl compiled with BoringSSL — to impersonate Chrome 136's exact TLS handshake. This makes the connection indistinguishable from a real browser at the TLS layer.

```python
# Internally uses curl_cffi with impersonate="chrome136"
ws_client = AxiomTradeWebSocketClient(auth_manager=auth_manager)
await ws_client.subscribe_new_tokens(callback)
await ws_client.start()
```

`curl_cffi` is now a required dependency and is installed automatically via pip.

---

### 🔄 Automatic Token Refresh (JWT-aware)

**Problem:** `AuthManager._set_tokens()` previously hardcoded `expires_at = now + 3600`, ignoring the real JWT `exp` claim. Access tokens have a ~16-minute lifetime, so they appeared valid until an hour after loading — and refresh was never triggered.

**Fix:** `_set_tokens()` now parses the JWT payload to extract the actual `exp` and `iat` timestamps. Expired tokens are detected immediately and refreshed automatically before any API call or WebSocket connection.

The token refresh request itself also now uses `curl_cffi` (Chrome TLS) so Cloudflare accepts it.

---

### 🌐 Pre-flight HTTP Warm-up

The WebSocket client now mirrors the browser's behaviour by making two HTTP requests immediately before opening the WebSocket:

1. `GET https://api.axiom.trade/wo/server-time` — establishes the Cloudflare session
2. `GET https://api6.axiom.trade/get-announcement` — secondary warm-up

Both use the same Chrome TLS session, ensuring Cloudflare's `__cf_bm` cookie is correctly associated with the subsequent WebSocket upgrade.

---

### 🔧 Other Fixes

| Area | Fix |
|------|-----|
| WebSocket URL | Removed trailing double-slash (`//` → `/`) that caused 502 on all clusters |
| User-Agent | Updated to Chrome 148 Windows to match `cf_clearance` fingerprint |
| Cluster fallback | Fixed broken fallback logic (old condition `"cluster-usc2" in url` was never true) — now tries cluster3/5/7 on primary failure |
| Logging | Fixed duplicate log lines caused by logger propagation to root handler |
| `subscribe_*` methods | Unified send path; all subscriptions work correctly with the new curl_cffi transport |

---

## New Dependency

```
curl_cffi>=0.7.0
```

Installed automatically. If you manage dependencies manually:

```bash
pip install "curl_cffi>=0.7.0"
```

---

## CF_CLEARANCE Environment Variable

For long-running bots, set `CF_CLEARANCE` in your `.env` file for the most reliable connections:

```env
CF_CLEARANCE=<value from browser DevTools → Application → Cookies → axiom.trade → cf_clearance>
AXIOM_ACCESS_TOKEN=<your access token>
AXIOM_REFRESH_TOKEN=<your refresh token>
```

`cf_clearance` lasts ~30 minutes in a browser session. The SDK will automatically refresh your access token using `curl_cffi`, but `cf_clearance` must be refreshed manually when it expires. A future release will automate this via headless browser integration.

---

## Upgrade

```bash
pip install --upgrade axiomtradeapi
```

---

## Links

- [Trade on Axiom →](https://axiom.trade/@chipadev)
- [ChipaEditor — AI IDE for DeFi →](https://chipaeditor.com/?utm_source=github&utm_medium=docs&utm_campaign=axiomtradeapi&utm_term=release&utm_content=cta)
- [GitHub](https://github.com/ChipaDevTeam/AxiomTradeAPI-py)
- [Discord](https://discord.gg/p7YyFqSmAz)
