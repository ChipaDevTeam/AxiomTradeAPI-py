# endpoints Attribute - Comprehensive Guide

## Overview

The `endpoints` attribute is an instance of the `Endpoints` class that centralizes all API endpoint URLs and base URLs used by the AxiomTradeClient. This provides a single source of truth for API endpoint configuration, making it easy to access, modify, or verify the URLs used for various API operations.

## What is endpoints?

The `endpoints` attribute stores:
- **Base URLs**: Root API URLs for different Axiom Trade services
- **Endpoint paths**: Specific API endpoint paths for various operations

## Class Definition

```python
from axiomtradeapi.content.endpoints import Endpoints

class Endpoints:
    # Base URLs
    BASE_URL_API = "https://axiom.trade/api"
    BASE_URL = "https://axiom.trade"
    
    # Endpoint Paths
    ENDPOINT_GET_BALANCE = "/sol-balance"
    ENDPOINT_GET_BATCHED_BALANCE = "/batched-sol-balance"
    ENDPOINT_BUY_TOKEN = "/buy"
    ENDPOINT_SELL_TOKEN = "/sell"
    ENDPOINT_SEND_TRANSACTION = "/send-transaction"
    ENDPOINT_GET_TOKEN_BALANCE = "/token-balance"
```

## Accessing endpoints

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

# Access the endpoints object
endpoints = client.endpoints

# Access base URLs
print(endpoints.BASE_URL_API)  # "https://axiom.trade/api"
print(endpoints.BASE_URL)      # "https://axiom.trade"

# Access endpoint paths
print(endpoints.ENDPOINT_GET_BALANCE)  # "/sol-balance"
print(endpoints.ENDPOINT_BUY_TOKEN)    # "/buy"
```

## Available Base URLs

### `BASE_URL_API`
- **Value**: `"https://axiom.trade/api"`
- **Purpose**: Primary API base URL for most operations
- **Used For**: Trading operations, balance queries, transactions
- **Example**: `https://axiom.trade/api/sol-balance`

### `BASE_URL`
- **Value**: `"https://axiom.trade"`
- **Purpose**: Main website base URL
- **Used For**: Web-related operations, authentication redirects
- **Example**: `https://axiom.trade`

## Available Endpoint Paths

### `ENDPOINT_GET_BALANCE`
- **Path**: `"/sol-balance"`
- **Full URL**: `https://axiom.trade/api/sol-balance`
- **Purpose**: Get SOL balance for a wallet address
- **Used By**: `GetBalance()`, `get_sol_balance()`
- **Method**: GET
- **Authentication**: Required

### `ENDPOINT_GET_BATCHED_BALANCE`
- **Path**: `"/batched-sol-balance"`
- **Full URL**: `https://axiom.trade/api/batched-sol-balance`
- **Purpose**: Get SOL balances for multiple wallet addresses in one request
- **Used By**: Internal batched operations
- **Method**: POST
- **Authentication**: Required

### `ENDPOINT_BUY_TOKEN`
- **Path**: `"/buy"`
- **Full URL**: `https://axiom.trade/api/buy`
- **Purpose**: Purchase tokens using SOL
- **Used By**: `buy_token()` (legacy - now uses PumpPortal API)
- **Method**: POST
- **Authentication**: Required

### `ENDPOINT_SELL_TOKEN`
- **Path**: `"/sell"`
- **Full URL**: `https://axiom.trade/api/sell`
- **Purpose**: Sell tokens for SOL
- **Used By**: `sell_token()` (legacy - now uses PumpPortal API)
- **Method**: POST
- **Authentication**: Required

### `ENDPOINT_SEND_TRANSACTION`
- **Path**: `"/send-transaction"`
- **Full URL**: `https://axiom.trade/api/send-transaction`
- **Purpose**: Submit signed transactions to Solana blockchain
- **Used By**: `send_transaction_to_rpc()`
- **Method**: POST
- **Authentication**: Required

### `ENDPOINT_GET_TOKEN_BALANCE`
- **Path**: `"/token-balance"`
- **Full URL**: `https://axiom.trade/api/token-balance`
- **Purpose**: Get balance of specific SPL tokens
- **Used By**: `get_token_balance()`
- **Method**: GET
- **Authentication**: Required

---

