"""
Authentication and Cookie Manager for Axiom Trade API
Handles automatic login, token refresh, and cookie management
"""

import requests
import json
import time
import logging
import os
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class AuthTokens:
    """Container for authentication tokens"""
    access_token: str
    refresh_token: str
    expires_at: float
    issued_at: float
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired (with 5 minute buffer)"""
        return time.time() >= (self.expires_at - 300)  # 5 minute buffer
    
    @property
    def needs_refresh(self) -> bool:
        """Check if token needs refresh (15 minute buffer)"""
        return time.time() >= (self.expires_at - 900)  # 15 minute buffer

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'issued_at': self.issued_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthTokens':
        """Create from dictionary"""
        return cls(
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            expires_at=data['expires_at'],
            issued_at=data['issued_at']
        )


class SecureTokenStorage:
    """Handles secure storage and retrieval of authentication tokens"""
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize secure token storage
        
        Args:
            storage_dir: Directory to store tokens (default: ~/.axiomtradeapi)
        """
        self.storage_dir = Path(storage_dir or Path.home() / '.axiomtradeapi')
        self.storage_dir.mkdir(exist_ok=True, mode=0o700)  # Only user can access
        
        self.token_file = self.storage_dir / 'tokens.enc'
        self.key_file = self.storage_dir / 'key.enc'
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize encryption key
        self._init_encryption_key()
    
    def _init_encryption_key(self):
        """Initialize or load encryption key"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
            # Set file permissions to be readable only by user
            os.chmod(self.key_file, 0o600)
        
        self.cipher_suite = Fernet(self.key)
    
    def save_tokens(self, tokens: AuthTokens) -> bool:
        """
        Securely save authentication tokens
        
        Args:
            tokens: AuthTokens to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Convert tokens to JSON
            token_data = json.dumps(tokens.to_dict()).encode('utf-8')
            
            # Encrypt the data
            encrypted_data = self.cipher_suite.encrypt(token_data)
            
            # Write to file
            with open(self.token_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set file permissions to be readable only by user
            os.chmod(self.token_file, 0o600)
            
            self.logger.debug("Tokens saved securely")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save tokens: {e}")
            return False
    
    def load_tokens(self) -> Optional[AuthTokens]:
        """
        Load and decrypt authentication tokens
        
        Returns:
            AuthTokens: Loaded tokens if successful, None otherwise
        """
        if not self.token_file.exists():
            self.logger.debug("No saved tokens found")
            return None
        
        try:
            # Read encrypted data
            with open(self.token_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            
            # Parse JSON
            token_data = json.loads(decrypted_data.decode('utf-8'))
            
            # Create AuthTokens object
            tokens = AuthTokens.from_dict(token_data)
            
            self.logger.debug("Tokens loaded successfully")
            return tokens
            
        except Exception as e:
            self.logger.error(f"Failed to load tokens: {e}")
            return None
    
    def delete_tokens(self) -> bool:
        """
        Delete saved tokens
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            if self.token_file.exists():
                self.token_file.unlink()
                self.logger.debug("Saved tokens deleted")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete tokens: {e}")
            return False
    
    def has_saved_tokens(self) -> bool:
        """Check if saved tokens exist"""
        return self.token_file.exists()


class CookieManager:
    """Manages cookies for HTTP requests"""
    
    def __init__(self):
        self.cookies = {}
        self.logger = logging.getLogger(__name__)
    
    def set_auth_cookies(self, auth_token: str, refresh_token: str) -> None:
        """Set authentication cookies"""
        self.cookies['auth-access-token'] = auth_token
        self.cookies['auth-refresh-token'] = refresh_token
        self.logger.debug("Authentication cookies updated")
    
    def get_cookie_header(self) -> str:
        """Get formatted cookie header string"""
        if not self.cookies:
            return ""
        
        cookie_pairs = [f"{key}={value}" for key, value in self.cookies.items()]
        return "; ".join(cookie_pairs)
    
    def clear_auth_cookies(self) -> None:
        """Clear authentication cookies"""
        self.cookies.pop('auth-access-token', None)
        self.cookies.pop('auth-refresh-token', None)
        self.logger.debug("Authentication cookies cleared")
    
    def has_auth_cookies(self) -> bool:
        """Check if auth cookies are present"""
        return 'auth-access-token' in self.cookies and 'auth-refresh-token' in self.cookies


class AuthManager:
    """
    Manages authentication for Axiom Trade API
    Handles automatic login, token refresh, and session management
    """
    
    def __init__(self, username: str = None, password: str = None, 
                 auth_token: str = None, refresh_token: str = None,
                 storage_dir: str = None, use_saved_tokens: bool = True):
        """
        Initialize AuthManager
        
        Args:
            username: Email for automatic login
            password: Password for automatic login  
            auth_token: Existing auth token (optional)
            refresh_token: Existing refresh token (optional)
            storage_dir: Directory for secure token storage
            use_saved_tokens: Whether to load saved tokens (default: True)
        """
        self.username = username
        self.password = password
        self.base_url = "https://axiom.trade"
        self.use_saved_tokens = use_saved_tokens
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize cookie manager
        self.cookie_manager = CookieManager()
        
        # Initialize secure token storage
        self.token_storage = SecureTokenStorage(storage_dir)
        
        # Token storage
        self.tokens: Optional[AuthTokens] = None
        
        # Try to load saved tokens first (if enabled)
        if use_saved_tokens:
            saved_tokens = self.token_storage.load_tokens()
            if saved_tokens and not saved_tokens.is_expired:
                self.tokens = saved_tokens
                self.cookie_manager.set_auth_cookies(
                    saved_tokens.access_token, 
                    saved_tokens.refresh_token
                )
                self.logger.info("Loaded valid saved tokens")
            elif saved_tokens and saved_tokens.is_expired:
                self.logger.info("Saved tokens are expired, will attempt refresh")
                self.tokens = saved_tokens
        
        # Initialize with provided tokens if given (overrides saved tokens)
        if auth_token and refresh_token:
            self._set_tokens(auth_token, refresh_token)
    
    def _set_tokens(self, auth_token: str, refresh_token: str, 
                   expires_in: int = 3600, save_tokens: bool = True) -> None:
        """Set authentication tokens"""
        current_time = time.time()
        
        self.tokens = AuthTokens(
            access_token=auth_token,
            refresh_token=refresh_token,
            expires_at=current_time + expires_in,
            issued_at=current_time
        )
        
        # Update cookies
        self.cookie_manager.set_auth_cookies(auth_token, refresh_token)
        
        # Save tokens securely if enabled
        if save_tokens and self.use_saved_tokens:
            if self.token_storage.save_tokens(self.tokens):
                self.logger.debug("Tokens saved securely")
            else:
                self.logger.warning("Failed to save tokens securely")
        
        self.logger.info("Authentication tokens updated successfully")
    
    def authenticate(self) -> bool:
        """
        Authenticate with username/password using Axiom's OTP login flow
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.username or not self.password:
            self.logger.error("Username and password required for authentication")
            return False
        
        try:
            self.logger.info("Starting Axiom Trade authentication...")
            
            # Step 1: Get OTP JWT token
            otp_jwt_token = self._login_step1()
            if not otp_jwt_token:
                return False
            
            # Step 2: Get OTP code from user
            otp_code = input("Enter the OTP code sent to your email: ")
            if not otp_code:
                self.logger.error("OTP code is required")
                return False
            
            # Step 3: Complete login with OTP
            return self._login_step2(otp_jwt_token, otp_code)
            
        except Exception as e:
            self.logger.error(f"❌ Authentication error: {e}")
            return False
    
    def _get_b64_password(self, password: str) -> str:
        """Hashes a password using PBKDF2-HMAC-SHA256 and returns a Base64 string."""
        SALT = bytes([
            217, 3, 161, 123, 53, 200, 206, 36, 143, 2, 220, 252, 240, 109, 204, 23,
            217, 174, 79, 158, 18, 76, 149, 117, 73, 40, 207, 77, 34, 194, 196, 163
        ])
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            SALT,
            600_000,
            dklen=32
        )

        return base64.b64encode(derived_key).decode('ascii')
    
    def _login_step1(self) -> Optional[str]:
        """First step of login - send email and password to get OTP JWT token"""
        from axiomtradeapi.urls import AAllBaseUrls, AxiomTradeApiUrls
        
        # Hash password
        b64_password = self._get_b64_password(self.password)
        
        url = f'{AAllBaseUrls.BASE_URL_v6}{AxiomTradeApiUrls.LOGIN_STEP1}'
        
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
            'Cookie': 'auth-otp-login-token='
        }
        
        data = {
            "email": self.username,
            "b64Password": b64_password
        }
        
        try:
            self.logger.debug(f"Sending login step 1 request for email: {self.username}")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                otp_token = response.cookies.get('auth-otp-login-token')
                if otp_token:
                    self.logger.debug("OTP JWT token received successfully")
                    return otp_token
                else:
                    self.logger.error("auth-otp-login-token not found in cookies!")
                    return None
            else:
                self.logger.error(f"Login step 1 failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Login step 1 error: {e}")
            return None
    
    def _login_step2(self, otp_jwt_token: str, otp_code: str) -> bool:
        """Second step of login - send OTP code to complete authentication"""
        from axiomtradeapi.urls import AAllBaseUrls, AxiomTradeApiUrls
        
        # Hash password
        b64_password = self._get_b64_password(self.password)
        
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
            "email": self.username,
            "b64Password": b64_password
        }
        
        try:
            self.logger.debug("Sending login step 2 request with OTP code")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                # Extract tokens from response cookies
                auth_token = response.cookies.get('auth-access-token')
                refresh_token = response.cookies.get('auth-refresh-token')
                
                if auth_token and refresh_token:
                    self._set_tokens(auth_token, refresh_token)
                    self.logger.info("✅ Authentication successful!")
                    return True
                else:
                    # Sometimes tokens are in response body
                    try:
                        response_data = response.json()
                        auth_token = response_data.get('accessToken') or response_data.get('auth-access-token')
                        refresh_token = response_data.get('refreshToken') or response_data.get('auth-refresh-token')
                        
                        if auth_token and refresh_token:
                            self._set_tokens(auth_token, refresh_token)
                            self.logger.info("✅ Authentication successful!")
                            return True
                    except:
                        pass
                    
                    self.logger.error("❌ No authentication tokens found in response")
                    return False
            else:
                self.logger.error(f"❌ Login step 2 failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Login step 2 error: {e}")
            return False
    
    def refresh_tokens(self) -> bool:
        """
        Refresh authentication tokens using the correct API endpoint
        
        Returns:
            bool: True if refresh successful, False otherwise
        """
        if not self.tokens or not self.tokens.refresh_token:
            self.logger.error("No refresh token available")
            return False

        # Headers based on your curl command
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6',
            'content-length': '0',
            'origin': 'https://axiom.trade/',
            'priority': 'u=1, i',
            'referer': 'https://axiom.trade/',
            'sec-ch-ua': '"Opera GX";v="120", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0'
        }
        
        # Add cookies with both tokens (as shown in your curl)
        cookies = {
            'auth-refresh-token': self.tokens.refresh_token,
            'auth-access-token': self.tokens.access_token
        }
        
        try:
            self.logger.info("Refreshing authentication tokens...")
            
            # Use the exact endpoint from your curl command
            refresh_url = 'https://api.axiom.trade/refresh-access-token'
            response = requests.post(
                refresh_url,
                headers=headers,
                cookies=cookies,
                timeout=30
            )
            
            if response.status_code == 200:
                # Extract new tokens from response cookies
                new_auth_token = response.cookies.get('auth-access-token')
                new_refresh_token = response.cookies.get('auth-refresh-token')
                
                if new_auth_token:
                    # Use new refresh token if provided, otherwise keep the existing one
                    refresh_token_to_use = new_refresh_token or self.tokens.refresh_token
                    self._set_tokens(new_auth_token, refresh_token_to_use)
                    self.logger.info("✅ Tokens refreshed successfully!")
                    return True
                else:
                    # Sometimes the response might be in JSON format
                    try:
                        response_data = response.json()
                        new_auth_token = (response_data.get('accessToken') or 
                                        response_data.get('auth-access-token') or
                                        response_data.get('access_token'))
                        new_refresh_token = (response_data.get('refreshToken') or 
                                           response_data.get('auth-refresh-token') or
                                           response_data.get('refresh_token'))
                        
                        if new_auth_token:
                            refresh_token_to_use = new_refresh_token or self.tokens.refresh_token
                            self._set_tokens(new_auth_token, refresh_token_to_use)
                            self.logger.info("✅ Tokens refreshed successfully from JSON response!")
                            return True
                    except (json.JSONDecodeError, AttributeError):
                        pass
                    
                    self.logger.error("❌ No new access token in refresh response")
                    return False
            else:
                self.logger.error(f"❌ Token refresh failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Token refresh request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected token refresh error: {e}")
            return False
    
    def ensure_valid_authentication(self) -> bool:
        """
        Ensure we have valid authentication tokens
        Automatically refreshes or re-authenticates as needed
        
        Returns:
            bool: True if valid authentication available, False otherwise
        """
        # No tokens at all - try to authenticate
        if not self.tokens:
            if self.username and self.password:
                return self.authenticate()
            else:
                self.logger.error("No authentication tokens and no credentials provided")
                return False
        
        # Tokens are still valid
        if not self.tokens.is_expired:
            return True
        
        # Try to refresh tokens
        if self.refresh_tokens():
            return True
        
        # Refresh failed - try to re-authenticate
        if self.username and self.password:
            self.logger.info("Token refresh failed, attempting re-authentication...")
            return self.authenticate()
        
        self.logger.error("Cannot refresh tokens and no credentials for re-authentication")
        return False
    
    def get_authenticated_headers(self, additional_headers: Dict[str, str] = None) -> Dict[str, str]:
        """
        Get headers with authentication cookies
        
        Args:
            additional_headers: Additional headers to include
            
        Returns:
            dict: Headers with authentication cookies
        """
        # Ensure we have valid authentication
        if not self.ensure_valid_authentication():
            self.logger.warning("No valid authentication available")
        
        # Base headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/discover",
            "User-Agent": "AxiomTradeAPI-py/1.0"
        }
        
        # Add authentication cookies if available
        cookie_header = self.cookie_manager.get_cookie_header()
        if cookie_header:
            headers["Cookie"] = cookie_header
        
        # Add any additional headers
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated with valid tokens"""
        return (self.tokens is not None and 
                not self.tokens.is_expired and 
                self.cookie_manager.has_auth_cookies())
    
    def logout(self) -> None:
        """Clear all authentication data including saved tokens"""
        self.tokens = None
        self.cookie_manager.clear_auth_cookies()
        
        # Also clear saved tokens if storage is enabled
        if self.use_saved_tokens:
            self.token_storage.delete_tokens()
        
        self.logger.info("Logged out successfully")
    
    def clear_saved_tokens(self) -> bool:
        """
        Clear saved tokens from secure storage
        
        Returns:
            bool: True if cleared successfully, False otherwise
        """
        return self.token_storage.delete_tokens()
    
    def has_saved_tokens(self) -> bool:
        """Check if saved tokens exist in secure storage"""
        return self.token_storage.has_saved_tokens()
    
    def get_token_info(self) -> Dict[str, Union[str, bool, float]]:
        """Get information about current tokens"""
        if not self.tokens:
            return {"authenticated": False}
        
        return {
            "authenticated": True,
            "access_token_preview": self.tokens.access_token[:20] + "..." if self.tokens.access_token else None,
            "expires_at": self.tokens.expires_at,
            "issued_at": self.tokens.issued_at,
            "is_expired": self.tokens.is_expired,
            "needs_refresh": self.tokens.needs_refresh,
            "time_until_expiry": self.tokens.expires_at - time.time() if not self.tokens.is_expired else 0
        }
    
    def get_tokens(self) -> Optional[AuthTokens]:
        """
        Get current authentication tokens
        
        Returns:
            AuthTokens: Current tokens if authenticated, None otherwise
        """
        return self.tokens
    
    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an authenticated HTTP request
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: HTTP response
            
        Raises:
            Exception: If authentication fails
        """
        # Ensure we have valid authentication
        if not self.ensure_valid_authentication():
            raise Exception("Authentication failed - unable to obtain valid tokens")
        
        # Get authenticated headers
        headers = kwargs.pop('headers', {})
        authenticated_headers = self.get_authenticated_headers(headers)
        
        # Make the request
        self.logger.debug(f"Making authenticated {method} request to {url}")
        response = requests.request(method, url, headers=authenticated_headers, **kwargs)
        
        return response


# Convenience function for quick authentication
def create_authenticated_session(username: str = None, password: str = None,
                                auth_token: str = None, refresh_token: str = None,
                                storage_dir: str = None, use_saved_tokens: bool = True) -> AuthManager:
    """
    Create an authenticated session
    
    Args:
        username: Email for automatic login
        password: Password for automatic login
        auth_token: Existing auth token (optional)
        refresh_token: Existing refresh token (optional)
        storage_dir: Directory for secure token storage
        use_saved_tokens: Whether to load/save tokens (default: True)
        
    Returns:
        AuthManager: Configured authentication manager
    """
    return AuthManager(
        username=username,
        password=password,
        auth_token=auth_token,
        refresh_token=refresh_token,
        storage_dir=storage_dir,
        use_saved_tokens=use_saved_tokens
    )
