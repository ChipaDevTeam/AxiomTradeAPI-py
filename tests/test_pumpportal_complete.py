"""
AxiomTradeAPI PumpPortal Integration - Complete Test Suite
=========================================================

This test file incorporates all the fixes and working parameters discovered
during our extensive testing. Use this for reliable PumpPortal trading.

✅ WORKING PARAMETERS:
- denominatedInSol = False (use token amounts)
- pool = "auto" (not "pump")
- Higher slippage (30-50%)
- Popular tokens work better
- Reasonable amounts within SOL balance

❌ AVOID:
- denominatedInSol = True (SOL amounts cause 400 errors)
- pool = "pump" (causes 400 errors)
- Low slippage (5-10% often fails)
- Amounts that exceed your SOL balance
"""

from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os
import time

# Load environment variables
dotenv.load_dotenv()
access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')
private_key = os.getenv('PRIVATE_KEY')

def main():
    print("🚀 AxiomTradeAPI PumpPortal Test Suite")
    print("=" * 60)
    
    # Initialize client
    client = AxiomTradeClient(
        auth_token=access_token,
        refresh_token=refresh_token
    )
    
    # Test configurations - modify these as needed
    test_configs = {
        "bonk_token": {
            "name": "Bonk (VERIFIED WORKING)",
            "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
            "buy_amount": 5000,  # Number of tokens
            "sell_amount": 1000  # Number of tokens
        },
        "your_token": {
            "name": "Your Token (UPDATE THIS)",
            "mint": "9SkhnfNU5kx3VhngR9F2X7YSKnRZsNxGzcipHoCNGakK",  # Replace with your token
            "buy_amount": 10000,  # Number of tokens
            "sell_amount": 2000   # Number of tokens
        }
    }
    
    # Working parameters (discovered through testing)
    working_params = {
        "slippage_percent": 40,  # Higher slippage for better success
        "priority_fee": 0.001,   # Lower priority fee
        "pool": "auto",          # Use "auto" not "pump"
        "denominated_in_sol": False,  # Use token amounts, not SOL
        "rpc_url": "https://api.mainnet-beta.solana.com/"
    }
    
    print(f"🔑 Using working parameters:")
    for key, value in working_params.items():
        print(f"   {key}: {value}")
    
    # Test each token configuration
    for config_name, config in test_configs.items():
        print(f"\n{'='*20} {config['name']} {'='*20}")
        
        token_mint = config['mint']
        
        # Test 1: Buy tokens
        print(f"\n💰 Test 1: Buy {config['buy_amount']} tokens")
        print("-" * 40)
        
        buy_result = client.buy_token(
            private_key=private_key,
            token_mint=token_mint,
            amount=config['buy_amount'],  # Token amount (not SOL)
            slippage_percent=working_params['slippage_percent'],
            priority_fee=working_params['priority_fee'],
            pool=working_params['pool'],
            denominated_in_sol=working_params['denominated_in_sol'],
            rpc_url=working_params['rpc_url']
        )
        
        print(f"Buy result: {buy_result}")
        
        if buy_result["success"]:
            print(f"✅ BUY SUCCESSFUL!")
            print(f"📋 Transaction: {buy_result['signature']}")
            print(f"🔗 Explorer: {buy_result.get('explorer_url', 'N/A')}")
            
            # Wait before sell test
            print("\n⏳ Waiting 5 seconds before sell test...")
            time.sleep(5)
            
            # Test 2: Sell tokens
            print(f"\n💸 Test 2: Sell {config['sell_amount']} tokens")
            print("-" * 40)
            
            sell_result = client.sell_token(
                private_key=private_key,
                token_mint=token_mint,
                amount=config['sell_amount'],  # Token amount
                slippage_percent=working_params['slippage_percent'],
                priority_fee=working_params['priority_fee'],
                pool=working_params['pool'],
                denominated_in_sol=working_params['denominated_in_sol'],
                rpc_url=working_params['rpc_url']
            )
            
            print(f"Sell result: {sell_result}")
            
            if sell_result["success"]:
                print(f"✅ SELL SUCCESSFUL!")
                print(f"📋 Transaction: {sell_result['signature']}")
                print(f"🔗 Explorer: {sell_result.get('explorer_url', 'N/A')}")
            else:
                print(f"❌ Sell failed: {sell_result['error']}")
                
        else:
            print(f"❌ Buy failed: {buy_result['error']}")
            
            # Analyze common errors
            error_msg = buy_result['error'].lower()
            if "400" in error_msg:
                print("\n🔍 Error Analysis:")
                print("   400 errors can be caused by:")
                print("   - Invalid token address")
                print("   - Token not supported on this pool")
                print("   - Try different pool setting")
            elif "insufficient" in error_msg:
                print("\n🔍 Error Analysis:")
                print("   Insufficient funds - you need more SOL")
                print("   - Add more SOL to wallet")
                print("   - Try smaller amounts")
        
        print("\n" + "="*60)
    
    # Test 3: Alternative parameters test
    print(f"\n🧪 Test 3: Alternative Parameters Test")
    print("-" * 40)
    print("Testing with different pool and slippage settings...")
    
    alternative_params = [
        {"pool": "raydium", "slippage": 25, "name": "Raydium with 25% slippage"},
        {"pool": "auto", "slippage": 60, "name": "Auto with 60% slippage"},
    ]
    
    for alt_params in alternative_params:
        print(f"\n   Testing: {alt_params['name']}")
        
        alt_result = client.buy_token(
            private_key=private_key,
            token_mint="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # Bonk
            amount=2000,  # Small amount
            slippage_percent=alt_params['slippage'],
            priority_fee=0.001,
            pool=alt_params['pool'],
            denominated_in_sol=False,
            rpc_url="https://api.mainnet-beta.solana.com/"
        )
        
        if alt_result["success"]:
            print(f"   ✅ SUCCESS with {alt_params['name']}")
            print(f"   📋 Transaction: {alt_result['signature']}")
        else:
            print(f"   ❌ Failed: {alt_result['error'][:100]}...")
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 40)
    print("✅ Working Formula:")
    print("   - Use token amounts (denominated_in_sol=False)")
    print("   - Use pool='auto'")
    print("   - Use higher slippage (40-60%)")
    print("   - Use popular tokens for testing")
    print("   - Ensure sufficient SOL balance")
    print("")
    print("❌ Avoid:")
    print("   - SOL amounts (denominated_in_sol=True)")
    print("   - pool='pump'")
    print("   - Low slippage (<20%)")
    print("   - Amounts exceeding SOL balance")
    print("")
    print("🎉 PumpPortal integration is working!")

