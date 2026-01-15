# Authentication Attributes Guide

## Table of Contents
- [Overview](#overview)
- [access_token](#access_token)
- [auth](#auth)
- [auth_manager](#auth_manager)
- [Quick Start](#quick-start)
- [Detailed Examples](#detailed-examples)
- [Best Practices](#best-practices)
- [Security Guidelines](#security-guidelines)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Axiom Trade API client provides three core authentication attributes that work together to manage your API access:

| Attribute | Type | Description |
|-----------|------|-------------|
| `access_token` | `str` (property) | Current JWT access token for API requests |
| `auth` | `AuthManager` | Legacy alias for `auth_manager` (backward compatibility) |
| `auth_manager` | `AuthManager` | Complete authentication manager with auto-refresh |

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    AxiomTradeClient                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  access_token ─────► Read-only property                    │
│       │              Returns current token                  │
│       │                                                     │
│  auth ─────────────► Legacy alias                          │
│       │              Points to auth_manager                 │
│       │                                                     │
│  auth_manager ─────► Full authentication system            │
│       │              ├─ Token storage                       │
│       │              ├─ Auto-refresh                        │
│       │              ├─ Session management                  │
│       │              └─ Secure encryption                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## access_token

### Description

`access_token` is a **read-only property** that returns the current JWT (JSON Web Token) used to authenticate API requests. This token is automatically managed by the `auth_manager` and should not be modified directly.

### Type
```python
@property
def access_token(self) -> Optional[str]
```

Returns: `str` if authenticated, `None` if not authenticated

### Token Format

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoZW50aWNhdGVkVXNlcklkIjoiYTFkMGIzMjMt...
```

Access tokens are JWT tokens that typically:
- Are **short-lived** (expire after ~15-60 minutes)
- Contain your **user identity** and **permissions**
- Are automatically **refreshed** when expired
- Should be kept **secure** and never shared

### Basic Usage

#### Example 1: Check Current Token

```python
from axiomtradeapi import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# Login to get token
client.login("your_email@example.com", "your_password")

# Access the token (read-only)
current_token = client.access_token

if current_token:
    print(f"✅ Authenticated with token: {current_token[:50]}...")
    print(f"   Token length: {len(current_token)} characters")
else:
    print("❌ Not authenticated")
```

**Output:**
```
✅ Authenticated with token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRo...
   Token length: 234 characters
```

#### Example 2: Verify Authentication Status

```python
from axiomtradeapi import AxiomTradeClient

def check_authentication_status():
    """Check if client is authenticated"""
    client = AxiomTradeClient()
    
    if client.access_token is None:
        print("🔒 Not authenticated - please login")
        return False
    else:
        print(f"🔓 Authenticated")
        print(f"   Token starts with: {client.access_token[:20]}...")
        return True

# Usage
is_authenticated = check_authentication_status()
```

#### Example 3: Using Token in Custom Requests

```python
from axiomtradeapi import AxiomTradeClient
import requests

client = AxiomTradeClient()
client.login("email@example.com", "password")

# Get current token
token = client.access_token

if token:
    # Use token in custom API request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Make custom request
    response = requests.get(
        'https://axiom.trade/api/some-endpoint',
        headers=headers
    )
    
    print(f"Response: {response.status_code}")
else:
    print("No token available")
```

### Important Notes

⚠️ **Read-Only:** You cannot set `access_token` directly. Use `set_tokens()` method instead.

```python
# ❌ WRONG - This will fail
client.access_token = "new_token"  # AttributeError

# ✅ CORRECT - Use set_tokens() method
client.set_tokens(
    access_token="your_access_token",
    refresh_token="your_refresh_token"
)
```

⚠️ **Automatic Refresh:** The token is automatically refreshed when it expires. You don't need to manually refresh it in most cases.

⚠️ **Security:** Never log or expose the full token in production code. Only log partial tokens for debugging.

```python
# ✅ SAFE - Only show first 20 characters
print(f"Token: {client.access_token[:20]}...")

# ❌ UNSAFE - Exposes full token
print(f"Token: {client.access_token}")  # Don't do this in production!
```

---

## auth

### Description

`auth` is a **legacy attribute** that provides backward compatibility with older versions of the library. It's simply an alias for `auth_manager`.

### Type
```python
auth: AuthManager  # Alias for auth_manager
```

### Usage

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Both of these are identical:
auth_manager_1 = client.auth          # Legacy way
auth_manager_2 = client.auth_manager  # Modern way

# They point to the same object
assert auth_manager_1 is auth_manager_2  # True
```

### When to Use

Use `auth_manager` for new code. The `auth` attribute is maintained only for backward compatibility with existing projects.

```python
# ✅ RECOMMENDED (Modern)
client.auth_manager.ensure_valid_authentication()

# ⚠️ LEGACY (Still works, but deprecated)
client.auth.ensure_valid_authentication()
```

---

## auth_manager

### Description

`auth_manager` is the complete authentication management system. It handles:
- 🔐 **Login and logout**
- 🔄 **Automatic token refresh**
- 💾 **Secure token storage**
- 🔒 **Token encryption**
- ⏰ **Expiration tracking**
- 🍪 **Cookie management**

### Type
```python
auth_manager: AuthManager
```

### Core Methods

| Method | Description |
|--------|-------------|
| `authenticate()` | Perform full authentication (login) |
| `ensure_valid_authentication()` | Check and refresh token if needed |
| `make_authenticated_request()` | Make API request with auth headers |
| `refresh_tokens()` | Manually refresh tokens |
| `logout()` | Clear authentication and delete saved tokens |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `tokens` | `AuthTokens` | Current token object with metadata |
| `username` | `str` | Current username/email |
| `password` | `str` | Current password (stored securely) |
| `cookie_manager` | `CookieManager` | Cookie management system |
| `token_storage` | `SecureTokenStorage` | Encrypted token storage |

---

## Quick Start

### Method 1: Login with Credentials

```python
from axiomtradeapi import AxiomTradeClient

# Initialize with credentials
client = AxiomTradeClient(
    username="your_email@example.com",
    password="your_password"
)

# Login automatically happens on first API call
balance = client.GetBalance("wallet_address")

# Or manually trigger login
client.login()
```

### Method 2: Use Existing Tokens

```python
from axiomtradeapi import AxiomTradeClient
import os

# Load tokens from environment variables
access_token = os.getenv('AXIOM_ACCESS_TOKEN')
refresh_token = os.getenv('AXIOM_REFRESH_TOKEN')

# Initialize with tokens
client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token
)

# Check token
print(f"Token: {client.access_token[:20]}...")
```

### Method 3: Automatic Token Storage

```python
from axiomtradeapi import AxiomTradeClient

# First time - login and save tokens
client = AxiomTradeClient(
    username="email@example.com",
    password="password",
    use_saved_tokens=True  # Enable automatic storage (default)
)
client.login()

# Later - tokens automatically loaded
client2 = AxiomTradeClient(use_saved_tokens=True)
# No login needed! Tokens loaded from secure storage

print(f"Auto-loaded token: {client2.access_token[:20]}...")
```

---

## Detailed Examples

### Example 1: Manual Token Management

```python
from axiomtradeapi import AxiomTradeClient

def manual_token_workflow():
    """Demonstrate manual token management"""
    client = AxiomTradeClient()
    
    # 1. Login and get tokens
    print("🔐 Logging in...")
    result = client.login("email@example.com", "password")
    
    if result['success']:
        print("✅ Login successful!")
        
        # 2. Access token through property
        access = client.access_token
        refresh = client.refresh_token
        
        print(f"   Access Token:  {access[:30]}...")
        print(f"   Refresh Token: {refresh[:30]}...")
        
        # 3. Save tokens for later use
        import os
        os.environ['SAVED_ACCESS'] = access
        os.environ['SAVED_REFRESH'] = refresh
        print("💾 Tokens saved to environment")
        
        # 4. Later - load tokens
        print("\n🔄 Simulating new session...")
        client2 = AxiomTradeClient()
        client2.set_tokens(
            access_token=os.environ['SAVED_ACCESS'],
            refresh_token=os.environ['SAVED_REFRESH']
        )
        
        print(f"✅ Tokens restored: {client2.access_token[:30]}...")
        
    else:
        print("❌ Login failed")

manual_token_workflow()
```

### Example 2: Check Token Expiration

```python
from axiomtradeapi import AxiomTradeClient
from datetime import datetime

def check_token_status():
    """Check authentication token status"""
    client = AxiomTradeClient()
    client.login("email@example.com", "password")
    
    # Access token info through auth_manager
    if client.auth_manager.tokens:
        tokens = client.auth_manager.tokens
        
        print("🔑 Token Status:")
        print(f"   Access Token:  {client.access_token[:30]}...")
        print(f"   Refresh Token: {client.refresh_token[:30]}...")
        
        # Check expiration
        expires_at = datetime.fromtimestamp(tokens.expires_at)
        issued_at = datetime.fromtimestamp(tokens.issued_at)
        now = datetime.now()
        
        time_left = (expires_at - now).total_seconds()
        
        print(f"\n⏰ Timing:")
        print(f"   Issued:  {issued_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Time Left: {int(time_left / 60)} minutes")
        
        # Check status
        if tokens.is_expired:
            print("   Status: ⚠️  EXPIRED")
        elif tokens.needs_refresh:
            print("   Status: 🔄 NEEDS REFRESH")
        else:
            print("   Status: ✅ VALID")
    else:
        print("❌ No tokens available")

check_token_status()
```

**Output:**
```
🔑 Token Status:
   Access Token:  eyJhbGciOiJIUzI1NiIsInR5cCI...
   Refresh Token: eyJhbGciOiJIUzI1NiIsInR5cCI...

⏰ Timing:
   Issued:  2026-01-14 15:30:00
   Expires: 2026-01-14 15:46:00
   Time Left: 14 minutes
   Status: ✅ VALID
```

### Example 3: Automatic Token Refresh

```python
from axiomtradeapi import AxiomTradeClient
import time

def demonstrate_auto_refresh():
    """Show automatic token refresh in action"""
    client = AxiomTradeClient()
    client.login("email@example.com", "password")
    
    print("🔄 Token Auto-Refresh Demo")
    print("=" * 60)
    
    for i in range(3):
        print(f"\nCheck #{i+1}:")
        
        # Check if authentication is valid
        if client.auth_manager.ensure_valid_authentication():
            current_token = client.access_token
            print(f"✅ Valid token: {current_token[:30]}...")
            
            # Check token status
            tokens = client.auth_manager.tokens
            if tokens.needs_refresh:
                print("🔄 Token will be refreshed soon")
            else:
                print("✅ Token is fresh")
        else:
            print("❌ Authentication failed")
        
        # Wait before next check
        if i < 2:
            print("⏳ Waiting 5 seconds...")
            time.sleep(5)
    
    print("\n✅ Auto-refresh handled automatically!")

demonstrate_auto_refresh()
```

### Example 4: Secure Token Storage

```python
from axiomtradeapi import AxiomTradeClient
from pathlib import Path

def demonstrate_secure_storage():
    """Show secure token storage features"""
    
    # Session 1: Login and save
    print("📝 Session 1: Login and Save Tokens")
    print("=" * 60)
    
    client1 = AxiomTradeClient(
        username="email@example.com",
        password="password",
        use_saved_tokens=True,
        storage_dir="~/.my_trading_bot"  # Custom storage location
    )
    client1.login()
    
    print(f"✅ Logged in with token: {client1.access_token[:30]}...")
    print(f"💾 Tokens saved to: ~/.my_trading_bot/")
    
    # Session 2: Load saved tokens
    print("\n📖 Session 2: Load Saved Tokens")
    print("=" * 60)
    
    client2 = AxiomTradeClient(
        use_saved_tokens=True,
        storage_dir="~/.my_trading_bot"
    )
    
    # Check if tokens loaded
    if client2.access_token:
        print(f"✅ Tokens loaded: {client2.access_token[:30]}...")
        print("🎉 No login required!")
    else:
        print("❌ No saved tokens found")
    
    # Check storage location
    storage_path = Path.home() / ".my_trading_bot"
    if storage_path.exists():
        print(f"\n📂 Storage Files:")
        for file in storage_path.iterdir():
            print(f"   - {file.name}")

demonstrate_secure_storage()
```

**Output:**
```
📝 Session 1: Login and Save Tokens
============================================================
✅ Logged in with token: eyJhbGciOiJIUzI1NiIsInR5cCI...
💾 Tokens saved to: ~/.my_trading_bot/

📖 Session 2: Load Saved Tokens
============================================================
✅ Tokens loaded: eyJhbGciOiJIUzI1NiIsInR5cCI...
🎉 No login required!

📂 Storage Files:
   - tokens.enc
   - key.enc
```

### Example 5: Advanced Authentication Manager Usage

```python
from axiomtradeapi import AxiomTradeClient

class AuthMonitor:
    """Monitor and manage authentication"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
    
    def login_with_retry(self, email: str, password: str, max_attempts: int = 3):
        """Login with retry logic"""
        for attempt in range(max_attempts):
            try:
                print(f"🔐 Login attempt {attempt + 1}/{max_attempts}")
                
                result = self.client.login(email, password)
                
                if result['success']:
                    print("✅ Login successful!")
                    return True
                else:
                    print(f"❌ Login failed: {result.get('message', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            if attempt < max_attempts - 1:
                print("⏳ Retrying in 2 seconds...")
                import time
                time.sleep(2)
        
        return False
    
    def get_auth_info(self):
        """Get detailed authentication information"""
        info = {
            'is_authenticated': self.client.access_token is not None,
            'has_saved_tokens': self.client.auth_manager.token_storage.has_saved_tokens(),
            'username': self.client.auth_manager.username,
            'access_token': self.client.access_token[:30] + "..." if self.client.access_token else None,
            'refresh_token': self.client.refresh_token[:30] + "..." if self.client.refresh_token else None
        }
        
        if self.client.auth_manager.tokens:
            tokens = self.client.auth_manager.tokens
            info['is_expired'] = tokens.is_expired
            info['needs_refresh'] = tokens.needs_refresh
        
        return info
    
    def print_auth_report(self):
        """Print authentication status report"""
        info = self.get_auth_info()
        
        print("\n📊 Authentication Report")
        print("=" * 60)
        print(f"🔐 Authenticated:    {info['is_authenticated']}")
        print(f"💾 Saved Tokens:     {info['has_saved_tokens']}")
        print(f"👤 Username:         {info['username']}")
        
        if info['access_token']:
            print(f"🔑 Access Token:     {info['access_token']}")
            print(f"🔄 Refresh Token:    {info['refresh_token']}")
            
            if 'is_expired' in info:
                print(f"⏰ Is Expired:       {info['is_expired']}")
                print(f"🔄 Needs Refresh:    {info['needs_refresh']}")
        else:
            print("❌ No active tokens")
        
        print("=" * 60)

# Usage
monitor = AuthMonitor()

# Login with retry
if monitor.login_with_retry("email@example.com", "password"):
    # Show auth report
    monitor.print_auth_report()
```

### Example 6: Making Custom Authenticated Requests

```python
from axiomtradeapi import AxiomTradeClient

def custom_api_call_example():
    """Demonstrate using auth_manager for custom API calls"""
    client = AxiomTradeClient()
    client.login("email@example.com", "password")
    
    # Method 1: Using auth_manager.make_authenticated_request()
    print("🌐 Method 1: Using auth_manager")
    
    response = client.auth_manager.make_authenticated_request(
        method='GET',
        url='https://axiom.trade/api/some-endpoint',
        params={'key': 'value'}
    )
    
    if response.status_code == 200:
        print(f"✅ Response: {response.json()}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    # Method 2: Manual request with token
    print("\n🌐 Method 2: Manual request")
    
    import requests
    
    headers = {
        'Authorization': f'Bearer {client.access_token}',
        'Content-Type': 'application/json',
        'Cookie': client.auth_manager.cookie_manager.get_cookie_header()
    }
    
    response = requests.post(
        'https://axiom.trade/api/another-endpoint',
        headers=headers,
        json={'data': 'example'}
    )
    
    print(f"Response: {response.status_code}")

custom_api_call_example()
```

### Example 7: Token Lifecycle Management

```python
from axiomtradeapi import AxiomTradeClient

class TokenLifecycleManager:
    """Manage complete token lifecycle"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
    
    def login(self, email: str, password: str):
        """Login and get initial tokens"""
        print("1️⃣  Login Phase")
        result = self.client.login(email, password)
        
        if result['success']:
            print(f"   ✅ Access token acquired")
            print(f"   ✅ Refresh token acquired")
            return True
        return False
    
    def use_tokens(self):
        """Use tokens for API calls"""
        print("\n2️⃣  Usage Phase")
        
        # The client automatically ensures tokens are valid
        balance = self.client.GetBalance("some_wallet_address")
        
        if balance:
            print(f"   ✅ API call successful (token valid)")
        else:
            print(f"   ❌ API call failed")
    
    def refresh_if_needed(self):
        """Check and refresh tokens if needed"""
        print("\n3️⃣  Refresh Phase")
        
        tokens = self.client.auth_manager.tokens
        
        if tokens:
            if tokens.needs_refresh:
                print("   🔄 Token needs refresh...")
                if self.client.auth_manager.refresh_tokens():
                    print("   ✅ Tokens refreshed")
                else:
                    print("   ❌ Refresh failed")
            else:
                print("   ✅ Tokens still valid, no refresh needed")
        else:
            print("   ❌ No tokens available")
    
    def logout(self):
        """Clean logout and token removal"""
        print("\n4️⃣  Logout Phase")
        
        self.client.auth_manager.logout()
        
        # Verify tokens are cleared
        if self.client.access_token is None:
            print("   ✅ Tokens cleared")
            print("   ✅ Saved tokens deleted")
        else:
            print("   ⚠️  Tokens may still be present")
    
    def run_full_lifecycle(self, email: str, password: str):
        """Run complete token lifecycle"""
        print("🔄 Token Lifecycle Demonstration")
        print("=" * 60)
        
        if self.login(email, password):
            self.use_tokens()
            self.refresh_if_needed()
            self.logout()
            print("\n✅ Complete lifecycle executed!")
        else:
            print("\n❌ Login failed, lifecycle aborted")

# Usage
manager = TokenLifecycleManager()
manager.run_full_lifecycle("email@example.com", "password")
```

---

## Best Practices

### 1. Use Environment Variables for Credentials

```python
from axiomtradeapi import AxiomTradeClient
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# ✅ GOOD - Credentials from environment
client = AxiomTradeClient(
    username=os.getenv('AXIOM_EMAIL'),
    password=os.getenv('AXIOM_PASSWORD')
)

# ❌ BAD - Hardcoded credentials
client = AxiomTradeClient(
    username="myemail@example.com",
    password="mypassword123"
)
```

### 2. Enable Automatic Token Storage

```python
# ✅ GOOD - Automatic token management
client = AxiomTradeClient(use_saved_tokens=True)  # Default behavior

# Only login once, tokens saved for future use
client.login(email, password)

# Later sessions automatically load tokens
client2 = AxiomTradeClient()  # No login needed!
```

### 3. Check Authentication Before Critical Operations

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

def safe_trade(amount: float):
    """Perform trade with authentication check"""
    
    # Always verify authentication
    if not client.auth_manager.ensure_valid_authentication():
        print("❌ Not authenticated - cannot trade")
        return False
    
    # Verify token is not expired
    if client.access_token is None:
        print("❌ No valid token - cannot trade")
        return False
    
    # Now safe to execute trade
    print(f"✅ Executing trade: {amount} SOL")
    # ... trade logic here ...
    return True

safe_trade(1.5)
```

### 4. Handle Token Refresh Gracefully

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()
client.login(email, password)

def api_call_with_retry():
    """Make API call with automatic retry on token expiration"""
    max_retries = 2
    
    for attempt in range(max_retries):
        try:
            # Ensure token is valid before request
            client.auth_manager.ensure_valid_authentication()
            
            # Make API call
            result = client.GetBalance("wallet_address")
            
            if result:
                return result
                
        except Exception as e:
            if "401" in str(e) or "Unauthorized" in str(e):
                print(f"⚠️  Token expired, refreshing... (attempt {attempt+1})")
                client.auth_manager.refresh_tokens()
            else:
                raise
    
    return None
```

### 5. Secure Token Logging

```python
from axiomtradeapi import AxiomTradeClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = AxiomTradeClient()
client.login(email, password)

def safe_log_token():
    """Safely log token information"""
    
    token = client.access_token
    
    if token:
        # ✅ SAFE - Only log partial token
        logger.info(f"Token (partial): {token[:20]}... (length: {len(token)})")
        
        # ❌ UNSAFE - Full token in logs
        # logger.info(f"Token: {token}")  # Never do this!
    else:
        logger.warning("No token available")

safe_log_token()
```

---

## Security Guidelines

### 🔒 DO:

✅ **Store tokens securely**
```python
# Use encrypted storage (automatic)
client = AxiomTradeClient(use_saved_tokens=True)
```

✅ **Use environment variables**
```python
import os
access_token = os.getenv('AXIOM_ACCESS_TOKEN')
```

✅ **Rotate tokens regularly**
```python
# Tokens auto-refresh, but you can manually trigger
client.auth_manager.refresh_tokens()
```

✅ **Clear tokens on logout**
```python
client.auth_manager.logout()  # Clears tokens and deletes saved files
```

✅ **Validate tokens before use**
```python
if client.auth_manager.ensure_valid_authentication():
    # Safe to proceed
    pass
```

### ⛔ DON'T:

❌ **Never commit tokens to version control**
```bash
# Add to .gitignore
.env
tokens.enc
key.enc
*.token
```

❌ **Don't share tokens**
```python
# ❌ BAD
print(f"My token: {client.access_token}")  # Don't share

# ✅ GOOD
print(f"Token: {client.access_token[:20]}...")  # Partial only
```

❌ **Don't hardcode tokens**
```python
# ❌ BAD
client.set_tokens(
    access_token="eyJhbGciOiJIUzI1NiIsInR5cCI...",
    refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI..."
)

# ✅ GOOD
client.set_tokens(
    access_token=os.getenv('AXIOM_ACCESS_TOKEN'),
    refresh_token=os.getenv('AXIOM_REFRESH_TOKEN')
)
```

❌ **Don't use expired tokens**
```python
# ❌ BAD
if client.access_token:
    make_request()  # May be expired!

# ✅ GOOD
if client.auth_manager.ensure_valid_authentication():
    make_request()  # Guaranteed valid
```

---

## Troubleshooting

### Issue 1: "access_token is None"

**Cause:** Client not authenticated

**Solution:**
```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Check authentication
if client.access_token is None:
    print("Not authenticated, logging in...")
    client.login("email@example.com", "password")
else:
    print("Already authenticated!")
```

### Issue 2: "Token expired" errors

**Cause:** Token expired and auto-refresh failed

**Solution:**
```python
# Force token validation
if not client.auth_manager.ensure_valid_authentication():
    print("Re-authenticating...")
    client.login()
```

### Issue 3: "Cannot modify access_token"

**Cause:** Trying to set read-only property

**Solution:**
```python
# ❌ WRONG
client.access_token = "new_token"

# ✅ CORRECT
client.set_tokens(
    access_token="new_token",
    refresh_token="new_refresh"
)
```

### Issue 4: Tokens not persisting between sessions

**Cause:** Token storage disabled

**Solution:**
```python
# Enable automatic storage
client = AxiomTradeClient(
    use_saved_tokens=True  # Make sure this is True
)

# Verify storage
if client.auth_manager.token_storage.has_saved_tokens():
    print("✅ Token storage working")
else:
    print("❌ No tokens saved")
```

### Issue 5: "401 Unauthorized" on requests

**Cause:** Token invalid or authentication failed

**Solution:**
```python
from axiomtradeapi import AxiomTradeClient

def diagnose_auth_issue():
    client = AxiomTradeClient()
    
    print("🔍 Diagnosing authentication...")
    
    # Check 1: Token exists
    if client.access_token is None:
        print("❌ No token - need to login")
        return
    
    # Check 2: Token format
    token = client.access_token
    if not token.startswith('eyJ'):
        print("❌ Invalid token format")
        return
    
    # Check 3: Token expiration
    tokens = client.auth_manager.tokens
    if tokens and tokens.is_expired:
        print("❌ Token expired - refreshing...")
        client.auth_manager.refresh_tokens()
        return
    
    # Check 4: Try a test request
    try:
        balance = client.GetBalance("test_wallet")
        print("✅ Authentication working!")
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

diagnose_auth_issue()
```

---

## Summary

### Key Takeaways

| Attribute | Use Case | Example |
|-----------|----------|---------|
| `access_token` | Check current token | `if client.access_token: ...` |
| `auth` | Legacy code compatibility | `client.auth.refresh_tokens()` |
| `auth_manager` | Full authentication control | `client.auth_manager.ensure_valid_authentication()` |

### Quick Reference

```python
from axiomtradeapi import AxiomTradeClient

# Initialize
client = AxiomTradeClient()

# Login
client.login("email@example.com", "password")

# Check token
token = client.access_token  # Read-only property

# Use auth_manager for advanced features
client.auth_manager.ensure_valid_authentication()
client.auth_manager.refresh_tokens()
client.auth_manager.logout()

# Set tokens directly
client.set_tokens(access_token="...", refresh_token="...")
```

### Related Documentation

- [GetBalance Guide](./getbalance-guide.md)
- [Authentication Guide](./authentication.md)
- [API Reference](./api-reference.md)

---

**Last Updated:** January 14, 2026  
**Package Version:** 1.0.5+  
**Documentation Version:** 1.0
