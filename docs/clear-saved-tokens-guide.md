# clear_saved_tokens() Method - Comprehensive Guide

## Overview

The `clear_saved_tokens()` method removes all securely stored authentication tokens from local storage. This is essential for logout operations, security cleanup, troubleshooting authentication issues, or when switching between different Axiom Trade accounts.

This method deletes the encrypted token files stored in `~/.axiomtradeapi/`, forcing the user to re-authenticate on the next API request.

## Method Signature

```python
def clear_saved_tokens(self) -> bool
```

## Parameters

**None** - This method takes no parameters.

## Return Value

Returns a boolean indicating success or failure:

- **`True`**: Tokens were successfully cleared (or no tokens existed)
- **`False`**: Failed to clear tokens (file system error, permission issue, etc.)

## How It Works

### Storage Location
Tokens are stored in encrypted files at:
```
~/.axiomtradeapi/
├── tokens.enc     # Encrypted authentication tokens (access + refresh tokens)
└── key.enc        # Encryption key used to decrypt tokens.enc
```

### What Gets Deleted
When you call `clear_saved_tokens()`:
1. **Deletes** `~/.axiomtradeapi/tokens.enc` (encrypted token file)
2. **Keeps** `~/.axiomtradeapi/key.enc` (encryption key remains for future use)
3. **Clears** in-memory token cache in the client instance

### Security Implications
- ✅ **Safe to use**: Tokens are removed from disk
- ✅ **Encryption key preserved**: Future logins will use same encryption key
- ✅ **Requires re-authentication**: Next API call will need login credentials or tokens
- ⚠️ **Does not revoke tokens**: Tokens may still be valid server-side until expiry

## Prerequisites

```python
from axiomtradeapi.client import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# You can call clear_saved_tokens() any time, regardless of authentication state
```

---

## Basic Usage Examples

### Example 1: Simple Logout
Clear tokens when user logs out of your application.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

# User logs in
client.login("username", "password")

# ... use API ...

# User logs out - clear stored tokens
if client.clear_saved_tokens():
    print("✅ Logged out successfully - tokens cleared")
else:
    print("⚠️ Warning: Failed to clear tokens")
```

**Output:**
```
✅ Logged out successfully - tokens cleared
```

### Example 2: Check Before Clearing
Verify tokens exist before attempting to clear them.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

# Check if tokens are saved
if client.has_saved_tokens():
    print("📁 Saved tokens found - clearing...")
    
    if client.clear_saved_tokens():
        print("✅ Tokens cleared successfully")
    else:
        print("❌ Failed to clear tokens")
else:
    print("ℹ️  No saved tokens to clear")
```

**Output:**
```
📁 Saved tokens found - clearing...
✅ Tokens cleared successfully
```

### Example 3: Complete Logout Flow
Comprehensive logout that clears both session and saved tokens.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

def logout():
    """
    Complete logout: clear session and stored tokens
    """
    print("🔓 Logging out...")
    
    # 1. Call API logout endpoint (if authenticated)
    if client.is_authenticated():
        try:
            client.logout()
            print("   ✅ API logout successful")
        except Exception as e:
            print(f"   ⚠️  API logout failed: {e}")
    
    # 2. Clear saved tokens from disk
    if client.clear_saved_tokens():
        print("   ✅ Local tokens cleared")
    else:
        print("   ❌ Failed to clear local tokens")
    
    # 3. Verify tokens are gone
    if not client.has_saved_tokens():
        print("✅ Logout complete - all tokens removed")
    else:
        print("⚠️ Warning: Some tokens may still remain")

# Perform logout
logout()
```

**Output:**
```
🔓 Logging out...
   ✅ API logout successful
   ✅ Local tokens cleared
✅ Logout complete - all tokens removed
```

---

## Advanced Examples

### Example 4: Multi-Account Switching
Switch between different Axiom Trade accounts by clearing tokens.

```python
from axiomtradeapi.client import AxiomTradeClient
import os

