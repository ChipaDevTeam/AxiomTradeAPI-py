from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os
import time
import logging
# To run this test, you need to have a valid wallet connecting to Solana network.
# Find the PRIVATE key of your wallet using any popular wallet provider can do this.
# (BUT Keep your PRIVATE key to yourself! Never share it with anyone! NEVER!)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'   
)
dotenv.load_dotenv()
# Create a .env file under the root directory of this project. 
# Within the .env file, put PRIVATE_KEY={YOUR_PRIVATE_KEY}
# Trading is using PumpPortal API, won't login to Axiom.trade.
# You don't have to input valid `auth_token` or `refresh_token` in this test
access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')
private_key = os.getenv('PRIVATE_KEY')
client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token
)

# Example token mint address (replace with actual token you want to trade)
# This test is using FARTCOIN, which has relatively deeper liquidity pools. 
# (Meaning less cost to run this test)
token_mint = "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"

print("🚀 Testing Buy and Sell Functions")
print("=" * 50)

print(f"\n💰 Testing Buy: 0.001 SOL worth of {token_mint}")
buy_result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint, 
    amount=0.001,  # Amount in SOL
    slippage_percent=10,  # PumpPortal expects integer
    priority_fee=0.00005,
    pool="auto",
    denominated_in_sol=True  # True means amount is in SOL
)

print(f"Buy result: {buy_result}")

if buy_result["success"]:
    print(f"✅ Buy successful! Transaction: {buy_result['signature']}")
    print(f"🔗 Explorer: {buy_result.get('explorer_url', 'N/A')}")
else:
    print(f"❌ Buy failed: {buy_result['error']}")

print("\nWaiting 2 seconds...")
time.sleep(2)

print(f"\n💸 Testing Sell: 100% of owned tokens of {token_mint}")
sell_result = client.sell_token(
    private_key=private_key,
    token_mint=token_mint,
    amount="100%",  # "100%" or 10000000.0 or 0.001 are all valid
    slippage_percent=10,  # PumpPortal expects integer
    priority_fee=0.005,
    pool="auto",
    denominated_in_sol=False,  # False means amount is in tokens
    # Here is demostrating that you can switch to a faster Solana RPC node if you want to.
    # This is optional, you can use the default RPC node by not specifying this argument.
    rpc_url="https://greer-651y13-fast-mainnet.helius-rpc.com/"  # Use faster RPC
)

print(f"Sell result: {sell_result}")

if sell_result["success"]:
    print(f"✅ Sell successful! Transaction: {sell_result['signature']}")
    print(f"🔗 Explorer: {sell_result.get('explorer_url', 'N/A')}")
else:
    print(f"❌ Sell failed: {sell_result['error']}")

print("\n🎉 Buy and Sell test completed!")
