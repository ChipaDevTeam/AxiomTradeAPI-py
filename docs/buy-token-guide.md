# buy_token() Method - Comprehensive Guide

## Overview

The `buy_token()` method enables you to purchase Solana tokens using SOL through the PumpPortal trading API. This method handles the complete transaction lifecycle, from building the transaction with your private key to submitting it to the Solana blockchain.

⚠️ **CRITICAL WARNING**: This method executes REAL blockchain transactions with REAL money. Always test with small amounts first and verify all parameters carefully before executing trades.

## Method Signature

```python
def buy_token(
    self, 
    private_key: str, 
    token_mint: str, 
    amount: float, 
    slippage_percent: float = 10, 
    priority_fee: float = 0.005, 
    pool: str = "auto", 
    denominated_in_sol: bool = True,
    rpc_url: str = "https://api.mainnet-beta.solana.com/"
) -> Dict[str, Union[str, bool]]
```

## Parameters

### Required Parameters

#### `private_key` (str)
- **Description**: Your wallet's private key encoded as a base58 string
- **Format**: Base58 encoded string (NOT hex, NOT array format)
- **Security**: ⚠️ NEVER commit private keys to version control or share them
- **Example**: `"5J6qw9kM2...base58string..."`

#### `token_mint` (str)
- **Description**: The token contract address (mint address) you want to purchase
- **Format**: Base58 encoded Solana public key (32 bytes)
- **Example**: `"CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"`
- **How to find**: Token addresses are found on Solscan, DEX Screener, or from new pair WebSocket events

#### `amount` (float)
- **Description**: The amount to trade
- **Interpretation**: Depends on the `denominated_in_sol` parameter
  - If `denominated_in_sol=True`: Amount of SOL to spend (e.g., `0.1` = 0.1 SOL)
  - If `denominated_in_sol=False`: Amount of tokens to receive (e.g., `1000` = 1000 tokens)
- **Example**: `0.05` (spend 0.05 SOL)

### Optional Parameters

#### `slippage_percent` (float, default=10)
- **Description**: Maximum price slippage tolerance as a percentage
- **Range**: Typically 1-50%
- **Impact**: 
  - Lower values (1-5%): Transaction may fail on volatile tokens
  - Higher values (15-50%): More likely to execute but with potential price impact
- **Recommendation**: Use 10-15% for most tokens, 20-50% for highly volatile meme coins
- **Example**: `15` (allows up to 15% price slippage)

#### `priority_fee` (float, default=0.005)
- **Description**: Priority fee paid to Solana validators to process your transaction faster
- **Unit**: SOL (0.005 = 0.005 SOL = 5,000 lamports)
- **Impact**: Higher fees = faster transaction processing
- **Recommendation**: 
  - Normal times: 0.001-0.005 SOL
  - High congestion: 0.01-0.05 SOL
  - Critical/time-sensitive: 0.1+ SOL
- **Example**: `0.01` (pay 0.01 SOL priority fee)

#### `pool` (str, default="auto")
- **Description**: Specific exchange/pool to trade on
- **Available Options**:
  - `"auto"`: Automatically selects best pool (recommended)
  - `"pump"`: pump.fun exchange
  - `"raydium"`: Raydium DEX
  - `"pump-amm"`: pump.fun AMM
  - `"launchlab"`: LaunchLab
  - `"raydium-cpmm"`: Raydium CPMM
  - `"bonk"`: Bonk Swap
- **Recommendation**: Use `"auto"` unless you have specific routing requirements
- **Example**: `"raydium"`

#### `denominated_in_sol` (bool, default=True)
- **Description**: Determines how the `amount` parameter is interpreted
- **Values**:
  - `True`: `amount` represents SOL to spend
  - `False`: `amount` represents tokens to receive
- **Default**: `True` (most common use case - "I want to spend X SOL")
- **Example**: `True`

#### `rpc_url` (str, default="https://api.mainnet-beta.solana.com/")
- **Description**: Solana RPC endpoint URL for transaction submission
- **Options**:
  - Default public RPC (free, may be rate-limited)
  - Premium RPC services (Helius, QuickNode, Triton, etc.)
