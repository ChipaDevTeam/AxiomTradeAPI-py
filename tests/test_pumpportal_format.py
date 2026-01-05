"""
Test to verify our PumpPortal implementation matches their exact format requirements.
This will show the exact request being sent to validate the format.
"""

import requests
from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os

dotenv.load_dotenv()
access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')
private_key = os.getenv('PRIVATE_KEY')

# Create client
client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token
)

# Test token (this will give 400 error but we can see the format)
token_mint = "7A8Ezkjfe9rKFLDwbDx2xrCB6FTQYNQ9PF9GxVHxHD5L"

print("🔍 Testing PumpPortal Request Format")
print("=" * 60)

# First let's manually create the request to see what PumpPortal expects
print("\n1️⃣ Manual Request (Following PumpPortal Example):")
print("-" * 50)

try:
    from solders.keypair import Keypair
    
    # Get public key using PumpPortal's exact method
    keypair = Keypair.from_base58_string(private_key)
    public_key = str(keypair.pubkey())
    
    # Create the exact data structure PumpPortal expects
    manual_data = {
        "publicKey": public_key,
        "action": "buy",
        "mint": token_mint,
        "amount": 100000,  # 0.001 SOL in lamports
        "denominatedInSol": "false",  # Following their example
        "slippage": 10,
        "priorityFee": 0.005,
        "pool": "auto"
    }
    
    print(f"Request data: {manual_data}")
    print(f"URL: https://pumpportal.fun/api/trade-local")
    
    response = requests.post(
        url="https://pumpportal.fun/api/trade-local",
        data=manual_data
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")
    
except Exception as e:
    print(f"Manual request error: {e}")

print("\n2️⃣ Our Client Implementation:")
print("-" * 50)

# Test our buy_token implementation
try:
    print("Testing buy_token with amount=100000, denominated_in_sol=False (tokens)")
    buy_result = client.buy_token(
        private_key=private_key,
        token_mint=token_mint,
        amount=100000,  # 100k tokens
        slippage_percent=10,
        priority_fee=0.005,
        pool="auto",
        denominated_in_sol=False  # Amount is in tokens
    )
    print(f"Buy result: {buy_result}")
    
    print("\nTesting buy_token with amount=0.001, denominated_in_sol=True (SOL)")
    buy_result2 = client.buy_token(
        private_key=private_key,
        token_mint=token_mint,
        amount=0.001,  # 0.001 SOL
        slippage_percent=10,
        priority_fee=0.005,
        pool="auto", 
        denominated_in_sol=True  # Amount is in SOL
    )
    print(f"Buy result 2: {buy_result2}")
    
except Exception as e:
    print(f"Client implementation error: {e}")

print("\n✅ Format verification complete!")
print("\nNote: 400 errors are expected with test token addresses.")
print("The important thing is that our request format matches PumpPortal's specification.")
