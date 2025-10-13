"""
Example: Using the Blockchain-Migrated AxiomTradeClient

This example demonstrates how to use the updated AxiomTradeClient after the
blockchain migration. All trading and balance operations now use blockchain-direct
methods instead of Axiom API endpoints.
"""

from axiomtradeapi import AxiomTradeClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_balance_check():
    """
    Example: Check SOL balance using Solana RPC directly
    """
    print("=" * 60)
    print("Example 1: Check SOL Balance")
    print("=" * 60)
    
    # Initialize client with authentication
    client = AxiomTradeClient(
        username=os.getenv("AXIOM_USERNAME"),
        password=os.getenv("AXIOM_PASSWORD")
    )
    
    # Get balance for your wallet
    wallet_address = os.getenv("WALLET_ADDRESS")
    balance = client.GetBalance(wallet_address)
    
    if balance:
        print(f"✅ Wallet: {wallet_address}")
        print(f"   Balance: {balance['sol']} SOL")
        print(f"   Lamports: {balance['lamports']}")
        print(f"   Slot: {balance['slot']}")
    else:
        print("❌ Failed to fetch balance")
    
    # You can also use a custom RPC endpoint
    balance_helius = client.GetBalance(
        wallet_address, 
        rpc_url="https://mainnet.helius-rpc.com/"
    )
    
    print("\n")

def example_token_balance():
    """
    Example: Check token balance using Solana RPC
    """
    print("=" * 60)
    print("Example 2: Check Token Balance")
    print("=" * 60)
    
    client = AxiomTradeClient(
        username=os.getenv("AXIOM_USERNAME"),
        password=os.getenv("AXIOM_PASSWORD")
    )
    
    wallet_address = os.getenv("WALLET_ADDRESS")
    token_mint = os.getenv("TOKEN_MINT")  # e.g., USDC mint address
    
    token_balance = client.get_token_balance(wallet_address, token_mint)
    
    if token_balance is not None:
        print(f"✅ Token Balance: {token_balance}")
    else:
        print("❌ No token account found or error occurred")
    
    print("\n")

def example_buy_token():
    """
    Example: Buy a token using PumpPortal API
    
    ⚠️  IMPORTANT SAFETY NOTES:
    - This executes a REAL transaction with REAL money
    - Test on DEVNET first before using mainnet
    - Use small amounts for initial testing
    - Verify addresses and amounts carefully
    
    For devnet testing, use devnet RPC:
    rpc_url="https://api.devnet.solana.com"
    """
    print("=" * 60)
    print("Example 3: Buy Token via PumpPortal")
    print("=" * 60)
    
    client = AxiomTradeClient(
        username=os.getenv("AXIOM_USERNAME"),
        password=os.getenv("AXIOM_PASSWORD")
    )
    
    # IMPORTANT: This will execute a real transaction!
    # Make sure you understand what you're doing before uncommenting
    # For testing, use devnet first: rpc_url="https://api.devnet.solana.com"
    
    # result = client.buy_token(
    #     private_key=os.getenv("PRIVATE_KEY"),
    #     token_mint="<TOKEN_MINT_ADDRESS>",
    #     amount_sol=0.01,              # Buy with 0.01 SOL
    #     slippage_percent=10,          # 10% slippage tolerance
    #     priority_fee=0.005,           # 0.005 SOL priority fee
    #     pool="auto"                   # Auto-select best DEX
    # )
    # 
    # if result['success']:
    #     print(f"✅ Transaction successful!")
    #     print(f"   Signature: {result['signature']}")
    #     print(f"   Explorer: {result['explorer_url']}")
    # else:
    #     print(f"❌ Transaction failed: {result['error']}")
    
    print("⚠️  Example commented out for safety")
    print("   Uncomment the code above to execute a real buy transaction")
    print("\n")

