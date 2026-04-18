"""
Advanced PumpPortal Diagnostic - Check token validity and wallet balance
"""

import requests
import json
from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os

dotenv.load_dotenv()
private_key = os.getenv('PRIVATE_KEY')
token_mint = "9SkhnfNU5kx3VhngR9F2X7YSKnRZsNxGzcipHoCNGakK"

print("🔍 Advanced PumpPortal Diagnostic")
print("=" * 60)

try:
    from solders.keypair import Keypair
    
    keypair = Keypair.from_base58_string(private_key)
    public_key = str(keypair.pubkey())
    
    print(f"Wallet: {public_key}")
    print(f"Token: {token_mint}")
    
    # 1. Check wallet SOL balance using Solana RPC
    print(f"\n1️⃣ Checking wallet SOL balance...")
    print("-" * 40)
    
    rpc_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [public_key]
    }
    
    try:
        rpc_response = requests.post(
            "https://api.mainnet-beta.solana.com",
            headers={"Content-Type": "application/json"},
            json=rpc_payload,
            timeout=10
        )
        
        if rpc_response.status_code == 200:
            balance_data = rpc_response.json()
            if "result" in balance_data:
                lamports = balance_data["result"]["value"]
                sol_balance = lamports / 1_000_000_000
                print(f"SOL Balance: {sol_balance:.6f} SOL ({lamports} lamports)")
                
                if sol_balance < 0.01:
                    print("⚠️  WARNING: Low SOL balance. Need at least 0.01 SOL for trading + fees")
            else:
                print(f"❌ Error getting balance: {balance_data}")
        else:
            print(f"❌ RPC request failed: {rpc_response.status_code}")
    except Exception as e:
        print(f"❌ Balance check failed: {e}")
    
    # 2. Check if token exists and get basic info
    print(f"\n2️⃣ Checking token metadata...")
    print("-" * 40)
    
    token_info_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [
            token_mint,
            {"encoding": "base64"}
        ]
    }
    
    try:
        token_response = requests.post(
            "https://api.mainnet-beta.solana.com",
            headers={"Content-Type": "application/json"},
            json=token_info_payload,
            timeout=10
        )
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            if "result" in token_data and token_data["result"]["value"]:
                print("✅ Token exists on Solana")
                owner = token_data["result"]["value"]["owner"]
                print(f"Token Program: {owner}")
            else:
                print("❌ Token not found or invalid")
        else:
            print(f"❌ Token info request failed: {token_response.status_code}")
    except Exception as e:
        print(f"❌ Token check failed: {e}")
    
    # 3. Try a minimal PumpPortal request with different parameters
    print(f"\n3️⃣ Testing minimal PumpPortal requests...")
    print("-" * 40)
    
    # Test if this specific token is supported
    minimal_tests = [
        {
            "name": "Very small amount (0.0001 SOL)",
            "amount": 100000,  # 0.0001 SOL in lamports
            "denominatedInSol": "true"
        },
        {
            "name": "Different token format test",
            "amount": 1000,
            "denominatedInSol": "false"
        }
    ]
    
    for test in minimal_tests:
        print(f"\n   Testing: {test['name']}")
        
        minimal_data = {
            "publicKey": public_key,
            "action": "buy",
            "mint": token_mint,
            "amount": test["amount"],
            "denominatedInSol": test["denominatedInSol"],
            "slippage": 50,  # Very high slippage
            "priorityFee": 0.001,  # Lower priority fee
            "pool": "pump"
        }
        
        try:
            response = requests.post(
                url="https://pumpportal.fun/api/trade-local",
                data=minimal_data,
                timeout=5
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    # 4. Test with a known working pump.fun token
    print(f"\n4️⃣ Testing with popular pump.fun token...")
    print("-" * 40)
    
    # Use a popular token that should definitely work
    popular_tokens = [
        "2weMjPLLybRMMva1fM3U31goWWrCpF59CHWNhnCJ9Vyh",  # Popular pump token
        "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr"   # Another popular one
    ]
    
    for popular_token in popular_tokens:
        print(f"\n   Testing token: {popular_token}")
        
        test_data = {
            "publicKey": public_key,
            "action": "buy",
            "mint": popular_token,
            "amount": 1000000,  # 0.001 SOL
            "denominatedInSol": "true",
            "slippage": 20,
            "priorityFee": 0.005,
            "pool": "pump"
        }
        
        try:
            response = requests.post(
                url="https://pumpportal.fun/api/trade-local",
                data=test_data,
                timeout=5
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! This token works!")
                break
            else:
                print(f"   Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")

except Exception as e:
    print(f"❌ Diagnostic failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n📋 Summary:")
print("If all tests fail with 400 errors, it could be:")
print("1. PumpPortal API temporarily down")
print("2. Rate limiting")
print("3. IP/region restrictions")
print("4. API key or authentication required")
print("5. Specific token not supported by PumpPortal")
print("6. Insufficient wallet balance")