- **Performance**: Premium RPCs offer faster transaction processing and higher reliability
- **Example**: `"https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"`

## Return Value

Returns a dictionary with transaction details:

### Success Response
```python
{
    "success": True,
    "signature": "5nh7w9kM2pqW...transaction_signature",
    "transactionId": "5nh7w9kM2pqW...transaction_signature",
    "explorer_url": "https://solscan.io/tx/5nh7w9kM2pqW..."
}
```

### Error Response
```python
{
    "success": False,
    "error": "Error description message"
}
```

### Response Fields

- **success** (bool): Whether the transaction was successful
- **signature** (str): Transaction signature (transaction hash/ID)
- **transactionId** (str): Duplicate of signature for compatibility
- **explorer_url** (str): Direct link to view transaction on Solscan
- **error** (str): Error message if transaction failed

## Prerequisites

### 1. Install Required Dependencies
```bash
pip install solders
```

The `buy_token()` method requires the `solders` library for Solana transaction handling.

### 2. Authentication Setup
```python
from axiomtradeapi.client import AxiomTradeClient

# Initialize client with authentication
client = AxiomTradeClient()

# If using environment variables (.env file):
# AXIOM_ACCESS_TOKEN=your_access_token
# AXIOM_REFRESH_TOKEN=your_refresh_token

# Or login manually:
# client.login("username", "password")
```

### 3. Obtain Your Private Key
Your wallet private key should be in base58 format. You can export it from:
- Phantom wallet (Settings → Show Private Key)
- Solflare wallet (Settings → Export Private Key)
- Other Solana wallets with export functionality

⚠️ **Security**: Store private keys in environment variables or secure key management systems.

---

## Basic Usage Examples

### Example 1: Simple Token Purchase
Purchase a token by spending a specific amount of SOL.

```python
from axiomtradeapi.client import AxiomTradeClient
import os

# Initialize client
client = AxiomTradeClient()

# Get private key from environment variable (secure practice)
private_key = os.getenv("SOLANA_PRIVATE_KEY")

# Token mint address (example from pump.fun)
token_mint = "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"

# Buy token with 0.1 SOL
result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint,
    amount=0.1,  # Spend 0.1 SOL
    slippage_percent=10
)

# Check result
if result["success"]:
    print(f"✅ Purchase successful!")
    print(f"Transaction: {result['signature']}")
    print(f"View on Solscan: {result['explorer_url']}")
else:
    print(f"❌ Purchase failed: {result['error']}")
```

**Output:**
```
✅ Purchase successful!
Transaction: 5nh7w9kM2pqWxY3jH8v5K9mN4rS6tU2vW3xY4zA5bC6d
View on Solscan: https://solscan.io/tx/5nh7w9kM2pqWxY3jH8v5K9mN4rS6tU2vW3xY4zA5bC6d
```

### Example 2: Purchase with Higher Slippage
For volatile meme coins, you may need higher slippage tolerance.

```python
# Buy highly volatile token with 25% slippage
result = client.buy_token(
    private_key=private_key,
    token_mint="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    amount=0.05,
    slippage_percent=25,  # Higher slippage for volatile tokens
    priority_fee=0.01     # Higher priority fee for faster execution
)

if result["success"]:
    print(f"✅ Bought volatile token successfully")
    print(f"Explorer: {result['explorer_url']}")
else:
    print(f"❌ Failed: {result['error']}")
```

### Example 3: Purchase Specific Token Amount
Specify the exact number of tokens you want to receive instead of SOL to spend.

```python
# Buy exactly 1,000,000 tokens
result = client.buy_token(
    private_key=private_key,
    token_mint="8z5VqjqYqF3zK8jM9nL3rT6wU4xY2zA1bC5dE8fG9hJ",
    amount=1000000,          # Want to receive 1M tokens
    denominated_in_sol=False,  # Amount is in TOKENS, not SOL
    slippage_percent=15
)

if result["success"]:
    print(f"✅ Received ~1,000,000 tokens")
    print(f"Transaction: {result['signature']}")
```

---

## Advanced Examples

