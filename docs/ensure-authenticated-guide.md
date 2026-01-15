# ensure_authenticated() Method - Comprehensive Guide

## Overview

The `ensure_authenticated()` method is an intelligent authentication guard that automatically ensures you have valid authentication tokens before making API requests. It handles token validation, automatic refresh, and re-authentication seamlessly, providing a robust authentication layer for your application.

This method is the **recommended way** to verify authentication status before performing API operations, as it handles the complete authentication lifecycle automatically.

## Method Signature

```python
def ensure_authenticated(self) -> bool
```

## Parameters

**None** - This method takes no parameters.

## Return Value

Returns a boolean indicating authentication status:

- **`True`**: Valid authentication is available (tokens are valid or were successfully refreshed/renewed)
- **`False`**: Authentication failed (no tokens, refresh failed, and no credentials available for re-authentication)

## How It Works

### Authentication Flow

```
ensure_authenticated() called
         ↓
    Has tokens?
         ↓
    Yes ────────→ Tokens valid?
    No              ↓
    ↓          Yes ────→ Return True
    ↓          No
    ↓           ↓
    ↓      Try refresh
    ↓           ↓
    ↓      Refresh success? ──Yes──→ Return True
    ↓           ↓
    ↓          No
    ↓           ↓
    └──→ Have credentials?
              ↓
         Yes ────→ Re-authenticate ──→ Return True/False
              ↓
             No
              ↓
         Return False
```

### Internal Logic

1. **Check if tokens exist**
   - If no tokens: Try to authenticate with stored credentials
   - If no credentials: Return `False`

2. **Check if tokens are valid**
   - If tokens not expired: Return `True`
   - If tokens expired: Proceed to step 3

3. **Try to refresh tokens**
   - If refresh successful: Return `True`
   - If refresh failed: Proceed to step 4

4. **Try to re-authenticate**
   - If credentials available: Re-authenticate
   - If no credentials: Return `False`

## Prerequisites

```python
from axiomtradeapi.client import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# Provide authentication (one of these):
# Option 1: Login with credentials
client.login("username", "password")

# Option 2: Initialize with credentials (auto-login)
client = AxiomTradeClient(username="user", password="pass")

# Option 3: Set tokens manually
client.set_tokens("access_token", "refresh_token")
```

---

## Basic Usage Examples

### Example 1: Simple Authentication Check
Check if authenticated before making API calls.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

# Login
client.login("username", "password")

# Verify authentication
if client.ensure_authenticated():
    print("✅ Authenticated - safe to make API calls")
    balance = client.GetBalance()
    print(f"Balance: {balance['sol']} SOL")
else:
    print("❌ Not authenticated - please login")
```

**Output:**
```
✅ Authenticated - safe to make API calls
Balance: 5.42 SOL
```

### Example 2: Automatic Re-authentication
`ensure_authenticated()` automatically handles expired tokens.

```python
from axiomtradeapi.client import AxiomTradeClient
import time

# Initialize with credentials for auto re-authentication
client = AxiomTradeClient(username="user", password="pass")

# First call - tokens are valid
if client.ensure_authenticated():
    print("✅ First check: Authenticated")

# Simulate time passing (tokens might expire)
# In reality, tokens expire after ~1 hour
time.sleep(2)

# Second call - will auto-refresh if needed
if client.ensure_authenticated():
    print("✅ Second check: Still authenticated")
    print("   (Tokens were automatically refreshed if needed)")
else:
    print("❌ Authentication failed")
```

**Output:**
```
✅ First check: Authenticated
✅ Second check: Still authenticated
   (Tokens were automatically refreshed if needed)
```

### Example 3: Guard API Calls
Use as a guard before every API operation.

```python
from axiomtradeapi.client import AxiomTradeClient

def get_balance_safely(client):
    """
    Safely get balance with authentication check
    """
    if not client.ensure_authenticated():
        return {"error": "Authentication required"}
    
    try:
        return client.GetBalance()
    except Exception as e:
        return {"error": str(e)}

# Usage
client = AxiomTradeClient()
client.login("username", "password")

balance = get_balance_safely(client)
if "error" in balance:
    print(f"❌ Error: {balance['error']}")
else:
    print(f"✅ Balance: {balance['sol']} SOL")
```

**Output:**
```
✅ Balance: 5.42 SOL
```

---

## Advanced Examples

### Example 4: Automatic Re-authentication Wrapper
Create a wrapper that automatically ensures authentication before any API call.

```python
from axiomtradeapi.client import AxiomTradeClient
from functools import wraps
from typing import Callable, Any

