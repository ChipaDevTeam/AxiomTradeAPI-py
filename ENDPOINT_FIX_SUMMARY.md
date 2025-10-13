# Endpoint Fix Summary - BLOCKCHAIN MIGRATION

## Issue
Users were experiencing 404 errors when calling:
- `client.GetBalance()` - Balance check method
- `client.buy_token()` - Buy transaction method
- `client.sell_token()` - Sell transaction method
- Other trading-related endpoints

Error messages:
```
{'success': False, 'error': 'Failed to get buy transaction: 404 - <html><body><h1>File Not Found</h1><hr><i>uWebSockets/20 Server</i></body></html>'}
```

## Root Cause
The SDK was using `https://axiom.trade/api` endpoints for balance and trading operations, but these endpoints were returning 404 errors and are no longer available.

## Solution Applied - BLOCKCHAIN MIGRATION
Following the maintainer's comment about migrating to use the Solana blockchain directly, we've migrated all trading and balance operations to use blockchain-native methods:

### Trading Operations (buy_token, sell_token)
- **Before:** Used Axiom API endpoints (`/buy`, `/sell`, `/send-transaction`)
- **After:** Use PumpPortal API (https://pumpportal.fun/api/trade-local) + Solana RPC
- **Implementation:** Same approach as the EnhancedAxiomTradeClient

### Balance Operations (GetBalance, GetBatchedBalance, get_token_balance)
- **Before:** Used Axiom API endpoints (`/sol-balance`, `/batched-sol-balance`, `/token-balance`)
- **After:** Use Solana RPC directly (`getBalance`, `getTokenAccountsByOwner`)
- **Benefit:** No dependency on Axiom API, works with any Solana RPC endpoint

## Impact
This migration affects the following methods and their underlying implementation:

### Trading Methods (Now use PumpPortal + Solana RPC)
- `buy_token()` → PumpPortal API + Solana RPC
- `sell_token()` → PumpPortal API + Solana RPC

### Balance Methods (Now use Solana RPC directly)
- `GetBalance()` → Solana RPC `getBalance`
- `GetBatchedBalance()` → Solana RPC `getBalance` (batched)
- `get_token_balance()` → Solana RPC `getTokenAccountsByOwner`

### No Longer Used (Removed)
- ~~`/buy` endpoint~~
- ~~`/sell` endpoint~~
- ~~`/send-transaction` endpoint~~
- ~~`/sol-balance` endpoint~~
- ~~`/batched-sol-balance` endpoint~~
- ~~`/token-balance` endpoint~~

## Affected Methods

### Default Client (`AxiomTradeClient`)
These methods in the default `AxiomTradeClient` class have been migrated:

#### Trading Methods
- `buy_token(private_key, token_mint, amount_sol, slippage_percent=5.0, priority_fee=0.005, pool="auto", rpc_url=...)` 
  - Now uses PumpPortal API for transaction creation
  - Signs and sends via Solana RPC
  - Returns transaction signature with Solscan explorer link
  
- `sell_token(private_key, token_mint, amount_tokens, slippage_percent=5.0, priority_fee=0.005, pool="auto", rpc_url=...)`
  - Now uses PumpPortal API for transaction creation
  - Signs and sends via Solana RPC
  - Returns transaction signature with Solscan explorer link

#### Balance Methods
- `GetBalance(wallet_address, rpc_url=...)` 
  - Now uses Solana RPC `getBalance` method
  - Returns dict with `sol`, `lamports`, and `slot`
  
- `GetBatchedBalance(wallet_addresses, rpc_url=...)`
  - Now fetches balances individually via Solana RPC
  - Returns dict mapping addresses to balance info
  
- `get_token_balance(wallet_address, token_mint, rpc_url=...)`
  - Now uses Solana RPC `getTokenAccountsByOwner` method
  - Returns token balance as float

### Enhanced Client (`EnhancedAxiomTradeClient`)
No changes needed - already uses PumpPortal for trading and has similar RPC-based balance methods.

## Technical Details

### PumpPortal Integration
Trading operations now follow the PumpPortal API specification:
1. Create transaction via POST to `https://pumpportal.fun/api/trade-local`
2. Sign the returned VersionedTransaction with user's keypair
3. Send to Solana RPC endpoint using `SendVersionedTransaction`

### Solana RPC Integration  
Balance operations use standard Solana JSON-RPC methods:
- `getBalance` - Get SOL balance
- `getTokenAccountsByOwner` - Get SPL token balances

### Removed Code
- `_get_keypair_from_private_key()` - No longer needed (use `Keypair.from_base58_string()`)
- `_sign_and_send_transaction()` - No longer needed (inline PumpPortal flow)


## Verification
All method signatures have been verified and tested:
- ✅ buy_token uses PumpPortal API
- ✅ sell_token uses PumpPortal API  
- ✅ GetBalance uses Solana RPC
- ✅ GetBatchedBalance uses Solana RPC
- ✅ get_token_balance uses Solana RPC
- ✅ Old helper methods removed
- ✅ Method signatures backward compatible with additional optional parameters

## Benefits of Blockchain Migration
1. **No API Dependencies**: Direct blockchain access means no reliance on Axiom's API endpoints
2. **More Reliable**: Solana RPC is the standard, stable interface
3. **Flexible**: Users can specify their own RPC endpoint
4. **Transparent**: Direct blockchain interaction is more trustworthy
5. **Future-proof**: Not affected by API changes or deprecations

## Migration Guide for Users
### For Existing Code
Your existing code will continue to work! The method signatures are backward compatible:

```python
# Old usage - still works!
balance = client.GetBalance(wallet_address)
result = client.buy_token(private_key, token_mint, 0.01, 5)
```

### Using Custom RPC Endpoints
You can now specify your own Solana RPC endpoint:

```python
# Use Helius RPC
balance = client.GetBalance(wallet_address, rpc_url="https://mainnet.helius-rpc.com/")

# Use QuickNode
result = client.buy_token(
    private_key, 
    token_mint, 
    0.01, 
    rpc_url="https://your-quicknode-endpoint.com/"
)
```

### Additional PumpPortal Parameters
Trading methods now support PumpPortal features:

```python
result = client.buy_token(
    private_key,
    token_mint,
    amount_sol=0.01,
    slippage_percent=10,      # Adjust slippage tolerance
    priority_fee=0.01,        # Set priority fee
    pool="raydium"            # Choose specific DEX
)
```

## Notes
- Authentication endpoints (like `refresh_access_token` at `api9.axiom.trade`) continue to use their respective base URLs - these were already working correctly
- WebSocket endpoints for new tokens, orders, and positions remain unchanged
- Only balance and trading operations have been migrated to blockchain-direct methods