### Example 4: Trading Bot with Error Handling
Robust trading bot implementation with comprehensive error handling.

```python
import os
import time
from axiomtradeapi.client import AxiomTradeClient
from typing import Optional

class TradingBot:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.private_key = os.getenv("SOLANA_PRIVATE_KEY")
        self.max_retries = 3
    
    def buy_with_retry(
        self, 
        token_mint: str, 
        amount_sol: float,
        max_slippage: float = 15
    ) -> Optional[str]:
        """
        Buy token with automatic retry logic
        
        Returns:
            Transaction signature if successful, None if failed
        """
        for attempt in range(1, self.max_retries + 1):
            print(f"🔄 Attempt {attempt}/{self.max_retries}")
            
            result = self.client.buy_token(
                private_key=self.private_key,
                token_mint=token_mint,
                amount=amount_sol,
                slippage_percent=max_slippage,
                priority_fee=0.005 * attempt  # Increase fee with each retry
            )
            
            if result["success"]:
                print(f"✅ Purchase successful on attempt {attempt}")
                print(f"Signature: {result['signature']}")
                return result["signature"]
            else:
                print(f"❌ Attempt {attempt} failed: {result['error']}")
                
                # Check if error is retryable
                if "slippage" in result['error'].lower():
                    print(f"   Slippage error - increasing tolerance")
                    max_slippage += 5  # Increase slippage for next attempt
                elif "insufficient funds" in result['error'].lower():
                    print(f"   Insufficient funds - cannot retry")
                    return None
                
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"   Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        print(f"❌ All {self.max_retries} attempts failed")
        return None

# Usage
bot = TradingBot()
token = "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"
signature = bot.buy_with_retry(token, 0.1)
```

### Example 5: Portfolio Dollar-Cost Averaging (DCA)
Automatically buy a token at regular intervals with fixed SOL amounts.

```python
import time
from datetime import datetime
from axiomtradeapi.client import AxiomTradeClient

class DCAStrategy:
    def __init__(self, private_key: str):
        self.client = AxiomTradeClient()
        self.private_key = private_key
        self.purchase_history = []
    
    def execute_dca(
        self,
        token_mint: str,
        amount_per_purchase: float,
        num_purchases: int,
        interval_seconds: int
    ):
        """
        Execute dollar-cost averaging strategy
        
        Args:
            token_mint: Token to purchase
            amount_per_purchase: SOL amount for each purchase
            num_purchases: Number of purchases to make
            interval_seconds: Time between purchases
        """
        print(f"🎯 Starting DCA Strategy")
        print(f"   Token: {token_mint}")
        print(f"   Amount per buy: {amount_per_purchase} SOL")
        print(f"   Total purchases: {num_purchases}")
        print(f"   Interval: {interval_seconds}s\n")
        
        for i in range(1, num_purchases + 1):
            print(f"📊 Purchase {i}/{num_purchases} at {datetime.now()}")
            
            result = self.client.buy_token(
                private_key=self.private_key,
                token_mint=token_mint,
                amount=amount_per_purchase,
                slippage_percent=12
            )
            
            if result["success"]:
                self.purchase_history.append({
                    "timestamp": datetime.now(),
                    "amount_sol": amount_per_purchase,
                    "signature": result["signature"]
                })
                print(f"   ✅ Success: {result['signature']}")
            else:
                print(f"   ❌ Failed: {result['error']}")
            
            # Wait before next purchase (except on last iteration)
            if i < num_purchases:
                print(f"   ⏳ Waiting {interval_seconds}s until next purchase...\n")
                time.sleep(interval_seconds)
        
        # Summary
        successful = len(self.purchase_history)
        total_spent = successful * amount_per_purchase
        print(f"\n📈 DCA Summary:")
        print(f"   Successful purchases: {successful}/{num_purchases}")
        print(f"   Total SOL spent: {total_spent}")
        print(f"   Average cost basis: {total_spent/successful if successful > 0 else 0} SOL")

# Usage: Buy 0.1 SOL worth every hour, 5 times
dca = DCAStrategy(os.getenv("SOLANA_PRIVATE_KEY"))
dca.execute_dca(
    token_mint="CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump",
    amount_per_purchase=0.1,
    num_purchases=5,
    interval_seconds=3600  # 1 hour
)
```