## Basic Usage Examples

### Example 1: View All Endpoints
Display all available endpoints and their values.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

print("📋 Axiom Trade API Endpoints")
print("=" * 50)

# Base URLs
print("\n🌐 Base URLs:")
print(f"  API Base:  {client.endpoints.BASE_URL_API}")
print(f"  Web Base:  {client.endpoints.BASE_URL}")

# Endpoint paths
print("\n🔗 Endpoint Paths:")
print(f"  Balance:          {client.endpoints.ENDPOINT_GET_BALANCE}")
print(f"  Batched Balance:  {client.endpoints.ENDPOINT_GET_BATCHED_BALANCE}")
print(f"  Buy Token:        {client.endpoints.ENDPOINT_BUY_TOKEN}")
print(f"  Sell Token:       {client.endpoints.ENDPOINT_SELL_TOKEN}")
print(f"  Send Transaction: {client.endpoints.ENDPOINT_SEND_TRANSACTION}")
print(f"  Token Balance:    {client.endpoints.ENDPOINT_GET_TOKEN_BALANCE}")

# Construct full URLs
print("\n🔗 Full URLs:")
print(f"  Balance:       {client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}")
print(f"  Buy Token:     {client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_BUY_TOKEN}")
print(f"  Sell Token:    {client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_SELL_TOKEN}")
```

**Output:**
```
📋 Axiom Trade API Endpoints
==================================================

🌐 Base URLs:
  API Base:  https://axiom.trade/api
  Web Base:  https://axiom.trade

🔗 Endpoint Paths:
  Balance:          /sol-balance
  Batched Balance:  /batched-sol-balance
  Buy Token:        /buy
  Sell Token:       /sell
  Send Transaction: /send-transaction
  Token Balance:    /token-balance

🔗 Full URLs:
  Balance:       https://axiom.trade/api/sol-balance
  Buy Token:     https://axiom.trade/api/buy
  Sell Token:    https://axiom.trade/api/sell
```

### Example 2: Build Custom API URLs
Use endpoints to construct API URLs programmatically.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()

def build_api_url(endpoint_path: str) -> str:
    """
    Build full API URL from endpoint path
    
    Args:
        endpoint_path: Endpoint path (e.g., "/sol-balance")
        
    Returns:
        Full API URL
    """
    return f"{client.endpoints.BASE_URL_API}{endpoint_path}"

# Build URLs for different endpoints
balance_url = build_api_url(client.endpoints.ENDPOINT_GET_BALANCE)
token_balance_url = build_api_url(client.endpoints.ENDPOINT_GET_TOKEN_BALANCE)
send_tx_url = build_api_url(client.endpoints.ENDPOINT_SEND_TRANSACTION)

print(f"Balance URL: {balance_url}")
print(f"Token Balance URL: {token_balance_url}")
print(f"Send Transaction URL: {send_tx_url}")
```

**Output:**
```
Balance URL: https://axiom.trade/api/sol-balance
Token Balance URL: https://axiom.trade/api/token-balance
Send Transaction URL: https://axiom.trade/api/send-transaction
```

### Example 3: Verify Endpoint Configuration
Check that endpoints are correctly configured before using the client.

```python
from axiomtradeapi.client import AxiomTradeClient

def verify_endpoints(client: AxiomTradeClient) -> bool:
    """
    Verify all endpoints are properly configured
    
    Returns:
        True if all endpoints valid, False otherwise
    """
    print("🔍 Verifying endpoint configuration...")
    
    endpoints = client.endpoints
    issues = []
    
    # Check base URLs
    if not endpoints.BASE_URL_API.startswith("https://"):
        issues.append("BASE_URL_API doesn't use HTTPS")
    
    if not endpoints.BASE_URL.startswith("https://"):
        issues.append("BASE_URL doesn't use HTTPS")
    
    # Check endpoint paths start with /
    endpoint_paths = [
        endpoints.ENDPOINT_GET_BALANCE,
        endpoints.ENDPOINT_GET_BATCHED_BALANCE,
        endpoints.ENDPOINT_BUY_TOKEN,
        endpoints.ENDPOINT_SELL_TOKEN,
        endpoints.ENDPOINT_SEND_TRANSACTION,
        endpoints.ENDPOINT_GET_TOKEN_BALANCE
    ]
    
    for path in endpoint_paths:
        if not path.startswith("/"):
            issues.append(f"Endpoint path '{path}' doesn't start with /")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All endpoints configured correctly")
        return True

# Verify configuration
client = AxiomTradeClient()
verify_endpoints(client)
```

