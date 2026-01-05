"""
AxiomTradeAPI PumpPortal - Interactive Buy & Sell Test
=====================================================

Simple test where you input a token address and it automatically:
1. Buys the token
2. Waits a moment
3. Sells the token

Uses all the working parameters we discovered during testing.
"""

from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os
import time

def main():
    print("🚀 PumpPortal Interactive Buy & Sell Test")
    print("=" * 50)
    
    # Load environment
    dotenv.load_dotenv()
    access_token = os.getenv('auth-access-token')
    refresh_token = os.getenv('auth-refresh-token')
    private_key = os.getenv('PRIVATE_KEY')
    
    if not all([access_token, refresh_token, private_key]):
        print("❌ Missing environment variables. Check your .env file:")
        print("   - auth-access-token")
        print("   - auth-refresh-token") 
        print("   - PRIVATE_KEY")
        return
    
    # Initialize client
    client = AxiomTradeClient(
        auth_token=access_token,
        refresh_token=refresh_token
    )
    
    # Get user input
    print("\n📝 Enter Token Details:")
    print("-" * 30)
    
    # Token address input
    token_mint = input("Token mint address (or press Enter for Bonk): ").strip()
    if not token_mint:
        token_mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"  # Default to Bonk
        print(f"Using default token: Bonk ({token_mint})")
    
    # Buy amount input
    buy_amount_input = input("Amount of tokens to buy (or press Enter for 5000): ").strip()
    buy_amount = int(buy_amount_input) if buy_amount_input else 5000
    
    # Sell percentage input
    sell_percentage_input = input("Percentage to sell back (or press Enter for 50%): ").strip()
    sell_percentage = int(sell_percentage_input) if sell_percentage_input else 50
    sell_amount = int(buy_amount * sell_percentage / 100)
    
    # Slippage input
    slippage_input = input("Slippage percentage (or press Enter for 40%): ").strip()
    slippage = int(slippage_input) if slippage_input else 40
    
    print(f"\n📋 Trade Summary:")
    print(f"   Token: {token_mint}")
    print(f"   Buy Amount: {buy_amount:,} tokens")
    print(f"   Sell Amount: {sell_amount:,} tokens ({sell_percentage}%)")
    print(f"   Slippage: {slippage}%")
    
    confirm = input(f"\nProceed with trade? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Trade cancelled")
        return
    
    # Working parameters (from our testing)
    trade_params = {
        "slippage_percent": slippage,
        "priority_fee": 0.001,
        "pool": "auto",  # This works better than "pump"
        "denominated_in_sol": False,  # Use token amounts
        "rpc_url": "https://api.mainnet-beta.solana.com/"
    }
    
    print(f"\n🔄 Starting Buy & Sell Test...")
    print("=" * 50)
    
    # STEP 1: BUY TOKENS
    print(f"\n💰 STEP 1: Buying {buy_amount:,} tokens...")
    print("-" * 40)
    
    buy_result = client.buy_token(
        private_key=private_key,
        token_mint=token_mint,
        amount=buy_amount,
        **trade_params
    )
    
    print(f"Buy Status: ", end="")
    if buy_result["success"]:
        print("✅ SUCCESS!")
        print(f"📋 Buy Transaction: {buy_result['signature']}")
        print(f"🔗 Explorer: {buy_result.get('explorer_url', 'N/A')}")
        
        # STEP 2: WAIT
        wait_time = 10
        print(f"\n⏳ STEP 2: Waiting {wait_time} seconds before selling...")
        for i in range(wait_time, 0, -1):
            print(f"   Waiting... {i}s", end="\r")
            time.sleep(1)
        print(f"   Waiting... Done! ✅")
        
        # STEP 3: SELL TOKENS
        print(f"\n💸 STEP 3: Selling {sell_amount:,} tokens...")
        print("-" * 40)
        
        sell_result = client.sell_token(
            private_key=private_key,
            token_mint=token_mint,
            amount=sell_amount,
            **trade_params
        )
        
        print(f"Sell Status: ", end="")
        if sell_result["success"]:
            print("✅ SUCCESS!")
            print(f"📋 Sell Transaction: {sell_result['signature']}")
            print(f"🔗 Explorer: {sell_result.get('explorer_url', 'N/A')}")
            
            # SUMMARY
            print(f"\n🎉 TRADE COMPLETE!")
            print("=" * 50)
            print(f"✅ Bought {buy_amount:,} tokens")
            print(f"✅ Sold {sell_amount:,} tokens")
            print(f"📊 Net Position: +{buy_amount - sell_amount:,} tokens")
            print(f"\n📋 Transactions:")
            print(f"   Buy:  {buy_result['signature']}")
            print(f"   Sell: {sell_result['signature']}")
            
        else:
            print("❌ FAILED!")
            print(f"❌ Sell Error: {sell_result['error']}")
            print(f"\n⚠️  You still own {buy_amount:,} tokens from the buy")
            print(f"📋 Buy Transaction: {buy_result['signature']}")
            
    else:
        print("❌ FAILED!")
        print(f"❌ Buy Error: {buy_result['error']}")
        
        # Error analysis
        error_msg = buy_result['error'].lower()
        print(f"\n🔍 Error Analysis:")
        if "400" in error_msg:
            print("   • 400 Bad Request - possible causes:")
            print("     - Token not supported on this exchange")
            print("     - Invalid token address")
            print("     - Try different slippage or pool setting")
        elif "insufficient" in error_msg:
            print("   • Insufficient funds:")
            print("     - Add more SOL to your wallet")
            print("     - Try smaller amount")
        elif "timeout" in error_msg:
            print("   • Network timeout:")
            print("     - Try again in a moment")
        else:
            print("   • Check token address and try again")

def quick_test():
    """Quick test with Bonk token (known to work)"""
    print("🚀 Quick Test with Bonk Token")
    print("=" * 40)
    
    dotenv.load_dotenv()
    client = AxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    # Test with Bonk (proven working token)
    token_mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    buy_amount = 3000
    sell_amount = 1500
    
    print(f"Testing with: {buy_amount} tokens buy, {sell_amount} tokens sell")
    
    # Buy
    print(f"\n💰 Buying {buy_amount} Bonk tokens...")
    buy_result = client.buy_token(
        private_key=os.getenv('PRIVATE_KEY'),
        token_mint=token_mint,
        amount=buy_amount,
        slippage_percent=40,
        priority_fee=0.001,
        pool="auto",
        denominated_in_sol=False
    )
    
    if buy_result["success"]:
        print(f"✅ Buy successful: {buy_result['signature']}")
        
        print(f"\n⏳ Waiting 5 seconds...")
        time.sleep(5)
        
        # Sell
        print(f"\n💸 Selling {sell_amount} Bonk tokens...")
        sell_result = client.sell_token(
            private_key=os.getenv('PRIVATE_KEY'),
            token_mint=token_mint,
            amount=sell_amount,
            slippage_percent=40,
            priority_fee=0.001,
            pool="auto",
            denominated_in_sol=False
        )
        
        if sell_result["success"]:
            print(f"✅ Sell successful: {sell_result['signature']}")
            print(f"🎉 Quick test complete!")
        else:
            print(f"❌ Sell failed: {sell_result['error']}")
    else:
        print(f"❌ Buy failed: {buy_result['error']}")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Interactive test (enter your own token)")
    print("2. Quick test (use Bonk token)")
    
    choice = input("\nEnter choice (1-2) or press Enter for interactive: ").strip()
    
    if choice == "2":
        quick_test()
    else:
        main()
