# AxiomTradeAPI-py: New API Functions Documentation

## 🎉 New API Functions Added Successfully!

All the new API functions from `api10.axiom.trade` have been successfully integrated and tested. Here's the complete documentation:

## 📋 Function Overview

### ✅ Working Functions

| Function | Purpose | Endpoint | Status |
|----------|---------|----------|--------|
| `get_token_info_by_pair()` | Token information by pair address | `/token-info` | ✅ Working |
| `get_last_transaction()` | Last transaction for a pair | `/last-transaction` | ✅ Working |
| `get_pair_info()` | Detailed pair information | `/pair-info` | ✅ Working |
| `get_pair_stats()` | Pair statistics | `/pair-stats` | ✅ Working |
| `get_meme_open_positions()` | Open meme positions for wallet | `/meme-open-positions` | ✅ Working |
| `get_holder_data()` | Holder data for a pair | `/holder-data-v3` | ✅ Working |
| `get_dev_tokens()` | Tokens created by developer | `/dev-tokens-v2` | ✅ Working |
| `get_token_analysis()` | Token analysis by dev & ticker | `/token-analysis` | ✅ Working |

## 📖 Detailed Function Documentation

### 1. Token Information by Pair
```python
def get_token_info_by_pair(self, pair_address: str) -> Dict:
    """
    Get token information by pair address
    
    Args:
        pair_address (str): The pair address to get info for
        
    Returns:
        Dict with keys: numHolders, numBotUsers, top10HoldersPercent, 
                       devHoldsPercent, insidersHoldPercent, bundlersHoldPercent,
                       snipersHoldPercent, dexPaid, totalPairFeesPaid
    """
```

**Example:**
```python
token_info = client.get_token_info_by_pair("Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
print(f"Number of holders: {token_info['numHolders']}")
print(f"Top 10 holders percentage: {token_info['top10HoldersPercent']}")
```

### 2. Last Transaction
```python
def get_last_transaction(self, pair_address: str) -> Dict:
    """
    Get last transaction for a pair
    
    Returns:
        Dict with keys: signature, pairAddress, type, createdAt, liquiditySol,
                       liquidityToken, makerAddress, priceSol, priceUsd, tokenAmount,
                       totalSol, totalUsd, innerIndex, outerIndex
    """
```

**Example:**
```python
last_tx = client.get_last_transaction("Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
print(f"Last transaction type: {last_tx['type']}")
print(f"Price in USD: ${last_tx['priceUsd']}")
print(f"Transaction signature: {last_tx['signature']}")
```

### 3. Pair Information
```python
def get_pair_info(self, pair_address: str) -> Dict:
    """
    Get detailed pair information
    
    Returns:
        Dict with extensive pair details including: tokenImage, dexPaid, protocol,
                tokenTicker, supply, createdAt, deployerAddress, top10Holders,
                website, telegram, discord, twitter, tokenName, etc.
    """
```

**Example:**
```python
pair_info = client.get_pair_info("Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
print(f"Token name: {pair_info['tokenName']}")
print(f"Token ticker: {pair_info['tokenTicker']}")
print(f"Website: {pair_info.get('website', 'N/A')}")
print(f"Twitter: {pair_info.get('twitter', 'N/A')}")
print(f"Telegram: {pair_info.get('telegram', 'N/A')}")
```

### 4. Pair Statistics
```python
def get_pair_stats(self, pair_address: str) -> Dict:
    """Get pair statistics"""
```

### 5. Meme Open Positions
```python
def get_meme_open_positions(self, wallet_address: str) -> Dict:
    """
    Get open meme token positions for a wallet
    
    Args:
        wallet_address (str): The wallet address to get positions for
    """
```

**Example:**
```python
positions = client.get_meme_open_positions("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
# Returns your current meme token holdings
```

### 6. Holder Data
```python
def get_holder_data(self, pair_address: str, only_tracked_wallets: bool = False) -> Dict:
    """
    Get holder data for a pair
    
    Args:
        pair_address (str): The pair address to get holder data for
        only_tracked_wallets (bool): Whether to only include tracked wallets
    """
```

**Example:**
```python
# Get all holders
all_holders = client.get_holder_data("Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY", False)

# Get only tracked wallets
tracked_holders = client.get_holder_data("Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY", True)
```

