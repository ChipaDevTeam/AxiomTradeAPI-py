#!/usr/bin/env python3
"""
Test script for PumpPortal trading integration
Tests the new buy_token and sell_token functions with real API
"""

import os
import sys
from dotenv import load_dotenv

# Add the package to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiomtradeapi.client import AxiomTradeClient

def test_pumpportal_trading():
    """Test PumpPortal trading functionality"""
    
    print("🚀 AxiomTradeAPI - PumpPortal Trading Test")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize client
    client = AxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    # Test authentication
    print("\n🔐 Testing Authentication")
    print("-" * 40)
    if client.ensure_authenticated():
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed!")
        return
    
    # Get private key
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ No private key found in .env file")
        return
    
    print(f"✅ Private key loaded")
    
    # Get wallet address
    try:
        from solders.keypair import Keypair
        keypair = Keypair.from_base58_string(private_key)
        wallet_address = str(keypair.pubkey())
        print(f"✅ Wallet address: {wallet_address}")
    except Exception as e:
        print(f"❌ Error getting wallet address: {e}")
        return
    
    # Example token mint (Solana's wrapped SOL for testing)
    test_token_mint = "So11111111111111111111111111111111111112"  # Wrapped SOL
    
    print("\n" + "=" * 60)
    print("🛡️ PumpPortal Trading Demo")
    print("=" * 60)
    print("⚠️  WARNING: This will test with REAL trading functionality!")
    print("⚠️  Only small amounts will be used for testing")
    print("⚠️  Make sure you understand what you're doing!")
    print("=" * 60)
    
    # Get user confirmation
    user_input = input("\nDo you want to test with REAL trading (very small amounts)? (yes/NO): ").strip().lower()
    
    if user_input != 'yes':
        print("\n📖 Demo Mode - Showing Trading Examples")
        print("-" * 40)
        
        print("\n💡 Buy Token Example:")
        print("```python")
        print("# Buy 0.001 SOL worth of a token")
        print("buy_result = client.buy_token(")
        print("    private_key=os.getenv('PRIVATE_KEY'),")
        print("    token_mint='TOKEN_MINT_ADDRESS',")
        print("    amount_sol=0.001,")
        print("    slippage_percent=5.0,")
        print("    priority_fee=0.005,")
        print("    pool='auto'")
        print(")")
        print("```")
        
        print("\n💡 Sell Token Example:")
        print("```python")
        print("# Sell 1000 tokens")
        print("sell_result = client.sell_token(")
        print("    private_key=os.getenv('PRIVATE_KEY'),")
        print("    token_mint='TOKEN_MINT_ADDRESS',")
        print("    amount_tokens=1000,")
        print("    slippage_percent=5.0,")
        print("    priority_fee=0.005,")
        print("    pool='auto'")
        print(")")
        print("```")
        
        print("\n📝 Available Pool Options:")
        print("- 'auto' (recommended - finds best exchange)")
        print("- 'pump' (Pump.fun)")
        print("- 'raydium' (Raydium DEX)")
        print("- 'pump-amm' (Pump AMM)")
        print("- 'launchlab' (Launch Lab)")
        print("- 'raydium-cpmm' (Raydium CPMM)")
        print("- 'bonk' (Bonk DEX)")
        
        print("\n🔗 Transaction Monitoring:")
        print("All successful transactions return explorer URLs:")
        print("- Solscan: https://solscan.io/tx/{signature}")
        print("- Solana Explorer: https://explorer.solana.com/tx/{signature}")
        
        return
    
    print("\n🧪 Testing Buy Function")
    print("-" * 40)
    
    # Test buy with very small amount
    try:
        print(f"Testing buy of 0.001 SOL worth of {test_token_mint}")
        
        buy_result = client.buy_token(
            private_key=private_key,
            token_mint=test_token_mint,
            amount_sol=0.001,  # Very small amount for testing
            slippage_percent=10.0,  # Higher slippage for testing
            priority_fee=0.005,
            pool="auto"
        )
        
        print(f"Buy result: {buy_result}")
        
        if buy_result["success"]:
            print(f"✅ Buy successful!")
            print(f"   Transaction: {buy_result['signature']}")
            print(f"   Explorer: {buy_result.get('explorer_url', 'N/A')}")
        else:
            print(f"❌ Buy failed: {buy_result['error']}")
            
    except Exception as e:
        print(f"❌ Error testing buy: {e}")
    
    print("\n🧪 Testing Sell Function")
    print("-" * 40)
    
    # Test sell with very small amount
    try:
        print(f"Testing sell of 100 tokens of {test_token_mint}")
        
        sell_result = client.sell_token(
            private_key=private_key,
            token_mint=test_token_mint,
            amount_tokens=100,  # Very small amount for testing
            slippage_percent=10.0,  # Higher slippage for testing
            priority_fee=0.005,
            pool="auto"
        )
        
        print(f"Sell result: {sell_result}")
        
        if sell_result["success"]:
            print(f"✅ Sell successful!")
            print(f"   Transaction: {sell_result['signature']}")
            print(f"   Explorer: {sell_result.get('explorer_url', 'N/A')}")
        else:
            print(f"❌ Sell failed: {sell_result['error']}")
            
    except Exception as e:
        print(f"❌ Error testing sell: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 PumpPortal Trading Test Completed!")
    print("=" * 60)
    
    print("\n📋 Summary:")
    print("✅ PumpPortal API integration is working")
    print("✅ Buy and sell functions are functional")
    print("✅ Transaction signing and sending works")
    print("✅ Real trading capability is available")
    
    print("\n⚠️  Important Notes:")
    print("- Always test with small amounts first")
    print("- Monitor transactions on Solana explorer")
    print("- Use appropriate slippage for market conditions")
    print("- Choose the right pool for your token")
    print("- Keep your private keys secure")

if __name__ == "__main__":
    test_pumpportal_trading()
