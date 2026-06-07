---
layout: guide
title: "Getting Started with AxiomTradeAPI-py"
description: "Complete beginner's guide to building Solana trading applications with AxiomTradeAPI-py. Step-by-step tutorials from installation to your first trading bot."
difficulty: "Beginner"
estimated_time: "30 minutes"
permalink: /getting-started/
---

# Getting Started with AxiomTradeAPI-py

## Your Complete Guide to Solana Trading Automation

Welcome to AxiomTradeAPI-py! This comprehensive guide will take you from zero to building your first Solana trading application in just 30 minutes. Whether you're a Python beginner or an experienced developer, this tutorial will help you harness the power of automated Solana trading.

---

## 🎯 What You'll Learn

By the end of this guide, you'll be able to:

- ✅ Install and configure AxiomTradeAPI-py
- ✅ Connect to the Axiom Trade API
- ✅ Query wallet balances and monitor portfolios
- ✅ Set up real-time token monitoring
- ✅ Build your first automated trading bot
- ✅ Implement proper error handling and security

---

## 📋 Prerequisites

### System Requirements

- **Python 3.8 or higher** (Python 3.10+ recommended)
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Memory**: At least 4GB RAM
- **Internet**: Stable connection for API access

### Python Knowledge

This guide assumes basic Python knowledge:
- Variables and functions
- Working with dictionaries and lists
- Basic async/await concepts (we'll explain as we go)

### Tools You'll Need

- **Code Editor**: VS Code, PyCharm, or any Python-friendly editor
- **Terminal/Command Prompt**: For running commands
- **Axiom Trade Account**: [Sign up here](https://axiom.trade) if you don't have one

---

## 🚀 Step 1: Installation and Setup

### 1.1 Create a Project Directory

First, let's create a dedicated directory for your Solana trading project:

```bash
# Create project directory
mkdir solana-trading-bot
cd solana-trading-bot

# Create a virtual environment (highly recommended)
python -m venv trading-env

# Activate the virtual environment
# On Windows:
trading-env\Scripts\activate
# On macOS/Linux:
source trading-env/bin/activate
```

### 1.2 Install AxiomTradeAPI-py

```bash
# Install the latest version
pip install axiomtradeapi

# Verify installation
python -c "from axiomtradeapi import AxiomTradeClient; print('✅ Installation successful!')"
```

### 1.3 Install Additional Dependencies

For this tutorial, we'll also need a few additional packages:

```bash
pip install python-dotenv  # For environment variables
pip install asyncio        # For async operations (usually included)
```

### 1.4 Project Structure

Create the following project structure:

```
solana-trading-bot/
├── .env                 # Environment variables (keep secret!)
├── config.py           # Configuration settings
├── portfolio_tracker.py # Portfolio monitoring example
├── token_monitor.py    # Real-time token monitoring
├── simple_bot.py       # Your first trading bot
└── utils.py            # Helper functions
```

---

## 🔐 Step 2: Authentication Setup

### 2.1 Get Your API Credentials

To use advanced features like WebSocket monitoring, you'll need authentication tokens:

1. **Visit** [Axiom Trade](https://axiom.trade)
2. **Sign in** to your account
3. **Open Developer Tools** (F12)
4. **Go to Application/Storage tab**
5. **Find these cookies**:
   - `auth-access-token`
   - `auth-refresh-token`
6. **Copy the values** (they start with `eyJ...`)

### 2.2 Create Environment File

Create a `.env` file in your project root:

```bash
# .env file - NEVER commit this to version control!
AXIOM_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
AXIOM_REFRESH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2.3 Create Configuration File

Create `config.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for our trading application"""
    
    # API Authentication
    AUTH_TOKEN = os.getenv('AXIOM_AUTH_TOKEN')
    REFRESH_TOKEN = os.getenv('AXIOM_REFRESH_TOKEN')
    
    # Trading Settings
    MAX_POSITION_SIZE = 1.0  # Maximum SOL per trade
    RISK_PER_TRADE = 0.02    # 2% risk per trade
    
    # Monitoring Settings
    PORTFOLIO_CHECK_INTERVAL = 60  # Check portfolio every 60 seconds
    
    # Test Wallets (for learning)
    TEST_WALLETS = [
        "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh",
        "Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb"
    ]

# Validate configuration
if not Config.AUTH_TOKEN:
    print("⚠️  Warning: No AUTH_TOKEN found. Some features will be limited.")
```

---

## 💰 Step 3: Your First Balance Query

Let's start with something simple - checking wallet balances.

Create `portfolio_tracker.py`:

```python
import logging
from axiomtradeapi import AxiomTradeClient
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PortfolioTracker:
    """Simple portfolio tracking for Solana wallets"""
    
    def __init__(self):
        self.client = AxiomTradeClient(log_level=logging.INFO)
        logger.info("✅ Portfolio tracker initialized")
    
    def check_single_wallet(self, wallet_address):
        """Check balance for a single wallet"""
        try:
            logger.info(f"🔍 Checking balance for {wallet_address[:8]}...")
            
            # Get the balance
            balance = self.client.GetBalance(wallet_address)
            
            # Display results
            print(f"\n💰 Wallet Balance Report")
            print(f"   Address: {wallet_address}")
            print(f"   SOL Balance: {balance['sol']:.6f}")
            print(f"   Lamports: {balance['lamports']:,}")
            print(f"   Slot: {balance['slot']}")
            
            return balance
            
        except Exception as e:
            logger.error(f"❌ Error checking wallet balance: {e}")
            return None
    
    def check_multiple_wallets(self, wallet_addresses):
        """Check balances for multiple wallets efficiently"""
        try:
            logger.info(f"🔍 Checking {len(wallet_addresses)} wallets...")
            
            # Use batch operation for efficiency
            balances = self.client.GetBatchedBalance(wallet_addresses)
            
            # Calculate portfolio metrics
            total_sol = 0
            active_wallets = 0
            
            print(f"\n📊 Portfolio Summary")
            print("=" * 50)
            
            for address, balance_data in balances.items():
                if balance_data:
                    sol_amount = balance_data['sol']
                    total_sol += sol_amount
                    active_wallets += 1
                    
                    # Display individual wallet
                    print(f"   {address[:8]}...{address[-8:]}: {sol_amount:.6f} SOL")
                else:
                    print(f"   {address[:8]}...{address[-8:]}: ❌ Error")
            
            # Display totals
            print("=" * 50)
            print(f"   Total Wallets: {len(wallet_addresses)}")
            print(f"   Active Wallets: {active_wallets}")
            print(f"   Total SOL: {total_sol:.6f}")
            print(f"   Average per wallet: {total_sol/active_wallets:.6f}" if active_wallets > 0 else "   Average: N/A")
            
            return balances
            
        except Exception as e:
            logger.error(f"❌ Error checking portfolio: {e}")
            return None

def main():
    """Main function to demonstrate portfolio tracking"""
    
    # Create portfolio tracker
    tracker = PortfolioTracker()
    
    print("🚀 AxiomTradeAPI-py Portfolio Tracker")
    print("====================================")
    
    # Example 1: Check single wallet
    print("\n📍 Example 1: Single Wallet Check")
    single_wallet = Config.TEST_WALLETS[0]
    tracker.check_single_wallet(single_wallet)
    
    # Example 2: Check multiple wallets
    print("\n📍 Example 2: Portfolio Check")
    tracker.check_multiple_wallets(Config.TEST_WALLETS)
    
    print("\n✅ Portfolio tracking complete!")

if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python portfolio_tracker.py
```

You should see output like:
```
🚀 AxiomTradeAPI-py Portfolio Tracker
====================================

📍 Example 1: Single Wallet Check
💰 Wallet Balance Report
   Address: BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh
   SOL Balance: 1.234567
   Lamports: 1,234,567,890
   Slot: 344031778

📍 Example 2: Portfolio Check
📊 Portfolio Summary
==================================================
   BJBgjyDZ...tcEVh: 1.234567 SOL
   Cpxu7gFh...VbPb: 0.567890 SOL
==================================================
   Total Wallets: 2
   Active Wallets: 2
   Total SOL: 1.802457
   Average per wallet: 0.901229

✅ Portfolio tracking complete!
```

---

## 📡 Step 4: Real-Time Token Monitoring

Now let's set up real-time monitoring for new token launches.

Create `token_monitor.py`:

```python
import asyncio
import logging
from datetime import datetime
from axiomtradeapi import AxiomTradeClient
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TokenMonitor:
    """Real-time token launch monitoring"""
    
    def __init__(self):
        # Initialize client with authentication for WebSocket features
        self.client = AxiomTradeClient(
            auth_token=Config.AUTH_TOKEN,
            refresh_token=Config.REFRESH_TOKEN,
            log_level=logging.INFO
        )
        
        # Monitoring settings
        self.min_market_cap = 5.0     # Minimum 5 SOL market cap
        self.min_liquidity = 10.0     # Minimum 10 SOL liquidity
        self.tokens_found = 0
        self.qualified_tokens = 0
        
        logger.info("✅ Token monitor initialized")
    
    async def handle_new_tokens(self, tokens):
        """Process incoming token data"""
        try:
            for token in tokens:
                self.tokens_found += 1
                
                # Basic token info
                token_name = token.get('tokenName', 'Unknown')
                token_ticker = token.get('tokenTicker', 'N/A')
                token_address = token.get('tokenAddress', 'N/A')
                market_cap = token.get('marketCapSol', 0)
                liquidity = token.get('liquiditySol', 0)
                protocol = token.get('protocol', 'Unknown')
                
                # Check if token meets our criteria
                meets_criteria = (
                    market_cap >= self.min_market_cap and
                    liquidity >= self.min_liquidity
                )
                
                if meets_criteria:
                    self.qualified_tokens += 1
                    status = "✅ QUALIFIED"
                    logger.info(f"🎯 Qualified token found: {token_name}")
                else:
                    status = "❌ FILTERED"
                
                # Display token information
                print(f"\n🚨 NEW TOKEN DETECTED")
                print(f"   Name: {token_name} ({token_ticker})")
                print(f"   Address: {token_address}")
                print(f"   Market Cap: {market_cap:.2f} SOL")
                print(f"   Liquidity: {liquidity:.2f} SOL")
                print(f"   Protocol: {protocol}")
                print(f"   Status: {status}")
                print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 50)
                
                # You could add trading logic here for qualified tokens
                if meets_criteria:
                    await self.analyze_token_opportunity(token)
                    
        except Exception as e:
            logger.error(f"❌ Error processing tokens: {e}")
    
    async def analyze_token_opportunity(self, token):
        """Analyze qualified token for trading opportunity"""
        # This is where you'd add your token analysis logic
        logger.info(f"📊 Analyzing {token['tokenName']} for trading opportunity...")
        
        # Example analysis factors:
        analysis = {
            'market_cap_score': min(token.get('marketCapSol', 0) / 100, 1.0),  # Max score at 100 SOL
            'liquidity_score': min(token.get('liquiditySol', 0) / 50, 1.0),   # Max score at 50 SOL
            'has_socials': bool(token.get('website') or token.get('twitter')),
            'protocol_score': 1.0 if token.get('protocol') in ['Raydium', 'Orca'] else 0.5
        }
        
        # Calculate overall score
        overall_score = (
            analysis['market_cap_score'] * 0.3 +
            analysis['liquidity_score'] * 0.4 +
            (1.0 if analysis['has_socials'] else 0.0) * 0.2 +
            analysis['protocol_score'] * 0.1
        )
        
        print(f"   📊 Analysis Score: {overall_score:.2f}/1.0")
        
        if overall_score > 0.7:
            print(f"   🎯 HIGH POTENTIAL - Consider for trading!")
        elif overall_score > 0.5:
            print(f"   📈 MODERATE POTENTIAL - Monitor closely")
        else:
            print(f"   ⏸️  LOW POTENTIAL - Pass for now")
    
    async def start_monitoring(self):
        """Start the token monitoring process"""
        try:
            logger.info("🔄 Starting real-time token monitoring...")
            print(f"\n🚀 Token Monitor Started")
            print(f"   Minimum Market Cap: {self.min_market_cap} SOL")
            print(f"   Minimum Liquidity: {self.min_liquidity} SOL")
            print(f"   Monitoring for new token launches...")
            print("   Press Ctrl+C to stop\n")
            
            # Subscribe to new token events
            await self.client.subscribe_new_tokens(self.handle_new_tokens)
            
            # Start the WebSocket connection
            await self.client.ws.start()
            
        except KeyboardInterrupt:
            logger.info("👋 Monitoring stopped by user")
            await self.show_session_summary()
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
    
    async def show_session_summary(self):
        """Show summary of monitoring session"""
        print(f"\n📊 Monitoring Session Summary")
        print("=" * 40)
        print(f"   Total tokens detected: {self.tokens_found}")
        print(f"   Qualified tokens: {self.qualified_tokens}")
        print(f"   Filter rate: {((self.tokens_found - self.qualified_tokens) / max(self.tokens_found, 1) * 100):.1f}%")
        print("=" * 40)

async def main():
    """Main async function"""
    
    # Check if we have authentication
    if not Config.AUTH_TOKEN:
        print("❌ No authentication token found!")
        print("   Please set up your .env file with AXIOM_AUTH_TOKEN and AXIOM_REFRESH_TOKEN")
        print("   See the authentication guide for help: https://chipadevteam.github.io/AxiomTradeAPI-py/authentication/")
        return
    
    # Create and start monitor
    monitor = TokenMonitor()
    await monitor.start_monitoring()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
```

**Run it:**
```bash
python token_monitor.py
```

This will start monitoring for new tokens in real-time!

---

## 🤖 Step 5: Build Your First Trading Bot

Now let's create a simple trading bot that combines everything we've learned.

Create `simple_bot.py`:

```python
import asyncio
import logging
from datetime import datetime, timedelta
from axiomtradeapi import AxiomTradeClient
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TradingBot")

class SimpleTradingBot:
    """A simple trading bot for educational purposes"""
    
    def __init__(self):
        self.client = AxiomTradeClient(
            auth_token=Config.AUTH_TOKEN,
            refresh_token=Config.REFRESH_TOKEN,
            log_level=logging.INFO
        )
        
        # Bot configuration
        self.config = {
            'max_position_size': Config.MAX_POSITION_SIZE,
            'risk_per_trade': Config.RISK_PER_TRADE,
            'min_market_cap': 20.0,        # SOL
            'min_liquidity': 50.0,         # SOL
            'target_profit': 0.15,         # 15%
            'stop_loss': -0.05,            # -5%
            'max_hold_time': 3600,         # 1 hour in seconds
        }
        
        # Bot state
        self.is_running = False
        self.portfolio_value = 0.0
        self.active_positions = {}
        self.daily_pnl = 0.0
        self.trades_today = 0
        
        # Statistics
        self.stats = {
            'tokens_analyzed': 0,
            'trades_executed': 0,
            'profitable_trades': 0,
            'total_pnl': 0.0
        }
        
        logger.info("✅ Simple Trading Bot initialized")
    
    async def start(self):
        """Start the trading bot"""
        try:
            self.is_running = True
            logger.info("🚀 Starting Simple Trading Bot...")
            
            # Start multiple tasks concurrently
            await asyncio.gather(
                self.token_monitoring_task(),
                self.portfolio_monitoring_task(),
                self.position_management_task(),
                self.statistics_task()
            )
            
        except KeyboardInterrupt:
            logger.info("👋 Bot stopped by user")
            await self.shutdown()
        except Exception as e:
            logger.error(f"❌ Bot error: {e}")
            await self.shutdown()
    
    async def token_monitoring_task(self):
        """Monitor for new tokens"""
        try:
            logger.info("📡 Starting token monitoring...")
            await self.client.subscribe_new_tokens(self.analyze_new_token)
            await self.client.ws.start()
        except Exception as e:
            logger.error(f"❌ Token monitoring error: {e}")
    
    async def analyze_new_token(self, tokens):
        """Analyze new tokens for trading opportunities"""
        for token in tokens:
            try:
                self.stats['tokens_analyzed'] += 1
                
                # Extract token data
                token_name = token.get('tokenName', 'Unknown')
                market_cap = token.get('marketCapSol', 0)
                liquidity = token.get('liquiditySol', 0)
                protocol = token.get('protocol', 'Unknown')
                
                # Apply filters
                if not self.passes_initial_filters(token):
                    continue
                
                # Calculate trading signal
                signal_strength = await self.calculate_signal_strength(token)
                
                if signal_strength > 0.7:  # Strong buy signal
                    await self.execute_buy_order(token, signal_strength)
                    
            except Exception as e:
                logger.error(f"❌ Error analyzing token {token.get('tokenName', 'Unknown')}: {e}")
    
    def passes_initial_filters(self, token):
        """Check if token passes basic filters"""
        market_cap = token.get('marketCapSol', 0)
        liquidity = token.get('liquiditySol', 0)
        
        # Basic criteria
        if market_cap < self.config['min_market_cap']:
            return False
        
        if liquidity < self.config['min_liquidity']:
            return False
        
        # Don't trade if we already have too many positions
        if len(self.active_positions) >= 3:
            return False
        
        # Don't trade if we've hit daily limits
        if self.trades_today >= 10:
            return False
        
        return True
    
    async def calculate_signal_strength(self, token):
        """Calculate trading signal strength (0-1)"""
        score = 0.0
        
        # Market cap score (0-0.3)
        market_cap = token.get('marketCapSol', 0)
        if market_cap > 100:
            score += 0.3
        elif market_cap > 50:
            score += 0.2
        elif market_cap > 20:
            score += 0.1
        
        # Liquidity score (0-0.3)
        liquidity = token.get('liquiditySol', 0)
        if liquidity > 200:
            score += 0.3
        elif liquidity > 100:
            score += 0.2
        elif liquidity > 50:
            score += 0.1
        
        # Protocol score (0-0.2)
        trusted_protocols = ['Raydium', 'Orca', 'Jupiter']
        if token.get('protocol') in trusted_protocols:
            score += 0.2
        
        # Social presence score (0-0.2)
        has_website = bool(token.get('website'))
        has_twitter = bool(token.get('twitter'))
        has_telegram = bool(token.get('telegram'))
        
        social_score = sum([has_website, has_twitter, has_telegram]) / 3 * 0.2
        score += social_score
        
        logger.info(f"📊 Signal strength for {token.get('tokenName')}: {score:.2f}")
        return score
    
    async def execute_buy_order(self, token, signal_strength):
        """Execute a buy order (simulated for this example)"""
        try:
            token_address = token.get('tokenAddress')
            token_name = token.get('tokenName')
            
            # Calculate position size based on signal strength
            base_size = self.config['max_position_size']
            position_size = base_size * signal_strength
            
            logger.info(f"🎯 EXECUTING BUY ORDER")
            logger.info(f"   Token: {token_name}")
            logger.info(f"   Address: {token_address}")
            logger.info(f"   Position Size: {position_size:.6f} SOL")
            logger.info(f"   Signal Strength: {signal_strength:.2f}")
            
            # In a real bot, you would execute the actual trade here
            # For this example, we'll simulate the trade
            
            entry_price = token.get('price', 1.0)  # Use actual price in real implementation
            
            # Record the position
            self.active_positions[token_address] = {
                'token_name': token_name,
                'entry_price': entry_price,
                'position_size': position_size,
                'entry_time': datetime.now(),
                'target_profit': self.config['target_profit'],
                'stop_loss': self.config['stop_loss']
            }
            
            self.stats['trades_executed'] += 1
            self.trades_today += 1
            
            logger.info(f"✅ Buy order executed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error executing buy order: {e}")
    
    async def portfolio_monitoring_task(self):
        """Monitor portfolio and update metrics"""
        while self.is_running:
            try:
                # Check if we have any wallets to monitor
                if Config.TEST_WALLETS:
                    balances = self.client.GetBatchedBalance(Config.TEST_WALLETS)
                    total_sol = sum(b['sol'] for b in balances.values() if b)
                    self.portfolio_value = total_sol
                
                await asyncio.sleep(Config.PORTFOLIO_CHECK_INTERVAL)
                
            except Exception as e:
                logger.error(f"❌ Portfolio monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def position_management_task(self):
        """Manage active positions"""
        while self.is_running:
            try:
                current_time = datetime.now()
                positions_to_close = []
                
                for token_address, position in self.active_positions.items():
                    # Check time-based exit
                    hold_time = (current_time - position['entry_time']).total_seconds()
                    
                    if hold_time > self.config['max_hold_time']:
                        positions_to_close.append(token_address)
                        logger.info(f"⏰ Closing position {position['token_name']} - Max hold time reached")
                
                # Close positions that need to be closed
                for token_address in positions_to_close:
                    await self.close_position(token_address, "Time limit")
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Position management error: {e}")
                await asyncio.sleep(60)
    
    async def close_position(self, token_address, reason):
        """Close a trading position"""
        try:
            position = self.active_positions.get(token_address)
            if not position:
                return
            
            # In a real bot, you would execute the actual sell order here
            # For this example, we'll simulate a random outcome
            import random
            simulated_pnl = random.uniform(-0.05, 0.15)  # Random P&L between -5% and +15%
            
            pnl_amount = position['position_size'] * simulated_pnl
            
            logger.info(f"🚪 CLOSING POSITION")
            logger.info(f"   Token: {position['token_name']}")
            logger.info(f"   Reason: {reason}")
            logger.info(f"   P&L: {simulated_pnl:.2%} ({pnl_amount:+.6f} SOL)")
            
            # Update statistics
            if simulated_pnl > 0:
                self.stats['profitable_trades'] += 1
            
            self.stats['total_pnl'] += pnl_amount
            self.daily_pnl += pnl_amount
            
            # Remove from active positions
            del self.active_positions[token_address]
            
            logger.info(f"✅ Position closed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error closing position: {e}")
    
    async def statistics_task(self):
        """Periodically log bot statistics"""
        while self.is_running:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                win_rate = (self.stats['profitable_trades'] / max(self.stats['trades_executed'], 1)) * 100
                
                logger.info(f"📊 Bot Statistics:")
                logger.info(f"   Portfolio Value: {self.portfolio_value:.6f} SOL")
                logger.info(f"   Active Positions: {len(self.active_positions)}")
                logger.info(f"   Tokens Analyzed: {self.stats['tokens_analyzed']}")
                logger.info(f"   Trades Executed: {self.stats['trades_executed']}")
                logger.info(f"   Win Rate: {win_rate:.1f}%")
                logger.info(f"   Total P&L: {self.stats['total_pnl']:+.6f} SOL")
                logger.info(f"   Daily P&L: {self.daily_pnl:+.6f} SOL")
                
            except Exception as e:
                logger.error(f"❌ Statistics error: {e}")
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        logger.info("🛑 Shutting down bot...")
        self.is_running = False
        
        # Close any remaining positions
        for token_address in list(self.active_positions.keys()):
            await self.close_position(token_address, "Bot shutdown")
        
        # Final statistics
        logger.info("📊 Final Bot Statistics:")
        logger.info(f"   Tokens Analyzed: {self.stats['tokens_analyzed']}")
        logger.info(f"   Trades Executed: {self.stats['trades_executed']}")
        logger.info(f"   Profitable Trades: {self.stats['profitable_trades']}")
        logger.info(f"   Total P&L: {self.stats['total_pnl']:+.6f} SOL")
        
        logger.info("✅ Bot shutdown complete")

async def main():
    """Main function"""
    
    print("🤖 Simple Trading Bot")
    print("=" * 30)
    print("This is an educational trading bot that simulates trading decisions.")
    print("It does NOT execute real trades - it's for learning purposes only!")
    print("=" * 30)
    
    if not Config.AUTH_TOKEN:
        print("❌ No authentication token found!")
        print("Please set up your .env file for WebSocket features.")
        return
    
    # Create and start the bot
    bot = SimpleTradingBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
```

**Run your bot:**
```bash
python simple_bot.py
```

---

## 🛡️ Step 6: Security and Best Practices

### 6.1 Secure Your API Keys

Create `utils.py` for security utilities:

```python
import os
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def require_auth(func):
    """Decorator to ensure authentication is available"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from config import Config
        if not Config.AUTH_TOKEN:
            raise ValueError("Authentication required for this operation")
        return func(*args, **kwargs)
    return wrapper

def validate_wallet_address(address):
    """Validate Solana wallet address format"""
    if not address or len(address) != 44:
        raise ValueError(f"Invalid Solana address: {address}")
    return True

def safe_divide(a, b, default=0):
    """Safely divide two numbers"""
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

class RiskManager:
    """Simple risk management utilities"""
    
    def __init__(self, max_daily_loss=0.05, max_position_size=0.1):
        self.max_daily_loss = max_daily_loss  # 5%
        self.max_position_size = max_position_size  # 10%
        self.daily_pnl = 0.0
        self.portfolio_value = 1.0  # Default portfolio value
    
    def check_position_size(self, position_size):
        """Check if position size is within limits"""
        position_ratio = position_size / self.portfolio_value
        return position_ratio <= self.max_position_size
    
    def check_daily_loss_limit(self):
        """Check if daily loss limit has been exceeded"""
        if self.daily_pnl < 0:
            loss_ratio = abs(self.daily_pnl) / self.portfolio_value
            return loss_ratio < self.max_daily_loss
        return True
    
    def update_pnl(self, pnl_amount):
        """Update daily P&L"""
        self.daily_pnl += pnl_amount
        logger.info(f"Daily P&L updated: {self.daily_pnl:+.6f}")
```

### 6.2 Error Handling Example

Add this to your bot for robust error handling:

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """Decorator for retrying failed operations"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator

# Usage in your bot:
@retry_on_failure(max_retries=3, delay=2)
async def safe_get_balance(self, address):
    """Get balance with retry logic"""
    return self.client.GetBalance(address)
```

---

## 🎯 Step 7: Testing and Validation

Create a test script to validate your setup:

```python
# test_setup.py
import asyncio
import logging
from axiomtradeapi import AxiomTradeClient
from config import Config

async def run_comprehensive_test():
    """Run comprehensive test of your setup"""
    
    print("🧪 Running AxiomTradeAPI-py Setup Tests")
    print("=" * 50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Basic import
    try:
        from axiomtradeapi import AxiomTradeClient
        print("✅ Test 1: Import successful")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        tests_failed += 1
    
    # Test 2: Client initialization
    try:
        client = AxiomTradeClient(log_level=logging.WARNING)
        print("✅ Test 2: Client initialization successful")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        tests_failed += 1
        return
    
    # Test 3: Balance query
    try:
        test_wallet = Config.TEST_WALLETS[0]
        balance = client.GetBalance(test_wallet)
        print(f"✅ Test 3: Balance query successful - {balance['sol']} SOL")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        tests_failed += 1
    
    # Test 4: Batch balance query
    try:
        balances = client.GetBatchedBalance(Config.TEST_WALLETS)
        print(f"✅ Test 4: Batch query successful - {len(balances)} wallets")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        tests_failed += 1
    
    # Test 5: WebSocket availability (requires auth)
    if Config.AUTH_TOKEN:
        try:
            auth_client = AxiomTradeClient(
                auth_token=Config.AUTH_TOKEN,
                refresh_token=Config.REFRESH_TOKEN
            )
            print("✅ Test 5: WebSocket client initialized")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Test 5 failed: {e}")
            tests_failed += 1
    else:
        print("⏭️  Test 5: Skipped (no auth token)")
    
    # Summary
    print("=" * 50)
    print(f"📊 Test Results:")
    print(f"   Passed: {tests_passed}")
    print(f"   Failed: {tests_failed}")
    print(f"   Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 All tests passed! Your setup is ready for trading.")
    else:
        print("\n⚠️  Some tests failed. Check your configuration and try again.")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
```

**Run the test:**
```bash
python test_setup.py
```

---

## 🚀 Step 8: Next Steps

Congratulations! You've successfully set up AxiomTradeAPI-py and built your first trading applications. Here's what to explore next:

### 📚 Advanced Guides

1. **[WebSocket Integration](./websocket-guide.md)** - Master real-time data streams
2. **[Trading Bots](./trading-bots.md)** - Build advanced automated strategies  
3. **[Performance Optimization](./performance.md)** - Scale your applications
4. **[Security Best Practices](./security.md)** - Secure your trading bots

### 🛠️ Project Ideas

**Beginner Projects:**
- Portfolio tracker with alerts
- Token launch notifier
- DeFi yield calculator

**Intermediate Projects:**
- Arbitrage opportunity scanner
- Social sentiment analyzer
- Multi-wallet management dashboard

**Advanced Projects:**
- High-frequency trading bot
- Market making algorithm
- Cross-chain bridge monitor

### 🌟 Community Resources

- **Discord**: [Join our community](https://discord.gg/p7YyFqSmAz)
- **Documentation**: [Full API docs](https://chipadevteam.github.io/AxiomTradeAPI-py)
- **Professional Services**: [Custom bot development](https://shop.chipatrade.com/products/create-your-bot)

---

## 🤝 Getting Help

If you run into issues:

1. **Check the logs** - Look at your bot's log files for error messages
2. **Review the documentation** - Most questions are answered in our guides
3. **Ask the community** - Join our Discord for help from other developers
4. **File an issue** - Report bugs on GitHub

### Common Issues

**"No module named 'axiomtradeapi'"**
```bash
# Solution: Install the package
pip install axiomtradeapi
```

**"Authentication failed"**
```bash
# Solution: Check your .env file and token validity
python -c "from config import Config; print('Auth token:', bool(Config.AUTH_TOKEN))"
```

**"Network timeout"**
```bash
# Solution: Check internet connection and try again
# The API has built-in retry logic
```

---

## 📝 Summary

You've learned how to:

✅ Install and configure AxiomTradeAPI-py  
✅ Set up secure authentication  
✅ Query wallet balances and track portfolios  
✅ Monitor real-time token launches  
✅ Build a complete trading bot framework  
✅ Implement security and risk management  
✅ Test and validate your setup  

You're now ready to build sophisticated Solana trading applications with AxiomTradeAPI-py!

---

*Need professional help with your trading bot? Check out our [custom development services](https://shop.chipatrade.com/products/create-your-bot) for expert assistance.*

---

## ✍️ Code Smarter with ChipaEditor

**[ChipaEditor](https://chipaeditor.com/?utm_source=code&utm_medium=example&utm_campaign=axiomtradeapi&utm_term=advanced&utm_content=getting_started_doc)** — The AI-powered editor built for DeFi developers. Write trading bots faster with Solana-aware AI completions and one-click deployment.

👉 **[Try ChipaEditor Free →](https://chipaeditor.com/?utm_source=code&utm_medium=example&utm_campaign=axiomtradeapi&utm_term=advanced&utm_content=try_free)** | **[Trade on Axiom →](https://axiom.trade/@chipadev)**