#!/usr/bin/env python3
"""
Example script demonstrating how to connect to Axiom Trade WebSocket
to monitor new token pairs in real-time.

This script shows how to:
1. Initialize authentication using AuthManager
2. Create a WebSocket client with proper authentication
3. Subscribe to new token pairs
4. Handle incoming new pair updates

Requirements:
- Valid Axiom Trade account credentials (email/password) OR existing access/refresh tokens
- websockets library (installed via requirements.txt)
"""

import asyncio
import logging
import os
from axiomtradeapi.auth.auth_manager import AuthManager
from axiomtradeapi.websocket._client import AxiomTradeWebSocketClient
import dotenv

dotenv.load_dotenv(".env")

# Configure logging to see detailed information
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def handle_new_pairs(data):
    """
    Callback function to handle new token pair updates.
    
    Args:
        data: Dictionary containing information about the new token pair
    
    Expected data structure:
    {
        "room": "new_pairs",
        "content": {
            "tokenName": "Token Name",
            "tokenTicker": "TICKER",
            "tokenAddress": "base58_address",
            "protocol": "raydium/orca/etc",
            "marketCapSol": 123.45,
            "volumeSol": 67.89,
            "liquiditySol": 100.00,
            "pairCreatedAt": "ISO_datetime",
            ...
        }
    }
    """
    try:
        # Extract content from the message
        content = data.get('content', {})
        
        # Display new token information
        logger.info("=" * 60)
        logger.info("🚨 NEW TOKEN PAIR DETECTED!")
        logger.info("=" * 60)
        
        # Basic token information (using correct field names from API)
        token_name = content.get('token_name', 'Unknown')
        token_ticker = content.get('token_ticker', 'N/A')
        token_address = content.get('token_address', 'N/A')
        protocol = content.get('protocol', content.get('display_protocol', 'N/A'))
        pair_address = content.get('pair_address', 'N/A')
        
        logger.info(f"Token: {token_name} ({token_ticker})")
        logger.info(f"Token Address: {token_address}")
        logger.info(f"Pair Address: {pair_address}")
        logger.info(f"Protocol: {protocol}")
        
        # Supply and liquidity information
        supply = content.get('supply', 0)
        initial_liquidity_sol = content.get('initial_liquidity_sol', 0)
        initial_liquidity_token = content.get('initial_liquidity_token', 0)
        
        logger.info(f"Supply: {supply:,.0f}")
        logger.info(f"Initial Liquidity: {initial_liquidity_sol:.2f} SOL / {initial_liquidity_token:,.0f} tokens")
        
        # Holder information
        dev_holds_percent = content.get('dev_holds_percent', 0)
        top_10_holders = content.get('top_10_holders', 0)
        snipers_hold_percent = content.get('snipers_hold_percent', 0)
        lp_burned = content.get('lp_burned', 0)
        
        logger.info(f"Dev Holds: {dev_holds_percent:.2f}%")
        logger.info(f"Top 10 Holders: {top_10_holders:.2f}%")
        logger.info(f"Snipers Hold: {snipers_hold_percent:.2f}%")
        logger.info(f"LP Burned: {lp_burned}%")
        
        # Social links (if available)
        website = content.get('website')
        twitter = content.get('twitter')
        telegram = content.get('telegram')
        discord = content.get('discord')
        
        if website:
            logger.info(f"🌐 Website: {website}")
        if twitter:
            logger.info(f"🐦 Twitter: {twitter}")
        if telegram:
            logger.info(f"💬 Telegram: {telegram}")
        if discord:
            logger.info(f"🎮 Discord: {discord}")
        
        # Deployer and creation info
        deployer_address = content.get('deployer_address', 'N/A')
        created_at = content.get('created_at', 'N/A')
        open_trading = content.get('open_trading', 'N/A')
        
        logger.info(f"Deployer: {deployer_address}")
        logger.info(f"Created: {created_at}")
        logger.info(f"Trading Opened: {open_trading}")
        
        # Security information
        mint_authority = content.get('mint_authority')
        freeze_authority = content.get('freeze_authority')
        logger.info(f"Mint Authority: {'None (Safe)' if mint_authority is None else mint_authority}")
        logger.info(f"Freeze Authority: {'None (Safe)' if freeze_authority is None else freeze_authority}")
        
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error handling new pair data: {e}")


