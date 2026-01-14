# GetBalance - Complete Guide

## Table of Contents
- [Overview](#overview)
- [Method Signature](#method-signature)
- [Return Value](#return-value)
- [Prerequisites](#prerequisites)
- [Basic Usage](#basic-usage)
- [Advanced Examples](#advanced-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Related Methods](#related-methods)

---

## Overview

The `GetBalance()` method retrieves the SOL (Solana native token) balance for any Solana wallet address. This is a **legacy method** maintained for backward compatibility. For new code, consider using `get_sol_balance()` which provides the same functionality with a more modern interface.

### Key Features
- ✅ Check SOL balance for any Solana wallet
- ✅ Returns balance in both SOL and lamports
- ✅ Automatic authentication handling
- ✅ Works with any valid Solana address
- ✅ No transaction fees (read-only operation)

### When to Use
- Check your wallet balance before trading
- Monitor multiple wallet balances
- Verify successful SOL transfers
- Build portfolio tracking systems
- Implement balance-based trading logic

---

## Method Signature

```python
def GetBalance(self, wallet_address: str) -> Dict[str, Union[float, int]]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `wallet_address` | `str` | Yes | A valid Solana wallet address (base58 encoded public key) |

### Return Value

Returns a dictionary with the following structure:

```python
{
    "sol": float,        # Balance in SOL (e.g., 1.5 SOL)
    "lamports": int,     # Balance in lamports (1 SOL = 1,000,000,000 lamports)
    "slot": int          # Blockchain slot (always 0 for this method)
}
```

Returns `None` if the request fails or wallet address is invalid.

---

## Prerequisites

### 1. Install the Package

```bash
pip install axiomtradeapi
```

### 2. Authentication Setup

You need valid Axiom Trade credentials. Set up authentication using one of these methods:

#### Method A: Environment Variables (Recommended)
```bash
export AXIOM_ACCESS_TOKEN='your_access_token'
export AXIOM_REFRESH_TOKEN='your_refresh_token'
```

Or create a `.env` file:
```env
AXIOM_ACCESS_TOKEN=your_access_token
AXIOM_REFRESH_TOKEN=your_refresh_token
```

#### Method B: Direct Login
```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()
client.login(email, base64_password, otp_code)
```

---

## Basic Usage

### Example 1: Simple Balance Check

```python
from axiomtradeapi import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# Get balance for a wallet
wallet_address = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
balance = client.GetBalance(wallet_address)

if balance:
    print(f"Wallet Balance: {balance['sol']} SOL")
    print(f"Lamports: {balance['lamports']}")
else:
    print("Failed to retrieve balance")
```

**Output:**
```
Wallet Balance: 2.543891234 SOL
Lamports: 2543891234
```

### Example 2: Check Your Own Wallet

```python
from axiomtradeapi import AxiomTradeClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client with authentication
client = AxiomTradeClient()

# Your wallet address
my_wallet = os.getenv("WALLET_ADDRESS")
balance = client.GetBalance(my_wallet)

if balance:
    print(f"💰 Your Balance: {balance['sol']} SOL")
    print(f"📊 In Lamports: {balance['lamports']:,}")
else:
    print("❌ Could not fetch balance")
```

**Output:**
```
💰 Your Balance: 10.5 SOL
📊 In Lamports: 10,500,000,000
```

### Example 3: Quick Balance Check Before Trading

```python
from axiomtradeapi import AxiomTradeClient

def can_afford_trade(wallet_address: str, required_sol: float) -> bool:
    """Check if wallet has enough SOL for a trade"""
    client = AxiomTradeClient()
    balance = client.GetBalance(wallet_address)
    
    if balance:
        return balance['sol'] >= required_sol
    return False

# Usage
my_wallet = "YourWalletAddressHere"
trade_amount = 0.5  # SOL

if can_afford_trade(my_wallet, trade_amount):
    print("✅ Sufficient balance for trade")
else:
    print("❌ Insufficient balance")
```

---

## Advanced Examples

### Example 4: Monitor Multiple Wallets

```python
from axiomtradeapi import AxiomTradeClient
from typing import List, Dict

def check_multiple_wallets(wallets: List[str]) -> Dict[str, float]:
    """
    Check balances for multiple wallets
    
    Args:
        wallets: List of wallet addresses
        
    Returns:
        Dictionary mapping wallet addresses to SOL balances
    """
    client = AxiomTradeClient()
    balances = {}
    
    for wallet in wallets:
        balance = client.GetBalance(wallet)
        if balance:
            balances[wallet] = balance['sol']
        else:
            balances[wallet] = None
    
    return balances

# Usage
wallet_list = [
    "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh",
    "Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb",
    "7rndUznKPwSSfDAKmpw7Ng43HUTkDFoAfchy7Y1QSzdQ"
]

balances = check_multiple_wallets(wallet_list)

print("🏦 Wallet Balances:")
print("=" * 80)
for wallet, balance in balances.items():
    short_addr = f"{wallet[:8]}...{wallet[-8:]}"
    if balance is not None:
        print(f"  {short_addr}: {balance:,.6f} SOL")
    else:
        print(f"  {short_addr}: ❌ Failed to retrieve")
```

**Output:**
```
🏦 Wallet Balances:
================================================================================
  BJBgjyDZ...5d9tcEVh: 2.543891 SOL
  Cpxu7gFh...ByNenVbPb: 0.015234 SOL
  7rndUznK...chy7Y1QSzdQ: 15.789456 SOL
```

### Example 5: Portfolio Tracker

```python
from axiomtradeapi import AxiomTradeClient
from datetime import datetime

class PortfolioTracker:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.wallets = []
    
    def add_wallet(self, address: str, label: str = ""):
        """Add a wallet to track"""
        self.wallets.append({"address": address, "label": label})
    
    def get_total_balance(self) -> float:
        """Calculate total SOL across all tracked wallets"""
        total = 0.0
        for wallet in self.wallets:
            balance = self.client.GetBalance(wallet['address'])
            if balance:
                total += balance['sol']
        return total
    
    def get_detailed_report(self):
        """Generate detailed balance report"""
        print(f"📊 Portfolio Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        total = 0.0
        for wallet in self.wallets:
            balance = self.client.GetBalance(wallet['address'])
            if balance:
                label = wallet.get('label', 'Unnamed')
                short_addr = f"{wallet['address'][:8]}...{wallet['address'][-8:]}"
                print(f"  {label:15} ({short_addr}): {balance['sol']:>12.6f} SOL")
                total += balance['sol']
        
        print("=" * 80)
        print(f"  {'TOTAL':15} {'':17}: {total:>12.6f} SOL")
        print()

# Usage
tracker = PortfolioTracker()
tracker.add_wallet("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh", "Main Wallet")
tracker.add_wallet("Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb", "Trading Wallet")
tracker.add_wallet("7rndUznKPwSSfDAKmpw7Ng43HUTkDFoAfchy7Y1QSzdQ", "Savings")

tracker.get_detailed_report()
total_balance = tracker.get_total_balance()
print(f"💎 Total Portfolio Value: {total_balance:.6f} SOL")
```

**Output:**
```
📊 Portfolio Report - 2026-01-14 15:30:45
================================================================================
  Main Wallet     (BJBgjyDZ...5d9tcEVh):     2.543891 SOL
  Trading Wallet  (Cpxu7gFh...ByNenVbPb):     0.015234 SOL
  Savings         (7rndUznK...chy7Y1QSzdQ):    15.789456 SOL
================================================================================
  TOTAL                                :    18.348581 SOL

💎 Total Portfolio Value: 18.348581 SOL
```

### Example 6: Balance Alert System

```python
from axiomtradeapi import AxiomTradeClient
import time

class BalanceAlert:
    def __init__(self, wallet_address: str, threshold: float):
        self.client = AxiomTradeClient()
        self.wallet = wallet_address
        self.threshold = threshold
    
    def check_and_alert(self):
        """Check balance and alert if below threshold"""
        balance = self.client.GetBalance(self.wallet)
        
        if balance:
            current_balance = balance['sol']
            short_addr = f"{self.wallet[:8]}...{self.wallet[-8:]}"
            
            if current_balance < self.threshold:
                print(f"⚠️  ALERT: Low Balance Detected!")
                print(f"   Wallet: {short_addr}")
                print(f"   Current: {current_balance:.6f} SOL")
                print(f"   Threshold: {self.threshold:.6f} SOL")
                print(f"   Difference: {self.threshold - current_balance:.6f} SOL short")
                return True
            else:
                print(f"✅ Balance OK: {current_balance:.6f} SOL (Threshold: {self.threshold} SOL)")
                return False
        else:
            print("❌ Failed to check balance")
            return None
    
    def monitor(self, interval_seconds: int = 300):
        """Continuously monitor balance"""
        print(f"🔍 Starting balance monitor for threshold: {self.threshold} SOL")
        print(f"   Checking every {interval_seconds} seconds")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_and_alert()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")

# Usage
alert = BalanceAlert(
    wallet_address="YourWalletAddressHere",
    threshold=1.0  # Alert if balance drops below 1 SOL
)

# One-time check
alert.check_and_alert()

# Or continuous monitoring (uncomment to use)
# alert.monitor(interval_seconds=60)  # Check every minute
```

### Example 7: Convert Between SOL and Lamports

```python
from axiomtradeapi import AxiomTradeClient

def format_balance(wallet_address: str):
    """Display balance in multiple formats"""
    client = AxiomTradeClient()
    balance = client.GetBalance(wallet_address)
    
    if balance:
        sol = balance['sol']
        lamports = balance['lamports']
        
        print(f"Wallet: {wallet_address[:8]}...{wallet_address[-8:]}")
        print(f"├─ SOL:       {sol:,.9f}")
        print(f"├─ Lamports:  {lamports:,}")
        print(f"├─ mSOL:      {sol * 1000:.6f} (milliSOL)")
        print(f"└─ µSOL:      {sol * 1000000:.3f} (microSOL)")
        
        # Calculate USD value (example with $100 per SOL)
        sol_price_usd = 100.0  # Replace with real price from an API
        usd_value = sol * sol_price_usd
        print(f"\n💵 Estimated Value: ${usd_value:,.2f} USD (@ ${sol_price_usd}/SOL)")

# Usage
format_balance("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
```

**Output:**
```
Wallet: BJBgjyDZ...5d9tcEVh
├─ SOL:       2.543891234
├─ Lamports:  2,543,891,234
├─ mSOL:      2543.891234 (milliSOL)
└─ µSOL:      2543891.234 (microSOL)

💵 Estimated Value: $254.39 USD (@ $100.0/SOL)
```

### Example 8: Trading Bot Balance Management

```python
from axiomtradeapi import AxiomTradeClient

class TradingBot:
    def __init__(self, wallet_address: str):
        self.client = AxiomTradeClient()
        self.wallet = wallet_address
        self.min_balance = 0.1  # Minimum SOL to keep
        self.max_trade_percent = 0.2  # Max 20% of balance per trade
    
    def get_available_balance(self) -> float:
        """Get balance available for trading (excluding minimum reserve)"""
        balance = self.client.GetBalance(self.wallet)
        if balance:
            total = balance['sol']
            available = max(0, total - self.min_balance)
            return available
        return 0.0
    
    def calculate_trade_size(self) -> float:
        """Calculate safe trade size based on current balance"""
        available = self.get_available_balance()
        max_trade = available * self.max_trade_percent
        return max_trade
    
    def can_execute_trade(self, amount_sol: float) -> bool:
        """Check if trade can be executed safely"""
        balance = self.client.GetBalance(self.wallet)
        
        if not balance:
            print("❌ Failed to check balance")
            return False
        
        current = balance['sol']
        after_trade = current - amount_sol
        
        print(f"📊 Trade Safety Check:")
        print(f"   Current Balance:  {current:.6f} SOL")
        print(f"   Trade Amount:     {amount_sol:.6f} SOL")
        print(f"   After Trade:      {after_trade:.6f} SOL")
        print(f"   Minimum Reserve:  {self.min_balance:.6f} SOL")
        
        if after_trade < self.min_balance:
            print(f"   ❌ REJECTED: Would leave only {after_trade:.6f} SOL")
            return False
        
        print(f"   ✅ APPROVED: Safe to trade")
        return True

# Usage
bot = TradingBot("YourWalletAddressHere")

# Check available balance
available = bot.get_available_balance()
print(f"Available for trading: {available:.6f} SOL")

# Calculate safe trade size
trade_size = bot.calculate_trade_size()
print(f"Recommended trade size: {trade_size:.6f} SOL")

# Verify trade before executing
if bot.can_execute_trade(0.5):
    print("Proceeding with trade...")
    # Execute your trade here
else:
    print("Trade rejected for safety")
```

---

## Error Handling

### Common Errors and Solutions

#### Error 1: Invalid Wallet Address

```python
from axiomtradeapi import AxiomTradeClient

def safe_balance_check(wallet_address: str):
    """Safely check balance with validation"""
    client = AxiomTradeClient()
    
    # Validate address format (Solana addresses are 32-44 characters)
    if not wallet_address or len(wallet_address) < 32:
        print(f"❌ Invalid wallet address: {wallet_address}")
        return None
    
    try:
        balance = client.GetBalance(wallet_address)
        
        if balance is None:
            print(f"❌ Failed to retrieve balance for: {wallet_address}")
            return None
        
        return balance
    
    except Exception as e:
        print(f"❌ Error checking balance: {str(e)}")
        return None

# Usage
result = safe_balance_check("InvalidAddress123")  # Will handle gracefully
```

#### Error 2: Authentication Failed

```python
from axiomtradeapi import AxiomTradeClient
import os

def check_balance_with_auth_retry(wallet_address: str, max_retries: int = 3):
    """Check balance with authentication retry logic"""
    client = AxiomTradeClient()
    
    for attempt in range(max_retries):
        try:
            balance = client.GetBalance(wallet_address)
            
            if balance:
                return balance
            
            # If None returned, might be auth issue
            print(f"Attempt {attempt + 1}/{max_retries}: Retrying authentication...")
            
            # Try to re-authenticate
            if not client.ensure_authenticated():
                print("Failed to authenticate")
                continue
                
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying...")
            
    print("❌ All attempts failed")
    return None

# Usage
balance = check_balance_with_auth_retry("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
```

#### Error 3: Network Issues

```python
from axiomtradeapi import AxiomTradeClient
import time

def get_balance_with_timeout(wallet_address: str, timeout_seconds: int = 30):
    """Get balance with timeout handling"""
    client = AxiomTradeClient()
    start_time = time.time()
    
    try:
        balance = client.GetBalance(wallet_address)
        
        elapsed = time.time() - start_time
        
        if balance:
            print(f"✅ Balance retrieved in {elapsed:.2f} seconds")
            return balance
        else:
            print(f"❌ Failed to retrieve balance after {elapsed:.2f} seconds")
            return None
            
    except Exception as e:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            print(f"⏱️  Timeout: Operation took longer than {timeout_seconds} seconds")
        else:
            print(f"❌ Error: {str(e)}")
        return None

# Usage
balance = get_balance_with_timeout("YourWalletAddress", timeout_seconds=10)
```

### Complete Error Handling Example

```python
from axiomtradeapi import AxiomTradeClient
from typing import Optional, Dict, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustBalanceChecker:
    def __init__(self):
        self.client = AxiomTradeClient()
    
    def validate_address(self, address: str) -> bool:
        """Validate Solana wallet address format"""
        if not address:
            logger.error("Empty wallet address")
            return False
        
        if len(address) < 32 or len(address) > 44:
            logger.error(f"Invalid address length: {len(address)}")
            return False
        
        # Check if it's base58 (basic check)
        import string
        base58_chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
        base58_chars = base58_chars.replace('0', '').replace('O', '').replace('I', '').replace('l', '')
        
        if not all(c in base58_chars for c in address):
            logger.error("Invalid characters in address")
            return False
        
        return True
    
    def get_balance(self, wallet_address: str) -> Optional[Dict[str, Union[float, int]]]:
        """
        Get balance with comprehensive error handling
        
        Returns:
            Balance dict or None if any error occurs
        """
        # Validate address
        if not self.validate_address(wallet_address):
            logger.error(f"Address validation failed: {wallet_address}")
            return None
        
        try:
            # Attempt to get balance
            balance = self.client.GetBalance(wallet_address)
            
            if balance is None:
                logger.warning(f"GetBalance returned None for {wallet_address}")
                return None
            
            # Validate response structure
            if not isinstance(balance, dict):
                logger.error(f"Unexpected response type: {type(balance)}")
                return None
            
            required_keys = ['sol', 'lamports']
            if not all(key in balance for key in required_keys):
                logger.error(f"Missing required keys in response: {balance.keys()}")
                return None
            
            # Validate values
            if balance['sol'] < 0 or balance['lamports'] < 0:
                logger.error(f"Negative balance values: {balance}")
                return None
            
            logger.info(f"Successfully retrieved balance: {balance['sol']} SOL")
            return balance
            
        except ConnectionError as e:
            logger.error(f"Network connection error: {str(e)}")
            return None
            
        except TimeoutError as e:
            logger.error(f"Request timeout: {str(e)}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return None

# Usage
checker = RobustBalanceChecker()
balance = checker.get_balance("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")

if balance:
    print(f"✅ Balance: {balance['sol']} SOL")
else:
    print("❌ Could not retrieve balance (check logs for details)")
```

---

## Best Practices

### 1. Cache Balance Results

```python
from axiomtradeapi import AxiomTradeClient
from datetime import datetime, timedelta
from typing import Optional, Dict

class CachedBalanceChecker:
    def __init__(self, cache_duration_seconds: int = 60):
        self.client = AxiomTradeClient()
        self.cache = {}
        self.cache_duration = timedelta(seconds=cache_duration_seconds)
    
    def get_balance(self, wallet_address: str, use_cache: bool = True) -> Optional[Dict]:
        """Get balance with caching to reduce API calls"""
        
        # Check cache
        if use_cache and wallet_address in self.cache:
            cached_data = self.cache[wallet_address]
            age = datetime.now() - cached_data['timestamp']
            
            if age < self.cache_duration:
                print(f"📦 Using cached balance (age: {age.seconds}s)")
                return cached_data['balance']
        
        # Fetch fresh data
        print("🌐 Fetching fresh balance...")
        balance = self.client.GetBalance(wallet_address)
        
        if balance:
            # Update cache
            self.cache[wallet_address] = {
                'balance': balance,
                'timestamp': datetime.now()
            }
        
        return balance

# Usage
checker = CachedBalanceChecker(cache_duration_seconds=60)

# First call - fetches from API
balance1 = checker.get_balance("YourWallet")

# Second call within 60s - uses cache
balance2 = checker.get_balance("YourWallet")

# Force fresh fetch
balance3 = checker.get_balance("YourWallet", use_cache=False)
```

### 2. Batch Balance Checks Efficiently

```python
from axiomtradeapi import AxiomTradeClient
from typing import List, Dict
import time

def check_balances_efficiently(wallets: List[str], delay_seconds: float = 0.5) -> Dict[str, float]:
    """
    Check multiple balances with rate limiting
    
    Args:
        wallets: List of wallet addresses
        delay_seconds: Delay between requests to avoid rate limiting
    """
    client = AxiomTradeClient()
    results = {}
    
    print(f"Checking {len(wallets)} wallets...")
    
    for i, wallet in enumerate(wallets, 1):
        print(f"[{i}/{len(wallets)}] Checking {wallet[:8]}...", end=" ")
        
        balance = client.GetBalance(wallet)
        
        if balance:
            results[wallet] = balance['sol']
            print(f"✅ {balance['sol']:.6f} SOL")
        else:
            results[wallet] = None
            print("❌ Failed")
        
        # Add delay to avoid rate limiting (except for last request)
        if i < len(wallets):
            time.sleep(delay_seconds)
    
    return results

# Usage
wallets = [
    "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh",
    "Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb"
]

balances = check_balances_efficiently(wallets, delay_seconds=0.5)
```

### 3. Log Balance History

```python
from axiomtradeapi import AxiomTradeClient
from datetime import datetime
import json
import os

class BalanceLogger:
    def __init__(self, wallet_address: str, log_file: str = "balance_history.json"):
        self.client = AxiomTradeClient()
        self.wallet = wallet_address
        self.log_file = log_file
        self.history = self._load_history()
    
    def _load_history(self):
        """Load existing history from file"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_history(self):
        """Save history to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def log_balance(self):
        """Check and log current balance"""
        balance = self.client.GetBalance(self.wallet)
        
        if balance:
            timestamp = datetime.now().isoformat()
            
            if self.wallet not in self.history:
                self.history[self.wallet] = []
            
            entry = {
                'timestamp': timestamp,
                'sol': balance['sol'],
                'lamports': balance['lamports']
            }
            
            self.history[self.wallet].append(entry)
            self._save_history()
            
            print(f"✅ Logged balance: {balance['sol']} SOL at {timestamp}")
            return True
        else:
            print("❌ Failed to log balance")
            return False
    
    def get_balance_change(self):
        """Calculate balance change since last check"""
        if self.wallet not in self.history or len(self.history[self.wallet]) < 2:
            return None
        
        entries = self.history[self.wallet]
        latest = entries[-1]
        previous = entries[-2]
        
        change = latest['sol'] - previous['sol']
        percent_change = (change / previous['sol']) * 100 if previous['sol'] > 0 else 0
        
        return {
            'change': change,
            'percent': percent_change,
            'previous': previous['sol'],
            'current': latest['sol']
        }

# Usage
logger = BalanceLogger("YourWalletAddress")

# Log current balance
logger.log_balance()

# Later... log again to track changes
# logger.log_balance()

# Check balance change
change = logger.get_balance_change()
if change:
    print(f"Balance changed by {change['change']:+.6f} SOL ({change['percent']:+.2f}%)")
```

---

## Troubleshooting

### Issue 1: Returns None

**Possible Causes:**
- Invalid wallet address
- Authentication token expired
- Network connectivity issues
- API service temporarily unavailable

**Solution:**
```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Verify authentication first
if not client.ensure_authenticated():
    print("Authentication failed - please check your credentials")
    exit(1)

# Then check balance
balance = client.GetBalance("YourWallet")
if balance is None:
    print("Troubleshooting steps:")
    print("1. Verify wallet address is correct")
    print("2. Check internet connection")
    print("3. Try again in a few moments")
```

### Issue 2: Slow Response Time

**Solution:** Implement timeout and retry logic
```python
from axiomtradeapi import AxiomTradeClient
import time

def get_balance_with_retry(wallet: str, max_attempts: int = 3, timeout: int = 10):
    client = AxiomTradeClient()
    
    for attempt in range(max_attempts):
        start = time.time()
        balance = client.GetBalance(wallet)
        elapsed = time.time() - start
        
        if balance:
            print(f"✅ Success in {elapsed:.2f}s")
            return balance
        
        if attempt < max_attempts - 1:
            print(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(2)
    
    return None
```

### Issue 3: Balance Shows 0 for New Wallet

**This is normal!** A brand new wallet that has never received SOL will show 0 balance.

```python
from axiomtradeapi import AxiomTradeClient

def check_wallet_status(wallet: str):
    client = AxiomTradeClient()
    balance = client.GetBalance(wallet)
    
    if balance:
        if balance['sol'] == 0:
            print("💤 Wallet exists but has no SOL")
            print("   This wallet needs to be funded before use")
        else:
            print(f"✅ Active wallet with {balance['sol']} SOL")
    else:
        print("❌ Unable to verify wallet")

check_wallet_status("YourNewWallet")
```

---

## Related Methods

### get_sol_balance()
Modern alternative to GetBalance():

```python
# Old way (GetBalance)
balance = client.GetBalance(wallet)
sol = balance['sol']

# New way (get_sol_balance)
sol = client.get_sol_balance(wallet)  # Returns float directly
```

### get_token_balance()
Check SPL token balances:

```python
# Check USDC balance
usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
usdc_balance = client.get_token_balance(wallet, usdc_mint)
```

### get_batched_sol_balance()
Check multiple wallets efficiently:

```python
# Check multiple wallets at once (if supported)
wallets = ["wallet1", "wallet2", "wallet3"]
balances = client.get_batched_sol_balance(wallets)
```

---

## Summary

The `GetBalance()` method is your go-to tool for checking SOL balances in the Axiom Trade API. Key takeaways:

- ✅ Simple one-line balance checks
- ✅ Returns both SOL and lamports
- ✅ Essential for pre-trade verification
- ✅ Use error handling for production code
- ✅ Consider caching for frequent checks
- ✅ Monitor rate limits with delays

For questions or issues, visit: https://github.com/ChipaDevTeam/AxiomTradeAPI-py/issues

---

**Last Updated:** January 14, 2026  
**Package Version:** 1.0.5+  
**Documentation Version:** 1.0