**Output:**
```
🔍 Verifying endpoint configuration...
✅ All endpoints configured correctly
```

---

## Advanced Examples

### Example 4: Endpoint Health Check
Check if all endpoints are accessible.

```python
from axiomtradeapi.client import AxiomTradeClient
import requests
from typing import Dict, List

class EndpointHealthChecker:
    def __init__(self, client: AxiomTradeClient):
        self.client = client
        self.endpoints = client.endpoints
    
    def check_endpoint_health(self, url: str, name: str) -> Dict:
        """
        Check if endpoint is accessible
        
        Args:
            url: Full endpoint URL
            name: Friendly name for endpoint
            
        Returns:
            Health check result
        """
        try:
            # Try HEAD request first (lightweight)
            response = requests.head(url, timeout=5)
            status = response.status_code
            
            # Some endpoints may not support HEAD, try OPTIONS
            if status == 405:
                response = requests.options(url, timeout=5)
                status = response.status_code
            
            return {
                "name": name,
                "url": url,
                "status": status,
                "accessible": status < 500,
                "message": "OK" if status < 500 else "Server Error"
            }
        except requests.exceptions.Timeout:
            return {
                "name": name,
                "url": url,
                "status": None,
                "accessible": False,
                "message": "Timeout"
            }
        except requests.exceptions.ConnectionError:
            return {
                "name": name,
                "url": url,
                "status": None,
                "accessible": False,
                "message": "Connection Failed"
            }
        except Exception as e:
            return {
                "name": name,
                "url": url,
                "status": None,
                "accessible": False,
                "message": str(e)
            }
    
    def check_all_endpoints(self) -> List[Dict]:
        """
        Check health of all API endpoints
        
        Returns:
            List of health check results
        """
        print("🏥 Running endpoint health checks...\n")
        
        endpoints_to_check = [
            (f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_GET_BALANCE}", "SOL Balance"),
            (f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_GET_TOKEN_BALANCE}", "Token Balance"),
            (f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_SEND_TRANSACTION}", "Send Transaction"),
            (f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_BUY_TOKEN}", "Buy Token"),
            (f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_SELL_TOKEN}", "Sell Token"),
            (self.endpoints.BASE_URL, "Main Website"),
        ]
        
        results = []
        for url, name in endpoints_to_check:
            result = self.check_endpoint_health(url, name)
            results.append(result)
            
            # Display result
            status_icon = "✅" if result["accessible"] else "❌"
            print(f"{status_icon} {result['name']}: {result['message']} (Status: {result['status']})")
        
        # Summary
        accessible_count = sum(1 for r in results if r["accessible"])
        total_count = len(results)
        
        print(f"\n📊 Summary: {accessible_count}/{total_count} endpoints accessible")
        
        return results

# Usage
client = AxiomTradeClient()
checker = EndpointHealthChecker(client)
results = checker.check_all_endpoints()
```

**Output:**
```
🏥 Running endpoint health checks...

✅ SOL Balance: OK (Status: 401)
✅ Token Balance: OK (Status: 401)
✅ Send Transaction: OK (Status: 401)
✅ Buy Token: OK (Status: 401)
✅ Sell Token: OK (Status: 401)
✅ Main Website: OK (Status: 200)

📊 Summary: 6/6 endpoints accessible
```

### Example 5: Custom Endpoint Override
Override endpoints for testing or alternative deployments.

```python
from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.content.endpoints import Endpoints

class CustomEndpoints(Endpoints):
    """Custom endpoints for testing environment"""
    # Override with test/staging URLs
    BASE_URL_API = "https://test-api.axiom.trade/api"
    BASE_URL = "https://test.axiom.trade"

class TestClient(AxiomTradeClient):
    """Client configured for testing environment"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace endpoints with test endpoints
        self.endpoints = CustomEndpoints()
        print("🧪 Test client initialized with test endpoints")

# Production client
prod_client = AxiomTradeClient()
print(f"Production API: {prod_client.endpoints.BASE_URL_API}")

# Test client
test_client = TestClient()
print(f"Test API: {test_client.endpoints.BASE_URL_API}")
```