async def main():
    """
    Main function to run the WebSocket client for monitoring new token pairs.
    """
    logger.info("Axiom Trade WebSocket - New Pairs Monitor")
    logger.info("=" * 60)
    
    # Option 1: Use environment variables (recommended for production)
    # Set these in your environment or .env file:
    # export AXIOM_ACCESS_TOKEN="your_access_token"
    # export AXIOM_REFRESH_TOKEN="your_refresh_token"
    
    access_token = os.getenv('AXIOM_ACCESS_TOKEN')
    refresh_token = os.getenv('AXIOM_REFRESH_TOKEN')
    
    # Option 2: Use credentials (email/password) for automatic login
    # email = os.getenv('AXIOM_EMAIL')
    # password = os.getenv('AXIOM_PASSWORD')
    
    # Option 3: Hardcode tokens for testing (NOT recommended for production)
    # Uncomment and fill these if you have tokens:
    # access_token = "your_access_token_here"
    # refresh_token = "your_refresh_token_here"
    
    # Validate that we have authentication credentials
    if not access_token or not refresh_token:
        logger.error("=" * 60)
        logger.error("❌ Authentication Required!")
        logger.error("=" * 60)
        logger.error("Please provide authentication credentials using one of these methods:")
        logger.error("")
        logger.error("Method 1: Environment Variables (Recommended)")
        logger.error("  export AXIOM_ACCESS_TOKEN='your_access_token'")
        logger.error("  export AXIOM_REFRESH_TOKEN='your_refresh_token'")
        logger.error("")
        logger.error("Method 2: .env File")
        logger.error("  Create a .env file with:")
        logger.error("    AXIOM_ACCESS_TOKEN=your_access_token")
        logger.error("    AXIOM_REFRESH_TOKEN=your_refresh_token")
        logger.error("")
        logger.error("Method 3: Hardcode in Script (Not Recommended)")
        logger.error("  Edit this file and set access_token and refresh_token variables")
        logger.error("")
        logger.error("To get tokens, use the login_example.py script or visit:")
        logger.error("  https://chipadevteam.github.io/AxiomTradeAPI-py/authentication/")
        logger.error("=" * 60)
        return
    
    try:
        # Initialize AuthManager with tokens
        logger.info("Initializing authentication...")
        auth_manager = AuthManager(
            auth_token=access_token,
            refresh_token=refresh_token,
            use_saved_tokens=False  # Don't try to load saved tokens
        )
        
        # Verify authentication is valid
        if not auth_manager.ensure_valid_authentication():
            logger.error("❌ Authentication failed - invalid or expired tokens")
            logger.error("Please get new tokens using login_example.py")
            return
        
        logger.info("✓ Authentication successful")
        
        # Create WebSocket client with authenticated manager
        logger.info("Creating WebSocket client...")
        ws_client = AxiomTradeWebSocketClient(
            auth_manager=auth_manager,
            log_level=logging.INFO
        )
        
        # Subscribe to new token pairs
        logger.info("Subscribing to new token pairs...")
        success = await ws_client.subscribe_new_tokens(handle_new_pairs)
        
        if not success:
            logger.error("❌ Failed to subscribe to new token pairs")
            logger.error("This may be due to authentication issues or network problems")
            return
        
        logger.info("✓ Successfully subscribed to new token pairs")
        logger.info("=" * 60)
        logger.info("🎧 Listening for new token pairs...")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 60)
        
        # Start listening for messages
        # This will run indefinitely until interrupted
        await ws_client.start()
        
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("🛑 Stopping WebSocket client...")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"❌ Error: {e}")
        logger.error("=" * 60)
        
        # Provide helpful error messages
        if "401" in str(e) or "Unauthorized" in str(e):
            logger.error("Authentication error - your tokens may be expired")
            logger.error("Please get new tokens using login_example.py")
        elif "Connection" in str(e):
            logger.error("Connection error - check your internet connection")
        else:
            logger.error("For help, visit: https://chipadevteam.github.io/AxiomTradeAPI-py/")
    
    finally:
        # Clean up WebSocket connection
        if 'ws_client' in locals() and ws_client.ws:
            logger.info("Closing WebSocket connection...")
            await ws_client.close()
        logger.info("✓ WebSocket closed")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
