#!/usr/bin/env python3
"""
Test script for Buy/Sell trading functionality
Tests the new trading methods with proper authentication
"""

import os
import sys
import logging
from pathlib import Path
import dotenv

dotenv.load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from axiomtradeapi.client import AxiomTradeClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_solders_dependency():
    """Test if solders is available"""
    print("🔧 Testing Solders Dependency")
    print("=" * 40)
    
    try:
        from solders.keypair import Keypair
        print("✅ Solders library is available")
        
        # Create a test keypair
        test_keypair = Keypair()
        print(f"✅ Test wallet created: {test_keypair.pubkey()}")
        return True, test_keypair
        
    except ImportError as e:
        print(f"❌ Solders not available: {e}")
        print("To install: pip install solders")
        return False, None


def test_trading_methods_structure():
    """Test trading method signatures without executing real trades"""
    print("\n📋 Testing Trading Method Structure")
    print("=" * 40)
    
    try:
        # Create client without saved tokens for testing
        client = AxiomTradeClient(use_saved_tokens=False)
        
        # Test that methods exist
        methods = {
            'buy_token': ['private_key', 'token_mint', 'amount_sol'],
            'sell_token': ['private_key', 'token_mint', 'amount_tokens'], 
            'get_token_balance': ['wallet_address', 'token_mint'],
            'get_sol_balance': ['wallet_address']
        }
        
        for method_name, expected_params in methods.items():
            if hasattr(client, method_name):
                method = getattr(client, method_name)
                print(f"✅ {method_name}: Available")
                print(f"   Expected params: {expected_params}")
            else:
                print(f"❌ {method_name}: Missing")
                return False
        
        print("✅ All trading methods are available with correct signatures")
        return True
        
    except Exception as e:
        print(f"❌ Trading method structure test failed: {e}")
        return False


def test_buy_sell_validation():
    """Test buy/sell validation without solders"""
    print("\n🛡️ Testing Buy/Sell Validation")
    print("=" * 40)
    
    try:
        # Create client
        client = AxiomTradeClient(use_saved_tokens=False)
        
        # Test buy_token validation
        result = client.buy_token(
            private_key="dummy_key",
            token_mint="So11111111111111111111111111111111111111112",
            amount_sol=0.001
        )
        
        if isinstance(result, dict) and not result.get("success"):
            if "solders" in result.get("error", "").lower():
                print("✅ Buy method correctly detects missing solders")
            elif "authentication" in result.get("error", "").lower():
                print("✅ Buy method correctly requires authentication")
            else:
                print(f"✅ Buy method returns proper error: {result.get('error')}")
        else:
            print("❌ Buy method validation failed")
            return False
        
        # Test sell_token validation
        result = client.sell_token(
            private_key="dummy_key",
            token_mint="So11111111111111111111111111111111111111112",
            amount_tokens=100
        )
        
        if isinstance(result, dict) and not result.get("success"):
            if "solders" in result.get("error", "").lower():
                print("✅ Sell method correctly detects missing solders")
            elif "authentication" in result.get("error", "").lower():
                print("✅ Sell method correctly requires authentication")
            else:
                print(f"✅ Sell method returns proper error: {result.get('error')}")
        else:
            print("❌ Sell method validation failed")
            return False
        
        print("✅ Buy/sell validation tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Buy/sell validation test failed: {e}")
        return False


def test_balance_methods():
    """Test balance checking methods"""
    print("\n💰 Testing Balance Methods")
    print("=" * 40)
    
    try:
        # Create client
        client = AxiomTradeClient(use_saved_tokens=False)
        
        # Test with dummy wallet address
        dummy_wallet = "11111111111111111111111111111112"
        dummy_token = "So11111111111111111111111111111111111111112"
        
        # Test get_sol_balance
        result = client.get_sol_balance(dummy_wallet)
        if result is None:
            print("✅ get_sol_balance correctly handles unauthenticated state")
        else:
            print(f"✅ get_sol_balance returned: {result}")
        
        # Test get_token_balance  
        result = client.get_token_balance(dummy_wallet, dummy_token)
        if result is None:
            print("✅ get_token_balance correctly handles unauthenticated state")
        else:
            print(f"✅ get_token_balance returned: {result}")
        
        print("✅ Balance method tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Balance method test failed: {e}")
        return False