def require_authentication(func: Callable) -> Callable:
    """
    Decorator that ensures authentication before calling API methods
    
    Usage:
        @require_authentication
        def my_api_call(client):
            return client.GetBalance()
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Assume first argument is the client
        if len(args) > 0 and hasattr(args[0], 'ensure_authenticated'):
            client = args[0]
            
            if not client.ensure_authenticated():
                raise ValueError("Authentication failed. Please login first.")
        
        return func(*args, **kwargs)
    
    return wrapper

class AuthenticatedClient(AxiomTradeClient):
    """Client with automatic authentication checking"""
    
    @require_authentication
    def GetBalance(self):
        """Get balance with automatic auth check"""
        return super().GetBalance()
    
    @require_authentication
    def get_trending_tokens(self, time_period: str = '1h'):
        """Get trending tokens with automatic auth check"""
        return super().get_trending_tokens(time_period)

# Usage
client = AuthenticatedClient(username="user", password="pass")

# These will automatically ensure authentication
try:
    balance = client.GetBalance()
    print(f"✅ Balance: {balance['sol']} SOL")
    
    trending = client.get_trending_tokens()
    print(f"✅ Found {len(trending)} trending tokens")
except ValueError as e:
    print(f"❌ {e}")
```

**Output:**
```
✅ Balance: 5.42 SOL
✅ Found 12 trending tokens
```

### Example 5: Session Management with Health Checks
Regularly verify authentication status for long-running applications.

```python
from axiomtradeapi.client import AxiomTradeClient
import time
from datetime import datetime

class SessionManager:
    """Manage authentication session with periodic health checks"""
    
    def __init__(self, username: str, password: str):
        self.client = AxiomTradeClient(username=username, password=password)
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = None
    
    def ensure_healthy_session(self) -> bool:
        """
        Ensure session is healthy (authenticated and tokens valid)
        
        Returns:
            True if session healthy, False otherwise
        """
        current_time = time.time()
        
        # Check if health check is needed
        if (self.last_health_check is None or 
            current_time - self.last_health_check > self.health_check_interval):
            
            print(f"🏥 Running session health check at {datetime.now()}")
            
            if self.client.ensure_authenticated():
                print("   ✅ Session healthy")
                self.last_health_check = current_time
                return True
            else:
                print("   ❌ Session unhealthy - authentication failed")
                return False
        
        # No health check needed yet
        return True
    
    def execute_with_health_check(self, operation: str, func):
        """
        Execute operation with automatic health check
        
        Args:
            operation: Description of operation
            func: Function to execute
        """
        print(f"\n📊 Executing: {operation}")
        
        if not self.ensure_healthy_session():
            print(f"   ❌ Skipped - session unhealthy")
            return None
        
        try:
            result = func()
            print(f"   ✅ Success")
            return result
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

# Usage
session = SessionManager("username", "password")

# These operations will have automatic health checks
balance = session.execute_with_health_check(
    "Get Balance",
    lambda: session.client.GetBalance()
)

trending = session.execute_with_health_check(
    "Get Trending Tokens",
    lambda: session.client.get_trending_tokens()
)

# Simulate time passing
time.sleep(301)  # More than health check interval

# Next operation will trigger health check
balance2 = session.execute_with_health_check(
    "Get Balance (again)",
    lambda: session.client.GetBalance()
)
```

**Output:**
```
📊 Executing: Get Balance
🏥 Running session health check at 2026-01-14 10:30:15
   ✅ Session healthy
   ✅ Success

📊 Executing: Get Trending Tokens
   ✅ Success

📊 Executing: Get Balance (again)
🏥 Running session health check at 2026-01-14 10:35:20
   ✅ Session healthy
   ✅ Success
```

### Example 6: Retry Logic with Authentication Recovery
Automatically retry failed operations with re-authentication.

```python
from axiomtradeapi.client import AxiomTradeClient
import time
from typing import Callable, Any, Optional

class ResilientClient:
    """Client with automatic retry and authentication recovery"""
    
    def __init__(self, username: str, password: str):
        self.client = AxiomTradeClient(username=username, password=password)
        self.max_retries = 3
    
    def execute_with_retry(
        self,
        operation: Callable,
        operation_name: str = "API Operation"
    ) -> Optional[Any]:
        """
        Execute operation with automatic retry and auth recovery
        
        Args:
            operation: Function to execute
            operation_name: Name for logging
            
        Returns:
            Operation result or None if all retries failed
        """
        for attempt in range(1, self.max_retries + 1):
            print(f"\n🔄 {operation_name} - Attempt {attempt}/{self.max_retries}")
            
            # Ensure authentication before each attempt
            if not self.client.ensure_authenticated():
                print(f"   ❌ Authentication failed")
                
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"   ⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                continue
            
            # Attempt operation
            try:
                result = operation()
                print(f"   ✅ Success on attempt {attempt}")
                return result
                
            except Exception as e:
                error_str = str(e).lower()
                print(f"   ❌ Error: {e}")
                
                # Check if error is auth-related
                if any(keyword in error_str for keyword in ['auth', 'token', 'unauthorized', '401']):
                    print(f"   🔧 Auth-related error - will re-authenticate")
                    # Clear tokens to force re-auth on next attempt
                    self.client.clear_saved_tokens()
                
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    print(f"   ⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        print(f"\n❌ {operation_name} failed after {self.max_retries} attempts")
        return None

# Usage
client = ResilientClient("username", "password")

# This will automatically retry with re-authentication if needed
balance = client.execute_with_retry(
    lambda: client.client.GetBalance(),
    "Get Balance"
)

if balance:
    print(f"\n💰 Final Balance: {balance['sol']} SOL")
```

**Output:**
```
🔄 Get Balance - Attempt 1/3
   ✅ Success on attempt 1

💰 Final Balance: 5.42 SOL
```

### Example 7: Multi-Client Session Manager
Manage authentication for multiple client instances.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import Dict, List
from datetime import datetime

class MultiClientManager:
    """Manage multiple authenticated clients"""
    
    def __init__(self):
        self.clients: Dict[str, AxiomTradeClient] = {}
        self.credentials: Dict[str, tuple] = {}
    
    def add_client(self, name: str, username: str, password: str):
        """
        Add a client with credentials
        
        Args:
            name: Friendly name for the client
            username: Axiom username
            password: Axiom password
        """
        client = AxiomTradeClient(username=username, password=password)
        self.clients[name] = client
        self.credentials[name] = (username, password)
        print(f"✅ Added client: {name}")
    
    def ensure_all_authenticated(self) -> Dict[str, bool]:
        """
        Ensure all clients are authenticated
        
        Returns:
            Dict mapping client names to authentication status
        """
        print("\n🔍 Checking authentication for all clients...")
        results = {}
        
        for name, client in self.clients.items():
            is_auth = client.ensure_authenticated()
            results[name] = is_auth
            
            status = "✅" if is_auth else "❌"
            print(f"   {status} {name}: {'Authenticated' if is_auth else 'Failed'}")
        
        return results
    
    def get_all_balances(self) -> Dict[str, dict]:
        """
        Get balances for all authenticated clients
        
        Returns:
            Dict mapping client names to balance data
        """
        print("\n💰 Fetching balances for all clients...")
        balances = {}
        
        for name, client in self.clients.items():
            if not client.ensure_authenticated():
                print(f"   ❌ {name}: Not authenticated")
                balances[name] = {"error": "Not authenticated"}
                continue
            
            try:
                balance = client.GetBalance()
                balances[name] = balance
                print(f"   ✅ {name}: {balance['sol']} SOL")
            except Exception as e:
                print(f"   ❌ {name}: Error - {e}")
                balances[name] = {"error": str(e)}
        
        return balances
    
    def reconnect_failed(self) -> int:
        """
        Reconnect clients that failed authentication
        
        Returns:
            Number of successfully reconnected clients
        """
        print("\n🔄 Reconnecting failed clients...")
        auth_status = self.ensure_all_authenticated()
        
        failed_clients = [name for name, status in auth_status.items() if not status]
        
        if not failed_clients:
            print("   ℹ️  No failed clients to reconnect")
            return 0
        
        reconnected = 0
        for name in failed_clients:
            print(f"   🔧 Reconnecting {name}...")
            client = self.clients[name]
            username, password = self.credentials[name]
            
            try:
                # Clear old tokens
                client.clear_saved_tokens()
                
                # Re-login
                client.login(username, password)
                
                # Verify
                if client.ensure_authenticated():
                    print(f"      ✅ Successfully reconnected")
                    reconnected += 1
                else:
                    print(f"      ❌ Reconnection failed")
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        print(f"\n✅ Reconnected {reconnected}/{len(failed_clients)} clients")
        return reconnected

# Usage
manager = MultiClientManager()

# Add multiple clients
manager.add_client("Main Account", "user1", "pass1")
manager.add_client("Trading Bot", "user2", "pass2")
manager.add_client("Test Account", "user3", "pass3")

# Ensure all authenticated
manager.ensure_all_authenticated()

# Get all balances
balances = manager.get_all_balances()

# Reconnect any failed clients
manager.reconnect_failed()
```

**Output:**
```
✅ Added client: Main Account
✅ Added client: Trading Bot
✅ Added client: Test Account

🔍 Checking authentication for all clients...
   ✅ Main Account: Authenticated
   ✅ Trading Bot: Authenticated
   ✅ Test Account: Authenticated

💰 Fetching balances for all clients...
   ✅ Main Account: 5.42 SOL
   ✅ Trading Bot: 2.15 SOL
   ✅ Test Account: 0.08 SOL

🔄 Reconnecting failed clients...
   ℹ️  No failed clients to reconnect
```

---

## Best Practices

### 1. Always Check Before API Calls
```python
# ✅ Good: Check authentication first
if client.ensure_authenticated():
    balance = client.GetBalance()
else:
    print("Authentication required")

# ❌ Bad: Assume you're authenticated
balance = client.GetBalance()  # May fail with auth error
```

### 2. Initialize with Credentials for Auto-Recovery
```python
# ✅ Good: Credentials enable auto-recovery
client = AxiomTradeClient(username="user", password="pass")
# ensure_authenticated() can auto re-authenticate if tokens expire

# ⚠️ Less Resilient: No credentials for recovery
client = AxiomTradeClient()
client.set_tokens(access_token, refresh_token)
# ensure_authenticated() can only refresh, not re-authenticate
```

### 3. Use in Long-Running Applications
```python
# ✅ Good: Periodic checks in long-running apps
while True:
    if client.ensure_authenticated():
        # Do work
        balance = client.GetBalance()
    else:
        print("Re-authentication needed")
        break
    
    time.sleep(60)
```

### 4. Combine with Error Handling
```python
# ✅ Good: Comprehensive error handling
try:
    if not client.ensure_authenticated():
        raise ValueError("Authentication failed")
    
    balance = client.GetBalance()
except ValueError as e:
    print(f"Auth error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### 5. Log Authentication Events
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Good: Log authentication status
if client.ensure_authenticated():
    logger.info("Authentication verified - proceeding with API call")
else:
    logger.error("Authentication failed - cannot proceed")
```

---

## Common Use Cases

### 1. API Request Guard
```python
def make_api_call():
    if not client.ensure_authenticated():
        return {"error": "Not authenticated"}
    
    return client.GetBalance()
```

### 2. Automated Trading Bot
```python
while trading_active:
    if not client.ensure_authenticated():
        logger.error("Bot stopped - authentication failed")
        break
    
    # Execute trading logic
    analyze_market()
    execute_trades()
    
    time.sleep(60)
```

### 3. Scheduled Tasks
```python
import schedule

def scheduled_task():
    if client.ensure_authenticated():
        balance = client.GetBalance()
        send_balance_report(balance)
    else:
        send_alert("Authentication failed")

schedule.every().hour.do(scheduled_task)
```

### 4. API Health Check
```python
def check_api_health():
    checks = {
        "authentication": client.ensure_authenticated(),
        "api_accessible": test_api_connection(),
        "balance_query": test_balance_query()
    }
    return all(checks.values())
```

### 5. User Session Validation
```python
def validate_user_session(user_id: str):
    client = get_client_for_user(user_id)
    
    if not client.ensure_authenticated():
        # Clear session, redirect to login
        clear_user_session(user_id)
        return False
    
    return True
```

---

## Troubleshooting

### Issue: Always Returns False

**Problem**: `ensure_authenticated()` consistently returns `False`.

**Possible Causes**:
1. No tokens and no credentials provided
2. Invalid credentials
3. Network connectivity issues
4. Refresh token expired

**Solutions**:

```python
# Check if client has credentials
client = AxiomTradeClient(username="user", password="pass")

# Verify credentials are correct
if not client.ensure_authenticated():
    print("Authentication failed - check credentials")
    
    # Try manual login to see specific error
    try:
        client.login("username", "password")
    except Exception as e:
        print(f"Login error: {e}")
```

### Issue: Repeated Re-authentication

**Problem**: Client keeps re-authenticating instead of refreshing tokens.

**Solution**:

```python
# Check token expiration
token_info = client.get_token_info_detailed()
print(f"Token expired: {token_info.get('is_expired')}")
print(f"Needs refresh: {token_info.get('needs_refresh')}")

# Verify refresh token is valid
if client.refresh_token:
    print(f"Refresh token available: Yes")
else:
    print(f"Refresh token available: No - will need full re-auth")
```

### Issue: Performance Degradation

**Problem**: `ensure_authenticated()` is slowing down your application.

**Solution**:

```python
# Cache authentication checks
last_auth_check = 0
AUTH_CHECK_INTERVAL = 60  # Check every 60 seconds

def check_auth_cached():
    global last_auth_check
    current_time = time.time()
    
    if current_time - last_auth_check > AUTH_CHECK_INTERVAL:
        is_authenticated = client.ensure_authenticated()
        last_auth_check = current_time
        return is_authenticated
    
    # Skip check if recently verified
    return True
```

### Issue: Authentication Fails After Long Idle Period

**Problem**: Client fails authentication after being idle for a long time.

**Solution**:

```python
# Implement session keepalive
def keepalive():
    """Periodically ensure authentication to prevent expiration"""
    if client.ensure_authenticated():
        print("✅ Session keepalive successful")
    else:
        print("❌ Session expired - re-authenticating")

# Run keepalive every 30 minutes
import schedule
schedule.every(30).minutes.do(keepalive)
```

---

## Related Methods

### `is_authenticated()`
Check authentication status without triggering refresh/re-auth.

```python
# Just check status (no auto-recovery)
if client.is_authenticated():
    print("Currently authenticated")

# Ensure with auto-recovery
if client.ensure_authenticated():
    print("Authenticated (will auto-recover if needed)")
```

See: [authentication-attributes-guide.md](./authentication-attributes-guide.md)

### `login()`
Manual authentication with username/password.

```python
# Manual login
client.login("username", "password")

# Then verify
if client.ensure_authenticated():
    print("Login successful")
```

See: [authentication.md](./authentication.md)

### `refresh_access_token()`
Manually refresh tokens.

```python
# Manual refresh
client.refresh_access_token()

# Or let ensure_authenticated handle it automatically
client.ensure_authenticated()  # Automatically refreshes if needed
```

### `set_tokens()`
Set tokens manually (useful when you have existing tokens).

```python
# Set tokens
client.set_tokens(access_token, refresh_token)

# Verify they're valid
if client.ensure_authenticated():
    print("Tokens are valid")
```

---

## Additional Resources

- **Authentication Guide**: [authentication.md](./authentication.md)
- **Authentication Attributes**: [authentication-attributes-guide.md](./authentication-attributes-guide.md)
- **Token Refresh**: [automatic-token-refresh.md](./automatic-token-refresh.md)
- **API Reference**: [api-reference.md](./api-reference.md)
- **Troubleshooting**: [troubleshooting.md](./troubleshooting.md)

---

## Summary

The `ensure_authenticated()` method provides:
- ✅ **Automatic token validation**: Checks if current tokens are valid
- ✅ **Automatic token refresh**: Refreshes expired tokens automatically
- ✅ **Automatic re-authentication**: Re-authenticates if refresh fails (when credentials available)
- ✅ **Resilient authentication**: Handles complete authentication lifecycle
- ✅ **Simple API**: Single method call for all auth concerns

**Key Takeaways**:
1. Always call before API operations for reliability
2. Returns `True` if authenticated, `False` otherwise
3. Automatically handles token refresh and re-authentication
4. Requires stored credentials for full auto-recovery
5. Use in long-running applications for continuous auth validation

**Usage Pattern**:
```python
# Initialize with credentials for auto-recovery
client = AxiomTradeClient(username="user", password="pass")

# Before any API call
if client.ensure_authenticated():
    # Safe to make API calls
    balance = client.GetBalance()
    trending = client.get_trending_tokens()
else:
    # Handle authentication failure
    print("Please login")
```

**When to Use**:
- ✅ Before every API call in production code
- ✅ In long-running applications (bots, services)
- ✅ When you need automatic token refresh
- ✅ When you want resilient authentication

**When NOT to Use**:
- ❌ When you only want to check status (use `is_authenticated()` instead)
- ❌ In tight loops (cache the result for performance)
- ❌ When you want manual control over auth flow

For questions or issues, refer to the [troubleshooting guide](./troubleshooting.md) or open an issue on GitHub.
