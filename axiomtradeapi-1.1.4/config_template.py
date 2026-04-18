"""
Configuration template for AxiomTradeAPI-py

Copy this file to config.py and fill in your authentication tokens.
"""

class Config:
    # Authentication tokens - Required for WebSocket functionality
    # Get these from your browser after logging into https://axiom.trade
    # Instructions:
    # 1. Visit https://axiom.trade and login
    # 2. Open Developer Tools (F12)
    # 3. Go to Application → Cookies
    # 4. Find 'auth-access-token' and 'auth-refresh-token'
    # 5. Copy the values below (keep the quotes)
    
    AUTH_TOKEN = "your_auth_access_token_here"
    REFRESH_TOKEN = "your_auth_refresh_token_here"
    
    # Optional settings
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # WebSocket URLs (usually don't need to change)
    WS_URL_MAIN = "wss://cluster3.axiom.trade/"
    WS_URL_TOKEN_PRICE = "wss://socket8.axiom.trade/"

# Example usage:
# from config import Config
# client = AxiomTradeWebSocketClient(
#     auth_token=Config.AUTH_TOKEN,
#     refresh_token=Config.REFRESH_TOKEN
# )