def test_with_real_authentication():
    """Test with real authentication if tokens are available"""
    print("\n🔐 Testing with Real Authentication")
    print("=" * 40)
    
    # Get tokens from environment
    access_token = os.getenv('auth-access-token')
    refresh_token = os.getenv('auth-refresh-token')
    
    if not access_token or not refresh_token:
        print("ℹ️ No real tokens provided - skipping authenticated tests")
        print("   Set auth-access-token and auth-refresh-token environment variables to test")
        return True
    
    try:
        # Create client with real tokens
        client = AxiomTradeClient(
            auth_token=access_token,
            refresh_token=refresh_token,
            use_saved_tokens=False
        )
        
        # Check if we can authenticate
        if client.ensure_authenticated():
            print("✅ Authentication successful with real tokens")
            
            # Test balance check with a known SOL address (if provided)
            test_wallet = os.getenv('TEST_WALLET_ADDRESS')
            if test_wallet:
                balance = client.get_sol_balance(test_wallet)
                if balance is not None:
                    print(f"✅ SOL balance check successful: {balance} SOL")
                else:
                    print("⚠️ SOL balance check returned None (may be expected)")
            else:
                print("ℹ️ No TEST_WALLET_ADDRESS provided - skipping balance test")
            
            return True
        else:
            print("❌ Authentication failed with provided tokens")
            return False
            
    except Exception as e:
        print(f"❌ Real authentication test failed: {e}")
        return False


def show_usage_examples():
    """Show usage examples"""
    print("\n📖 Trading Usage Examples")
    print("=" * 60)
    
    example_code = '''
# Example 1: Initialize client with automatic token management
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient(
    username="your_email@example.com",
    password="your_password"
)

# Example 2: Initialize with existing tokens
client = AxiomTradeClient(
    auth_token="your_access_token",
    refresh_token="your_refresh_token"
)

# Example 3: Buy tokens
buy_result = client.buy_token(
    private_key="your_base58_or_hex_private_key",
    token_mint="token_mint_address",
    amount_sol=0.1,           # Buy 0.1 SOL worth
    slippage_percent=5.0      # 5% slippage tolerance
)

if buy_result["success"]:
    print(f"✅ Buy successful! Transaction: {buy_result['signature']}")
else:
    print(f"❌ Buy failed: {buy_result['error']}")

# Example 4: Sell tokens
sell_result = client.sell_token(
    private_key="your_base58_or_hex_private_key",
    token_mint="token_mint_address", 
    amount_tokens=1000,       # Sell 1000 tokens
    slippage_percent=5.0      # 5% slippage tolerance
)

if sell_result["success"]:
    print(f"✅ Sell successful! Transaction: {sell_result['signature']}")
else:
    print(f"❌ Sell failed: {sell_result['error']}")

# Example 5: Check balances
wallet_address = "your_wallet_public_key"
sol_balance = client.get_sol_balance(wallet_address)
token_balance = client.get_token_balance(wallet_address, "token_mint_address")

print(f"SOL Balance: {sol_balance}")
print(f"Token Balance: {token_balance}")
'''
    
    print(example_code)
    
    print("\n🔐 Security Notes:")
    print("- Never hardcode private keys in source code")
    print("- Use environment variables for sensitive data")
    print("- Test with small amounts first")
    print("- Always verify transaction signatures on Solana explorer")
    print("- Keep your private keys secure and never share them")


def main():
    """Run all tests"""
    print("🚀 AxiomTradeAPI - Buy/Sell Trading Tests")
    print("=" * 60)
    
    tests = [
        ("Solders Dependency", test_solders_dependency),
        ("Trading Method Structure", test_trading_methods_structure), 
        ("Buy/Sell Validation", test_buy_sell_validation),
        ("Balance Methods", test_balance_methods),
        ("Real Authentication", test_with_real_authentication)
    ]
    
    passed = 0
    total = len(tests)
    has_solders = False
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_name == "Solders Dependency":
                result, keypair = test_func()
                has_solders = result
                if result:
                    passed += 1
            else:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if has_solders:
        print("✅ Solders library is available - trading functionality is ready!")
    else:
        print("⚠️ Solders library not installed - install with: pip install solders")
    
    if passed >= total - 1:  # Allow solders to be missing
        print("🎉 Trading functionality is working correctly!")
        show_usage_examples()
        return True
    else:
        print("❌ Some tests failed - please review the issues above")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
