from axiomtradeapi import AxiomTradeClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = AxiomTradeClient(
    username=os.getenv("email"),
    password=os.getenv("password")
)

# Automatically logs in if no saved session exists
# Will trigger an OTP flow if 2FA is required
if not client.is_authenticated():
    print("Please follow the login prompt...")
    client.login() # Takes optional otp_callback

# Simulate browser connection to initialize tracking sessions
# This is required for some endpoints to register you as an "active user"
# and to pass detailed bot or scraper protection checks.
client.connect(
    token_address="8P5kBTzvG7xyjTZRzi4ftzpy6mnL74AHLtHDqyDq44ST", # Optional: Simulate landing on a token page
    sol_public_keys=["Address1...", "Address2..."], # Optional: Check balances during connect
    evm_public_keys=["0xAddress1..."] 
)

print(f"Logged in as: {client.auth_manager.username}")

print(client.auth.get_authenticated_headers())
print(client.get_trending_tokens())