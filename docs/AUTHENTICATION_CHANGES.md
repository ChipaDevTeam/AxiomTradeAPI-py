# AxiomTradeAPI-py Token Authentication Update

## Summary of Changes

This update introduces a new token-based authentication system that eliminates the need to pass username and password to the client constructor, improving security and flexibility.

## Key Changes Made

### 1. Enhanced Client Constructor
- **Before**: Required username and password in constructor
- **After**: Clean initialization without credentials
```python
# Old approach (deprecated)
client = AxiomTradeClient(username="user@email.com", password="password")

# New approach (recommended)
client = AxiomTradeClient()
```

### 2. New Authentication Methods

#### `login(email, b64_password, otp_code)` 
- Single method for complete OTP-based login
- Returns structured response with access_token and refresh_token
- Automatically stores tokens in client instance

#### `set_tokens(access_token, refresh_token)`
- Manually set authentication tokens
- Perfect for using stored tokens or environment variables

#### `get_tokens()`
- Retrieve current authentication tokens
- Returns dictionary with access_token and refresh_token

#### `is_authenticated()`
- Check if client has valid authentication
- Returns boolean indicating auth status

#### `refresh_access_token()`
- Refresh expired access token using refresh token
- Automatically updates stored access token

### 3. Enhanced Authentication Flow

#### Login Process
```python
client = AxiomTradeClient()
result = client.login(email, b64_password, otp_code)
# Returns: {
#   'access_token': 'eyJhbGc...',
#   'refresh_token': 'eyJhbGc...',
#   'client_credentials': {...}
# }
```

#### Token Management
```python
# Set tokens from secure storage
client.set_tokens(
    access_token=os.getenv('AXIOM_ACCESS_TOKEN'),
    refresh_token=os.getenv('AXIOM_REFRESH_TOKEN')
)

# Check authentication status
if client.is_authenticated():
    # Use API methods
    trending = client.get_trending_tokens('1h')
```

### 4. Improved Security Features

- **No credentials in constructor** - Eliminates accidental exposure
- **Environment variable support** - Secure credential management
- **Token refresh capability** - Handles token expiration automatically
- **Cookie extraction** - Properly extracts tokens from HTTP responses

### 5. Updated Import Structure

- **Primary import**: `AxiomTradeClient` now uses the new token-based client
- **Legacy support**: `LegacyAxiomTradeClient` available for compatibility
- **Graceful fallback**: Legacy imports are optional (won't break if dependencies missing)

### 6. New Example Files

- **`token_based_example.py`** - Comprehensive token authentication example
- **`migration_guide.py`** - Shows differences between old and new approaches
- **`TOKEN_AUTHENTICATION.md`** - Detailed documentation

### 7. Updated Test Suite

- **`test_login.py`** - Updated to test new authentication methods
- **Token management tests** - Verify token setting, getting, and status checking
- **Method signature validation** - Ensure all new methods have correct parameters

## Migration Guide

### From Old API
```python
# OLD: Constructor with credentials
client = AxiomTradeClient(
    username=os.getenv("email"),
    password=os.getenv("password"),
)
```

### To New API
```python
# NEW: Clean constructor + separate authentication
client = AxiomTradeClient()

# Option 1: Login with OTP
tokens = client.login(email, b64_password, otp_code)

# Option 2: Set existing tokens  
client.set_tokens(
    access_token=os.getenv('AXIOM_ACCESS_TOKEN'),
    refresh_token=os.getenv('AXIOM_REFRESH_TOKEN')
)
```

## Benefits

1. **Enhanced Security**: No credentials in code/constructor
2. **Flexibility**: Multiple authentication methods
3. **Production Ready**: Environment variable support
4. **Token Management**: Built-in refresh and status checking
5. **Clean Architecture**: Separation of concerns
6. **Future Proof**: Extensible authentication system

## Testing

All changes have been tested with:
- Unit tests for new methods
- Integration tests for authentication flow  
- Example scripts demonstrating usage
- Migration scenarios

Run tests: `python test_login.py`

## Compatibility

- **Backwards Compatible**: Legacy client still available
- **Import Safe**: Won't break existing installations
- **Optional Dependencies**: Legacy features don't require additional packages

This update provides a more secure, flexible, and production-ready authentication system while maintaining full backwards compatibility.