def example_sell_token():
    """
    Example: Sell a token using PumpPortal API
    
    ⚠️  IMPORTANT SAFETY NOTES:
    - This executes a REAL transaction with REAL money
    - Test on DEVNET first before using mainnet
    - Use small amounts for initial testing
    - Verify addresses and amounts carefully
    
    For devnet testing, use devnet RPC:
    rpc_url="https://api.devnet.solana.com"
    """
    print("=" * 60)
    print("Example 4: Sell Token via PumpPortal")
    print("=" * 60)
    
    client = AxiomTradeClient(
        username=os.getenv("AXIOM_USERNAME"),
        password=os.getenv("AXIOM_PASSWORD")
    )
    
    # IMPORTANT: This will execute a real transaction!
    # Make sure you understand what you're doing before uncommenting
    # For testing, use devnet first: rpc_url="https://api.devnet.solana.com"
    
    # Sell specific amount
    # result = client.sell_token(
    #     private_key=os.getenv("PRIVATE_KEY"),
    #     token_mint="<TOKEN_MINT_ADDRESS>",
    #     amount_tokens=1000,           # Sell 1000 tokens
    #     slippage_percent=10,
    #     priority_fee=0.005,
    #     pool="auto"
    # )
    
    # Or sell all tokens (100%)
    # result = client.sell_token(
    #     private_key=os.getenv("PRIVATE_KEY"),
    #     token_mint="<TOKEN_MINT_ADDRESS>",
    #     amount_tokens="100%",         # Sell all owned tokens
    #     slippage_percent=10,
    #     priority_fee=0.005,
    #     pool="auto"
    # )
    # 
    # if result['success']:
    #     print(f"✅ Transaction successful!")
    #     print(f"   Signature: {result['signature']}")
    #     print(f"   Explorer: {result['explorer_url']}")
    # else:
    #     print(f"❌ Transaction failed: {result['error']}")
    
    print("⚠️  Example commented out for safety")
    print("   Uncomment the code above to execute a real sell transaction")
    print("\n")

def example_custom_rpc():
    """
    Example: Using custom RPC endpoints for better performance
    """
    print("=" * 60)
    print("Example 5: Custom RPC Endpoints")
    print("=" * 60)
    
    client = AxiomTradeClient(
        username=os.getenv("AXIOM_USERNAME"),
        password=os.getenv("AXIOM_PASSWORD")
    )
    
    wallet_address = os.getenv("WALLET_ADDRESS")
    
    # Use Helius RPC (faster, rate-limited)
    helius_balance = client.GetBalance(
        wallet_address,
        rpc_url="https://mainnet.helius-rpc.com/"
    )
    
    # Use QuickNode (if you have an account)
    # quicknode_balance = client.GetBalance(
    #     wallet_address,
    #     rpc_url="https://your-quicknode-endpoint.com/"
    # )
    
    # Use Triton (if you have an account)
    # triton_balance = client.GetBalance(
    #     wallet_address,
    #     rpc_url="https://your-triton-endpoint.com/"
    # )
    
    print("✅ You can use any Solana RPC endpoint you prefer!")
    print("   Popular options: Helius, QuickNode, Triton, Alchemy")
    print("\n")

if __name__ == "__main__":
    print("\n🚀 AxiomTradeClient Blockchain Migration Examples\n")
    print("These examples show how to use the updated client after")
    print("migrating from Axiom API endpoints to blockchain-direct methods.\n")
    
    # Safe examples (read-only operations)
    print("📖 Read-Only Examples (Safe to run):")
    print("-" * 60)
    example_balance_check()
    example_token_balance()
    example_custom_rpc()
    
    # Transaction examples (commented for safety)
    print("⚠️  Transaction Examples (Commented for safety):")
    print("-" * 60)
    example_buy_token()
    example_sell_token()
    
    print("=" * 60)
    print("✅ Examples completed!")
    print("\nNext steps:")
    print("1. Set your credentials in .env file")
    print("2. Run the read-only examples first")
    print("3. Carefully uncomment transaction examples if needed")
    print("4. Always test with small amounts first!")
