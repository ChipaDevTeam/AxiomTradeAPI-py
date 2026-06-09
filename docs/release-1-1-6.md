---
layout: guide
title: "Release Notes — v1.1.6"
description: "Fully automated browser login with Cloudflare Turnstile bypass and optional IMAP OTP auto-reading."
permalink: /release-1-1-6/
---

# Release Notes — v1.1.6

> **Trade on Axiom:** [axiom.trade/@chipadev](https://axiom.trade/@chipadev)  
> **Build bots faster with [ChipaEditor](https://chipaeditor.com/?utm_source=github&utm_medium=docs&utm_campaign=axiomtradeapi&utm_term=release&utm_content=release_1_1_6)** — the AI-powered IDE for DeFi developers.

---

## What's New

### 🌐 Browser-Based Login (Cloudflare Turnstile bypass)

**Problem:** Axiom Trade's login endpoint requires a Cloudflare Turnstile token that can only be generated inside a real browser. Direct API login was blocked server-side.

**Fix:** The SDK now uses [`nodriver`](https://github.com/ultrafunkamsterdam/nodriver) to drive a real Chrome instance for login. Cloudflare Turnstile solves itself automatically inside the browser — no manual intervention required.

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient(
    username="you@example.com",
    password="yourpassword",
)
result = client.login()
# Chrome opens, fills credentials, solves Turnstile, prompts for OTP
```

`nodriver` is an **optional** dependency. Install it with:

```bash
pip install "axiomtradeapi[browser]"
# or
pip install nodriver
```

If `nodriver` is not installed, the SDK falls back to the direct API path (which will fail on axiom.trade due to Turnstile).

---

### 📬 Automatic OTP Reading via IMAP

If you provide IMAP credentials the SDK connects to your inbox, waits for the Axiom OTP email, extracts the 6-digit code, and enters it automatically — the entire login is zero-touch.

```python
client = AxiomTradeClient(
    username="you@example.com",
    password="yourpassword",
)
result = client.login(
    imap_password="your_email_password",  # or Gmail App Password
    imap_user="real@example.com",          # only needed if 'you@' is an alias
)
```

Or via environment variables:

```env
AXIOM_EMAIL=you@example.com
AXIOM_PASSWORD=yourpassword
AXIOM_IMAP_PASSWORD=your_email_password
AXIOM_IMAP_USER=real@example.com        # omit if not using an alias
```

**Supported email providers** (auto-detected from domain):

| Provider | IMAP host (auto) |
|----------|-----------------|
| Gmail | `imap.gmail.com` |
| Outlook / Hotmail / Live | `outlook.office365.com` |
| Yahoo | `imap.mail.yahoo.com` |
| iCloud | `imap.mail.me.com` |
| ProtonMail | `imap.protonmail.com` |
| Hostinger | `imap.hostinger.com` |
| Other | `imap.hostinger.com` (override with `AXIOM_IMAP_HOST`) |

> **Gmail with 2FA:** use an [App Password](https://myaccount.google.com/apppasswords) instead of your regular password.

---

### 💾 Persistent Token Storage — Login Once, Run Forever

After a successful browser login, tokens are saved to encrypted local storage (`~/.axiomtradeapi/`). On every subsequent run the SDK loads and auto-refreshes them — no browser launch, no OTP.

```python
# First run: browser opens, you (or IMAP) enter the OTP
result = client.login(imap_password="...")

# All future runs: instant, no browser
client = AxiomTradeClient(username="you@example.com", password="yourpassword")
# tokens loaded from disk and refreshed automatically
```

---

### 🔧 Other Fixes

| Area | Fix |
|------|-----|
| `client.login()` | Syncs new tokens into the HTTP session after login |
| `client.login()` | Dead `return login_result` after the return statement removed |
| `AxiomTradeClient` | `cf_clearance`, `imap_password`, `imap_user`, `imap_host` params added |
| Browser window | Minimized automatically after launch so terminal stays accessible |

---

## Full Login Example

```python
import os
from dotenv import load_dotenv
from axiomtradeapi import AxiomTradeClient

load_dotenv()

client = AxiomTradeClient(
    username=os.getenv("AXIOM_EMAIL"),
    password=os.getenv("AXIOM_PASSWORD"),
)

# login() is only needed the first time (or after refresh token expires).
# Subsequent runs skip this entirely — saved tokens are used automatically.
result = client.login(
    imap_password=os.getenv("AXIOM_IMAP_PASSWORD"),
    imap_user=os.getenv("AXIOM_IMAP_USER"),   # omit if not an alias
)

if result["success"]:
    balance = client.GetBalance("YOUR_WALLET_ADDRESS")
    print(balance)
```

---

## Upgrade

```bash
pip install --upgrade axiomtradeapi
pip install "axiomtradeapi[browser]"   # adds nodriver for browser login
```

---

## Links

- [Trade on Axiom →](https://axiom.trade/@chipadev)
- [ChipaEditor — AI IDE for DeFi →](https://chipaeditor.com/?utm_source=github&utm_medium=docs&utm_campaign=axiomtradeapi&utm_term=release&utm_content=cta)
- [GitHub](https://github.com/ChipaDevTeam/AxiomTradeAPI-py)
- [Discord](https://discord.gg/p7YyFqSmAz)
