"""
Detailed PumpPortal API Diagnostic
This will help us understand why we're getting 400 errors even with real tokens
"""

import requests
import json
from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os

dotenv.load_dotenv()
access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')
private_key = os.getenv('PRIVATE_KEY')

# Real pump.fun token you're using
token_mint = "9SkhnfNU5kx3VhngR9F2X7YSKnRZsNxGzcipHoCNGakK"

print("🔍 PumpPortal API Diagnostic")
print("=" * 60)
print(f"Token: {token_mint}")
print(f"Private key length: {len(private_key) if private_key else 'Not set'}")

try:
    from solders.keypair import Keypair
    
    # Get public key
    keypair = Keypair.from_base58_string(private_key)
    public_key = str(keypair.pubkey())
    print(f"Public key: {public_key}")
    
    # Test different request variations to see what PumpPortal accepts
    test_cases = [
        {
            "name": "Small SOL amount (0.001 SOL)",
            "data": {
                "publicKey": public_key,
                "action": "buy",
                "mint": token_mint,
                "amount": 1000000,  # 0.001 SOL in lamports
                "denominatedInSol": "true",
                "slippage": 10,
                "priorityFee": 0.005,
                "pool": "auto"
            }
        },
        {
            "name": "Larger SOL amount (0.01 SOL)",
            "data": {
                "publicKey": public_key,
                "action": "buy",
                "mint": token_mint,
                "amount": 10000000,  # 0.01 SOL in lamports
                "denominatedInSol": "true",
                "slippage": 15,
                "priorityFee": 0.01,
                "pool": "auto"
            }
        },
        {
            "name": "Token amount instead of SOL",
            "data": {
                "publicKey": public_key,
                "action": "buy",
                "mint": token_mint,
                "amount": 100000,  # 100k tokens
                "denominatedInSol": "false",
                "slippage": 20,
                "priorityFee": 0.005,
                "pool": "auto"
            }
        },
        {
            "name": "Different pool (pump instead of auto)",
            "data": {
                "publicKey": public_key,
                "action": "buy",
                "mint": token_mint,
                "amount": 5000000,  # 0.005 SOL in lamports
                "denominatedInSol": "true",
                "slippage": 10,
                "priorityFee": 0.005,
                "pool": "pump"
            }
        }
    ]
    
    print("\n🧪 Testing different request variations:")
    print("-" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Data: {json.dumps(test_case['data'], indent=6)}")
        
        try:
            response = requests.post(
                url="https://pumpportal.fun/api/trade-local",
                data=test_case['data'],
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Error: {response.text}")
                
                # Try to get more detailed error info
                try:
                    error_json = response.json()
                    print(f"   JSON Error: {json.dumps(error_json, indent=6)}")
                except:
                    pass
            else:
                print(f"   ✅ Success! Response length: {len(response.content)} bytes")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    # Test with our client implementation
    print(f"\n🤖 Testing with our client implementation:")
    print("-" * 50)
    
    client = AxiomTradeClient(
        auth_token=access_token,
        refresh_token=refresh_token
    )
    
    # Test buy with very small amount
    print("\nTesting client.buy_token with 0.001 SOL...")
    result = client.buy_token(
        private_key=private_key,
        token_mint=token_mint,
        amount=0.001,
        slippage_percent=15,
        priority_fee=0.01,
        pool="pump",  # Try pump instead of auto
        denominated_in_sol=True
    )
    print(f"Result: {result}")

except Exception as e:
    print(f"❌ Diagnostic failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n📝 Notes:")
print("- 400 errors could be due to:")
print("  1. Insufficient SOL balance in wallet")
print("  2. Token not tradeable on specified pool")
print("  3. Amount too small or too large")
print("  4. Network/timing issues")
print("  5. Wallet restrictions")