### Example 6: Pre-Transaction Safety Checks
Verify your balance and token information before executing trades.

```python
from axiomtradeapi.client import AxiomTradeClient
import os

class SafeTrader:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.private_key = os.getenv("SOLANA_PRIVATE_KEY")
    
    def safe_buy(
        self,
        token_mint: str,
        amount_sol: float,
        min_balance_sol: float = 0.01  # Keep minimum balance for fees
    ) -> dict:
        """
        Buy token with pre-flight safety checks
        """
        print("🔍 Running pre-flight checks...")
        
        # 1. Check SOL balance
        balance = self.client.GetBalance()
        if not balance:
            return {"success": False, "error": "Failed to fetch balance"}
        
        current_sol = balance['sol']
        print(f"   Current balance: {current_sol} SOL")
        
        # 2. Verify sufficient funds
        total_needed = amount_sol + min_balance_sol + 0.01  # Buy amount + buffer + priority fee
        if current_sol < total_needed:
            return {
                "success": False, 
                "error": f"Insufficient balance. Need {total_needed} SOL, have {current_sol} SOL"
            }
        print(f"   ✅ Sufficient balance ({current_sol} SOL available)")
        
        # 3. Validate token address format
        if len(token_mint) < 32 or len(token_mint) > 44:
            return {"success": False, "error": "Invalid token address format"}
        print(f"   ✅ Token address format valid")
        
        # 4. Check if amount is reasonable
        if amount_sol > current_sol * 0.5:
            warning = f"⚠️  WARNING: Buying with >50% of balance ({amount_sol}/{current_sol} SOL)"
            print(warning)
            confirm = input("Continue? (yes/no): ")
            if confirm.lower() != "yes":
                return {"success": False, "error": "Trade cancelled by user"}
        
        print("   ✅ All pre-flight checks passed\n")
        
        # 5. Execute trade
        print(f"🚀 Executing purchase: {amount_sol} SOL → {token_mint}")
        result = self.client.buy_token(
            private_key=self.private_key,
            token_mint=token_mint,
            amount=amount_sol,
            slippage_percent=15
        )
        
        if result["success"]:
            print(f"✅ Purchase successful!")
            print(f"   Transaction: {result['signature']}")
            print(f"   Explorer: {result['explorer_url']}")
        else:
            print(f"❌ Purchase failed: {result['error']}")
        
        return result

# Usage
trader = SafeTrader()
result = trader.safe_buy(
    token_mint="CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump",
    amount_sol=0.1
)
```

### Example 7: Using Premium RPC for Faster Execution
Critical trades benefit from premium RPC endpoints with higher reliability.

```python
from axiomtradeapi.client import AxiomTradeClient
import os

client = AxiomTradeClient()
private_key = os.getenv("SOLANA_PRIVATE_KEY")

# Token to snipe at launch
token_mint = "NewTokenLaunchAddress123..."

# Fast execution with premium RPC
result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint,
    amount=0.5,
    slippage_percent=20,          # Higher slippage for launch volatility
    priority_fee=0.1,             # High priority fee for immediate execution
    rpc_url="https://mainnet.helius-rpc.com/?api-key=YOUR_HELIUS_KEY"  # Premium RPC
)

if result["success"]:
    print(f"⚡ Fast execution successful!")
    print(f"Transaction: {result['signature']}")
else:
    print(f"❌ Failed: {result['error']}")
```

### Example 8: Multi-Token Portfolio Rebalancing
Buy multiple tokens in a single session with proportional allocation.

