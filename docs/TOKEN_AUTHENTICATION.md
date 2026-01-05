# AxiomTradeAPI-py Token-Based Authentication

This document explains the new token-based authentication system that eliminates the need to pass username and password to the client constructor.

## Quick Start

### Basic Usage (No credentials in constructor)

```python
from axiomtradeapi import AxiomTradeClient

# Initialize client without any credentials
client = AxiomTradeClient()

# Method 1: Login with OTP to get tokens
login_result = client.login(
    email="your_email@example.com",
    b64_password="your_base64_encoded_password",
    otp_code="123456"  # OTP code from email
)

print(f"Access Token: {login_result['access_token']}")
print(f"Refresh Token: {login_result['refresh_token']}")

# Now you can use API methods
trending = client.get_trending_tokens('1h')
```

### Using Existing Tokens

```python
from axiomtradeapi import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# Set tokens manually (from secure storage)
client.set_tokens(
    access_token="your_access_token_here",
    refresh_token="your_refresh_token_here"
)

# Check if authenticated
if client.is_authenticated():
    trending = client.get_trending_tokens('1h')
```

### Environment Variables (Recommended for Production)

```python
import os
from axiomtradeapi import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# Set tokens from environment variables
client.set_tokens(
    access_token=os.getenv('AXIOM_ACCESS_TOKEN'),
    refresh_token=os.getenv('AXIOM_REFRESH_TOKEN')
)

# Use the API
trending = client.get_trending_tokens('1h')
```

## Available Methods

### Authentication Methods

- `login(email, b64_password, otp_code)` - Complete login process and get tokens
- `set_tokens(access_token, refresh_token)` - Set tokens manually
- `get_tokens()` - Get current tokens
- `is_authenticated()` - Check if client has valid tokens
- `refresh_access_token()` - Refresh the access token

### API Methods

- `get_trending_tokens(time_period='1h')` - Get trending meme tokens
- `get_token_info(token_address)` - Get information about a specific token
- `get_user_portfolio()` - Get user's portfolio information

## Migration from Old API

### Before (Old API)
```python
# Old way - required username/password in constructor
client = AxiomTradeClient(
    username=os.getenv("email"),
    password=os.getenv("password"),
)
```

### After (New API)
```python
# New way - no credentials in constructor
client = AxiomTradeClient()

# Option 1: Login to get tokens
tokens = client.login(email, b64_password, otp_code)

# Option 2: Set existing tokens
client.set_tokens(access_token=token, refresh_token=refresh_token)
```

## Security Best Practices

1. **Never hardcode tokens in source code**
2. **Use environment variables or secure key management**
3. **Store tokens securely (encrypted at rest)**
4. **Implement token refresh logic for long-running applications**
5. **Monitor for token expiration and handle gracefully**

## Example: Complete Trading Bot

```python
import os
from axiomtradeapi import AxiomTradeClient

def create_authenticated_client():
    """Create an authenticated client using stored tokens"""
    client = AxiomTradeClient()
    
    # Try to use existing tokens first
    access_token = os.getenv('AXIOM_ACCESS_TOKEN')
    refresh_token = os.getenv('AXIOM_REFRESH_TOKEN')
    
    if access_token and refresh_token:
        client.set_tokens(access_token, refresh_token)
        return client
    
    # If no tokens, perform fresh login
    email = os.getenv('AXIOM_EMAIL')
    password = os.getenv('AXIOM_B64_PASSWORD')
    
    if not email or not password:
        raise ValueError("No tokens or credentials available")
    
    otp_code = input("Enter OTP code: ")
    login_result = client.login(email, password, otp_code)
    
    # Save tokens for next time (implement secure storage)
    save_tokens_securely(login_result['access_token'], login_result['refresh_token'])
    
    return client

def main():
    client = create_authenticated_client()
    
    # Use the authenticated client
    if client.is_authenticated():
        trending = client.get_trending_tokens('1h')
        print(f"Found {len(trending.get('tokens', []))} trending tokens")
    else:
        print("Authentication failed")

if __name__ == "__main__":
    main()
```

This new approach provides better security, flexibility, and follows modern authentication patterns.
