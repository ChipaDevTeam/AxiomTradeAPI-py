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
                 storage_dir: str = None, use_saved_tokens: bool = True,
                 proxies: Dict[str, str] = None, cf_clearance: str = None,
                 imap_password: str = None, imap_host: str = None):
        """
        Initialize AuthManager

        Args:
            username: Email for automatic login
            password: Password for automatic login
            auth_token: Existing auth token (optional)
            refresh_token: Existing refresh token (optional)
            storage_dir: Directory for secure token storage
            use_saved_tokens: Whether to load saved tokens (default: True)
            proxies: Dictionary mapping protocol to proxy URL
            cf_clearance: Cloudflare clearance cookie (also read from CF_CLEARANCE env var)
            imap_password: Password for IMAP OTP reading. For Gmail with 2FA use an
                           App Password (myaccount.google.com/apppasswords). If omitted,
                           the login password is tried. Also read from AXIOM_IMAP_PASSWORD env var.
            imap_host: IMAP server hostname. Auto-detected from email domain when not set.
                       Also read from AXIOM_IMAP_HOST env var.
        """
        self.username = username
        self.password = password
        self.base_url = "https://axiom.trade"
        self.use_saved_tokens = use_saved_tokens
        self.proxies = proxies
        self.cf_clearance = cf_clearance or os.environ.get("CF_CLEARANCE")
        self.imap_password = imap_password or os.environ.get("AXIOM_IMAP_PASSWORD") or password
        self.imap_host = imap_host or os.environ.get("AXIOM_IMAP_HOST")
        
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
    
    def _parse_jwt_expiry(self, token: str):
        """Extract exp claim from a JWT without verifying signature."""
        try:
            payload = token.split('.')[1]
            payload += '=' * (-len(payload) % 4)
            data = json.loads(base64.b64decode(payload))
            exp = data.get('exp')
            iat = data.get('iat')
            return float(exp) if exp else None, float(iat) if iat else None
        except Exception:
            return None, None

    def _set_tokens(self, auth_token: str, refresh_token: str,
                   expires_in: int = 3600, save_tokens: bool = True) -> None:
        """Set authentication tokens"""
        current_time = time.time()

        # Use the real JWT expiry if present so is_expired reflects actual token lifetime
        jwt_exp, jwt_iat = self._parse_jwt_expiry(auth_token)
        expires_at = jwt_exp if jwt_exp else current_time + expires_in
        issued_at = jwt_iat if jwt_iat else current_time

        self.tokens = AuthTokens(
            access_token=auth_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            issued_at=issued_at,
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
    
    def authenticate(self, otp_callback=None) -> bool:
        """
        Authenticate with username/password.

        Tries nodriver (headless Chrome) first so Cloudflare Turnstile is
        solved automatically inside a real browser. Falls back to the direct
        API flow (which requires a Turnstile token that is no longer obtainable
        without a browser, so it will fail on axiom.trade as of v1.1.5+).

        Args:
            otp_callback: Optional callable that returns the OTP string.
                          Used only in the fallback API path.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.username or not self.password:
            self.logger.error("Username and password required for authentication")
            return False

        try:
            import nodriver  # noqa: F401
            self.logger.info("nodriver available — using browser-based login")
            import asyncio
            return asyncio.run(self._login_with_browser())
        except ImportError:
            self.logger.warning(
                "nodriver not installed — falling back to direct API login "
                "(will fail if Turnstile is required). "
                "Install with: pip install nodriver"
            )

        # --- direct API fallback (Turnstile-blocked on current axiom.trade) ---
        try:
            self.logger.info("Starting Axiom Trade authentication (direct API)...")
            otp_jwt_token = self._login_step1()
            if not otp_jwt_token:
                return False
            otp_code = otp_callback() if otp_callback else input("Enter the OTP code sent to your email: ")
            if not otp_code:
                self.logger.error("OTP code is required")
                return False
            return self._login_step2(otp_jwt_token, otp_code)
        except Exception as e:
            self.logger.error(f"❌ Authentication error: {e}")
            return False

    def _detect_imap_host(self) -> str:
        """Guess the IMAP host from the email domain."""
        if not self.username or '@' not in self.username:
            return 'imap.gmail.com'
        domain = self.username.split('@')[1].lower()
        known = {
            'gmail.com': 'imap.gmail.com',
            'googlemail.com': 'imap.gmail.com',
            'outlook.com': 'outlook.office365.com',
            'hotmail.com': 'outlook.office365.com',
            'live.com': 'outlook.office365.com',
            'yahoo.com': 'imap.mail.yahoo.com',
            'icloud.com': 'imap.mail.me.com',
            'me.com': 'imap.mail.me.com',
            'protonmail.com': 'imap.protonmail.com',
            'proton.me': 'imap.protonmail.com',
        }
        if domain in known:
            return known[domain]
        # Try to detect Hostinger / cPanel-hosted domains by probing imap.hostinger.com
        # then fall back to the generic imap.<domain> pattern
        return 'imap.hostinger.com'

    async def _get_otp_from_imap(self, timeout: int = 60) -> Optional[str]:
        """
        Connect to the user's mailbox via IMAP and wait for the Axiom OTP email.

        Searches unseen messages for a 6-digit code in any email that arrived
        after this method was called, from any sender containing 'axiom'.

        Args:
            timeout: Seconds to wait for the email before giving up.

        Returns:
            The 6-digit OTP string, or None if not found in time.
        """
        import imaplib
        import email as email_lib
        import re
        import asyncio

        host = self.imap_host or self._detect_imap_host()
        imap_pwd = self.imap_password or self.password

        if not imap_pwd:
            self.logger.warning("No IMAP password — cannot auto-read OTP")
            return None

        self.logger.info(f"📬 Connecting to IMAP ({host}) to auto-read OTP...")

        try:
            mail = imaplib.IMAP4_SSL(host)
            mail.login(self.username, imap_pwd)
            mail.select("INBOX")
        except Exception as e:
            self.logger.warning(f"IMAP connection failed: {e}")
            self.logger.warning("Falling back to manual OTP entry")
            return None

        import time
        start = time.time()
        seen_ids: set = set()

        # Snapshot existing unread IDs so we only look at NEW ones
        try:
            _, existing = mail.search(None, 'UNSEEN')
            seen_ids = set(existing[0].split())
        except Exception:
            pass

        try:
            while time.time() - start < timeout:
                await asyncio.sleep(2)
                try:
                    mail.check()  # flush any buffered state
                    _, msgs = mail.search(None, 'UNSEEN')
                    for msg_id in msgs[0].split():
                        if msg_id in seen_ids:
                            continue
                        seen_ids.add(msg_id)

                        _, data = mail.fetch(msg_id, '(RFC822)')
                        msg = email_lib.message_from_bytes(data[0][1])

                        sender = msg.get('From', '').lower()
                        subject = msg.get('Subject', '').lower()

                        if 'axiom' not in sender and 'axiom' not in subject:
                            continue

                        # Extract text body
                        body = ''
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == 'text/plain':
                                    body = part.get_payload(decode=True).decode(errors='replace')
                                    break
                            if not body:
                                for part in msg.walk():
                                    if part.get_content_type() == 'text/html':
                                        body = part.get_payload(decode=True).decode(errors='replace')
                                        break
                        else:
                            body = msg.get_payload(decode=True).decode(errors='replace')

                        # Find 6-digit code (not part of a longer number)
                        match = re.search(r'(?<!\d)(\d{6})(?!\d)', body)
                        if match:
                            otp = match.group(1)
                            self.logger.info(f"✅ OTP found in email: {otp}")
                            return otp

                except Exception as e:
                    self.logger.debug(f"IMAP poll error: {e}")

        finally:
            try:
                mail.close()
                mail.logout()
            except Exception:
                pass

        self.logger.warning("OTP not found in inbox within timeout — falling back to manual entry")
        return None

    async def _login_with_browser(self) -> bool:
        """
        Full automated login flow via nodriver (real Chrome).

        Steps:
          1. Open axiom.trade, click Login button
          2. Auto-fill email + password
          3. Turnstile solves itself inside the real browser
          4. Submit form
          5. Get OTP — auto-reads from IMAP if imap_password is set,
             otherwise prompts for manual terminal input
          6. Submit OTP, extract auth cookies

        Returns:
            bool: True if tokens were successfully extracted.
        """
        import nodriver as uc
        import asyncio

        self.logger.info("🌐 Launching browser for Axiom Trade login...")
        browser = None
        try:
            browser = await uc.start(headless=False)
            tab = await browser.get("https://axiom.trade")

            # ── Wait for page to settle ───────────────────────────────────────
            await asyncio.sleep(5)

            # ── Open login modal ─────────────────────────────────────────────
            self.logger.debug("Opening login modal...")
            opened = await tab.evaluate("""
                (function() {
                    var btns = document.querySelectorAll('button');
                    for (var i = 0; i < btns.length; i++) {
                        if (btns[i].innerText.trim() === 'Login') {
                            btns[i].click(); return true;
                        }
                    }
                    return false;
                })()
            """)
            if not opened:
                self.logger.error("Could not find Login button on axiom.trade")
                return False

            # ── Wait for email input to appear ───────────────────────────────
            email_field = await tab.select('input[placeholder="Enter email"]', timeout=10)
            if not email_field:
                self.logger.error("Login modal did not open — email input not found")
                return False

            await asyncio.sleep(0.5)

            # ── Fill email ───────────────────────────────────────────────────
            await email_field.clear_input()
            await email_field.send_keys(self.username)
            self.logger.debug(f"Email entered: {self.username}")

            # ── Fill password ────────────────────────────────────────────────
            pw_field = await tab.select('input[placeholder="Enter password"]', timeout=5)
            if not pw_field:
                self.logger.error("Password input not found")
                return False
            await pw_field.clear_input()
            await pw_field.send_keys(self.password)
            self.logger.debug("Password entered")

            # ── Give Turnstile time to auto-solve ────────────────────────────
            self.logger.debug("Waiting for Turnstile to solve...")
            await asyncio.sleep(4)

            # ── Submit the form ──────────────────────────────────────────────
            # Click the Login button that's INSIDE the modal (y > 100px from top)
            submitted = await tab.evaluate("""
                (function() {
                    var btns = document.querySelectorAll('button');
                    for (var i = 0; i < btns.length; i++) {
                        var r = btns[i].getBoundingClientRect();
                        if (btns[i].innerText.trim() === 'Login' && r.top > 100) {
                            btns[i].click();
                            return r.top;
                        }
                    }
                    return 0;
                })()
            """)
            if not submitted:
                self.logger.error("Could not find submit button inside login modal")
                return False
            self.logger.info(f"Form submitted (button at y≈{submitted:.0f}) — waiting for OTP screen...")

            # ── OTP step ─────────────────────────────────────────────────────
            # Start IMAP listener concurrently with waiting for the OTP input
            otp_task = None
            if self.imap_password:
                self.logger.info("📬 IMAP configured — will auto-read OTP from your inbox")
                otp_task = asyncio.create_task(self._get_otp_from_imap(timeout=90))

            # Wait for OTP screen to appear — Axiom uses 6 individual maxlength=1 boxes
            otp_input = await tab.select('input[maxlength="1"]', timeout=20)

            # Axiom uses 6 individual single-character inputs for OTP
            otp_boxes = await tab.select_all('input[maxlength="1"]')
            # Filter to only the visible ones (the modal is an overlay on the homepage)
            if not otp_boxes:
                self.logger.warning("OTP screen not detected — may have logged in directly or an error occurred")
                if otp_task:
                    otp_task.cancel()
            else:
                self.logger.info(f"📧 OTP screen detected ({len(otp_boxes)} digit boxes)")

                if otp_task:
                    self.logger.info("⏳ Waiting for OTP email (up to 90s)...")
                    otp_code = await otp_task
                else:
                    otp_code = None

                if not otp_code:
                    self.logger.info("Manual OTP entry required")
                    otp_code = input("Enter the OTP code sent to your email: ").strip()

                if not otp_code or len(otp_code) != 6:
                    self.logger.error(f"Invalid OTP code: '{otp_code}' (expected 6 digits)")
                    return False

                self.logger.info(f"Entering OTP: {otp_code}")
                # Type one digit into each input box
                for i, box in enumerate(otp_boxes[:6]):
                    await box.send_keys(otp_code[i])
                    await asyncio.sleep(0.1)

                self.logger.info("OTP digits entered — waiting for auto-submit or submitting...")
                await asyncio.sleep(2)

                # Some OTP UIs auto-submit when all boxes are filled; if not, click submit
                await tab.evaluate("""
                    (function() {
                        var btns = document.querySelectorAll('button');
                        for (var i = 0; i < btns.length; i++) {
                            var r = btns[i].getBoundingClientRect();
                            if (r.top > 100 && r.width > 0) { btns[i].click(); return; }
                        }
                    })()
                """)
                self.logger.info("OTP submitted — waiting for login to complete...")
                await asyncio.sleep(5)

            # ── Poll for auth cookies ─────────────────────────────────────────
            # Poll up to 15s in case the page is still loading
            access_token = None
            refresh_token = None
            cf_clearance = None

            for _ in range(15):
                cookies = await browser.cookies.get_all()
                for cookie in cookies:
                    name = getattr(cookie, 'name', None) or cookie.get('name', '')
                    value = getattr(cookie, 'value', None) or cookie.get('value', '')
                    if name == 'auth-access-token' and value:
                        access_token = value
                    elif name == 'auth-refresh-token' and value:
                        refresh_token = value
                    elif name == 'cf_clearance' and value:
                        cf_clearance = value

                if access_token and refresh_token:
                    break
                await asyncio.sleep(1)

            if access_token and refresh_token:
                self._set_tokens(access_token, refresh_token)
                if cf_clearance:
                    self.cf_clearance = cf_clearance
                    self.logger.info("✅ cf_clearance cookie captured")
                self.logger.info("✅ Browser login successful — tokens saved")
                return True

            cookies = await browser.cookies.get_all()
            cookie_names = [getattr(c, 'name', None) or c.get('name', '') for c in cookies]
            self.logger.error(
                f"❌ Auth cookies not found after login. "
                f"Cookies present: {[n for n in cookie_names if n]}"
            )
            return False

        except Exception as e:
            self.logger.error(f"❌ Browser login error: {e}", exc_info=True)
            return False
        finally:
            if browser:
                try:
                    browser.stop()
                except Exception:
                    pass
    
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
        from curl_cffi import requests as cffi_requests

        b64_password = self._get_b64_password(self.password)

        url = f'{AAllBaseUrls.BASE_URL_v6}{AxiomTradeApiUrls.LOGIN_STEP1}'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://axiom.trade',
            'referer': 'https://axiom.trade/',
            'sec-ch-ua': '"Google Chrome";v="136", "Chromium";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }

        cookies = {}
        if self.cf_clearance:
            cookies['cf_clearance'] = self.cf_clearance

        data = {
            "email": self.username,
            "b64Password": b64_password
        }

        try:
            self.logger.debug(f"Sending login step 1 request for email: {self.username}")
            response = cffi_requests.post(
                url, headers=headers, json=data, cookies=cookies,
                timeout=30, impersonate="chrome136"
            )

            self.logger.debug(f"Login step 1 status: {response.status_code}")
            if response.status_code == 200:
                otp_token = response.cookies.get('auth-otp-login-token')
                if otp_token:
                    self.logger.debug("OTP JWT token received successfully")
                    return otp_token
                else:
                    self.logger.error(f"auth-otp-login-token not found in cookies! Response: {response.text[:300]}")
                    return None
            else:
                self.logger.error(f"Login step 1 failed: {response.status_code} - {response.text[:300]}")
                return None

        except Exception as e:
            self.logger.error(f"Login step 1 error: {e}")
            return None
    
    def _login_step2(self, otp_jwt_token: str, otp_code: str) -> bool:
        """Second step of login - send OTP code to complete authentication"""
        from axiomtradeapi.urls import AAllBaseUrls, AxiomTradeApiUrls
        from curl_cffi import requests as cffi_requests

        b64_password = self._get_b64_password(self.password)

        url = f'{AAllBaseUrls.BASE_URL_v3}{AxiomTradeApiUrls.LOGIN_STEP2}'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://axiom.trade',
            'referer': 'https://axiom.trade/',
            'sec-ch-ua': '"Google Chrome";v="136", "Chromium";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }

        cookies = {'auth-otp-login-token': otp_jwt_token}
        if self.cf_clearance:
            cookies['cf_clearance'] = self.cf_clearance

        data = {
            "code": otp_code,
            "email": self.username,
            "b64Password": b64_password
        }

        try:
            self.logger.debug("Sending login step 2 request with OTP code")
            response = cffi_requests.post(
                url, headers=headers, json=data, cookies=cookies,
                timeout=30, impersonate="chrome136"
            )

            self.logger.debug(f"Login step 2 status: {response.status_code}")
            if response.status_code == 200:
                auth_token = response.cookies.get('auth-access-token')
                refresh_token = response.cookies.get('auth-refresh-token')

                if auth_token and refresh_token:
                    self._set_tokens(auth_token, refresh_token)
                    self.logger.info("✅ Authentication successful!")
                    return True

                # Fallback: check response body
                try:
                    response_data = response.json()
                    auth_token = response_data.get('accessToken') or response_data.get('auth-access-token')
                    refresh_token = response_data.get('refreshToken') or response_data.get('auth-refresh-token')
                    if auth_token and refresh_token:
                        self._set_tokens(auth_token, refresh_token)
                        self.logger.info("✅ Authentication successful!")
                        return True
                except Exception:
                    pass

                self.logger.error(f"❌ No authentication tokens found in response: {response.text[:300]}")
                return False
            else:
                self.logger.error(f"❌ Login step 2 failed: {response.status_code} - {response.text[:300]}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Login step 2 error: {e}")
            return False
    
    def refresh_tokens(self) -> bool:
        """
        Refresh authentication tokens using Chrome TLS impersonation (curl_cffi) to pass Cloudflare.

        Returns:
            bool: True if refresh successful, False otherwise
        """
        if not self.tokens or not self.tokens.refresh_token:
            self.logger.error("No refresh token available")
            return False

        cookies = {
            'auth-refresh-token': self.tokens.refresh_token,
            'auth-access-token': self.tokens.access_token,
        }
        if self.cf_clearance:
            cookies['cf_clearance'] = self.cf_clearance

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en,es-CL;q=0.9,es-419;q=0.8,es;q=0.7,fr;q=0.6',
            'content-length': '0',
            'origin': 'https://axiom.trade',
            'priority': 'u=1, i',
            'referer': 'https://axiom.trade/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }

        try:
            self.logger.info("Refreshing authentication tokens...")
            from curl_cffi import requests as cffi_requests
            response = cffi_requests.post(
                'https://api.axiom.trade/refresh-access-token',
                headers=headers,
                cookies=cookies,
                timeout=30,
                impersonate="chrome136",
            )
        except ImportError:
            self.logger.warning("curl_cffi not available, falling back to requests for token refresh")
            response = requests.post(
                'https://api.axiom.trade/refresh-access-token',
                headers=headers,
                cookies=cookies,
                timeout=30,
                proxies=self.proxies,
            )
        except Exception as e:
            self.logger.error(f"❌ Token refresh request failed: {e}")
            return False

        try:
            if response.status_code == 200:
                new_auth_token = response.cookies.get('auth-access-token')
                new_refresh_token = response.cookies.get('auth-refresh-token')

                if new_auth_token:
                    self._set_tokens(new_auth_token, new_refresh_token or self.tokens.refresh_token)
                    self.logger.info("✅ Tokens refreshed successfully!")
                    return True

                try:
                    data = response.json()
                    new_auth_token = data.get('accessToken') or data.get('auth-access-token') or data.get('access_token')
                    new_refresh_token = data.get('refreshToken') or data.get('auth-refresh-token') or data.get('refresh_token')
                    if new_auth_token:
                        self._set_tokens(new_auth_token, new_refresh_token or self.tokens.refresh_token)
                        self.logger.info("✅ Tokens refreshed successfully!")
                        return True
                except Exception:
                    pass

                self.logger.error("❌ No new access token in refresh response")
                return False
            else:
                self.logger.error(f"❌ Token refresh failed: {response.status_code} - {response.text}")
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
        
        # Add proxies if configured
        if self.proxies and 'proxies' not in kwargs:
            kwargs['proxies'] = self.proxies
            
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