```python
from axiomtradeapi.client import AxiomTradeClient
import os

class PortfolioRebalancer:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.private_key = os.getenv("SOLANA_PRIVATE_KEY")
    
    def rebalance_portfolio(self, target_allocations: dict, total_investment_sol: float):
        """
        Buy multiple tokens based on target allocation percentages
        
        Args:
            target_allocations: Dict of {token_mint: allocation_percent}
            total_investment_sol: Total SOL to invest
            
        Example:
            {
                "TokenA...": 40,  # 40% of total
                "TokenB...": 35,  # 35% of total
                "TokenC...": 25   # 25% of total
            }
        """
        # Validate allocations sum to 100%
        total_percent = sum(target_allocations.values())
        if abs(total_percent - 100) > 0.01:
            print(f"❌ Error: Allocations must sum to 100% (got {total_percent}%)")
            return
        
        print(f"🎯 Portfolio Rebalancing")
        print(f"   Total investment: {total_investment_sol} SOL\n")
        
        results = []
        
        for token_mint, allocation_percent in target_allocations.items():
            amount = (allocation_percent / 100) * total_investment_sol
            print(f"📊 Buying {token_mint[:8]}... ({allocation_percent}% = {amount} SOL)")
            
            result = self.client.buy_token(
                private_key=self.private_key,
                token_mint=token_mint,
                amount=amount,
                slippage_percent=12
            )
            
            if result["success"]:
                print(f"   ✅ Success: {result['signature']}\n")
                results.append({
                    "token": token_mint,
                    "success": True,
                    "signature": result["signature"]
                })
            else:
                print(f"   ❌ Failed: {result['error']}\n")
                results.append({
                    "token": token_mint,
                    "success": False,
                    "error": result["error"]
                })
        
        # Summary
        successful = sum(1 for r in results if r["success"])
        print(f"\n📈 Rebalancing Summary:")
        print(f"   Successful: {successful}/{len(results)}")
        print(f"   Total invested: {total_investment_sol * (successful/len(results)):.4f} SOL")
        
        return results

# Usage
rebalancer = PortfolioRebalancer()
rebalancer.rebalance_portfolio(
    target_allocations={
        "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump": 40,  # 40%
        "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": 35,  # 35%
        "8z5VqjqYqF3zK8jM9nL3rT6wU4xY2zA1bC5dE8fG9hJ": 25   # 25%
    },
    total_investment_sol=1.0  # Invest 1 SOL total
)
```

### Example 9: WebSocket-Triggered Automated Buying
Automatically buy new tokens as they're detected via WebSocket.

```python
from axiomtradeapi.client import AxiomTradeClient
import asyncio
import os

class TokenSniper:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.private_key = os.getenv("SOLANA_PRIVATE_KEY")
        self.buy_amount = 0.05  # SOL per token
        
    def should_buy(self, token_data: dict) -> bool:
        """
        Filtering logic to determine if token is worth buying
        """
        # Example criteria
        initial_liquidity = token_data.get('initial_liquidity_sol', 0)
        lp_burned = token_data.get('lp_burned', False)
        dev_holds = token_data.get('dev_holds_percent', 100)
        
        # Only buy if:
        # - Has reasonable liquidity (>= 1 SOL)
        # - LP is burned (safer)
        # - Dev holds < 20% (less rug risk)
        return (
            initial_liquidity >= 1.0 and
            lp_burned == True and
            dev_holds < 20
        )
    
    async def handle_new_pair(self, token_data: dict):
        """
        Called when new token pair is detected
        """
        token_mint = token_data.get('token_address')
        token_name = token_data.get('token_name', 'Unknown')
        
        print(f"\n🔔 New token detected: {token_name}")
        print(f"   Address: {token_mint}")
        
        # Apply buying criteria
        if not self.should_buy(token_data):
            print(f"   ❌ Does not meet buy criteria - skipping")
            return
        
        print(f"   ✅ Meets criteria - attempting to buy")
        
        # Execute buy
        result = self.client.buy_token(
            private_key=self.private_key,
            token_mint=token_mint,
            amount=self.buy_amount,
            slippage_percent=20,  # Higher for new launches
            priority_fee=0.02     # High priority for early entry
        )
        
        if result["success"]:
            print(f"   🎉 Purchase successful!")
            print(f"   Signature: {result['signature']}")
            print(f"   Explorer: {result['explorer_url']}")
        else:
            print(f"   ❌ Purchase failed: {result['error']}")
    
    async def start_sniping(self):
        """
        Start listening for new tokens via WebSocket
        """
        print("🎯 Token Sniper started - listening for new pairs...")
        
        async for message in self.client.stream_new_pairs():
            await self.handle_new_pair(message)

# Usage
sniper = TokenSniper()
asyncio.run(sniper.start_sniping())
```

