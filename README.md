# AxiomTradeAPI-py

<div align="center">

[![PyPI version](https://badge.fury.io/py/axiomtradeapi.svg)](https://badge.fury.io/py/axiomtradeapi)
[![Version](https://img.shields.io/badge/version-1.1.6-blue)](https://chipadevteam.github.io/AxiomTradeAPI-py/release-1-1-6/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://chipadevteam.github.io/AxiomTradeAPI-py)
[![Trade on Axiom](https://img.shields.io/badge/Trade%20on-Axiom-blue)](https://axiom.trade/@chipadev)
[![ChipaEditor](https://img.shields.io/badge/Built%20with-ChipaEditor-orange)](https://chipaeditor.com/?utm_source=github&utm_medium=readme&utm_campaign=axiomtradeapi&utm_term=badge&utm_content=shield)

**The Professional Python SDK for Solana Trading on Axiom Trade**

*Build advanced trading bots, monitor portfolios, and automate Solana DeFi strategies with enterprise-grade reliability*

[📚 **Documentation**](https://chipadevteam.github.io/AxiomTradeAPI-py) • [🚀 **Quick Start**](#quick-start) • [💬 **Community**](https://chipatrade.com/community) • [🛒 **Bot Development Services**](https://chipatrade.com/services/bot-development) • [🔗 **Trade on Axiom**](https://axiom.trade/@chipadev)

</div>

---

## 🌟 Why AxiomTradeAPI-py?

AxiomTradeAPI-py is the **most comprehensive Python library** for Solana trading automation, trusted by professional traders and DeFi developers worldwide. Whether you're building trading bots, portfolio trackers, or DeFi analytics tools, our SDK provides everything you need.

### ⚡ Key Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| 🚀 **Real-time WebSocket** | Sub-millisecond token updates | Token sniping, live monitoring |
| 📊 **Portfolio Tracking** | Multi-wallet balance monitoring | Portfolio management, analytics |
| 🤖 **Trading Automation** | Advanced bot frameworks | Automated trading strategies |
| 🔐 **Enterprise Security** | Production-grade authentication | Secure API access |
| 📈 **Market Data** | Comprehensive Solana market info | Price feeds, volume analysis |
| 🛡️ **Risk Management** | Built-in trading safeguards | Position sizing, loss limits |

## 🆕 What's New in v1.1.6

- **Browser-based login** via `nodriver` — drives real Chrome to bypass Cloudflare Turnstile automatically. No manual steps required.
- **IMAP OTP auto-reading** — provide your email password and the SDK reads the 6-digit OTP from your inbox and enters it automatically. Full zero-touch login.
- **Login-once, run-forever** — tokens saved to encrypted local storage and auto-refreshed. The browser only opens on first login or when the refresh token expires.
- **Alias email support** — set `AXIOM_IMAP_USER` separately when your Axiom login email is an alias pointing to a different mailbox.

```bash
pip install --upgrade axiomtradeapi
pip install "axiomtradeapi[browser]"   # adds nodriver
```

[📋 Full release notes →](https://chipadevteam.github.io/AxiomTradeAPI-py/release-1-1-6/)

<details>
<summary>v1.1.5 notes</summary>

- **Chrome TLS impersonation** via `curl_cffi` — WebSocket connections bypass Cloudflare's bot detection.
- **JWT-aware token refresh** — reads the real `exp` claim; no more silent expiry failures.
- **Pre-flight HTTP warm-up** — mirrors browser behaviour before WebSocket connect.
- **Cluster fallback fixed** — automatically tries cluster3/5/7 on primary failure.

[📋 Release notes →](https://chipadevteam.github.io/AxiomTradeAPI-py/release-1-1-5/)
</details>

---

## 🚀 Quick Start

### Installation

```bash
# Core SDK
pip install axiomtradeapi

# + browser login support (recommended)
pip install "axiomtradeapi[browser]"

# Or install with development dependencies
pip install axiomtradeapi[dev]

# Verify installation
python -c "from axiomtradeapi import AxiomTradeClient; print('✅ Installation successful!')"
```

### Basic Usage

#### 1. Browser Login — Fully Automatic (Recommended)

The SDK uses a real Chrome window to bypass Cloudflare Turnstile. Provide your IMAP credentials and the entire flow — including the OTP — is zero-touch. Tokens are saved locally and auto-refreshed, so the browser only opens **once**.

```python
import os
from axiomtradeapi import AxiomTradeClient
from dotenv import load_dotenv

load_dotenv()

client = AxiomTradeClient(
    username=os.getenv("AXIOM_EMAIL"),
    password=os.getenv("AXIOM_PASSWORD"),
)

# First run: Chrome opens, fills credentials, reads OTP from inbox automatically
# Subsequent runs: tokens loaded from disk — login() not needed
if not client.auth_manager.is_authenticated():
    result = client.login(
        imap_password=os.getenv("AXIOM_IMAP_PASSWORD"),
        # imap_user="real@yourdomain.com"  # only if AXIOM_EMAIL is an alias
    )
    if not result["success"]:
        raise RuntimeError("Login failed")

balance = client.GetBalance("YOUR_WALLET_ADDRESS")
print(f"Balance: {balance}")
```

**.env setup:**
```env
AXIOM_EMAIL=you@example.com
AXIOM_PASSWORD=yourpassword
AXIOM_IMAP_PASSWORD=your_email_password   # enables auto-OTP
AXIOM_IMAP_USER=real@yourdomain.com       # only needed if AXIOM_EMAIL is an alias
```

> **Gmail with 2FA?** Use an [App Password](https://myaccount.google.com/apppasswords) for `AXIOM_IMAP_PASSWORD`.

#### 2. Token Authentication (Serverless / CI)
Use pre-obtained tokens directly — no browser required. The SDK auto-refreshes them.

```python
import os
from axiomtradeapi import AxiomTradeClient
from dotenv import load_dotenv

load_dotenv()

client = AxiomTradeClient(
    auth_token=os.getenv("AXIOM_ACCESS_TOKEN"),
    refresh_token=os.getenv("AXIOM_REFRESH_TOKEN"),
)

if client.auth_manager.ensure_valid_authentication():
    balance = client.GetBalance("YOUR_WALLET_ADDRESS")
    print(f"Balance: {balance}")
```

#### 3. Manual Token Authentication
Use this for serverless environments or when you manage tokens externally.

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()
client.set_tokens(
    access_token="your_access_token_here",
    refresh_token="your_refresh_token_here"
)
```

### Advanced Features

#### Real-time Token Monitoring
```python
import asyncio
from axiomtradeapi import AxiomTradeClient

async def token_monitor():
    client = AxiomTradeClient(
        auth_token="your-auth-token",
        refresh_token="your-refresh-token"
    )
    
    async def handle_new_tokens(tokens):
        for token in tokens:
            print(f"🚨 New Token: {token['tokenName']} - ${token['marketCapSol']} SOL")
    
    await client.subscribe_new_tokens(handle_new_tokens)
    await client.ws.start()

# Run the monitor
asyncio.run(token_monitor())
```

#### Batch Portfolio Tracking
```python
# Monitor multiple wallets efficiently
wallets = [
    "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh",
    "Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb",
    "DsHk4F6QNTK6RdTmaDSKeFzGXMnQ9QxKTkDkG8XF8F4F"
]

balances = client.GetBatchedBalance(wallets)
total_sol = sum(b['sol'] for b in balances.values() if b)
print(f"📈 Total Portfolio: {total_sol:.6f} SOL")
```

## 📚 Comprehensive Documentation

Our documentation covers everything from basic setup to advanced trading strategies:

| Guide | Description | Skill Level |
|-------|-------------|-------------|
| [📥 **Installation**](https://chipadevteam.github.io/AxiomTradeAPI-py/installation/) | Setup, requirements, troubleshooting | Beginner |
| [🔐 **Authentication**](https://chipadevteam.github.io/AxiomTradeAPI-py/authentication/) | API keys, security, token management | Beginner |
| [💰 **Balance Queries**](https://chipadevteam.github.io/AxiomTradeAPI-py/balance-queries/) | Wallet monitoring, portfolio tracking | Intermediate |
| [📡 **WebSocket Guide**](https://chipadevteam.github.io/AxiomTradeAPI-py/websocket-guide/) | Real-time data, streaming APIs | Intermediate |
| [🤖 **Trading Bots**](https://chipadevteam.github.io/AxiomTradeAPI-py/trading-bots/) | Automated strategies, bot frameworks | Advanced |
| [⚡ **Performance**](https://chipadevteam.github.io/AxiomTradeAPI-py/performance/) | Optimization, scaling, monitoring | Advanced |
| [🛡️ **Security**](https://chipadevteam.github.io/AxiomTradeAPI-py/security/) | Best practices, secure deployment | All Levels |
| [📝 **Release Notes 1.1.6**](https://chipadevteam.github.io/AxiomTradeAPI-py/release-1-1-6/) | Browser login, IMAP auto-OTP | All Levels |
| [📝 **Release Notes 1.1.5**](https://chipadevteam.github.io/AxiomTradeAPI-py/release-1-1-5/) | Cloudflare bypass, auto token refresh | All Levels |

## 🏆 Professional Use Cases

### 🎯 Token Sniping Bots
```python
# High-speed token acquisition on new launches
class TokenSniperBot:
    def __init__(self):
        self.client = AxiomTradeClient(auth_token="...")
        self.min_liquidity = 10.0  # SOL
        self.target_profit = 0.20  # 20%
    
    async def analyze_token(self, token_data):
        if token_data['liquiditySol'] > self.min_liquidity:
            return await self.execute_snipe(token_data)
```

### 📊 DeFi Portfolio Analytics
```python
# Track yield farming and LP positions
class DeFiTracker:
    def track_yields(self, positions):
        total_yield = 0
        for position in positions:
            balance = self.client.GetBalance(position['wallet'])
            yield_pct = (balance['sol'] - position['initial']) / position['initial']
            total_yield += yield_pct
        return total_yield
```

### 🔄 Arbitrage Detection
```python
# Find profitable price differences across DEXs
class ArbitrageBot:
    def scan_opportunities(self):
        # Compare prices across Raydium, Orca, Serum
        opportunities = self.find_price_differences()
        return [op for op in opportunities if op['profit'] > 0.005]  # 0.5%
```

## 🛠️ Development & Contribution

### Development Setup
```bash
# Clone repository
git clone https://github.com/ChipaDevTeam/AxiomTradeAPI-py.git
cd AxiomTradeAPI-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest tests/
```

### Testing Your Installation
```python
#!/usr/bin/env python3
"""Test script to verify AxiomTradeAPI-py installation"""

async def test_installation():
    from axiomtradeapi import AxiomTradeClient
    
    client = AxiomTradeClient()
    test_wallet = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
    
    try:
        balance = client.GetBalance(test_wallet)
        print(f"✅ API Test Passed: {balance['sol']} SOL")
        return True
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False

# Run test
import asyncio
if asyncio.run(test_installation()):
    print("🎉 AxiomTradeAPI-py is ready for use!")
```

## 🌟 Community & Support

<div align="center">

### Join Our Growing Community

[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/p7YyFqSmAz)
[![Twitter](https://img.shields.io/twitter/follow/ChipaDevTeam?style=social)](https://twitter.com/ChipaDevTeam)
[![GitHub Stars](https://img.shields.io/github/stars/ChipaDevTeam/AxiomTradeAPI-py?style=social)](https://github.com/ChipaDevTeam/AxiomTradeAPI-py)

**📈 Learn from Successful Traders** • **🛠️ Get Technical Support** • **💡 Share Strategies** • **🚀 Access Premium Content**

</div>

### Professional Services

Need a custom trading solution? Our team of expert developers can build:

- 🤖 **Custom Trading Bots** - Tailored to your strategy
- 📊 **Portfolio Analytics** - Advanced tracking and reporting  
- 🔄 **Multi-Exchange Integration** - Cross-platform trading
- 🛡️ **Enterprise Security** - Production-grade deployment

[**Get Professional Help →**](https://chipatrade.com/services/bot-development)

## 📊 Performance Benchmarks

Our SDK is optimized for professional trading applications:

| Metric | Performance | Industry Standard |
|--------|-------------|------------------|
| Balance Query Speed | < 50ms | < 200ms |
| WebSocket Latency | < 10ms | < 50ms |
| Batch Operations | 1000+ wallets/request | 100 wallets/request |
| Memory Usage | < 30MB | < 100MB |
| Uptime | 99.9%+ | 99.5%+ |

## 🔧 Configuration Options

### Environment Variables
```bash
# ── Credentials (for browser login) ──────────────────────────────────────────
export AXIOM_EMAIL="you@example.com"
export AXIOM_PASSWORD="yourpassword"

# ── IMAP auto-OTP (optional — enables fully zero-touch login) ─────────────────
export AXIOM_IMAP_PASSWORD="your_email_password"   # Gmail: use an App Password
export AXIOM_IMAP_USER="real@yourdomain.com"       # only if AXIOM_EMAIL is an alias
export AXIOM_IMAP_HOST="imap.hostinger.com"        # only if auto-detection is wrong

# ── Token authentication (for serverless / CI) ────────────────────────────────
export AXIOM_ACCESS_TOKEN="your-access-token"
export AXIOM_REFRESH_TOKEN="your-refresh-token"

# ── Cloudflare (captured automatically by browser login) ──────────────────────
export CF_CLEARANCE="your-cf_clearance-cookie-value"

# API Configuration
export AXIOM_API_TIMEOUT=30
export AXIOM_MAX_RETRIES=3
export AXIOM_LOG_LEVEL=INFO

# WebSocket Settings
export AXIOM_WS_RECONNECT_DELAY=5
export AXIOM_WS_MAX_RECONNECTS=10
```

### Client Configuration
```python
client = AxiomTradeClient(
    auth_token="...",
    refresh_token="...",
    timeout=30,
    max_retries=3,
    log_level=logging.INFO,
    rate_limit={"requests": 100, "window": 60}  # 100 requests per minute
)
```

## 🚨 Important Disclaimers

⚠️ **Trading Risk Warning**: Cryptocurrency trading involves substantial risk of loss. Never invest more than you can afford to lose.

🔐 **Security Notice**: Always secure your API keys and never commit them to version control.

📊 **No Financial Advice**: This software is for educational and development purposes. We provide tools, not trading advice.

## 📄 License & Legal

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

- ✅ **Commercial Use Allowed**
- ✅ **Modification Allowed** 
- ✅ **Distribution Allowed**
- ✅ **Private Use Allowed**

## 🙏 Acknowledgments

Special thanks to:
- The Solana Foundation for the robust blockchain infrastructure
- Axiom Trade for providing excellent API services
- Our community of developers and traders for continuous feedback
- All contributors who help improve this library

## ✍️ Write Better Trading Bots with ChipaEditor

> **[ChipaEditor](https://chipaeditor.com/?utm_source=github&utm_medium=readme&utm_campaign=axiomtradeapi&utm_term=cta&utm_content=section)** — The AI-powered code editor purpose-built for DeFi developers and Solana traders.

ChipaEditor supercharges your AxiomTradeAPI-py workflow with:

- 🤖 **AI-assisted bot generation** — describe your strategy, get working code
- ⚡ **Real-time Solana code completions** — context-aware suggestions for trading patterns
- 🔍 **Built-in DeFi debugging** — trace token flows, inspect transactions inline
- 📦 **One-click deployment** — ship your trading bots faster than ever

👉 **[Try ChipaEditor Free →](https://chipaeditor.com/?utm_source=github&utm_medium=readme&utm_campaign=axiomtradeapi&utm_term=cta&utm_content=try_free)**

## 🔗 Trade on Axiom

Ready to put your bots to work? **[Start trading on Axiom Trade →](https://axiom.trade/@chipadev)**

## 🌐 Community & Services

Join our growing community of traders and developers!

<div align="center">

### [💬 Join our Community](https://chipatrade.com/community)
Connect with other traders, share strategies, and get help with the API.

### [🤖 Bot Development Services](https://chipatrade.com/services/bot-development)
Need a custom trading bot? Our expert team builds high-performance custom solutions tailored to your strategy.

</div>

---

<div align="center">

**Built with ❤️ by the ChipaDevTeam**

[Website](https://chipatrade.com) • [Documentation](https://chipadevteam.github.io/AxiomTradeAPI-py) • [Community](https://chipatrade.com/community) • [Services](https://chipatrade.com/services/bot-development) • [Trade on Axiom](https://axiom.trade/@chipadev) • [ChipaEditor](https://chipaeditor.com/?utm_source=github&utm_medium=readme&utm_campaign=axiomtradeapi&utm_term=footer&utm_content=link)

*⭐ Star this repository if you find it useful!*

</div>