class MultiAccountManager:
    def __init__(self):
        self.current_client = None
        self.current_account = None
    
    def switch_account(self, account_name: str, username: str, password: str):
        """
        Switch to a different Axiom Trade account
        
        Args:
            account_name: Friendly name for the account
            username: Account username
            password: Account password
        """
        print(f"🔄 Switching to account: {account_name}")
        
        # 1. Clear existing tokens if any
        if self.current_client and self.current_client.has_saved_tokens():
            print(f"   Clearing tokens for: {self.current_account}")
            self.current_client.clear_saved_tokens()
        
        # 2. Create new client instance
        self.current_client = AxiomTradeClient()
        
        # 3. Login with new credentials
        try:
            self.current_client.login(username, password)
            self.current_account = account_name
            print(f"   ✅ Logged into: {account_name}")
            return True
        except Exception as e:
            print(f"   ❌ Login failed: {e}")
            return False
    
    def get_current_balance(self):
        """Get balance for current account"""
        if not self.current_client:
            print("❌ No account active")
            return None
        
        balance = self.current_client.GetBalance()
        print(f"💰 Balance for {self.current_account}: {balance['sol']} SOL")
        return balance

# Usage
manager = MultiAccountManager()

# Switch to trading account
manager.switch_account(
    "Trading Account",
    os.getenv("AXIOM_TRADING_USER"),
    os.getenv("AXIOM_TRADING_PASS")
)
manager.get_current_balance()

# Switch to testing account
manager.switch_account(
    "Test Account",
    os.getenv("AXIOM_TEST_USER"),
    os.getenv("AXIOM_TEST_PASS")
)
manager.get_current_balance()
```

**Output:**
```
🔄 Switching to account: Trading Account
   ✅ Logged into: Trading Account
💰 Balance for Trading Account: 5.42 SOL
🔄 Switching to account: Test Account
   Clearing tokens for: Trading Account
   ✅ Logged into: Test Account
💰 Balance for Test Account: 0.15 SOL
```

### Example 5: Automatic Token Refresh Failure Recovery
Clear corrupted tokens when automatic refresh fails.

```python
from axiomtradeapi.client import AxiomTradeClient
import time

class RobustClient:
    def __init__(self, username: str, password: str):
        self.client = AxiomTradeClient()
        self.username = username
        self.password = password
        self.max_retry_attempts = 3
    
    def make_request_with_recovery(self, request_func, *args, **kwargs):
        """
        Make API request with automatic recovery from token issues
        
        Args:
            request_func: Client method to call (e.g., client.GetBalance)
            *args, **kwargs: Arguments for the request function
        """
        for attempt in range(1, self.max_retry_attempts + 1):
            try:
                # Attempt the request
                return request_func(*args, **kwargs)
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if error is authentication-related
                if any(keyword in error_str for keyword in ['auth', 'token', 'unauthorized', '401']):
                    print(f"⚠️ Authentication error on attempt {attempt}: {e}")
                    
                    if attempt < self.max_retry_attempts:
                        print(f"🔧 Attempting recovery...")
                        
                        # Clear potentially corrupted tokens
                        if self.client.clear_saved_tokens():
                            print("   ✅ Cleared saved tokens")
                        
                        # Re-authenticate
                        try:
                            self.client.login(self.username, self.password)
                            print("   ✅ Re-authenticated successfully")
                            
                            # Wait before retry
                            time.sleep(1)
                            continue
                            
                        except Exception as login_error:
                            print(f"   ❌ Re-authentication failed: {login_error}")
                            raise
                else:
                    # Non-auth error, don't retry
                    raise
        
        raise Exception(f"Failed after {self.max_retry_attempts} attempts")

# Usage
client = RobustClient(
    username=os.getenv("AXIOM_USERNAME"),
    password=os.getenv("AXIOM_PASSWORD")
)

# This will automatically recover if tokens are corrupted
balance = client.make_request_with_recovery(
    client.client.GetBalance
)
print(f"Balance: {balance['sol']} SOL")
```

**Output:**
```
⚠️ Authentication error on attempt 1: 401 Unauthorized
🔧 Attempting recovery...
   ✅ Cleared saved tokens
   ✅ Re-authenticated successfully
Balance: 5.42 SOL
```

### Example 6: Security Audit and Token Cleanup
Periodically clear tokens for security compliance.

```python
from axiomtradeapi.client import AxiomTradeClient
from datetime import datetime, timedelta
import json
import os

