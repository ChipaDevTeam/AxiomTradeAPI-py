import asyncio
import logging
import os
import signal
import sys
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Import Axiom Trade API
try:
    from axiomtradeapi import AxiomTradeClient
    from axiomtradeapi.tools import login_with_email_otp
except ImportError:
    print("CRITICAL ERROR: 'axiomtradeapi' not found. Please install it using: pip install axiomtradeapi")
    sys.exit(1)

# Configure logging structure for a professional application
# We create a specific logger for our bot to separate it from library logs
logger = logging.getLogger("UserMonitorBot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler (keep a record of execution)
file_handler = logging.FileHandler("bot.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ActiveUserMonitorBot:
    """
    A professional-grade bot to monitor active users on Axiom.
    Features:
    - Robust configuration loading
    - Graceful shutdown handling
    - Automatic token management
    - Structured logging
    - Continuous monitoring
    """

    def __init__(self):
        self.client: Optional[AxiomTradeClient] = None
        self.is_running = False
        self._load_config()

    def _load_config(self):
        """Load configuration from environment variables."""
        load_dotenv()
        self.email = os.getenv('email') or os.getenv('EMAIL_ADDRESS')
        self.axiom_password = os.getenv('AXIOM_PASSWORD')
        self.email_app_password = os.getenv('EMAIL_APP_PASSWORD')
    
    async def initialize(self):
        """Initialize the client and session."""
        logger.info("Initializing UserMonitorBot...")
        
        # Storage for session persistence
        storage_dir = os.path.join(os.getcwd(), ".chipadev_data")
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize client with storage to persist session
        self.client = AxiomTradeClient(
            username=self.email,  # Needed for auto-relogin if implemented in lib
            password=self.axiom_password, # Needed for optional login flows
            storage_dir=storage_dir,
            use_saved_tokens=True # Try to load from disk first
        )

        if not self.client.is_authenticated():
            logger.info("No valid session found. Attempting login flow...")
            await self._perform_login()
        else:
            logger.info("✅ Successfully resumed existing session.")

    async def _perform_login(self):
        """Handle the login process if not authenticated."""
        if not self.email or not self.axiom_password or not self.email_app_password:
             logger.error("Authentication required but credentials missing in .env.")
             logger.error("Please provide EMAIL_ADDRESS, AXIOM_PASSWORD, and EMAIL_APP_PASSWORD.")
             sys.exit(1)
             
        logger.info(f"Attempting login for user: {self.email}")
        
        # Use the tool provided by the library for email OTP login
        # This is blocking in the example, so we wrap or call directly if it supports async
        # Looking at examples/test-loginsystem.py, it seems synchronous or we need to check if it returns a coroutine.
        # Most likely synchronous based on the example structure.
        
        # We run this in a thread executor to avoid blocking the async loop if it's synchronous IO
        loop = asyncio.get_event_loop()
        try:
             # Assuming login_with_email_otp is the function from the example
             result = await loop.run_in_executor(
                 None, 
                 lambda: login_with_email_otp(self.client, self.email_app_password)
             )
             
             if result and self.client.is_authenticated():
                 logger.info("✅ Login successful!")
             else:
                 logger.error("❌ Login failed. Check credentials and OTP.")
                 sys.exit(1)
        except Exception as e:
            logger.error(f"Login process encountered an error: {e}")
            sys.exit(1)

    async def _user_count_callback(self, count: int):
        """Callback function triggered when user count updates."""
        # Here you could implement logic to:
        # - Save to database
        # - Send alert if count drops below threshold
        # - Update a dashboard
        logger.info(f"👥 Current Active Users: {count}")

    async def run(self):
        """Main execution loop."""
        await self.initialize()
        
        self.is_running = True
        logger.info("🚀 Bot started. Press Ctrl+C to stop.")
        
        # Setup signal handlers for graceful shutdown (PC only - Windows has limitations with add_signal_handler in loops)
        # We'll use a try/finally block in the main loop instead for better cross-platform support generic
        
        try:
            while self.is_running:
                logger.info("Starting monitoring cycle...")
                # We monitor in chunks (e.g., 1 hour) to allow for periodic re-checks or restarts if needed
                # or pass a very long duration if the library supports it.
                # Just using a large number like 3600 (1 hour) for now.
                try:
                    await self.client.get_active_axiom_users(
                        callback=self._user_count_callback,
                        duration=3600,  # Monitor for 1 hour 
                        token_address="8P5kBTzvG7xyjTZRzi4ftzpy6mnL74AHLtHDqyDq44ST"
                    )
                except Exception as e:
                    logger.error(f"Connection lost or error in monitoring: {e}")
                    logger.info("Attempting to reconnect in 5 seconds...")
                    await asyncio.sleep(5)
                
        except asyncio.CancelledError:
            logger.info("Bot stopping...")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Cleanup resources."""
        logger.info("Shutting down gracefully...")
        self.is_running = False
        # If the client has a close method, call it here.
        # if hasattr(self.client, 'close'): await self.client.close()
        logger.info("👋 Goodbye!")

if __name__ == "__main__":
    bot = ActiveUserMonitorBot()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        # This catches the Ctrl+C at the top level
        pass
