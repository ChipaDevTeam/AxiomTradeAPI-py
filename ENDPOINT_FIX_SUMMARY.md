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

### Default Client (`AxiomTradeClient` from `_client.py`)
- `AxiomTradeClient.GetBalance()` - Get balance for a single wallet
- `AxiomTradeClient.GetBatchedBalance()` - Get balances for multiple wallets
- `AxiomTradeClient.buy_token()` - Buy tokens
- `AxiomTradeClient.sell_token()` - Sell tokens
- `AxiomTradeClient.get_token_balance()` - Get token balance

### Enhanced Client (`EnhancedAxiomTradeClient` from `client.py`)
- `EnhancedAxiomTradeClient.get_sol_balance()` - Get SOL balance
- `EnhancedAxiomTradeClient.get_token_balance()` - Get token balance

## Verification
All endpoint URLs have been verified to match the expected format used by the Axiom Trade web application.

## Notes
- Authentication endpoints (like `refresh_access_token`) continue to use their respective base URLs (e.g., `api9.axiom.trade`)
- Other feature endpoints (trending tokens, portfolio) remain unchanged as they were already working correctly