---

## Security Guidelines

### 🔐 Private Key Security

#### ✅ DO:
- Store private keys in environment variables
- Use secure key management services (AWS Secrets Manager, HashiCorp Vault)
- Encrypt private keys at rest
- Use hardware wallets for large amounts
- Regularly rotate keys
- Use separate wallets for trading bots vs main holdings

#### ❌ DON'T:
- Hard-code private keys in source code
- Commit private keys to Git repositories
- Share private keys via email, chat, or any communication channel
- Store private keys in plain text files
- Use the same private key across multiple applications

#### Example: Secure Key Loading
```python
import os
from dotenv import load_dotenv

# Load from .env file (add .env to .gitignore)
load_dotenv()
private_key = os.getenv("SOLANA_PRIVATE_KEY")

if not private_key:
    raise ValueError("SOLANA_PRIVATE_KEY not found in environment variables")

# Use the key
result = client.buy_token(private_key=private_key, ...)
```

### 💰 Financial Safety

#### Always Test First
```python
# Test with minimum amounts first
TEST_AMOUNT = 0.001  # Very small amount for testing

result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint,
    amount=TEST_AMOUNT,  # Test with tiny amount
    slippage_percent=15
)

if result["success"]:
    print("✅ Test successful - safe to proceed with larger amounts")
```

#### Set Maximum Limits
```python
MAX_TRADE_SIZE_SOL = 0.5  # Never trade more than 0.5 SOL

def safe_buy(amount_sol):
    if amount_sol > MAX_TRADE_SIZE_SOL:
        print(f"❌ Blocked: Amount {amount_sol} exceeds limit {MAX_TRADE_SIZE_SOL}")
        return None
    
    return client.buy_token(private_key, token_mint, amount_sol)
```

#### Verify Token Addresses
```python
# Maintain whitelist of verified tokens
VERIFIED_TOKENS = {
    "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump": "SafeToken",
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": "TrustedCoin"
}

def buy_verified_only(token_mint, amount):
    if token_mint not in VERIFIED_TOKENS:
        print(f"⚠️  WARNING: Token {token_mint} not in verified list")
        confirm = input("Continue anyway? (yes/no): ")
        if confirm.lower() != "yes":
            return None
    
    return client.buy_token(private_key, token_mint, amount)
```

---

## Best Practices

### 1. Always Handle Errors
```python
result = client.buy_token(...)

if result["success"]:
    # Success path
    print(f"Transaction: {result['signature']}")
else:
    # Error path
    print(f"Failed: {result['error']}")
    # Log error, send alert, retry, etc.
```

### 2. Log All Transactions
```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

result = client.buy_token(...)

logger.info(f"[{datetime.now()}] Buy attempt: {token_mint}, Amount: {amount} SOL")
if result["success"]:
    logger.info(f"SUCCESS: {result['signature']}")
else:
    logger.error(f"FAILED: {result['error']}")
```

### 3. Use Appropriate Slippage
```python
# Conservative for established tokens
SLIPPAGE_STABLE = 5      # 5% for established tokens

# Moderate for mid-caps
SLIPPAGE_MODERATE = 12   # 12% for moderate volatility

# Aggressive for meme coins
SLIPPAGE_HIGH = 25       # 25% for high volatility

result = client.buy_token(
    ...,
    slippage_percent=SLIPPAGE_HIGH if is_meme_coin else SLIPPAGE_STABLE
)
```

### 4. Monitor Transaction Status
```python
import time

result = client.buy_token(...)

if result["success"]:
    signature = result["signature"]
    print(f"Transaction submitted: {signature}")
    print(f"Monitor at: {result['explorer_url']}")
    
    # Wait for confirmation
    print("Waiting for confirmation...")
    time.sleep(5)  # Give transaction time to confirm
    
    print("✅ Transaction should be confirmed - check explorer link")
```

