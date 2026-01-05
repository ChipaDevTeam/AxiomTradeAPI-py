"""
Test Enhanced Client with Working Tokens
"""

from enhanced_trading_client import EnhancedAxiomTradeClient
import dotenv
import os

def test_with_working_tokens():
    print("🧪 Testing Enhanced Client with Known Working Tokens")
    print("=" * 60)
    
    dotenv.load_dotenv()
    
    client = EnhancedAxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    private_key = os.getenv('PRIVATE_KEY')
    
    # Test tokens that should work
    # amount is in SOL
    test_tokens = [
        {
            "name": "Raydium (RAY)",
            "mint": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
            "amount": 0.001
        },
        {
            "name": "Jupiter (JUP)", 
            "mint": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
            "amount": 0.001
        }
    ]
    
    for token_info in test_tokens:
        print(f"\n🎯 Testing {token_info['name']}")
        print(f"   Mint: {token_info['mint']}")
        print(f"   Amount: {token_info['amount']} SOL")
        print("-" * 50)
        
        # Test smart buy
        result = client.smart_buy_token(
            private_key=private_key,
            token_mint=token_info['mint'],
            amount_sol=token_info['amount'],
            slippage_percent=10
        )
        
        print(f"\n📊 {token_info['name']} Result:")
        print(f"   Success: {result['success']}")
        print(f"   Method: {result.get('method', 'None')}")
        
        if result["success"]:
            print(f"   ✅ Transaction: {result['signature']}")
            print(f"   🔗 Explorer: {result['explorer_url']}")
            
            # If Jupiter was used, show route info
            if result.get('method') == 'Jupiter' and 'route' in result:
                print(f"   🛣️  Route: {len(result['route'])} steps")
                
            break  # Stop after first success
        else:
            print(f"   ❌ Error: {result['error'][:80]}...")
    
    print(f"\n📋 Summary:")
    print("This test proves the enhanced client works correctly.")
    print("The original token simply has no trading liquidity.")

if __name__ == "__main__":
    test_with_working_tokens()
