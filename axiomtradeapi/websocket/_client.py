import json
import logging
import websockets
import asyncio
from typing import Optional, Callable, Dict, Any
import inspect

class AxiomTradeWebSocketClient:    
    def __init__(self, auth_manager, log_level=logging.INFO) -> None:
        self.ws_url = "wss://cluster6.axiom.trade/"
        self.ws_url_token_price = "wss://socket8.axiom.trade/"
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        
        if not auth_manager:
            raise ValueError("auth_manager is required and must be an authenticated AuthManager instance")
        
        self.auth_manager = auth_manager
        
        # Setup logging
        self.logger = logging.getLogger("AxiomTradeWebSocket")
        self.logger.setLevel(log_level)
        
        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self._callbacks: Dict[str, Callable] = {}
        
        # Detect which parameter name to use for headers based on websockets.connect signature
        sig = inspect.signature(websockets.connect)
        self._uses_additional_headers = 'additional_headers' in sig.parameters
        self._uses_extra_headers = 'extra_headers' in sig.parameters
        
        if self._uses_additional_headers:
            self.logger.debug("Using 'additional_headers' parameter for websockets (version 13+)")
        elif self._uses_extra_headers:
            self.logger.debug("Using 'extra_headers' parameter for websockets (version 10.x)")
        else:
            self.logger.warning("Could not detect headers parameter name for websockets.connect")

    async def _connect_with_headers(self, url: str, headers: Dict[str, str]):
        """
        Connect to WebSocket with compatibility for different websockets versions.
        Uses additional_headers (websockets 13+) or extra_headers (websockets 10.x) based on detection.
        """
        if self._uses_additional_headers:
            return await websockets.connect(url, additional_headers=headers)
        elif self._uses_extra_headers:
            return await websockets.connect(url, extra_headers=headers)
        else:
            # Fallback: try both
            try:
                return await websockets.connect(url, additional_headers=headers)
            except TypeError:
                self.logger.debug("Fallback: Retrying connection with extra_headers parameter")
                return await websockets.connect(url, extra_headers=headers)

    async def connect(self, is_token_price: bool = False) -> bool:
        """Connect to the WebSocket server."""
        # Ensure we have valid authentication
        if not self.auth_manager.ensure_valid_authentication():
            self.logger.error("WebSocket authentication failed - unable to obtain valid tokens")
            self.logger.error("Please login with valid email and password")
            return False
        
        # Get tokens from auth manager
        tokens = self.auth_manager.get_tokens()
        if not tokens:
            self.logger.error("No authentication tokens available")
            return False
        
        headers = {
            'Origin': 'https://axiom.trade',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0',
        }
        
        # Add authentication cookies from auth manager
        cookie_header = f"auth-access-token={tokens.access_token}; auth-refresh-token={tokens.refresh_token}"
        headers["Cookie"] = cookie_header
        
        self.logger.debug(f"Connecting to WebSocket with headers: {headers}")
        self.logger.debug(f"Using tokens: access_token length={len(tokens.access_token)}, refresh_token length={len(tokens.refresh_token)}")
        
        try:
            if is_token_price:
                current_url = self.ws_url_token_price
            else:
                current_url = self.ws_url
            
            # Try the primary URL first
            self.logger.info(f"Attempting to connect to WebSocket: {current_url}")
            self.ws = await self._connect_with_headers(current_url, headers)
            self.logger.info("Connected to WebSocket server")
            return True
        except Exception as e:
            if "HTTP 401" in str(e) or "401" in str(e):
                self.logger.error("WebSocket authentication failed - invalid or missing tokens")
                self.logger.error("Please check that your tokens are valid and not expired")
                self.logger.error(f"Error details: {e}")
                self.logger.error(f"Current tokens: {tokens}")
            else:
                self.logger.error(f"Failed to connect to WebSocket: {e}")
                # Try alternative URL if the primary one fails
                if not is_token_price and "cluster-usc2" in self.ws_url:
                    try:
                        alternative_url = "wss://cluster3.axiom.trade/"
                        self.logger.info(f"Trying alternative WebSocket URL: {alternative_url}")
                        self.ws = await self._connect_with_headers(alternative_url, headers)
                        self.logger.info("Connected to alternative WebSocket server")
                        return True
                    except Exception as e2:
                        self.logger.error(f"Alternative WebSocket connection also failed: {e2}")
            return False

    async def subscribe_new_tokens(self, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to new token updates."""
        if not self.ws:
            if not await self.connect():
                return False

        self._callbacks["new_pairs"] = callback
        
        try:
            await self.ws.send(json.dumps({
                "action": "join",
                "room": "new_pairs"
            }))
            self.logger.info("Subscribed to new token updates")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to new tokens: {e}")
            return False

    async def subscribe_token_price(self, token: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to token price updates."""
        if not self.ws:
            if not await self.connect(is_token_price=True):
                return False

        self._callbacks[f"token_price_{token}"] = callback
        
        try:
            await self.ws.send(json.dumps({
                "action": "join",
                "room": token
            }))
            self.logger.info(f"Subscribed to token price updates for {token}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to token price: {e}")
            return False
        
    async def subscribe_wallet_transactions(self, wallet_address: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to wallet transaction updates."""
        """
        Response format:
        {
            "room": "v:<WALLET_ADDRESS>",
            "content": {
                "created_at": "<ISO_DATETIME>",
                "liquidity_sol": <LIQUIDITY_SOL_AMOUNT>,
                "liquidity_token": <LIQUIDITY_TOKEN_AMOUNT>,
                "maker_address": "<WALLET_ADDRESS>",
                "price_sol": <PRICE_IN_SOL>,
                "price_usd": <PRICE_IN_USD>,
                "signature": "<TRANSACTION_SIGNATURE>",
                "token_amount": <TOKEN_AMOUNT>,
                "total_sol": <TOTAL_SOL_AMOUNT>,
                "total_usd": <TOTAL_USD_AMOUNT>,
                "type": "<TRANSACTION_TYPE>",  // "buy" ou "sell"
                "pair_address": "<PAIR_ADDRESS>",
                "f": <FEE_OR_FACTOR>,
                "pair": {
                    "tokenAddress": "<TOKEN_ADDRESS>",
                    "tokenName": "<TOKEN_NAME>",
                    "tokenTicker": "<TOKEN_TICKER>",
                    "tokenImage": "<IMAGE_URL_OR_NULL>",
                    "protocol": "<PROTOCOL_NAME>",
                    "protocolDetails": {
                        "pairSolAccount": "<PAIR_SOL_ACCOUNT>",
                        "tokenProgram": "<TOKEN_PROGRAM_ID>",
                        "pairTokenAccount": "<PAIR_TOKEN_ACCOUNT>",
                        "isTokenSideX": <BOOLEAN>
                    },
                    "supply": <TOKEN_SUPPLY>,
                    "tokenDecimals": <DECIMALS>,
                    "pairCreatedAt": "<ISO_DATETIME>",
                    "extra": null
                }
            }
        }
        """
        if not self.ws:
            if not await self.connect():
                return False

        self._callbacks[f"wallet_transactions_{wallet_address}"] = callback
        
        try:
            await self.ws.send(json.dumps({
                "action": "join",
                "room": f"v:{wallet_address}"
            }))
            self.logger.info(f"Subscribed to wallet transactions for {wallet_address}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to wallet transactions: {e}")
            return False

    async def _message_handler(self):
        """Handle incoming WebSocket messages."""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    
                    # Handle new token updates
                    if "new_pairs" in self._callbacks and data.get("room") == "new_pairs":
                        content = data.get("content")
                        if content:
                            # Wrap single token in array for callback compatibility
                            await self._callbacks["new_pairs"]([content])
                    
                    # Handle token price updates
                    for key, callback in self._callbacks.items():
                        if key.startswith("token_price_"):
                            # Extract token from callback key
                            token = key.replace("token_price_", "")
                            # Check if room matches the token
                            if data.get("room") == token and data.get("content"):
                                await callback(data.get("content"))
                            
                    # Handle wallet transactions
                    for key, callback in self._callbacks.items():
                        if key.startswith("wallet_transactions_"):
                            # Extract wallet address from callback key
                            wallet_address = key.replace("wallet_transactions_", "")
                            # Check if room matches the expected format for this wallet
                            if data.get("room") == f"v:{wallet_address}" and data.get("content"):
                                await callback(data.get("content"))
                    
                except json.JSONDecodeError:
                    self.logger.error(f"Failed to parse WebSocket message: {message}")
                except Exception as e:
                    self.logger.error(f"Error handling WebSocket message: {e}")
        except websockets.exceptions.ConnectionClosed:
            self.logger.warning("WebSocket connection closed")
        except Exception as e:
            self.logger.error(f"WebSocket message handler error: {e}")

    async def start(self):
        """Start the WebSocket client and message handler."""
        if not self.ws:
            if not await self.connect():
                return
        
        await self._message_handler()

    async def close(self):
        """Close the WebSocket connection."""
        if self.ws:
            await self.ws.close()
            self.logger.info("WebSocket connection closed")