### 5. Implement Rate Limiting
```python
import time

class RateLimitedTrader:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.last_trade_time = 0
        self.min_trade_interval = 10  # Minimum 10 seconds between trades
    
    def buy_with_rate_limit(self, private_key, token_mint, amount):
        current_time = time.time()
        time_since_last = current_time - self.last_trade_time
        
        if time_since_last < self.min_trade_interval:
            wait_time = self.min_trade_interval - time_since_last
            print(f"⏳ Rate limit: waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
        
        result = self.client.buy_token(private_key, token_mint, amount)
        self.last_trade_time = time.time()
        
        return result
```

### 6. Use Different Pools When Needed
```python
# Try auto pool first
result = client.buy_token(..., pool="auto")

if not result["success"] and "liquidity" in result["error"].lower():
    # Retry with specific pool if auto fails
    print("Auto pool failed, trying Raydium...")
    result = client.buy_token(..., pool="raydium")
```

---

## Troubleshooting

### Common Errors and Solutions

#### Error: "solders library not installed"
**Problem**: The required `solders` package is missing.

**Solution**:
```bash
pip install solders
```

#### Error: "Insufficient funds"
**Problem**: Wallet doesn't have enough SOL for the trade + fees.

**Solution**:
```python
# Check balance first
balance = client.GetBalance()
print(f"Available: {balance['sol']} SOL")

# Ensure you have: trade amount + priority fee + network fees (~0.000005 SOL)
total_needed = amount + priority_fee + 0.001
if balance['sol'] < total_needed:
    print(f"Need {total_needed} SOL, have {balance['sol']} SOL")
```

#### Error: "Slippage tolerance exceeded"
**Problem**: Token price moved beyond your slippage tolerance during execution.

**Solution**:
```python
# Increase slippage for volatile tokens
result = client.buy_token(
    ...,
    slippage_percent=20,  # Increase from default 10%
    priority_fee=0.01     # Higher priority for faster execution
)
```

#### Error: "Transaction failed to confirm"
**Problem**: Transaction didn't confirm within timeout period.

**Solution**:
```python
# Use premium RPC for better reliability
result = client.buy_token(
    ...,
    rpc_url="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"
)

# Or increase priority fee
result = client.buy_token(
    ...,
    priority_fee=0.05  # Much higher priority
)
```

#### Error: "Invalid private key format"
**Problem**: Private key is not in base58 format.

**Solution**:
```python
# Private key should be base58 string, not array or hex
# ✅ Correct: "5J6qw9kM2pqW..."
# ❌ Wrong: [1, 2, 3, 4, ...]
# ❌ Wrong: "0x1234..."

# Export from Phantom: Settings → Show Private Key (base58 format)
```

#### Error: "PumpPortal API error: 400"
**Problem**: Invalid request parameters sent to PumpPortal.

**Solution**:
```python
# Verify token address is valid Solana address (32-44 characters)
if len(token_mint) < 32:
    print("Invalid token address")

# Verify amount is positive
if amount <= 0:
    print("Amount must be positive")

# Verify slippage is reasonable (1-100%)
if slippage_percent < 1 or slippage_percent > 100:
    print("Slippage must be between 1-100%")
```

### Debug Mode

Enable detailed logging to troubleshoot issues:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Now buy_token will log detailed information
result = client.buy_token(...)

# You'll see:
# - Trade parameters sent to PumpPortal
# - Request/response data
# - Transaction details
# - Any errors with full stack traces
```

### Transaction Not Showing Tokens

**Problem**: Transaction succeeded but tokens don't appear in wallet.

**Possible Causes**:
1. Transaction still confirming (wait 30-60 seconds)
2. Need to manually add token to wallet (import custom token with mint address)
3. Token has transfer restrictions
4. Transaction actually failed (check Solscan)

**Solution**:
```python
result = client.buy_token(...)

if result["success"]:
    print(f"Check transaction status: {result['explorer_url']}")
    print(f"If tokens not visible, add custom token: {token_mint}")
    print("In Phantom: Settings → Manage Token List → Add Custom Token")