**Output:**
```
Production API: https://axiom.trade/api
🧪 Test client initialized with test endpoints
Test API: https://test-api.axiom.trade/api
```

### Example 6: Endpoint Usage Logger
Track which endpoints are being used in your application.

```python
from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.content.endpoints import Endpoints
from collections import defaultdict
from datetime import datetime
import json

class EndpointUsageTracker:
    """Track endpoint usage statistics"""
    
    def __init__(self):
        self.usage_stats = defaultdict(int)
        self.usage_history = []
    
    def log_usage(self, endpoint_name: str, endpoint_url: str):
        """Log an endpoint usage"""
        self.usage_stats[endpoint_name] += 1
        self.usage_history.append({
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint_name,
            "url": endpoint_url
        })
    
    def get_stats(self) -> dict:
        """Get usage statistics"""
        return {
            "total_calls": len(self.usage_history),
            "unique_endpoints": len(self.usage_stats),
            "endpoint_breakdown": dict(self.usage_stats),
            "most_used": max(self.usage_stats.items(), key=lambda x: x[1]) if self.usage_stats else None
        }
    
    def print_stats(self):
        """Print usage statistics"""
        stats = self.get_stats()
        
        print("📊 Endpoint Usage Statistics")
        print("=" * 50)
        print(f"Total API Calls: {stats['total_calls']}")
        print(f"Unique Endpoints: {stats['unique_endpoints']}")
        
        if stats['most_used']:
            print(f"Most Used: {stats['most_used'][0]} ({stats['most_used'][1]} calls)")
        
        print("\n📈 Breakdown by Endpoint:")
        for endpoint, count in sorted(stats['endpoint_breakdown'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_calls']) * 100
            print(f"  {endpoint}: {count} calls ({percentage:.1f}%)")

class InstrumentedClient(AxiomTradeClient):
    """Client with endpoint usage tracking"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracker = EndpointUsageTracker()
    
    def GetBalance(self):
        """GetBalance with tracking"""
        endpoint_url = f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_GET_BALANCE}"
        self.tracker.log_usage("GetBalance", endpoint_url)
        return super().GetBalance()
    
    def get_token_balance(self, token_mint: str, wallet_address: str):
        """get_token_balance with tracking"""
        endpoint_url = f"{self.endpoints.BASE_URL_API}{self.endpoints.ENDPOINT_GET_TOKEN_BALANCE}"
        self.tracker.log_usage("GetTokenBalance", endpoint_url)
        return super().get_token_balance(token_mint, wallet_address)

# Usage
client = InstrumentedClient()

# Make some API calls (example)
try:
    client.GetBalance()
    client.GetBalance()
    client.GetBalance()
    # client.get_token_balance("token...", "wallet...")
except:
    pass  # Ignore auth errors for demo

# View stats
client.tracker.print_stats()
```

**Output:**
```
📊 Endpoint Usage Statistics
==================================================
Total API Calls: 3
Unique Endpoints: 1
Most Used: GetBalance (3 calls)

📈 Breakdown by Endpoint:
  GetBalance: 3 calls (100.0%)
```

### Example 7: Endpoint Configuration Validator
Validate endpoint configuration before deployment.

