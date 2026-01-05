# AxiomTradeAPI Trading Functions

This document explains how to use the new buy and sell functions added to the AxiomTradeAPI Python client.

## Prerequisites

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Have your AxiomTrade account credentials
3. Have your Solana wallet private key (base58 encoded)

## New Trading Functions

### `buy_token(private_key, token_mint, amount_sol, slippage_percent=5.0)`

Buys a token using SOL from your wallet.

**Parameters:**
- `private_key` (str): Your wallet's private key in base58 format
- `token_mint` (str): The mint address of the token you want to buy
- `amount_sol` (float): Amount of SOL to spend on the purchase
- `slippage_percent` (float, optional): Slippage tolerance percentage (default: 5.0%)

**Returns:**
Dictionary with:
- `success` (bool): Whether the transaction was successful
- `signature` (str): Transaction signature if successful
- `error` (str): Error message if failed

**Example:**
```python
result = client.buy_token(
    private_key="your_base58_private_key",
    token_mint="So11111111111111111111111111111111111111112",
    amount_sol=0.1,
    slippage_percent=5.0
)
```

### `sell_token(private_key, token_mint, amount_tokens, slippage_percent=5.0)`

Sells tokens from your wallet for SOL.

**Parameters:**
- `private_key` (str): Your wallet's private key in base58 format
- `token_mint` (str): The mint address of the token you want to sell
- `amount_tokens` (float): Amount of tokens to sell
- `slippage_percent` (float, optional): Slippage tolerance percentage (default: 5.0%)

**Returns:**
Dictionary with:
- `success` (bool): Whether the transaction was successful
- `signature` (str): Transaction signature if successful
- `error` (str): Error message if failed

**Example:**
```python
result = client.sell_token(
    private_key="your_base58_private_key",
    token_mint="So11111111111111111111111111111111111111112",
    amount_tokens=1000,
    slippage_percent=5.0
)
```

### `get_token_balance(wallet_address, token_mint)`

Gets the balance of a specific token in your wallet.

**Parameters:**
- `wallet_address` (str): Your wallet's public key
- `token_mint` (str): The mint address of the token

**Returns:**
- `float`: Token balance, or `None` if error

**Example:**
```python
balance = client.get_token_balance(
    wallet_address="your_wallet_public_key",
    token_mint="So11111111111111111111111111111111111111112"
)
```

## Complete Trading Example

```python
import asyncio
import logging
from axiomtradeapi import AxiomTradeClient

async def trading_example():
    # Initialize client
    client = AxiomTradeClient(
        username="your_email@example.com",
        password="your_password"
    )
    
    private_key = "your_base58_private_key"
    token_mint = "token_mint_address"
    wallet_address = "your_wallet_public_key"
    
    try:
        # Check current balances
        sol_balance = client.GetBalance(wallet_address)
        token_balance = client.get_token_balance(wallet_address, token_mint)
        
        print(f"SOL Balance: {sol_balance['sol'] if sol_balance else 'N/A'}")
        print(f"Token Balance: {token_balance if token_balance else 'N/A'}")
        
        # Buy tokens
        buy_result = client.buy_token(
            private_key=private_key,
            token_mint=token_mint,
            amount_sol=0.1,
            slippage_percent=5.0
        )
        
        if buy_result["success"]:
            print(f"✅ Buy successful: {buy_result['signature']}")
        else:
            print(f"❌ Buy failed: {buy_result['error']}")
        
        # Wait a moment, then sell
        await asyncio.sleep(5)
        
        # Check new token balance
        new_token_balance = client.get_token_balance(wallet_address, token_mint)
        
        if new_token_balance and new_token_balance > 0:
            # Sell half of the tokens
            sell_amount = new_token_balance / 2
            
            sell_result = client.sell_token(
                private_key=private_key,
                token_mint=token_mint,
                amount_tokens=sell_amount,
                slippage_percent=5.0
            )
            
            if sell_result["success"]:
                print(f"✅ Sell successful: {sell_result['signature']}")
            else:
                print(f"❌ Sell failed: {sell_result['error']}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if hasattr(client, 'ws') and client.ws:
            await client.ws.close()

# Run the example
asyncio.run(trading_example())
```

## Security Notes

1. **Never hardcode private keys** in your source code
2. Use environment variables or secure key management
3. Always test with small amounts first
4. Be aware of slippage and market conditions
5. Monitor your transactions on Solana explorers

## Error Handling

The trading functions return detailed error information. Always check the `success` field:

```python
result = client.buy_token(...)
if result["success"]:
    print(f"Transaction successful: {result['signature']}")
else:
    print(f"Transaction failed: {result['error']}")
```

## Supported Private Key Formats

The client supports multiple private key formats:
- Base58 encoded string (recommended)
- Hex encoded string
- Raw bytes

## Dependencies

The trading functions use the following key libraries:
- `solders`: Solana SDK for Python
- `base58`: Base58 encoding/decoding
- `requests`: HTTP requests to AxiomTrade API
