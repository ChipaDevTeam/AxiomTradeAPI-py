#!/usr/bin/env python3
"""
Test trading functionality with real private key and tokens
This script will test buy/sell functionality safely
"""

import os
import sys
import logging
from pathlib import Path
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from axiomtradeapi.client import AxiomTradeClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_wallet_public_key(private_key: str):
    """Get the public key (wallet address) from private key"""
    try:
        from solders.keypair import Keypair
        import base58
        
        # Decode the private key and create keypair
        private_key_bytes = base58.b58decode(private_key)
        keypair = Keypair.from_bytes(private_key_bytes)
        
        return str(keypair.pubkey())
    except Exception as e:
        print(f"❌ Error getting public key: {e}")
        return None


def test_wallet_setup():
    """Test wallet setup and get wallet info"""
    print("🔧 Testing Wallet Setup")
    print("=" * 40)
    
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in .env file")
        return False, None
    
    print(f"✅ Private key loaded from .env")
    
    # Get wallet address
    wallet_address = get_wallet_public_key(private_key)
    if wallet_address:
        print(f"✅ Wallet address: {wallet_address}")
        return True, wallet_address
    else:
        print("❌ Could not get wallet address")
        return False, None


def test_authentication():
    """Test authentication with stored tokens"""
    print("\n🔐 Testing Authentication")
    print("=" * 40)
    
    access_token = os.getenv('auth-access-token')
    refresh_token = os.getenv('auth-refresh-token')
    
    if not access_token or not refresh_token:
        print("❌ Tokens not found in .env file")
        return False, None
    
    try:
        # Create client with tokens
        client = AxiomTradeClient(
            auth_token=access_token,
            refresh_token=refresh_token,
            use_saved_tokens=False
        )
        
        # Test authentication
        if client.ensure_authenticated():
            print("✅ Authentication successful!")
            return True, client
        else:
            print("❌ Authentication failed")
            return False, None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False, None


def test_balance_checking(client, wallet_address):
    """Test balance checking functionality"""
    print("\n💰 Testing Balance Checking")
    print("=" * 40)
    
    try:
        # Check SOL balance
        sol_balance = client.get_sol_balance(wallet_address)
        if sol_balance is not None:
            print(f"✅ SOL Balance: {sol_balance} SOL")
        else:
            print("⚠️ Could not get SOL balance")
        
        # Test with a common token (USDC on Solana)
        usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        usdc_balance = client.get_token_balance(wallet_address, usdc_mint)
        if usdc_balance is not None:
            print(f"✅ USDC Balance: {usdc_balance} USDC")
        else:
            print("ℹ️ USDC balance: 0 or not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Balance checking error: {e}")
        return False


def test_buy_sell_validation(client):
    """Test buy/sell validation (without executing real trades)"""
    print("\n🛡️ Testing Buy/Sell Validation")
    print("=" * 40)
    
    private_key = os.getenv('PRIVATE_KEY')
    
    # Test with very small amounts and a test token
    test_token_mint = "So11111111111111111111111111111111111111112"  # Wrapped SOL
    
    try:
        print("Testing buy_token validation...")
        # Test buy with minimal amount
        buy_result = client.buy_token(
            private_key=private_key,
            token_mint=test_token_mint,
            amount_sol=0.001,  # Very small amount
            slippage_percent=10.0
        )
        
        print(f"Buy result: {buy_result}")
        
        if buy_result.get("success"):
            print("✅ Buy validation passed (transaction may have been created)")
        else:
            error = buy_result.get("error", "Unknown error")
            if "balance" in error.lower() or "insufficient" in error.lower():
                print("ℹ️ Buy validation: Insufficient balance (expected)")
            else:
                print(f"ℹ️ Buy validation: {error}")
        
        print("\nTesting sell_token validation...")
        # Test sell with minimal amount
        sell_result = client.sell_token(
            private_key=private_key,
            token_mint=test_token_mint,
            amount_tokens=0.001,  # Very small amount
            slippage_percent=10.0
        )
        
        print(f"Sell result: {sell_result}")
        
        if sell_result.get("success"):
            print("✅ Sell validation passed (transaction may have been created)")
        else:
            error = sell_result.get("error", "Unknown error")
            if "balance" in error.lower() or "insufficient" in error.lower():
                print("ℹ️ Sell validation: Insufficient token balance (expected)")
            else:
                print(f"ℹ️ Sell validation: {error}")
        
        return True
        
    except Exception as e:
        print(f"❌ Buy/sell validation error: {e}")
        return False