```python
from axiomtradeapi.client import AxiomTradeClient
import re
from typing import List, Tuple

class EndpointValidator:
    """Validate endpoint configuration"""
    
    def __init__(self, client: AxiomTradeClient):
        self.client = client
        self.endpoints = client.endpoints
        self.issues = []
        self.warnings = []
    
    def validate_url_format(self, url: str, name: str) -> bool:
        """Validate URL format"""
        # Check HTTPS
        if not url.startswith("https://"):
            self.issues.append(f"{name}: Must use HTTPS (got: {url})")
            return False
        
        # Check valid domain format
        if not re.match(r'^https://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}', url):
            self.issues.append(f"{name}: Invalid URL format (got: {url})")
            return False
        
        return True
    
    def validate_path_format(self, path: str, name: str) -> bool:
        """Validate endpoint path format"""
        # Check starts with /
        if not path.startswith("/"):
            self.issues.append(f"{name}: Path must start with '/' (got: {path})")
            return False
        
        # Check no double slashes
        if "//" in path:
            self.warnings.append(f"{name}: Path contains '//' (got: {path})")
        
        # Check lowercase (convention)
        if path != path.lower():
            self.warnings.append(f"{name}: Path should be lowercase (got: {path})")
        
        return True
    
    def validate_all(self) -> Tuple[List[str], List[str]]:
        """
        Validate all endpoints
        
        Returns:
            Tuple of (issues, warnings)
        """
        print("🔍 Validating endpoint configuration...\n")
        
        # Validate base URLs
        self.validate_url_format(self.endpoints.BASE_URL_API, "BASE_URL_API")
        self.validate_url_format(self.endpoints.BASE_URL, "BASE_URL")
        
        # Validate endpoint paths
        paths = {
            "ENDPOINT_GET_BALANCE": self.endpoints.ENDPOINT_GET_BALANCE,
            "ENDPOINT_GET_BATCHED_BALANCE": self.endpoints.ENDPOINT_GET_BATCHED_BALANCE,
            "ENDPOINT_BUY_TOKEN": self.endpoints.ENDPOINT_BUY_TOKEN,
            "ENDPOINT_SELL_TOKEN": self.endpoints.ENDPOINT_SELL_TOKEN,
            "ENDPOINT_SEND_TRANSACTION": self.endpoints.ENDPOINT_SEND_TRANSACTION,
            "ENDPOINT_GET_TOKEN_BALANCE": self.endpoints.ENDPOINT_GET_TOKEN_BALANCE,
        }
        
        for name, path in paths.items():
            self.validate_path_format(path, name)
        
        # Display results
        if self.issues:
            print("❌ Issues Found:")
            for issue in self.issues:
                print(f"   - {issue}")
        else:
            print("✅ No issues found")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if not self.issues and not self.warnings:
            print("✅ All validations passed - endpoints are correctly configured")
        
        return self.issues, self.warnings

# Usage
client = AxiomTradeClient()
validator = EndpointValidator(client)
issues, warnings = validator.validate_all()
```

**Output:**
```
🔍 Validating endpoint configuration...

✅ No issues found
✅ All validations passed - endpoints are correctly configured
```

---

## Best Practices

### 1. Don't Hardcode URLs
```python
# ❌ Bad: Hardcoded URL
url = "https://axiom.trade/api/sol-balance"

# ✅ Good: Use endpoints
url = f"{client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}"
```

### 2. Reference Endpoints Consistently
```python
# ✅ Good: Consistent reference
def get_balance_url(client):
    return f"{client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}"

# Always use this function instead of building URL manually
url = get_balance_url(client)
```

### 3. Validate Configuration on Startup
```python
def initialize_client():
    """Initialize client with validation"""
    client = AxiomTradeClient()
    
    # Verify endpoints are configured
    assert client.endpoints.BASE_URL_API.startswith("https://")
    assert client.endpoints.ENDPOINT_GET_BALANCE.startswith("/")
    
    return client
```

### 4. Use Helper Functions for URL Construction
```python
def build_full_url(client, endpoint_path: str) -> str:
    """Helper to build full URL"""
    return f"{client.endpoints.BASE_URL_API}{endpoint_path}"

# Usage
balance_url = build_full_url(client, client.endpoints.ENDPOINT_GET_BALANCE)
```

### 5. Document Endpoint Usage
```python
def fetch_balance():
    """
    Fetch SOL balance
    
    Endpoint: /sol-balance
    Full URL: https://axiom.trade/api/sol-balance
    """
    url = f"{client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}"
    # ... make request
```

---

## Use Cases

### 1. Building API Requests
```python
# Construct full endpoint URL
url = f"{client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}"

# Make request
response = requests.get(url, headers=client.base_headers)
```

### 2. Logging API Calls
```python
def log_api_call(endpoint_path: str):
    full_url = f"{client.endpoints.BASE_URL_API}{endpoint_path}"
    print(f"Calling: {full_url}")

log_api_call(client.endpoints.ENDPOINT_GET_BALANCE)
```

### 3. Testing Different Environments
```python
# Production
prod_client = AxiomTradeClient()
print(prod_client.endpoints.BASE_URL_API)  # Production URL

# Override for testing
test_client = AxiomTradeClient()
test_client.endpoints.BASE_URL_API = "https://test-api.axiom.trade/api"
```

