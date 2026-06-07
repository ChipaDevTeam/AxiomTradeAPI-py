import asyncio
from axiomtradeapi import AxiomTradeClient
import logging
import dotenv
import os

dotenv.load_dotenv()

async def handle_tokens(tokens):
    print(tokens)

async def main():
    # Get tokens from .env file
    access_token = os.getenv("AXIOM_ACCESS_TOKEN")
    refresh_token = os.getenv("AXIOM_REFRESH_TOKEN")
    
    if not access_token or not refresh_token:
        print("Error: Missing AXIOM_ACCESS_TOKEN or AXIOM_REFRESH_TOKEN in .env file")
        return
    
    try:
        # Create client with tokens from .env file
        client = AxiomTradeClient(
            auth_token=access_token,
            refresh_token=refresh_token,
            # log_level=logging.DEBUG
        )
        
        if client.auth_manager.ensure_valid_authentication():
            print("✓ Client authenticated with tokens from .env")
            balance = client.GetBalance("FRbUNvGxYNC1eFngpn7AD3f14aKKTJVC6zSMtvj2dyCS")
            print(f"Balance: {balance}")
        else:
            print("✗ Authentication failed with provided tokens")
            
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")

asyncio.run(main())