class SecurityManager:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.audit_log_file = "token_audit.json"
        self.max_token_age_hours = 24  # Force re-auth after 24 hours
    
    def load_audit_log(self):
        """Load token creation timestamp"""
        if os.path.exists(self.audit_log_file):
            with open(self.audit_log_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_audit_log(self, data):
        """Save token creation timestamp"""
        with open(self.audit_log_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_and_enforce_token_age(self):
        """
        Check token age and clear if too old (security policy)
        """
        print("🔍 Running security audit...")
        
        # Check if tokens exist
        if not self.client.has_saved_tokens():
            print("   ℹ️  No saved tokens found")
            return
        
        # Load audit log
        audit_log = self.load_audit_log()
        last_login = audit_log.get('last_login_time')
        
        if not last_login:
            print("   ⚠️  No login timestamp found - clearing tokens")
            self.client.clear_saved_tokens()
            return
        
        # Calculate token age
        login_time = datetime.fromisoformat(last_login)
        token_age = datetime.now() - login_time
        max_age = timedelta(hours=self.max_token_age_hours)
        
        print(f"   Token age: {token_age}")
        print(f"   Max allowed age: {max_age}")
        
        if token_age > max_age:
            print(f"   ⚠️  Tokens exceeded max age - clearing for security")
            
            if self.client.clear_saved_tokens():
                print("   ✅ Old tokens cleared")
                
                # Clear audit log
                audit_log = {}
                self.save_audit_log(audit_log)
                
                print("   🔐 Please re-authenticate")
            else:
                print("   ❌ Failed to clear tokens")
        else:
            time_remaining = max_age - token_age
            print(f"   ✅ Tokens still valid ({time_remaining} remaining)")
    
    def record_login(self):
        """Record successful login for audit"""
        audit_log = {
            'last_login_time': datetime.now().isoformat(),
            'last_login_user': os.getenv('AXIOM_USERNAME', 'unknown')
        }
        self.save_audit_log(audit_log)
        print("📝 Login recorded in audit log")

# Usage
security = SecurityManager()

# Run security audit
security.check_and_enforce_token_age()

# After login, record it
# client.login(username, password)
# security.record_login()
```

**Output:**
```
🔍 Running security audit...
   Token age: 1 day, 3:25:10
   Max allowed age: 1 day, 0:00:00
   ⚠️  Tokens exceeded max age - clearing for security
   ✅ Old tokens cleared
   🔐 Please re-authenticate
```

### Example 7: Testing Environment Reset
Clear tokens before running automated tests.

```python
from axiomtradeapi.client import AxiomTradeClient
import unittest
import os

class TestAxiomTrading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests - ensure clean state"""
        print("\n🧪 Test Setup: Clearing any existing tokens...")
        
        # Create temporary client to clear tokens
        temp_client = AxiomTradeClient()
        
        if temp_client.has_saved_tokens():
            temp_client.clear_saved_tokens()
            print("   ✅ Previous tokens cleared")
        else:
            print("   ℹ️  No tokens to clear")
    
    def setUp(self):
        """Run before each test"""
        self.client = AxiomTradeClient()
        
        # Login for test
        self.client.login(
            os.getenv("AXIOM_TEST_USER"),
            os.getenv("AXIOM_TEST_PASS")
        )
    
    def tearDown(self):
        """Run after each test - cleanup"""
        # Clear tokens after each test
        self.client.clear_saved_tokens()
    
    def test_get_balance(self):
        """Test balance retrieval"""
        balance = self.client.GetBalance()
        self.assertIsNotNone(balance)
        self.assertIn('sol', balance)
        print(f"   Balance: {balance['sol']} SOL")
    
    def test_authentication(self):
        """Test authentication state"""
        self.assertTrue(self.client.is_authenticated())
        
        # Clear tokens
        self.client.clear_saved_tokens()
        
        # Should still be authenticated (in-memory)
        self.assertTrue(self.client.is_authenticated())
        
        # Create new client - should not be authenticated
        new_client = AxiomTradeClient()
        self.assertFalse(new_client.is_authenticated())

if __name__ == "__main__":
    unittest.main()
```

**Output:**
```
🧪 Test Setup: Clearing any existing tokens...
   ✅ Previous tokens cleared
..   Balance: 0.15 SOL
.
----------------------------------------------------------------------
Ran 2 tests in 2.456s

OK
```

### Example 8: Emergency Security Response
Immediately clear tokens if security breach is suspected.

```python
from axiomtradeapi.client import AxiomTradeClient
import os
import sys

def emergency_lockdown(reason: str = "Security concern"):
    """
    Emergency security lockdown - clear all tokens immediately
    
    Args:
        reason: Reason for lockdown (for logging)
    """
    print("🚨 EMERGENCY SECURITY LOCKDOWN 🚨")
    print(f"Reason: {reason}")
    print("=" * 50)
    
    client = AxiomTradeClient()
    
    # 1. Check if tokens exist
    if client.has_saved_tokens():
        print("📁 Saved tokens detected")
        
        # 2. Clear tokens
        if client.clear_saved_tokens():
            print("✅ Saved tokens CLEARED")
        else:
            print("❌ FAILED to clear saved tokens!")
            print("⚠️  MANUAL ACTION REQUIRED:")
            print(f"   Delete: ~/.axiomtradeapi/tokens.enc")
            return False
    else:
        print("ℹ️  No saved tokens found")
    
    # 3. Verify tokens are gone
    if not client.has_saved_tokens():
        print("✅ Verification passed - no tokens on disk")
    else:
        print("❌ VERIFICATION FAILED - tokens still present!")
        return False
    
    # 4. Security recommendations
    print("\n📋 Security Checklist:")
    print("   ✅ Tokens cleared from disk")
    print("   ⚠️  Change your password at: https://axiom.trade/")
    print("   ⚠️  Review recent account activity")
    print("   ⚠️  Check for unauthorized transactions")
    
    print("\n🔐 Lockdown complete")
    return True

# Usage examples:

# Scenario 1: User reports unauthorized access
if __name__ == "__main__":
    emergency_lockdown("User reported unauthorized access")

# Scenario 2: Automatic detection of suspicious activity
def detect_suspicious_activity():
    """Example: Detect unusual trading patterns"""
    # Your detection logic here
    unusual_transactions = 5
    return unusual_transactions > 3

if detect_suspicious_activity():
    emergency_lockdown("Suspicious trading activity detected")
```

**Output:**
```
🚨 EMERGENCY SECURITY LOCKDOWN 🚨
Reason: User reported unauthorized access
==================================================
📁 Saved tokens detected
✅ Saved tokens CLEARED
✅ Verification passed - no tokens on disk

📋 Security Checklist:
   ✅ Tokens cleared from disk
   ⚠️  Change your password at: https://axiom.trade/
   ⚠️  Review recent account activity
   ⚠️  Check for unauthorized transactions

🔐 Lockdown complete
```

---

## Best Practices

### 1. Always Check Return Value
```python
# ✅ Good: Check if clearing succeeded
if client.clear_saved_tokens():
    print("Tokens cleared successfully")
else:
    print("Failed to clear tokens - check permissions")
    # Handle error appropriately

# ❌ Bad: Ignore return value
client.clear_saved_tokens()  # Did it work? Unknown!
```

### 2. Clear on Logout
```python
def logout_user():
    """Complete logout process"""
    # Call API logout
    client.logout()
    
    # Clear local tokens
    client.clear_saved_tokens()
    
    print("Logged out successfully")
```

### 3. Verify Tokens Are Gone
```python
# Clear tokens
client.clear_saved_tokens()

# Verify
if not client.has_saved_tokens():
    print("✅ Tokens successfully removed")
else:
    print("⚠️ Tokens may still exist")
```

### 4. Handle Cleanup in Application Exit
```python
import atexit

def cleanup():
    """Cleanup function on app exit"""
    client = AxiomTradeClient()
    if client.has_saved_tokens():
        client.clear_saved_tokens()
        print("Cleaned up tokens on exit")

# Register cleanup function
atexit.register(cleanup)
```

### 5. Use in Context Manager
```python
from contextlib import contextmanager

@contextmanager
def axiom_session(username, password, clear_on_exit=True):
    """
    Context manager for Axiom API session
    
    Args:
        username: Axiom username
        password: Axiom password
        clear_on_exit: Whether to clear tokens when done
    """
    client = AxiomTradeClient()
    
    try:
        # Login
        client.login(username, password)
        yield client
    finally:
        # Cleanup
        if clear_on_exit:
            client.clear_saved_tokens()
            print("Session tokens cleared")

# Usage
with axiom_session("user", "pass") as client:
    balance = client.GetBalance()
    print(f"Balance: {balance['sol']} SOL")
# Tokens automatically cleared here
```

### 6. Log Token Operations
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_clear_tokens(client):
    """Clear tokens with logging"""
    if client.has_saved_tokens():
        logger.info("Clearing saved tokens...")
        
        if client.clear_saved_tokens():
            logger.info("✅ Tokens cleared successfully")
            return True
        else:
            logger.error("❌ Failed to clear tokens")
            return False
    else:
        logger.info("No tokens to clear")
        return True
```

---

## Common Use Cases

### 1. User Logout
```python
# User clicks "Logout" button
def handle_logout_button():
    client.logout()  # Server-side logout
    client.clear_saved_tokens()  # Local cleanup
    redirect_to_login_page()
```

### 2. Account Switching
```python
# Switch from account A to account B
def switch_account(new_username, new_password):
    # Clear current account tokens
    client.clear_saved_tokens()
    
    # Login with new account
    client.login(new_username, new_password)
```

### 3. Security Timeout
```python
# Clear tokens after inactivity
import time

last_activity = time.time()
TIMEOUT_SECONDS = 1800  # 30 minutes

def check_timeout():
    if time.time() - last_activity > TIMEOUT_SECONDS:
        print("Session timed out - clearing tokens")
        client.clear_saved_tokens()
```

### 4. Troubleshooting Authentication
```python
# User reports "unable to authenticate"
def fix_auth_issues():
    print("Clearing potentially corrupted tokens...")
    client.clear_saved_tokens()
    
    print("Please login again")
    client.login(username, password)
```

### 5. Testing and Development
```python
# Start each test with clean state
def test_setup():
    test_client = AxiomTradeClient()
    test_client.clear_saved_tokens()
    # Now run tests
```

---

## Troubleshooting

### Issue: `clear_saved_tokens()` Returns False

**Problem**: Method returns `False`, indicating failure to clear tokens.

**Possible Causes**:
1. **File permissions issue**: No write access to `~/.axiomtradeapi/`
2. **File locked**: Token file is open in another process
3. **Disk full**: No space to perform deletion
4. **File system error**: Corrupted file system

**Solutions**:

```python
import os
from pathlib import Path

# Check if token file exists
token_file = Path.home() / '.axiomtradeapi' / 'tokens.enc'

if token_file.exists():
    # Check permissions
    print(f"File permissions: {oct(token_file.stat().st_mode)}")
    
    # Try manual deletion
    try:
        token_file.unlink()
        print("✅ Manually deleted token file")
    except PermissionError:
        print("❌ Permission denied - need admin rights")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("File doesn't exist")
```

### Issue: Tokens Still Exist After Clearing

**Problem**: `has_saved_tokens()` returns `True` even after `clear_saved_tokens()`.

**Solution**:

```python
# Verify token file location
from pathlib import Path

token_dir = Path.home() / '.axiomtradeapi'
token_file = token_dir / 'tokens.enc'

print(f"Token directory: {token_dir}")
print(f"Token file: {token_file}")
print(f"File exists: {token_file.exists()}")

# Force delete if needed
if token_file.exists():
    import os
    os.remove(token_file)
    print("✅ Forcefully removed token file")
```

### Issue: Multiple Token Files

**Problem**: Multiple token files from different instances.

**Solution**:

```python
from pathlib import Path

# List all files in token directory
token_dir = Path.home() / '.axiomtradeapi'

if token_dir.exists():
    print("Files in token directory:")
    for file in token_dir.iterdir():
        print(f"  - {file.name} ({file.stat().st_size} bytes)")
    
    # Clean up all token files
    for file in token_dir.glob('tokens*.enc'):
        file.unlink()
        print(f"Deleted: {file.name}")
```

### Issue: Permission Denied on macOS/Linux

**Problem**: Cannot delete token file due to permissions.

**Solution**:

```bash
# Check permissions
ls -la ~/.axiomtradeapi/

# Fix permissions
chmod 700 ~/.axiomtradeapi/
chmod 600 ~/.axiomtradeapi/tokens.enc

# Retry
```

In Python:
```python
import os
from pathlib import Path

token_dir = Path.home() / '.axiomtradeapi'
token_file = token_dir / 'tokens.enc'

# Fix directory permissions
os.chmod(token_dir, 0o700)

# Fix file permissions if it exists
if token_file.exists():
    os.chmod(token_file, 0o600)

# Now try clearing
client.clear_saved_tokens()
```

---

## Security Considerations

### ⚠️ Important Security Notes

1. **Tokens May Still Be Valid**: Clearing tokens locally doesn't invalidate them server-side. The tokens can still be used until they expire if someone else has a copy.

2. **Encryption Key Remains**: The `key.enc` file is NOT deleted by `clear_saved_tokens()`. This means if someone has access to an old `tokens.enc` file, they can't decrypt it with the current key (files change after deletion).

3. **In-Memory Tokens**: Clearing saved tokens doesn't clear tokens in the current client instance's memory. To fully logout:
   ```python
   client.clear_saved_tokens()  # Clear disk
   client.logout()              # Clear memory + server-side
   ```

4. **Shared Filesystem**: If multiple applications share `~/.axiomtradeapi/`, clearing tokens affects all of them.

### Secure Token Clearing Checklist

```python
def secure_logout():
    """
    Complete secure logout procedure
    """
    # 1. Server-side logout
    try:
        client.logout()
        print("✅ Server logout successful")
    except:
        print("⚠️ Server logout failed (may already be logged out)")
    
    # 2. Clear saved tokens
    if client.clear_saved_tokens():
        print("✅ Local tokens cleared")
    else:
        print("❌ Failed to clear local tokens")
    
    # 3. Verify removal
    if not client.has_saved_tokens():
        print("✅ Verification passed")
    else:
        print("⚠️ Tokens still present")
    
    # 4. Clear in-memory state
    client.access_token = None
    client.refresh_token = None
    
    print("🔐 Secure logout complete")
```

---

## Related Methods

### `has_saved_tokens()`
Check if tokens exist before clearing.

```python
if client.has_saved_tokens():
    client.clear_saved_tokens()
    print("Tokens were cleared")
else:
    print("No tokens to clear")
```

See: [authentication-attributes-guide.md](./authentication-attributes-guide.md)

### `logout()`
Server-side logout that should be used with `clear_saved_tokens()`.

```python
# Complete logout
client.logout()  # Server-side
client.clear_saved_tokens()  # Client-side
```

### `login()`
Re-authenticate after clearing tokens.

```python
# Clear old tokens
client.clear_saved_tokens()

# Login again
client.login("username", "password")
```

See: [authentication.md](./authentication.md)

### `set_tokens()`
Manually set tokens (opposite of clearing).

```python
# Clear existing
client.clear_saved_tokens()

# Set new tokens
client.set_tokens(access_token, refresh_token)
```

---

## Additional Resources

- **Authentication Guide**: [authentication.md](./authentication.md)
- **Authentication Attributes**: [authentication-attributes-guide.md](./authentication-attributes-guide.md)
- **Token Refresh**: [automatic-token-refresh.md](./automatic-token-refresh.md)
- **Security Best Practices**: [security.md](./security.md)
- **Troubleshooting**: [troubleshooting.md](./troubleshooting.md)

---

## Summary

The `clear_saved_tokens()` method is essential for:
- ✅ **User logout**: Complete logout process
- ✅ **Account switching**: Clear before switching accounts
- ✅ **Security cleanup**: Remove tokens in case of breach
- ✅ **Testing**: Ensure clean state for tests
- ✅ **Troubleshooting**: Fix corrupted token issues

**Key Points**:
1. Always check the return value (`True`/`False`)
2. Use with `logout()` for complete logout
3. Verify with `has_saved_tokens()` after clearing
4. Tokens are deleted from `~/.axiomtradeapi/tokens.enc`
5. Encryption key (`key.enc`) is preserved
6. Does NOT invalidate tokens server-side

**Security Best Practice**:
```python
# Complete secure logout
def secure_logout():
    client.logout()              # 1. Server-side
    client.clear_saved_tokens()  # 2. Local disk
    # 3. Verify
    assert not client.has_saved_tokens()
```

For questions or issues, refer to the [troubleshooting guide](./troubleshooting.md) or open an issue on GitHub.
