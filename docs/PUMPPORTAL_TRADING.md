# AxiomTradeAPI-py: PumpPortal Trading Integration 🚀

## 🎉 Real Trading Functionality Added!

Your AxiomTradeAPI now includes **real trading capabilities** using the PumpPortal API for actual buy/sell transactions on Solana!

## 🔧 New Trading Functions

### `buy_token()` - Buy tokens with SOL
```python
buy_result = client.buy_token(
    private_key="your_base58_private_key",
    token_mint="token_contract_address", 
    amount_sol=0.01,                    # Amount of SOL to spend
    slippage_percent=5.0,               # Slippage tolerance (5%)
    priority_fee=0.005,                 # Priority fee in SOL
    pool="auto"                         # Exchange selection
)
```

### `sell_token()` - Sell tokens for SOL
```python
sell_result = client.sell_token(
    private_key="your_base58_private_key",
    token_mint="token_contract_address",
    amount_tokens=1000,                 # Number of tokens to sell
    slippage_percent=5.0,               # Slippage tolerance (5%)
    priority_fee=0.005,                 # Priority fee in SOL
    pool="auto"                         # Exchange selection
)
```

## 🏦 Supported Exchanges (Pool Options)

- **`"auto"`** (Recommended) - Automatically finds the best exchange
- **`"pump"`** - Pump.fun
- **`"raydium"`** - Raydium DEX
- **`"pump-amm"`** - Pump AMM
- **`"launchlab"`** - Launch Lab
- **`"raydium-cpmm"`** - Raydium CPMM
- **`"bonk"`** - Bonk DEX

## 🔒 How It Works

1. **PumpPortal Integration**: Uses PumpPortal's `/api/trade-local` endpoint
2. **Transaction Building**: PumpPortal builds the optimized transaction
3. **Local Signing**: Your private key signs the transaction locally (never sent to servers)
4. **RPC Submission**: Signed transaction is sent to Solana RPC endpoint
5. **Transaction Confirmation**: Returns transaction signature for monitoring

## 📖 Complete Trading Example

```python
from axiomtradeapi.client import AxiomTradeClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client with authentication
client = AxiomTradeClient(
    auth_token=os.getenv('auth-access-token'),
    refresh_token=os.getenv('auth-refresh-token')
)

# Your private key (keep secure!)
private_key = os.getenv('PRIVATE_KEY')

# Example: Buy a meme token
token_mint = "ACTUAL_TOKEN_MINT_ADDRESS_HERE"

# Buy 0.01 SOL worth of the token
buy_result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint,
    amount_sol=0.01,
    slippage_percent=5.0,
    priority_fee=0.005,
    pool="auto"
)

if buy_result["success"]:
    print(f"✅ Buy successful!")
    print(f"Transaction: https://solscan.io/tx/{buy_result['signature']}")
else:
    print(f"❌ Buy failed: {buy_result['error']}")

# Sell 500 tokens
sell_result = client.sell_token(
    private_key=private_key,
    token_mint=token_mint,
    amount_tokens=500,
    slippage_percent=5.0,
    priority_fee=0.005,
    pool="auto"
)

if sell_result["success"]:
    print(f"✅ Sell successful!")
    print(f"Transaction: https://solscan.io/tx/{sell_result['signature']}")
else:
    print(f"❌ Sell failed: {sell_result['error']}")
```

## 💡 Trading Tips

### 🎯 Finding Tokens to Trade
Use the analytics functions to find promising tokens:
```python
# Get trending tokens
trending = client.get_trending_tokens('1h')

# Analyze a specific token
pair_address = "TOKEN_PAIR_ADDRESS"
token_info = client.get_token_info_by_pair(pair_address)
pair_info = client.get_pair_info(pair_address)

# Get the token mint from pair info
token_mint = pair_info['tokenAddress']

# Now you can trade it!
buy_result = client.buy_token(private_key, token_mint, 0.01)
```

### 📊 Risk Management
```python
# Check developer reputation first
dev_address = pair_info['deployerAddress']
dev_analysis = client.get_token_analysis(dev_address, pair_info['tokenTicker'])

print(f"Developer risk level: {dev_analysis['creatorRiskLevel']}")
print(f"Developer rug count: {dev_analysis['creatorRugCount']}")

# Check holder distribution
holder_data = client.get_holder_data(pair_address)
```

### 💰 Portfolio Tracking
```python
# Check your positions
positions = client.get_meme_open_positions("YOUR_WALLET_ADDRESS")

# Monitor your trades
for position in positions:
    print(f"Token: {position['token']}, Amount: {position['amount']}")
```

## ⚠️ Important Safety Notes

### 🔐 Security
- **Private keys never leave your machine** - they're only used for local signing
- Always keep your private keys secure and never share them
- Use `.env` files for storing sensitive data
- Never commit private keys to version control

### 💸 Trading Safety
- **Start with small amounts** to test functionality
- Use appropriate slippage for market conditions (5-15% for volatile tokens)
- Monitor transactions on [Solscan](https://solscan.io/) or [Solana Explorer](https://explorer.solana.com/)
- Be aware of MEV bots and front-running
- Only trade tokens you've researched

### 🚨 Common Issues and Solutions

#### Bad Request (400) Error
- **Token not supported**: Some tokens may not be available on PumpPortal
- **Invalid mint address**: Ensure you're using the correct token contract address
- **Insufficient balance**: Make sure you have enough SOL or tokens
- **Pool not found**: Try using "auto" pool or a different exchange

#### Transaction Failed
- **Increase slippage**: Volatile tokens may need higher slippage tolerance
- **Increase priority fee**: During congestion, higher fees help transactions succeed
- **Try different pool**: Some exchanges may have better liquidity

## 🔄 Backward Compatibility

The existing functionality remains unchanged:
- All analytics functions still work
- Authentication system unchanged
- Balance checking and portfolio management intact
- WebSocket and other features unaffected

## 🚀 Ready for Production Trading!

Your AxiomTradeAPI client now supports:
- ✅ **Real trading** with actual buy/sell functionality
- ✅ **Multiple exchanges** via PumpPortal routing
- ✅ **Secure local signing** - private keys never sent to servers
- ✅ **Transaction monitoring** with explorer links
- ✅ **Comprehensive analytics** for informed trading decisions
- ✅ **Risk management tools** for safer trading

## 📋 Next Steps

1. **Test with small amounts** first
2. **Find tokens** using the analytics functions
3. **Analyze risks** before trading
4. **Start trading** with the new functionality
5. **Monitor** your transactions and portfolio

**Happy trading! 🎯📈**
