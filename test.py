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
    access_token = os.getenv("auth-access-token")
    refresh_token = os.getenv("auth-refresh-token")
    
    if not access_token or not refresh_token:
        print("Error: Missing auth-access-token or auth-refresh-token in .env file")
        return
    
    try:
        # Create client with tokens from .env file
        client = AxiomTradeClient(
            auth_token=access_token,
            refresh_token=refresh_token,
            # log_level=logging.DEBUG
        )
        
        if client.is_authenticated():
            print("✓ Client authenticated with tokens from .env")
            balance = client.GetBalance("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
            print(f"Balance: {balance}")
            result = client.buy_token(os.getenv("PRIVATE_KEY"), "8x5VqbHA8D7NkD52uNuS5nnt3PwA8pLD34ymskeSo2Wn", 0.012, 5)
            print(result)
        else:
            print("✗ Authentication failed with provided tokens")
            
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")

asyncio.run(main())