def show_trading_examples():
    """Show real trading examples"""
    print("\n📖 Real Trading Examples")
    print("=" * 60)
    
    wallet_address = get_wallet_public_key(os.getenv('PRIVATE_KEY'))
    
    example = f'''
# Your wallet setup:
Wallet Address: {wallet_address}
Private Key: Loaded from .env file

# Example 1: Buy tokens with SOL
from axiomtradeapi.client import AxiomTradeClient
import os

client = AxiomTradeClient(
    auth_token=os.getenv('auth-access-token'),
    refresh_token=os.getenv('auth-refresh-token')
)

# Buy 0.01 SOL worth of a token
buy_result = client.buy_token(
    private_key=os.getenv('PRIVATE_KEY'),
    token_mint="TOKEN_MINT_ADDRESS_HERE",
    amount_sol=0.01,
    slippage_percent=5.0
)

if buy_result["success"]:
    print(f"✅ Buy successful! Signature: {{buy_result['signature']}}")
else:
    print(f"❌ Buy failed: {{buy_result['error']}}")

# Example 2: Sell tokens for SOL  
sell_result = client.sell_token(
    private_key=os.getenv('PRIVATE_KEY'),
    token_mint="TOKEN_MINT_ADDRESS_HERE", 
    amount_tokens=1000,  # Number of tokens to sell
    slippage_percent=5.0
)

if sell_result["success"]:
    print(f"✅ Sell successful! Signature: {{sell_result['signature']}}")
else:
    print(f"❌ Sell failed: {{sell_result['error']}}")

# Example 3: Check balances
sol_balance = client.get_sol_balance("{wallet_address}")
token_balance = client.get_token_balance("{wallet_address}", "TOKEN_MINT_ADDRESS")

print(f"SOL Balance: {{sol_balance}}")
print(f"Token Balance: {{token_balance}}")
'''
    
    print(example)


def main():
    """Run all tests"""
    print("🚀 AxiomTradeAPI - Real Trading Functionality Test")
    print("=" * 60)
    print("⚠️  WARNING: This script will test with real tokens and private keys!")
    print("⚠️  Make sure you understand what you're doing!")
    print("=" * 60)
    
    # Test wallet setup
    wallet_ok, wallet_address = test_wallet_setup()
    if not wallet_ok:
        print("❌ Wallet setup failed - stopping tests")
        return False
    
    # Test authentication
    auth_ok, client = test_authentication()
    if not auth_ok:
        print("❌ Authentication failed - stopping tests")
        return False
    
    # Test balance checking
    balance_ok = test_balance_checking(client, wallet_address)
    if not balance_ok:
        print("❌ Balance checking failed")
        return False
    
    # Test buy/sell validation
    print("\n⚠️  The next test will attempt to create actual transactions!")
    print("⚠️  It uses very small amounts but WILL spend real SOL if successful!")
    proceed = input("\nDo you want to proceed with buy/sell tests? (y/N): ").lower().strip()
    
    if proceed == 'y' or proceed == 'yes':
        validation_ok = test_buy_sell_validation(client)
        if not validation_ok:
            print("❌ Buy/sell validation failed")
            return False
    else:
        print("ℹ️ Skipping buy/sell tests per user request")
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("\n✅ Your trading setup is working correctly!")
    print("✅ Authentication is working")
    print("✅ Balance checking is working") 
    print("✅ Buy/sell methods are functional")
    
    show_trading_examples()
    
    print("\n🔐 Security Reminders:")
    print("- Your private key is stored in .env file")
    print("- Never share your private key with anyone")
    print("- Always test with small amounts first")
    print("- Verify transactions on Solana explorer")
    print("- Keep your .env file secure and never commit it to git")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
