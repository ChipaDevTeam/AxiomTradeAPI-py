import json
import logging
import os
import asyncio
import time
from typing import Optional, Callable, Dict, Any

try:
    from curl_cffi.requests import AsyncSession as CurlAsyncSession
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False

try:
    import websockets
    import inspect as _inspect
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

try:
    from websockets_proxy import proxy_connect
    PROXY_SUPPORT = True
except ImportError:
    PROXY_SUPPORT = False


class AxiomTradeWebSocketClient:
    def __init__(self, auth_manager, log_level=logging.INFO, cf_clearance: str = None) -> None:
        self.ws_url = "wss://cluster9.axiom.trade/"
        self.ws_url_token_price = "wss://socket8.axiom.trade/"
        self.cf_clearance = cf_clearance or os.environ.get("CF_CLEARANCE")

        # curl_cffi session + ws (primary path)
        self._curl_session: Optional[CurlAsyncSession] = None
        self._curl_ws = None       # actual WebSocket object
        self._curl_ws_ctx = None   # async context manager (must be kept alive)

        # websockets fallback
        self.ws = None

        if not auth_manager:
            raise ValueError("auth_manager is required and must be an authenticated AuthManager instance")

        self.auth_manager = auth_manager

        self.logger = logging.getLogger("AxiomTradeWebSocket")
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
        self.logger.propagate = False

        self._callbacks: Dict[str, Callable] = {}

        # websockets version detection for fallback
        if WEBSOCKETS_AVAILABLE:
            sig = _inspect.signature(websockets.connect)
            self._uses_additional_headers = 'additional_headers' in sig.parameters
            self._uses_extra_headers = 'extra_headers' in sig.parameters
        else:
            self._uses_additional_headers = False
            self._uses_extra_headers = False

        if CURL_CFFI_AVAILABLE:
            self.logger.debug("curl_cffi available — will use Chrome TLS impersonation")
        elif WEBSOCKETS_AVAILABLE:
            self.logger.warning("curl_cffi not installed — falling back to websockets (may fail Cloudflare TLS check). "
                                "Install with: pip install curl_cffi")
        else:
            raise RuntimeError("Neither curl_cffi nor websockets is installed.")

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _build_cookies(self, tokens, extra: dict = None) -> dict:
        cookies = {
            'auth-access-token': tokens.access_token,
            'auth-refresh-token': tokens.refresh_token,
        }
        if self.cf_clearance:
            cookies['cf_clearance'] = self.cf_clearance
        if extra:
            for k, v in extra.items():
                if k not in cookies:
                    cookies[k] = v
        return cookies

    def _common_headers(self) -> dict:
        return {
            'accept': '*/*',
            'accept-language': 'en,es-CL;q=0.9,es-419;q=0.8,es;q=0.7,fr;q=0.6',
            'origin': 'https://axiom.trade',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    async def _preflight_curl(self, session: CurlAsyncSession, tokens) -> None:
        """Pre-flight HTTP requests using curl_cffi (Chrome TLS fingerprint)."""
        v = int(time.time() * 1000)
        headers = {**self._common_headers(), 'referer': 'https://axiom.trade/',
                   'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site'}
        cookies = self._build_cookies(tokens)
        for url in [
            f'https://api.axiom.trade/wo/server-time?v={v}',
            f'https://api6.axiom.trade/get-announcement?v={v}',
        ]:
            try:
                await session.get(url, headers=headers, cookies=cookies, timeout=10)
                self.logger.debug(f"Pre-flight OK: {url}")
            except Exception as e:
                self.logger.debug(f"Pre-flight failed (non-fatal): {url} — {e}")

    async def _send(self, data: str) -> None:
        """Send a text message over whichever transport is active."""
        if self._curl_ws is not None:
            try:
                self._curl_ws.send(data.encode(), 1)  # 1 = CURLWS_TEXT
                return
            except Exception:
                pass
        if self.ws is not None:
            await self.ws.send(data)

    # ------------------------------------------------------------------ #
    #  Connection                                                          #
    # ------------------------------------------------------------------ #

    async def connect(self, is_token_price: bool = False) -> bool:
        """Connect to the WebSocket server using Chrome TLS impersonation via curl_cffi."""
        if not self.auth_manager.ensure_valid_authentication():
            self.logger.error("WebSocket authentication failed — unable to obtain valid tokens")
            return False

        tokens = self.auth_manager.get_tokens()
        if not tokens:
            self.logger.error("No authentication tokens available")
            return False

        if not self.cf_clearance:
            self.logger.warning("CF_CLEARANCE not set — connection may be rejected. "
                                "Set CF_CLEARANCE in .env (DevTools → Application → Cookies → cf_clearance)")

        current_url = self.ws_url_token_price if is_token_price else self.ws_url
        urls_to_try = [current_url]
        if not is_token_price:
            urls_to_try += [
                "wss://cluster3.axiom.trade/",
                "wss://cluster5.axiom.trade/",
                "wss://cluster7.axiom.trade/",
            ]

        if CURL_CFFI_AVAILABLE:
            return await self._connect_curl(tokens, urls_to_try)
        return await self._connect_websockets(tokens, urls_to_try)

    async def _connect_curl(self, tokens, urls_to_try: list) -> bool:
        """Connect using curl_cffi with Chrome TLS impersonation."""
        # Re-use session across reconnects so Cloudflare cookies persist
        if self._curl_session is None:
            self._curl_session = CurlAsyncSession(impersonate="chrome136")

        self.logger.info("Running pre-flight requests (curl_cffi / Chrome TLS)...")
        await self._preflight_curl(self._curl_session, tokens)

        cookies = self._build_cookies(tokens)
        ws_headers = {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Accept-Language': 'en,es-CL;q=0.9,es-419;q=0.8,es;q=0.7,fr;q=0.6',
        }

        for url in urls_to_try:
            try:
                self.logger.info(f"Attempting WebSocket: {url}")
                ctx = self._curl_session.ws_connect(url, headers=ws_headers, cookies=cookies)
                ws = await ctx.__aenter__()
                self._curl_ws_ctx = ctx
                self._curl_ws = ws
                self.logger.info(f"Connected: {url}")
                return True
            except Exception as e:
                self.logger.error(f"Failed {url}: {e}")
                self._curl_ws = None
                self._curl_ws_ctx = None

        return False

    async def _connect_websockets(self, tokens, urls_to_try: list) -> bool:
        """Fallback: connect using the websockets library (may fail Cloudflare TLS check)."""
        import requests as _req
        v = int(time.time() * 1000)
        cookies = self._build_cookies(tokens)
        session = _req.Session()
        for k, v_val in cookies.items():
            session.cookies.set(k, v_val, domain='axiom.trade')
        headers_http = {**self._common_headers(), 'referer': 'https://axiom.trade/',
                        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site'}
        for url in [f'https://api.axiom.trade/wo/server-time?v={v}',
                    f'https://api6.axiom.trade/get-announcement?v={v}']:
            try:
                session.get(url, headers=headers_http, timeout=10)
            except Exception:
                pass
        collected = {c.name: c.value for c in session.cookies}

        cookie_str = '; '.join(f'{k}={v}' for k, v in {**cookies, **{k: v for k, v in collected.items() if k not in cookies}}.items())
        ws_headers = {
            'Origin': 'https://axiom.trade',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'en,es-CL;q=0.9,es-419;q=0.8,es;q=0.7,fr;q=0.6',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'Cookie': cookie_str,
        }

        for url in urls_to_try:
            try:
                self.logger.info(f"Attempting WebSocket (fallback): {url}")
                self.ws = await self._ws_connect_with_headers(url, ws_headers)
                self.logger.info(f"Connected (fallback): {url}")
                return True
            except Exception as e:
                self.logger.error(f"Failed {url}: {e}")

        return False

    async def _ws_connect_with_headers(self, url: str, headers: dict):
        proxy_url = None
        if hasattr(self.auth_manager, 'proxies') and self.auth_manager.proxies:
            proxy_url = self.auth_manager.proxies.get('https') or self.auth_manager.proxies.get('http')

        connect_func = websockets.connect
        kwargs = {}
        if proxy_url and PROXY_SUPPORT:
            connect_func = proxy_connect
            kwargs['proxy'] = proxy_url

        if self._uses_additional_headers:
            return await connect_func(url, additional_headers=headers, **kwargs)
        elif self._uses_extra_headers:
            return await connect_func(url, extra_headers=headers, **kwargs)
        else:
            try:
                return await connect_func(url, additional_headers=headers, **kwargs)
            except TypeError:
                return await connect_func(url, extra_headers=headers, **kwargs)

    # ------------------------------------------------------------------ #
    #  Subscribe helpers                                                   #
    # ------------------------------------------------------------------ #

    async def _ensure_connected(self, is_token_price: bool = False) -> bool:
        connected = self._curl_ws is not None or self.ws is not None
        if not connected:
            return await self.connect(is_token_price=is_token_price)
        return True

    async def subscribe_new_tokens(self, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to new token updates."""
        if not await self._ensure_connected():
            return False
        self._callbacks["new_pairs"] = callback
        try:
            await self._send(json.dumps({"action": "join", "room": "new_pairs"}))
            self.logger.info("Subscribed to new token updates")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to new tokens: {e}")
            return False

    async def subscribe_token_price(self, token: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to token price updates."""
        if not await self._ensure_connected(is_token_price=True):
            return False
        self._callbacks[f"token_price_{token}"] = callback
        try:
            await self._send(json.dumps({"action": "join", "room": token}))
            self.logger.info(f"Subscribed to token price updates for {token}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to token price: {e}")
            return False

    async def subscribe_wallet_transactions(self, wallet_address: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to wallet transaction updates.

        Response format:
        {
            "room": "v:<WALLET_ADDRESS>",
            "content": {
                "created_at": "<ISO_DATETIME>",
                "maker_address": "<WALLET_ADDRESS>",
                "type": "buy" | "sell",
                "total_sol": <float>,
                "total_usd": <float>,
                ...
            }
        }
        """
        if not await self._ensure_connected():
            return False
        self._callbacks[f"wallet_transactions_{wallet_address}"] = callback
        try:
            await self._send(json.dumps({"action": "join", "room": f"v:{wallet_address}"}))
            self.logger.info(f"Subscribed to wallet transactions for {wallet_address}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to wallet transactions: {e}")
            return False

    async def subscribe_active_users(self, callback: Callable[[int], None],
                                     token_address: str = "FFcYgSSgWHforA9rXXkA48p8YFoz8TSW85Jpo3CQHDyS"):
        """Subscribe to active Axiom users count updates for a specific token."""
        if not await self._ensure_connected():
            return False
        self._callbacks[f"active_users_{token_address}"] = callback
        rooms = [
            f"t:{token_address}", f"f:{token_address}", f"td:{token_address}",
            f"{token_address}-dex-paid", f"s:{token_address}", f"{token_address}_refresh",
            f"{token_address}-wallet_funding", f"kol_tx:{token_address}",
            f"pump-cto:{token_address}", f"e-{token_address}", f"b-{token_address}",
        ]
        try:
            for room in rooms:
                await self._send(json.dumps({"action": "join", "room": room}))
            self.logger.info(f"Subscribed to active users updates for token {token_address}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe to active users: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Message loop                                                        #
    # ------------------------------------------------------------------ #

    async def _dispatch(self, raw: str) -> None:
        """Route a raw JSON message to the appropriate callback."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse WebSocket message: {raw[:200]}")
            return

        room = data.get("room", "")
        content = data.get("content")

        if "new_pairs" in self._callbacks and room == "new_pairs" and content:
            await self._callbacks["new_pairs"]([content])

        for key, cb in list(self._callbacks.items()):
            if key.startswith("active_users_"):
                addr = key[len("active_users_"):]
                if room == f"e-{addr}" and content is not None:
                    try:
                        await cb(int(content))
                    except (ValueError, TypeError):
                        self.logger.error(f"Failed to parse active users count: {content}")
                elif room == f"s:{addr}" and isinstance(content, dict) and "active_users" in content:
                    await cb(int(content["active_users"]))

            elif key.startswith("token_price_"):
                token = key[len("token_price_"):]
                if room == token and content:
                    await cb(content)

            elif key.startswith("wallet_transactions_"):
                wallet = key[len("wallet_transactions_"):]
                if room == f"v:{wallet}" and content:
                    await cb(content)

    async def _message_handler_curl(self) -> None:
        """Message loop for curl_cffi WebSocket."""
        loop = asyncio.get_event_loop()
        while self._curl_ws is not None:
            try:
                data, _ = await loop.run_in_executor(None, self._curl_ws.recv)
                if data:
                    await self._dispatch(data.decode('utf-8', errors='replace'))
            except Exception as e:
                self.logger.warning(f"WebSocket connection closed: {e}")
                break

    async def _message_handler_websockets(self) -> None:
        """Message loop for websockets fallback."""
        try:
            async for message in self.ws:
                try:
                    await self._dispatch(message)
                except Exception as e:
                    self.logger.error(f"Error handling message: {e}")
        except Exception as e:
            self.logger.warning(f"WebSocket connection closed: {e}")

    async def start(self):
        """Start the WebSocket client and message handler."""
        if not await self._ensure_connected():
            return
        if self._curl_ws is not None:
            await self._message_handler_curl()
        elif self.ws is not None:
            await self._message_handler_websockets()

    async def close(self):
        """Close the WebSocket connection."""
        if self._curl_ws is not None:
            try:
                self._curl_ws.close()
            except Exception:
                pass
            self._curl_ws = None
        if self.ws is not None:
            await self.ws.close()
            self.ws = None
        if self._curl_session is not None:
            await self._curl_session.close()
            self._curl_session = None
        self.logger.info("WebSocket connection closed")