```

---

## Performance Optimization

### Use Premium RPC Endpoints

Free RPCs can be slow and rate-limited. Premium services offer:
- Faster transaction submission
- Higher rate limits
- Better reliability
- Transaction status webhooks

**Recommended Services**:
- [Helius](https://helius.xyz/) - Fast, reliable, generous free tier
- [QuickNode](https://quicknode.com/) - Enterprise-grade infrastructure
- [Triton](https://triton.one/) - Specialized for trading

```python
# Helius example
result = client.buy_token(
    ...,
    rpc_url="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY",
    priority_fee=0.01
)
```

### Optimize Priority Fees

Monitor network congestion and adjust fees dynamically:

```python
def get_dynamic_priority_fee():
    """
    Calculate priority fee based on network conditions
    """
    # In production, query Solana RPC for recent prioritization fees
    # For now, simple time-based heuristic:
    from datetime import datetime
    
    hour = datetime.now().hour
    
    # Peak trading hours (9 AM - 5 PM UTC): higher fees
    if 9 <= hour <= 17:
        return 0.01  # High priority
    else:
        return 0.005  # Normal priority

priority_fee = get_dynamic_priority_fee()
result = client.buy_token(..., priority_fee=priority_fee)
```

### Batch Operations

When buying multiple tokens, execute in sequence with appropriate delays:

```python
import time

tokens = ["TokenA...", "TokenB...", "TokenC..."]

for i, token in enumerate(tokens):
    print(f"Buying token {i+1}/{len(tokens)}")
    
    result = client.buy_token(private_key, token, 0.1)
    
    if result["success"]:
        print(f"✅ {result['signature']}")
    
    # Small delay between transactions
    if i < len(tokens) - 1:
        time.sleep(2)
```

---

## Related Methods

### `sell_token()`
Sell tokens for SOL - complement to `buy_token()`.

```python
# Buy token
buy_result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint,
    amount=0.1
)

# Later, sell token
sell_result = client.sell_token(
    private_key=private_key,
    token_mint=token_mint,
    amount="100%",  # Sell all tokens
    denominated_in_sol=False
)
```

See: [sell_token() documentation](#) (if available)

### `GetBalance()`
Check wallet SOL balance before trading.

```python
balance = client.GetBalance()
print(f"Available SOL: {balance['sol']}")

# Only buy if sufficient balance
if balance['sol'] > 0.2:
    result = client.buy_token(...)
```

See: [GetBalance Guide](./getbalance-guide.md)

### WebSocket New Pairs
Monitor new token launches to buy immediately.

```python
async for token_data in client.stream_new_pairs():
    token_mint = token_data['token_address']
    # Buy new token
    result = client.buy_token(private_key, token_mint, 0.05)
```

See: [WebSocket Guide](./websocket-guide.md)

---

## Additional Resources

- **PumpPortal API Documentation**: [https://pumpportal.fun/trading-api](https://pumpportal.fun/trading-api)
- **Solana Explorer (Solscan)**: [https://solscan.io/](https://solscan.io/)
- **Authentication Guide**: [authentication.md](./authentication.md)
- **Trading Best Practices**: [TRADING_GUIDE.md](./TRADING_GUIDE.md)
- **Error Handling**: [error-handling.md](./error-handling.md)

---

## Summary

The `buy_token()` method provides a powerful interface for purchasing Solana tokens with comprehensive control over:
- ✅ Trade size and denomination (SOL or tokens)
- ✅ Slippage tolerance
- ✅ Transaction priority
- ✅ Pool/DEX selection
- ✅ RPC endpoint selection

**Key Takeaways**:
1. ⚠️ **Always test with small amounts first**
2. 🔐 **Never expose private keys**
3. 📊 **Check balance before trading**
4. 🎯 **Use appropriate slippage for token volatility**
5. ⚡ **Consider premium RPC for critical trades**
6. 🔄 **Implement error handling and retry logic**
7. 📝 **Log all transactions for audit trail**

For questions or issues, refer to the [troubleshooting guide](./troubleshooting.md) or open an issue on GitHub.
