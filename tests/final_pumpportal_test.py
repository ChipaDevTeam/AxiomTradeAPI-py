"""
Final PumpPortal test with a currently active pump.fun token
"""

import requests
import json

# Let's try with a token that's currently trending on pump.fun
# We'll test with multiple currently popular tokens
print("🚀 Testing with Currently Active Pump.Fun Tokens")
print("=" * 60)

# Test wallet (the same one we've been using)
public_key = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"

# Try with several different popular tokens
# These are tokens that should definitely be active
active_tokens = [
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # Bonk
    "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",  # Ethereum on Solana  
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So",   # Marinade SOL
]

for i, token in enumerate(active_tokens, 1):
    print(f"\n{i}. Testing with token: {token}")
    print("-" * 50)
    
    test_data = {
        "publicKey": public_key,
        "action": "buy", 
        "mint": token,
        "amount": 1000000,  # 0.001 SOL in lamports
        "denominatedInSol": "true",
        "slippage": 25,  # Higher slippage
        "priorityFee": 0.001,  # Lower priority fee
        "pool": "pump"
    }
    
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            url="https://pumpportal.fun/api/trade-local",
            data=test_data,  # Using form data as per their example
            timeout=15
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Transaction data received!")
            print(f"Response length: {len(response.content)} bytes")
            break
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

# Also try with a minimal request to see if the API is working at all
print(f"\n🔬 Testing minimal request...")
print("-" * 30)

minimal_data = {
    "publicKey": public_key,
    "action": "buy",
    "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # Bonk
    "amount": 100000,  # Very small amount
    "denominatedInSol": "false",  # Token amount
    "slippage": 50,  # Very high slippage
    "priorityFee": 0.001,
    "pool": "auto"
}

try:
    response = requests.post(
        url="https://pumpportal.fun/api/trade-local",
        data=minimal_data,
        timeout=10
    )
    
    print(f"Minimal request status: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Minimal request failed: {e}")

print(f"\n📊 Analysis:")
print("If ALL requests return 400, then:")
print("1. PumpPortal Local API may be temporarily disabled")
print("2. They may have added authentication requirements")  
print("3. There might be IP/regional restrictions")
print("4. The API might be under maintenance")
print("\nRecommendation: Try the Lightning API or contact PumpPortal support")
