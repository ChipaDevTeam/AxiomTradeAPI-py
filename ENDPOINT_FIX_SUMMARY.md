# Endpoint Fix Summary

## Issue
Users were experiencing 404 errors when calling:
- `client.GetBalance()` - Balance check method
- `client.buy_token()` - Buy transaction method
- Other trading-related endpoints

Error messages:
```
{'success': False, 'error': 'Failed to get buy transaction: 404 - <html><body><h1>File Not Found</h1><hr><i>uWebSockets/20 Server</i></body></html>'}
```

## Root Cause
The SDK was using `https://api6.axiom.trade` as the base URL for balance and trading endpoints, but the actual Axiom Trade application uses `https://axiom.trade/api`.

## Fix Applied
Changed `BASE_URL_API` in `axiomtradeapi/content/endpoints.py`:
- **Before:** `BASE_URL_API = "https://api6.axiom.trade"`
- **After:** `BASE_URL_API = "https://axiom.trade/api"`

## Impact
This fix affects the following endpoints:

### Balance Endpoints
- `/sol-balance` → `https://axiom.trade/api/sol-balance`
- `/batched-sol-balance` → `https://axiom.trade/api/batched-sol-balance`
- `/token-balance` → `https://axiom.trade/api/token-balance`

### Trading Endpoints
- `/buy` → `https://axiom.trade/api/buy`
- `/sell` → `https://axiom.trade/api/sell`
- `/send-transaction` → `https://axiom.trade/api/send-transaction`

## Affected Methods

### Default Client (`AxiomTradeClient`)
These methods in the default `AxiomTradeClient` class are now fixed:
- `GetBalance()` - Get balance for a single wallet
- `GetBatchedBalance()` - Get balances for multiple wallets
- `buy_token()` - Buy tokens
- `sell_token()` - Sell tokens
- `get_token_balance()` - Get token balance

### Enhanced Client (`EnhancedAxiomTradeClient`)
These methods in the enhanced client are now fixed:
- `get_sol_balance()` - Get SOL balance
- `get_token_balance()` - Get token balance

## Verification
All endpoint URLs have been verified to match the expected format used by the Axiom Trade web application.

## Notes
- Authentication endpoints (like `refresh_access_token` at `api9.axiom.trade`) continue to use their respective base URLs - these were already working correctly
- Trending tokens endpoint (`/meme-trending` at `api6.axiom.trade`) remains unchanged - this was already working correctly
- Portfolio endpoint (`/portfolio` at `api6.axiom.trade`) remains unchanged - this was already working correctly
- **Only balance and trading endpoints** were affected by this fix, as they are the ones that should use `https://axiom.trade/api`