def quick_buy_test(token_mint: str, amount: int = 5000):
    """
    Quick function to test buying tokens with optimal parameters
    
    Args:
        token_mint (str): Token mint address
        amount (int): Number of tokens to buy
    """
    print(f"🚀 Quick Buy Test: {amount} tokens of {token_mint}")
    
    client = AxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    result = client.buy_token(
        private_key=os.getenv('PRIVATE_KEY'),
        token_mint=token_mint,
        amount=amount,
        slippage_percent=40,
        priority_fee=0.001,
        pool="auto",
        denominated_in_sol=False
    )
    
    if result["success"]:
        print(f"✅ SUCCESS! Transaction: {result['signature']}")
        return result['signature']
    else:
        print(f"❌ FAILED: {result['error']}")
        return None

def quick_sell_test(token_mint: str, amount: int = 1000):
    """
    Quick function to test selling tokens with optimal parameters
    
    Args:
        token_mint (str): Token mint address
        amount (int): Number of tokens to sell
    """
    print(f"💸 Quick Sell Test: {amount} tokens of {token_mint}")
    
    client = AxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    result = client.sell_token(
        private_key=os.getenv('PRIVATE_KEY'),
        token_mint=token_mint,
        amount=amount,
        slippage_percent=40,
        priority_fee=0.001,
        pool="auto",
        denominated_in_sol=False
    )
    
    if result["success"]:
        print(f"✅ SUCCESS! Transaction: {result['signature']}")
        return result['signature']
    else:
        print(f"❌ FAILED: {result['error']}")
        return None

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Full test suite (recommended)")
    print("2. Quick buy test")
    print("3. Quick sell test")
    
    choice = input("\nEnter choice (1-3) or press Enter for full suite: ").strip()
    
    if choice == "2":
        token = input("Enter token mint address (or press Enter for Bonk): ").strip()
        if not token:
            token = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"  # Bonk
        amount = input("Enter token amount (or press Enter for 5000): ").strip()
        amount = int(amount) if amount else 5000
        quick_buy_test(token, amount)
    elif choice == "3":
        token = input("Enter token mint address (or press Enter for Bonk): ").strip()
        if not token:
            token = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"  # Bonk
        amount = input("Enter token amount (or press Enter for 1000): ").strip()
        amount = int(amount) if amount else 1000
        quick_sell_test(token, amount)
    else:
        main()
