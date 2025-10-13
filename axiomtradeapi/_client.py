from axiomtradeapi.content.endpoints import Endpoints
from axiomtradeapi.helpers.help import Helping
from axiomtradeapi.websocket._client import AxiomTradeWebSocketClient
from axiomtradeapi.auth import AuthManager
import requests
import logging
import json
from typing import List, Dict, Union, Optional
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
import base64
import time
import hashlib

from axiomtradeapi.urls import AAllBaseUrls, AxiomTradeApiUrls
from axiomtradeapi.helpers.TryServers import try_servers

class AxiomTradeClient:
    def __init__(self, username: str = None, password: str = None, 
                 auth_token: str = None, refresh_token: str = None,
                 log_level: int = logging.INFO) -> None:
        """
        Initialize Axiom Trade Client with automatic authentication
        
        Args:
            username: Email for automatic login (optional if tokens provided)
            password: Password for automatic login (optional if tokens provided)
            auth_token: Existing auth token (optional)
            refresh_token: Existing refresh token (optional)
            log_level: Logging level
        """
        self.endpoints = Endpoints()
        self.base_url_api = self.endpoints.BASE_URL_API
        self.helper = Helping()
        
        # Validate that either credentials or tokens are provided
        has_credentials = username and password
        has_tokens = auth_token and refresh_token
        
        if not has_credentials and not has_tokens:
            raise ValueError("Either username/password or auth_token/refresh_token must be provided")
        
        # Initialize authentication manager
        self.auth_manager = AuthManager(
            username=username,
            password=password,
            auth_token=auth_token,
            refresh_token=refresh_token
        )
        
        # Setup logging
        self.logger = logging.getLogger("AxiomTradeAPI")
        self.logger.setLevel(log_level)
        
        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Initialize WebSocket client with auth manager
        self.ws = AxiomTradeWebSocketClient(
            auth_manager=self.auth_manager,
            log_level=log_level
        )
    
    def set_tokens(self, access_token: str = None, refresh_token: str = None):
        """
        Set access and refresh tokens manually
        """
        if access_token or refresh_token:
            from axiomtradeapi.auth.auth_manager import AuthTokens
            # Update the auth manager's tokens
            if not self.auth_manager.tokens:
                self.auth_manager.tokens = AuthTokens(
                    access_token=access_token or "",
                    refresh_token=refresh_token or "",
                    expires_at=None
                )
            else:
                if access_token:
                    self.auth_manager.tokens.access_token = access_token
                if refresh_token:
                    self.auth_manager.tokens.refresh_token = refresh_token
    
    def get_tokens(self) -> Dict[str, Optional[str]]:
        """
        Get current tokens
        """
        if self.auth_manager.tokens:
            return {
                'access_token': self.auth_manager.tokens.access_token,
                'refresh_token': self.auth_manager.tokens.refresh_token
            }
        return {'access_token': None, 'refresh_token': None}
    
    def is_authenticated(self) -> bool:
        """
        Check if the client has valid authentication tokens
        """
        return self.auth_manager.tokens is not None and bool(self.auth_manager.tokens.access_token)
            
    async def GetTokenPrice(self, token_symbol: str) -> Optional[float]:
        """Get the current price of a token by its symbol."""
        try:
            await self.ws.connect(is_token_price=True)
            token_subscribe = await self.ws.subscribe_token_price(token_symbol, lambda data: data.get("price"))
            if not token_subscribe:
                self.logger.error(f"Failed to subscribe to token price for {token_symbol}")
                return None
            self.logger.debug(f"Subscribed to token price for {token_symbol}")
            return token_subscribe
                
        except requests.exceptions.RequestException as err:
            error_msg = f"An error occurred: {err}"
            self.logger.error(error_msg)
            return None
            
    def GetBalance(self, wallet_address: str, rpc_url: str = "https://api.mainnet-beta.solana.com") -> Dict[str, Union[float, int]]:
        """
        Get SOL balance for a single wallet address using Solana RPC directly.
        
        Args:
            wallet_address (str): Wallet public key
            rpc_url (str): Solana RPC endpoint URL
            
        Returns:
            Dict with balance info or None on error
        """
        try:
            # Use Solana RPC getBalance method
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [wallet_address]
            }
            
            self.logger.debug(f"Fetching balance for wallet: {wallet_address}")
            
            response = requests.post(
                url=rpc_url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    balance_data = result["result"]
                    lamports = balance_data.get("value", 0)
                    sol = lamports / 1_000_000_000  # Convert lamports to SOL
                    
                    self.logger.info(f"Successfully retrieved balance for {wallet_address}: {sol} SOL")
                    return {
                        "sol": sol,
                        "lamports": lamports,
                        "slot": balance_data.get("context", {}).get("slot", 0)
                    }
                elif "error" in result:
                    error_msg = f"RPC Error: {result['error']}"
                    self.logger.error(error_msg)
                    return None
            else:
                error_msg = f"Error: {response.status_code}"
                self.logger.error(error_msg)
                return None
                
        except Exception as err:
            error_msg = f"An error occurred: {err}"
            self.logger.error(error_msg)
            return None
            
    def GetBatchedBalance(self, wallet_addresses: List[str], rpc_url: str = "https://api.mainnet-beta.solana.com") -> Dict[str, Dict[str, Union[float, int]]]:
        """
        Get SOL balances for multiple wallet addresses using Solana RPC directly.
        
        Args:
            wallet_addresses (List[str]): List of wallet public keys
            rpc_url (str): Solana RPC endpoint URL
            
        Returns:
            Dict mapping wallet addresses to balance info
        """
        try:
            result = {}
            
            # Fetch balance for each wallet using RPC
            for address in wallet_addresses:
                balance_info = self.GetBalance(address, rpc_url)
                result[address] = balance_info
            
            return result
                
        except Exception as err:
            error_msg = f"An error occurred: {err}"
            self.logger.error(error_msg)
            return {addr: None for addr in wallet_addresses}
    
    def buy_token(self, private_key: str, token_mint: str, amount_sol: float, 
                  slippage_percent: float = 5.0, priority_fee: float = 0.005,
                  pool: str = "auto", rpc_url: str = "https://api.mainnet-beta.solana.com/") -> Dict[str, Union[str, bool]]:
        """
        Buy a token using SOL via PumpPortal API.
        
        Args:
            private_key (str): Private key as base58 string
            token_mint (str): Token mint address to buy
            amount_sol (float): Amount of SOL to spend
            slippage_percent (float): Slippage tolerance percentage (default: 5%)
            priority_fee (float): Priority fee in SOL (default: 0.005)
            pool (str): Exchange to trade on - "pump", "raydium", "auto", etc. (default: "auto")
            rpc_url (str): Solana RPC endpoint URL
            
        Returns:
            Dict with transaction signature and success status
        """
        try:
            from solders.keypair import Keypair
            from solders.transaction import VersionedTransaction
            from solders.commitment_config import CommitmentLevel
            from solders.rpc.requests import SendVersionedTransaction
            from solders.rpc.config import RpcSendTransactionConfig
            
            # Convert private key to Keypair using base58 string format
            keypair = Keypair.from_base58_string(private_key)
            public_key = str(keypair.pubkey())
            
            self.logger.info(f"Initiating buy order for {amount_sol} SOL worth of token {token_mint}")
            self.logger.debug(f"  Buyer Public Key: {public_key}")
            self.logger.debug(f"  Slippage: {int(slippage_percent)}%")
            self.logger.debug(f"  Priority Fee: {priority_fee} SOL")
            self.logger.debug(f"  Pool: {pool}")
            
            # Prepare trade data for PumpPortal API
            trade_data = {
                "publicKey": public_key,
                "action": "buy",
                "mint": token_mint,
                "amount": amount_sol,
                "denominatedInSol": "true",
                "slippage": int(slippage_percent),
                "priorityFee": priority_fee,
                "pool": pool
            }
            
            self.logger.debug(f"Sending trade request to PumpPortal with data: {trade_data}")
            
            # Get transaction from PumpPortal
            response = requests.post(url="https://pumpportal.fun/api/trade-local", data=trade_data)
            
            if response.status_code != 200:
                error_msg = f"PumpPortal API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Create and sign transaction
            tx = VersionedTransaction(VersionedTransaction.from_bytes(response.content).message, [keypair])
            
            # Configure and send transaction to RPC
            commitment = CommitmentLevel.Confirmed
            config = RpcSendTransactionConfig(preflight_commitment=commitment)
            txPayload = SendVersionedTransaction(tx, config)
            
            response = requests.post(
                url=rpc_url,
                headers={"Content-Type": "application/json"},
                data=txPayload.to_json()
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    tx_signature = result['result']
                    self.logger.info(f"Transaction successful. Signature: {tx_signature}")
                    return {
                        "success": True,
                        "signature": tx_signature,
                        "transactionId": tx_signature,
                        "explorer_url": f"https://solscan.io/tx/{tx_signature}"
                    }
                elif "error" in result:
                    error_msg = f"RPC Error: {result['error']}"
                    self.logger.error(error_msg)
                    return {"success": False, "error": error_msg}
                else:
                    error_msg = f"Unexpected RPC response: {result}"
                    self.logger.error(error_msg)
                    return {"success": False, "error": error_msg}
            else:
                error_msg = f"Failed to send transaction: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Error in buy_token: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def sell_token(self, private_key: str, token_mint: str, amount_tokens: Union[float, str], 
                   slippage_percent: float = 5.0, priority_fee: float = 0.005,
                   pool: str = "auto", rpc_url: str = "https://api.mainnet-beta.solana.com/") -> Dict[str, Union[str, bool]]:
        """
        Sell a token for SOL via PumpPortal API.
        
        Args:
            private_key (str): Private key as base58 string
            token_mint (str): Token mint address to sell
            amount_tokens (Union[float, str]): Amount of tokens to sell (can be float or "100%" to sell all)
            slippage_percent (float): Slippage tolerance percentage (default: 5%)
            priority_fee (float): Priority fee in SOL (default: 0.005)
            pool (str): Exchange to trade on - "pump", "raydium", "auto", etc. (default: "auto")
            rpc_url (str): Solana RPC endpoint URL
            
        Returns:
            Dict with transaction signature and success status
        """
        try:
            from solders.keypair import Keypair
            from solders.transaction import VersionedTransaction
            from solders.commitment_config import CommitmentLevel
            from solders.rpc.requests import SendVersionedTransaction
            from solders.rpc.config import RpcSendTransactionConfig
            
            # Convert private key to Keypair using base58 string format
            keypair = Keypair.from_base58_string(private_key)
            public_key = str(keypair.pubkey())
            
            self.logger.info(f"Initiating sell order for {amount_tokens} tokens of {token_mint}")
            self.logger.debug(f"  Seller Public Key: {public_key}")
            self.logger.debug(f"  Slippage: {int(slippage_percent)}%")
            self.logger.debug(f"  Priority Fee: {priority_fee} SOL")
            self.logger.debug(f"  Pool: {pool}")
            
            # Prepare trade data for PumpPortal API
            trade_data = {
                "publicKey": public_key,
                "action": "sell",
                "mint": token_mint,
                "amount": amount_tokens,
                "denominatedInSol": "false",  # Selling tokens, not SOL
                "slippage": int(slippage_percent),
                "priorityFee": priority_fee,
                "pool": pool
            }
            
            self.logger.debug(f"Sending trade request to PumpPortal with data: {trade_data}")
            
            # Get transaction from PumpPortal
            response = requests.post(url="https://pumpportal.fun/api/trade-local", data=trade_data)
            
            if response.status_code != 200:
                error_msg = f"PumpPortal API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Create and sign transaction
            tx = VersionedTransaction(VersionedTransaction.from_bytes(response.content).message, [keypair])
            
            # Configure and send transaction to RPC
            commitment = CommitmentLevel.Confirmed
            config = RpcSendTransactionConfig(preflight_commitment=commitment)
            txPayload = SendVersionedTransaction(tx, config)
            
            response = requests.post(
                url=rpc_url,
                headers={"Content-Type": "application/json"},
                data=txPayload.to_json()
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    tx_signature = result['result']
                    self.logger.info(f"Transaction successful. Signature: {tx_signature}")
                    return {
                        "success": True,
                        "signature": tx_signature,
                        "transactionId": tx_signature,
                        "explorer_url": f"https://solscan.io/tx/{tx_signature}"
                    }
                elif "error" in result:
                    error_msg = f"RPC Error: {result['error']}"
                    self.logger.error(error_msg)
                    return {"success": False, "error": error_msg}
                else:
                    error_msg = f"Unexpected RPC response: {result}"
                    self.logger.error(error_msg)
                    return {"success": False, "error": error_msg}
            else:
                error_msg = f"Failed to send transaction: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Error in sell_token: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def get_token_balance(self, wallet_address: str, token_mint: str, rpc_url: str = "https://api.mainnet-beta.solana.com") -> Optional[float]:
        """
        Get the balance of a specific token for a wallet using Solana RPC directly.
        
        Args:
            wallet_address (str): Wallet public key
            token_mint (str): Token mint address
            rpc_url (str): Solana RPC endpoint URL
            
        Returns:
            Token balance as float, or None if error
        """
        try:
            from solders.pubkey import Pubkey
            
            # Use Solana RPC getTokenAccountsByOwner method
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenAccountsByOwner",
                "params": [
                    wallet_address,
                    {
                        "mint": token_mint
                    },
                    {
                        "encoding": "jsonParsed"
                    }
                ]
            }
            
            self.logger.debug(f"Fetching token balance for wallet: {wallet_address}, mint: {token_mint}")
            
            response = requests.post(
                url=rpc_url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result and result["result"]["value"]:
                    # Get the first token account (there should typically be only one)
                    token_account = result["result"]["value"][0]
                    balance_info = token_account["account"]["data"]["parsed"]["info"]["tokenAmount"]
                    balance = float(balance_info["uiAmount"])
                    
                    self.logger.info(f"Token balance for {token_mint}: {balance}")
                    return balance
                elif "result" in result:
                    # No token account found, balance is 0
                    self.logger.info(f"No token account found for {token_mint}, balance: 0")
                    return 0.0
                elif "error" in result:
                    error_msg = f"RPC Error: {result['error']}"
                    self.logger.error(error_msg)
                    return None
            else:
                self.logger.error(f"Failed to get token balance: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting token balance: {str(e)}")
            return None

    async def subscribe_new_tokens(self, callback):
        """Subscribe to new token updates via WebSocket."""
        return await self.ws.subscribe_new_tokens(callback)
    
    def login_step1(self, email: str, b64_password: str) -> str:
        """
        First step of login - send email and password to get OTP JWT token
        Returns the OTP JWT token needed for step 2
        """
        url = f'{AAllBaseUrls.BASE_URL_v3}{AxiomTradeApiUrls.LOGIN_STEP1}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }
        
        data = {
            "email": email,
            "b64Password": b64_password
        }
        
        self.logger.debug(f"Sending login step 1 request for email: {email}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        otp_token = result.get('otpJwtToken')
        self.logger.debug("OTP JWT token received successfully")
        return otp_token

    def login_step1_try_servers(self, email: str, b64_password: str, otp_token: str = "") -> str:
        """
        First step of login - tries all servers for login step 1, returns the OTP JWT token from the first server that responds with 200.
        The token is extracted from the response cookies (auth-otp-login-token).
        All headers are set as in the curl example, including the Cookie header.
        Args:
            email (str): User email
            b64_password (str): Base64-encoded password
            otp_token (str): Optional, value for auth-otp-login-token cookie (default: empty)
        """
        path = AxiomTradeApiUrls.LOGIN_STEP1
        data = {
            "email": email,
            "b64Password": b64_password
        }
        print(data)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://axiom.trade',
            'priority': 'u=1, i',
            'referer': 'https://axiom.trade/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Opera GX";v="119"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0',
            'Cookie': f'auth-otp-login-token={otp_token}'
        }
        self.logger.debug(f"Trying login step 1 on all servers for email: {email}")
        base_url = f'{AAllBaseUrls.BASE_URL_v6}{AxiomTradeApiUrls.LOGIN_STEP1}'
        if base_url is None:
            raise Exception("No server responded with 200 for login step 1.")
        response = requests.post(base_url, headers=headers, json=data)
        print(f"Response from server: {response.json()}")
        otp_token = response.cookies.get('auth-otp-login-token')
        if not otp_token:
            self.logger.error("auth-otp-login-token not found in cookies!")
            raise Exception("auth-otp-login-token not found in cookies!")
        self.logger.debug(f"OTP JWT token received from {base_url} (from cookies)")
        return otp_token

    def login_step2(self, otp_jwt_token: str, otp_code: str, email: str, b64_password: str) -> Dict:
        """
        Second step of login - send OTP code to complete authentication
        Returns client credentials (clientSecret, orgId, userId)
        """
        url = f'{AAllBaseUrls.BASE_URL_v3}{AxiomTradeApiUrls.LOGIN_STEP2}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/',
            'Cookie': f'auth-otp-login-token={otp_jwt_token}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }
        
        data = {
            "code": otp_code,
            "email": email,
            "b64Password": b64_password
        }
        
        self.logger.debug("Sending login step 2 request with OTP code")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        credentials = response.json()
        self.logger.info("Login completed successfully")
        return credentials

    def get_b64_password(self, password: str) -> str:
        """
        Hash the password with SHA256 and then base64 encode the result, using ISO-8859-1 encoding for the password.
        """
        sha256_hash = hashlib.sha256(password.encode('iso-8859-1')).digest()
        b64_password = base64.b64encode(sha256_hash).decode('utf-8')
        return b64_password

    def complete_login(self, email: str, b64_password: str) -> Dict:
        """
        Complete the full login process
        Returns client credentials (clientSecret, orgId, userId)
        """
        self.logger.info("Starting login process...")
        #b64_password = self.get_b64_password(password)
        otp_jwt_token = self.login_step1_try_servers(email, b64_password)
        otp_code = input("Enter the OTP code sent to your email: ")
        credentials = self.login_step2(otp_jwt_token, otp_code, email, b64_password)
        
        # Store credentials in auth manager if available
        if hasattr(self, 'auth_manager'):
            # Update auth manager with new credentials
            # Note: This may need adjustment based on how auth_manager handles these credentials
            pass
            
        return credentials

    def refresh_access_token_direct(self, refresh_token: str) -> str:
        """
        Refresh the access token using a refresh token
        Returns the new access token
        """
        url = 'https://api9.axiom.trade/refresh-access-token'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/',
            'Cookie': f'auth-refresh-token={refresh_token}',
            'Content-Length': '0',
            'TE': 'trailers'
        }
        
        self.logger.debug("Refreshing access token")
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        # Check if token is in response JSON or cookies
        try:
            result = response.json()
            new_token = result.get('auth-access-token')
        except:
            new_token = None
            
        if not new_token:
            # Try to get from cookies
            new_token = response.cookies.get('auth-access-token')
            
        if new_token:
            self.logger.debug("Access token refreshed successfully")
        else:
            self.logger.warning("Could not extract new access token from response")
            
        return new_token

    def get_trending_tokens(self, access_token: str, time_period: str = '1h') -> Dict:
        """
        Get trending meme tokens
        Available time periods: 1h, 24h, 7d
        """
        url = f'https://api6.axiom.trade/meme-trending?timePeriod={time_period}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/',
            'Cookie': f'auth-access-token={access_token}',
            'TE': 'trailers'
        }
        
        self.logger.debug(f"Fetching trending tokens for period: {time_period}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        self.logger.debug(f"Retrieved {len(result) if isinstance(result, list) else 'N/A'} trending tokens")
        return result