### 7. Developer Tokens
```python
def get_dev_tokens(self, dev_address: str) -> Dict:
    """
    Get tokens created by a developer address
    
    Returns:
        Dict with keys: tokens, counts
    """
```

**Example:**
```python
dev_tokens = client.get_dev_tokens("A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV")
print(f"Number of tokens created: {len(dev_tokens['tokens'])}")
print(f"Token counts: {dev_tokens['counts']}")
```

### 8. Token Analysis
```python
def get_token_analysis(self, dev_address: str, token_ticker: str) -> Dict:
    """
    Get token analysis for a developer and token ticker
    
    Returns:
        Dict with keys: creatorRiskLevel, creatorRugCount, creatorTokenCount,
                       topMarketCapCoins, topOgCoins
    """
```

**Example:**
```python
analysis = client.get_token_analysis("A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV", "green")
print(f"Creator risk level: {analysis['creatorRiskLevel']}")
print(f"Creator rug count: {analysis['creatorRugCount']}")
print(f"Creator token count: {analysis['creatorTokenCount']}")
```

## 🚀 Complete Usage Example

```python
from axiomtradeapi.client import AxiomTradeClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = AxiomTradeClient(
    auth_token=os.getenv('auth-access-token'),
    refresh_token=os.getenv('auth-refresh-token')
)

# Example pair address
pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"
wallet_address = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"

# Get comprehensive token information
print("=== Token Analysis ===")
token_info = client.get_token_info_by_pair(pair_address)
pair_info = client.get_pair_info(pair_address)
last_tx = client.get_last_transaction(pair_address)

print(f"Token: {pair_info['tokenName']} ({pair_info['tokenTicker']})")
print(f"Holders: {token_info['numHolders']}")
print(f"Last price: ${last_tx['priceUsd']}")
print(f"Top 10 holders: {token_info['top10HoldersPercent']}%")

# Check your positions
print("\n=== Your Positions ===")
positions = client.get_meme_open_positions(wallet_address)
print(f"Open positions: {positions}")

# Analyze developer
print("\n=== Developer Analysis ===")
dev_tokens = client.get_dev_tokens(dev_address)
analysis = client.get_token_analysis(dev_address, "green")

print(f"Developer created {len(dev_tokens['tokens'])} tokens")
print(f"Risk level: {analysis['creatorRiskLevel']}")
print(f"Rug count: {analysis['creatorRugCount']}")

# Get holder data
print("\n=== Holder Analysis ===")
holders = client.get_holder_data(pair_address, only_tracked_wallets=False)
print(f"Holder data retrieved: {type(holders)}")
```

## 🔐 Authentication

All functions automatically handle authentication using your existing tokens:
- Uses the same authentication system as before
- Automatically refreshes tokens when needed
- Secure token storage with encryption

## 📊 API Endpoints Used

All functions use the `api10.axiom.trade` base URL with these endpoints:
- `/token-info` - Token information by pair
- `/last-transaction` - Latest transaction data
- `/pair-info` - Comprehensive pair details
- `/pair-stats` - Pair statistics
- `/meme-open-positions` - User's open positions
- `/holder-data-v3` - Token holder analysis
- `/dev-tokens-v2` - Developer token tracking
- `/token-analysis` - Risk analysis for tokens

## ✅ Your AxiomTradeAPI Now Includes

### Core Features:
- ✅ Authentication with automatic token refresh
- ✅ Trending tokens and portfolio management
- ✅ Balance checking (SOL and tokens)
- ✅ Direct RPC transaction sending

### New Analytics Features:
- ✅ **Token Information**: Holder stats, bot detection, insider analysis
- ✅ **Transaction Tracking**: Latest trades and price movements
- ✅ **Pair Analysis**: Comprehensive token pair details
- ✅ **Position Management**: Track your meme token holdings
- ✅ **Holder Analytics**: Deep dive into token distribution
- ✅ **Developer Tracking**: Monitor token creators and their history
- ✅ **Risk Analysis**: Evaluate token and developer risk levels

Your AxiomTradeAPI client is now a comprehensive tool for Solana meme token analysis and tracking! 🎉
