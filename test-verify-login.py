from axiomtradeapi.client import AxiomTradeClient
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define storage directory
storage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chipadev_data")
print(f"📂 Checking for tokens in: {storage_dir}")

# Initialize client pointing to the custom storage
client = AxiomTradeClient(storage_dir=storage_dir)

if client.is_authenticated():
    print("✅ STARTUP: Client successfully loaded existing tokens!")
    tokens = client.get_tokens()
    print(f"   Access Token Info: ...{tokens['access_token'][-10:] if tokens['access_token'] else 'None'}")
    print(f"   Expires At: {tokens['expires_at']}")
    
    if client.ensure_authenticated():
         print("✅ AUTH CHECK: Token is valid and ready to use.")
    else:
         print("❌ AUTH CHECK: Token validation failed (expired and refresh failed?).")
else:
    print("❌ STARTUP: No valid tokens found. Please run test-tools.py to login first.")
