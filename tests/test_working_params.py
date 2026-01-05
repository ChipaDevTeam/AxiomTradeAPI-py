"""
Success! Test with the working parameters from PumpPortal
"""

from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os

dotenv.load_dotenv()
access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')
private_key = os.getenv('PRIVATE_KEY')

client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token
)

# Use the token that worked (Bonk)
working_token = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"

print("🎉 Testing with WORKING PumpPortal Parameters")
print("=" * 60)

print(f"Using token: {working_token} (Bonk)")
print("Parameters that worked:")
print("- denominatedInSol: false (token amount)")
print("- amount: 100000 (tokens)")
print("- pool: auto")
print("- slippage: 50")

# Test the successful parameters
print(f"\n💰 Testing Buy with working parameters...")

buy_result = client.buy_token(
    private_key=private_key,
    token_mint=working_token,
    amount=100000,  # Number of tokens (what worked)
    slippage_percent=50,  # High slippage
    priority_fee=0.001,
    pool="auto",  # What worked
    denominated_in_sol=False  # Token amount (what worked)
)

print(f"Buy result: {buy_result}")

if buy_result["success"]:
    print(f"✅ BUY SUCCESSFUL! Transaction: {buy_result['signature']}")
    print(f"🔗 Explorer: {buy_result.get('explorer_url', 'N/A')}")
else:
    print(f"❌ Buy failed: {buy_result['error']}")

# Also test with a smaller token amount
print(f"\n💸 Testing smaller token amount...")

buy_result2 = client.buy_token(
    private_key=private_key,
    token_mint=working_token,
    amount=10000,  # Smaller amount
    slippage_percent=50,
    priority_fee=0.001,
    pool="auto",
    denominated_in_sol=False
)

print(f"Small amount result: {buy_result2}")

if buy_result2["success"]:
    print(f"✅ SMALL BUY SUCCESSFUL! Transaction: {buy_result2['signature']}")
    print(f"🔗 Explorer: {buy_result2.get('explorer_url', 'N/A')}")
else:
    print(f"❌ Small buy failed: {buy_result2['error']}")

print(f"\n📋 Key Learning:")
print("PumpPortal works when:")
print("✅ denominatedInSol = false (token amounts)")
print("✅ pool = 'auto' (not 'pump')")
print("✅ Higher slippage (50%)")
print("✅ Popular tokens like Bonk")
print("❌ SOL amounts seem to cause issues")
print("❌ Pool 'pump' seems to cause issues")