### 4. API Documentation Generation
```python
def generate_endpoint_docs():
    """Generate documentation for all endpoints"""
    endpoints = client.endpoints
    
    docs = []
    docs.append(f"Base API URL: {endpoints.BASE_URL_API}")
    docs.append(f"\nEndpoints:")
    docs.append(f"- Balance: {endpoints.BASE_URL_API}{endpoints.ENDPOINT_GET_BALANCE}")
    docs.append(f"- Buy: {endpoints.BASE_URL_API}{endpoints.ENDPOINT_BUY_TOKEN}")
    docs.append(f"- Sell: {endpoints.BASE_URL_API}{endpoints.ENDPOINT_SELL_TOKEN}")
    
    return "\n".join(docs)

print(generate_endpoint_docs())
```

---

## Endpoint Reference Table

| Endpoint Constant | Path | Full URL | Purpose | Auth Required |
|-------------------|------|----------|---------|---------------|
| `ENDPOINT_GET_BALANCE` | `/sol-balance` | `https://axiom.trade/api/sol-balance` | Get SOL balance | ✅ Yes |
| `ENDPOINT_GET_BATCHED_BALANCE` | `/batched-sol-balance` | `https://axiom.trade/api/batched-sol-balance` | Get multiple balances | ✅ Yes |
| `ENDPOINT_BUY_TOKEN` | `/buy` | `https://axiom.trade/api/buy` | Buy tokens | ✅ Yes |
| `ENDPOINT_SELL_TOKEN` | `/sell` | `https://axiom.trade/api/sell` | Sell tokens | ✅ Yes |
| `ENDPOINT_SEND_TRANSACTION` | `/send-transaction` | `https://axiom.trade/api/send-transaction` | Send transaction | ✅ Yes |
| `ENDPOINT_GET_TOKEN_BALANCE` | `/token-balance` | `https://axiom.trade/api/token-balance` | Get token balance | ✅ Yes |

---

## Related Attributes

### `base_headers`
HTTP headers used with endpoints for API requests.

```python
url = f"{client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}"
response = requests.get(url, headers=client.base_headers)
```

See: [base-headers-guide.md](./base-headers-guide.md)

### `auth_manager`
Handles authentication for endpoint requests.

```python
url = f"{client.endpoints.BASE_URL_API}{client.endpoints.ENDPOINT_GET_BALANCE}"
response = client.auth_manager.make_authenticated_request('GET', url)
```

See: [authentication-attributes-guide.md](./authentication-attributes-guide.md)

---

## Additional Resources

- **API Reference**: [api-reference.md](./api-reference.md)
- **Getting Started**: [getting-started.md](./getting-started.md)
- **Authentication**: [authentication.md](./authentication.md)
- **Troubleshooting**: [troubleshooting.md](./troubleshooting.md)

---

## Summary

The `endpoints` attribute provides:
- ✅ **Centralized configuration**: Single source for all API URLs
- ✅ **Easy access**: Simple attribute access to base URLs and paths
- ✅ **Maintainability**: Change URLs in one place
- ✅ **Type safety**: Predefined constants prevent typos
- ✅ **Documentation**: Clear naming indicates purpose

**Quick Reference**:
```python
# Access endpoints
endpoints = client.endpoints

# Base URLs
endpoints.BASE_URL_API    # "https://axiom.trade/api"
endpoints.BASE_URL        # "https://axiom.trade"

# Endpoint paths
endpoints.ENDPOINT_GET_BALANCE          # "/sol-balance"
endpoints.ENDPOINT_GET_TOKEN_BALANCE    # "/token-balance"
endpoints.ENDPOINT_BUY_TOKEN            # "/buy"
endpoints.ENDPOINT_SELL_TOKEN           # "/sell"
endpoints.ENDPOINT_SEND_TRANSACTION     # "/send-transaction"

# Build full URL
url = f"{endpoints.BASE_URL_API}{endpoints.ENDPOINT_GET_BALANCE}"
# Result: "https://axiom.trade/api/sol-balance"
```

For questions or issues, refer to the [troubleshooting guide](./troubleshooting.md) or open an issue on GitHub.
