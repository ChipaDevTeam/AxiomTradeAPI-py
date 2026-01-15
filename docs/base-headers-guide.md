# base_headers - Complete Guide

## Table of Contents
- [Overview](#overview)
- [Structure](#structure)
- [Headers Explained](#headers-explained)
- [Basic Usage](#basic-usage)
- [Advanced Examples](#advanced-examples)
- [Customization](#customization)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)
- [Related Topics](#related-topics)

---

## Overview

The `base_headers` attribute is a **dictionary** containing standard HTTP headers used for all API requests to Axiom Trade. These headers ensure proper communication with the API and help requests appear as legitimate browser traffic.

### Purpose
- 🌐 **Browser Emulation**: Makes requests look like they come from a real browser
- 🔒 **CORS Compliance**: Ensures proper Cross-Origin Resource Sharing
- 📡 **Content Negotiation**: Specifies accepted response formats
- 🔧 **Request Context**: Provides necessary metadata for the API

### Type
```python
base_headers: Dict[str, str]
```

---

## Structure

### Default Headers

```python
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://axiom.trade',
    'Connection': 'keep-alive',
    'Referer': 'https://axiom.trade/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site'
}
```

### Visual Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│                       base_headers                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User-Agent ──────────► Browser identification             │
│  Accept ──────────────► Accepted content types             │
│  Accept-Language ─────► Preferred languages                │
│  Accept-Encoding ─────► Supported compression              │
│  Origin ──────────────► Request origin (CORS)              │
│  Connection ──────────► Connection persistence             │
│  Referer ─────────────► Previous page URL                  │
│  sec-fetch-* ─────────► Fetch metadata (security)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Headers Explained

### User-Agent
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
```

**Purpose**: Identifies the client making the request  
**Why Important**: 
- API servers often check User-Agent to block bots
- Emulates a real Chrome browser on Windows 10
- Helps requests pass anti-bot measures

**Format Breakdown**:
- `Mozilla/5.0` - Standard prefix
- `Windows NT 10.0` - Windows 10
- `Win64; x64` - 64-bit architecture
- `Chrome/135.0.0.0` - Chrome version

### Accept
```python
'Accept': 'application/json, text/plain, */*'
```

**Purpose**: Tells server what content types the client can handle  
**Values**:
- `application/json` - Primary: JSON responses
- `text/plain` - Secondary: Plain text
- `*/*` - Fallback: Accept any content type

### Accept-Language
```python
'Accept-Language': 'en-US,en;q=0.9'
```

**Purpose**: Specifies preferred language(s)  
**Format**:
- `en-US` - American English (priority 1.0)
- `en;q=0.9` - Generic English (priority 0.9)

### Accept-Encoding
```python
'Accept-Encoding': 'gzip, deflate, br'
```

**Purpose**: Indicates supported compression algorithms  
**Algorithms**:
- `gzip` - Standard compression
- `deflate` - Alternative compression
- `br` - Brotli compression (modern)

### Origin
```python
'Origin': 'https://axiom.trade'
```

**Purpose**: CORS header indicating request origin  
**Why Important**: Required for cross-origin API requests

### Connection
```python
'Connection': 'keep-alive'
```

**Purpose**: Controls connection persistence  
**Value**: `keep-alive` - Reuse TCP connection for multiple requests

### Referer
```python
'Referer': 'https://axiom.trade/'
```

**Purpose**: URL of the page that initiated the request  
**Why Important**: Some APIs check referer for security

### Security Headers (sec-fetch-*)
```python
'sec-fetch-dest': 'empty'
'sec-fetch-mode': 'cors'
'sec-fetch-site': 'same-site'
```

**Purpose**: Modern security metadata  
**Values**:
- `sec-fetch-dest: empty` - Not requesting a specific resource type
- `sec-fetch-mode: cors` - Cross-origin request
- `sec-fetch-site: same-site` - Same site request

---

## Basic Usage

### Example 1: Viewing Base Headers

```python
from axiomtradeapi import AxiomTradeClient

# Initialize client
client = AxiomTradeClient()

# View all base headers
print("📋 Base Headers:")
print("=" * 60)
for key, value in client.base_headers.items():
    print(f"{key:20} : {value[:50]}...")
```

**Output:**
```
📋 Base Headers:
============================================================
User-Agent           : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe...
Accept               : application/json, text/plain, */*...
Accept-Language      : en-US,en;q=0.9...
Accept-Encoding      : gzip, deflate, br...
Origin               : https://axiom.trade...
Connection           : keep-alive...
Referer              : https://axiom.trade/...
sec-fetch-dest       : empty...
sec-fetch-mode       : cors...
sec-fetch-site       : same-site...
```

### Example 2: Check Specific Header

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Get specific header
user_agent = client.base_headers.get('User-Agent')
accept = client.base_headers.get('Accept')

print(f"User-Agent: {user_agent}")
print(f"Accept: {accept}")
```

### Example 3: Headers Are Automatically Used

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()
client.login("email@example.com", "password")

# All API calls automatically use base_headers
# You don't need to do anything special!
balance = client.GetBalance("wallet_address")

# Behind the scenes, the client uses base_headers
# combined with authentication headers
```

---

## Advanced Examples

### Example 1: Inspecting Headers in Action

```python
from axiomtradeapi import AxiomTradeClient
import requests

def show_headers_in_action():
    """Demonstrate how base_headers are used in requests"""
    
    client = AxiomTradeClient()
    
    print("🔍 Headers Used in API Calls:")
    print("=" * 60)
    print("\n1. Base Headers (Standard):")
    for key, value in client.base_headers.items():
        print(f"   {key}: {value[:40]}...")
    
    print("\n2. Additional Headers (Authentication):")
    print("   - Authorization: Bearer <token>")
    print("   - Content-Type: application/json")
    print("   - Cookie: auth-access-token=<token>")
    
    print("\n3. Combined Headers (Actual Request):")
    print("   Base Headers + Auth Headers = Complete Request")

show_headers_in_action()
```

**Output:**
```
🔍 Headers Used in API Calls:
============================================================

1. Base Headers (Standard):
   User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64...
   Accept: application/json, text/plain, */*...
   Accept-Language: en-US,en;q=0.9...
   Accept-Encoding: gzip, deflate, br...
   Origin: https://axiom.trade...
   Connection: keep-alive...
   Referer: https://axiom.trade/...
   sec-fetch-dest: empty...
   sec-fetch-mode: cors...
   sec-fetch-site: same-site...

2. Additional Headers (Authentication):
   - Authorization: Bearer <token>
   - Content-Type: application/json
   - Cookie: auth-access-token=<token>

3. Combined Headers (Actual Request):
   Base Headers + Auth Headers = Complete Request
```

### Example 2: Custom Request with Base Headers

```python
from axiomtradeapi import AxiomTradeClient
import requests

def make_custom_request_with_base_headers():
    """Make a custom API request using base_headers"""
    
    client = AxiomTradeClient()
    client.login("email@example.com", "password")
    
    # Get base headers
    headers = client.base_headers.copy()
    
    # Add custom headers
    headers.update({
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client.access_token}'
    })
    
    # Make custom request
    response = requests.post(
        'https://axiom.trade/api/some-endpoint',
        headers=headers,
        json={'key': 'value'}
    )
    
    print(f"Status: {response.status_code}")
    return response

# Usage
response = make_custom_request_with_base_headers()
```

### Example 3: Debugging Request Headers

```python
from axiomtradeapi import AxiomTradeClient
import json

class HeaderDebugger:
    """Debug and analyze HTTP headers"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
    
    def analyze_headers(self):
        """Analyze all headers"""
        print("🔬 Header Analysis")
        print("=" * 60)
        
        headers = self.client.base_headers
        
        # Browser identification
        print("\n🌐 Browser Identification:")
        print(f"   User-Agent: {headers.get('User-Agent')}")
        
        # Content negotiation
        print("\n📦 Content Negotiation:")
        print(f"   Accept: {headers.get('Accept')}")
        print(f"   Accept-Language: {headers.get('Accept-Language')}")
        print(f"   Accept-Encoding: {headers.get('Accept-Encoding')}")
        
        # CORS headers
        print("\n🔒 CORS Headers:")
        print(f"   Origin: {headers.get('Origin')}")
        print(f"   Referer: {headers.get('Referer')}")
        
        # Security headers
        print("\n🛡️  Security Headers:")
        for key in headers:
            if key.startswith('sec-'):
                print(f"   {key}: {headers[key]}")
        
        # Connection
        print("\n🔗 Connection:")
        print(f"   Connection: {headers.get('Connection')}")
    
    def validate_headers(self):
        """Validate headers are properly set"""
        headers = self.client.base_headers
        required = ['User-Agent', 'Accept', 'Origin']
        
        print("\n✅ Header Validation:")
        for header in required:
            if header in headers and headers[header]:
                print(f"   ✅ {header}: Present")
            else:
                print(f"   ❌ {header}: Missing!")
    
    def compare_with_browser(self):
        """Compare with real browser headers"""
        headers = self.client.base_headers
        
        print("\n🔍 Browser Compatibility:")
        
        # Check User-Agent
        ua = headers.get('User-Agent', '')
        if 'Chrome' in ua:
            print("   ✅ Emulates Chrome browser")
        elif 'Firefox' in ua:
            print("   ✅ Emulates Firefox browser")
        else:
            print("   ⚠️  Unknown browser emulation")
        
        # Check modern headers
        modern_headers = ['sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site']
        has_modern = all(h in headers for h in modern_headers)
        
        if has_modern:
            print("   ✅ Includes modern security headers")
        else:
            print("   ⚠️  Missing modern security headers")
        
        # Check compression
        encoding = headers.get('Accept-Encoding', '')
        if 'br' in encoding:
            print("   ✅ Supports Brotli compression")
        if 'gzip' in encoding:
            print("   ✅ Supports GZIP compression")

# Usage
debugger = HeaderDebugger()
debugger.analyze_headers()
debugger.validate_headers()
debugger.compare_with_browser()
```

**Output:**
```
🔬 Header Analysis
============================================================

🌐 Browser Identification:
   User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...

📦 Content Negotiation:
   Accept: application/json, text/plain, */*
   Accept-Language: en-US,en;q=0.9
   Accept-Encoding: gzip, deflate, br

🔒 CORS Headers:
   Origin: https://axiom.trade
   Referer: https://axiom.trade/

🛡️  Security Headers:
   sec-fetch-dest: empty
   sec-fetch-mode: cors
   sec-fetch-site: same-site

🔗 Connection:
   Connection: keep-alive

✅ Header Validation:
   ✅ User-Agent: Present
   ✅ Accept: Present
   ✅ Origin: Present

🔍 Browser Compatibility:
   ✅ Emulates Chrome browser
   ✅ Includes modern security headers
   ✅ Supports Brotli compression
   ✅ Supports GZIP compression
```

### Example 4: Header Comparison Tool

```python
from axiomtradeapi import AxiomTradeClient

def compare_headers():
    """Compare client headers with ideal headers"""
    
    client = AxiomTradeClient()
    
    # Recommended headers for best compatibility
    recommended = {
        'User-Agent': 'Should contain browser info',
        'Accept': 'Should accept JSON',
        'Origin': 'Should match API domain',
        'Referer': 'Should match website',
        'Connection': 'Should be keep-alive',
        'Accept-Encoding': 'Should include gzip, br'
    }
    
    print("📊 Header Comparison Report")
    print("=" * 60)
    
    for key, requirement in recommended.items():
        actual = client.base_headers.get(key, 'NOT SET')
        
        # Check if requirement is met
        status = "✅" if actual != 'NOT SET' else "❌"
        
        print(f"\n{key}:")
        print(f"   Status: {status}")
        print(f"   Requirement: {requirement}")
        print(f"   Actual: {actual[:50]}..." if len(str(actual)) > 50 else f"   Actual: {actual}")

compare_headers()
```

---

## Customization

### Adding Custom Headers

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Add a custom header
client.base_headers['X-Custom-Header'] = 'MyValue'

# Add multiple custom headers
client.base_headers.update({
    'X-Api-Version': '1.0',
    'X-Client-ID': 'my-trading-bot',
    'X-Request-ID': '12345'
})

print("Updated headers:")
for key, value in client.base_headers.items():
    print(f"  {key}: {value}")
```

### Modifying Existing Headers

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Change User-Agent
client.base_headers['User-Agent'] = 'MyCustomBot/1.0'

# Change Accept
client.base_headers['Accept'] = 'application/json'

# Change language preference
client.base_headers['Accept-Language'] = 'es-ES,es;q=0.9'

print("Modified headers:")
print(f"User-Agent: {client.base_headers['User-Agent']}")
print(f"Accept-Language: {client.base_headers['Accept-Language']}")
```

### Removing Headers

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Remove a header (not recommended for base headers)
if 'Referer' in client.base_headers:
    del client.base_headers['Referer']
    print("Removed Referer header")

# Pop a header
removed_value = client.base_headers.pop('Accept-Language', None)
print(f"Removed Accept-Language: {removed_value}")
```

⚠️ **Warning**: Removing default headers may cause API requests to fail!

### Creating Custom Header Profiles

```python
from axiomtradeapi import AxiomTradeClient

class CustomHeaderProfiles:
    """Predefined header profiles for different scenarios"""
    
    @staticmethod
    def chrome_windows():
        """Chrome on Windows"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/'
        }
    
    @staticmethod
    def firefox_linux():
        """Firefox on Linux"""
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/'
        }
    
    @staticmethod
    def safari_mac():
        """Safari on macOS"""
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/'
        }

# Usage
client = AxiomTradeClient()

# Apply Firefox profile
client.base_headers = CustomHeaderProfiles.firefox_linux()
print(f"Using Firefox profile: {client.base_headers['User-Agent']}")

# Apply Safari profile
client.base_headers = CustomHeaderProfiles.safari_mac()
print(f"Using Safari profile: {client.base_headers['User-Agent']}")
```

---

## Best Practices

### ✅ DO:

#### 1. Keep Default Headers
```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# ✅ GOOD - Use default headers
# They're optimized for the API
balance = client.GetBalance("wallet")
```

#### 2. Add Headers, Don't Replace
```python
# ✅ GOOD - Add to existing headers
client.base_headers.update({
    'X-Custom-Header': 'value'
})

# ❌ BAD - Replace all headers
client.base_headers = {'User-Agent': 'MyBot'}  # Missing required headers!
```

#### 3. Copy Before Modifying
```python
# ✅ GOOD - Copy before modifying
custom_headers = client.base_headers.copy()
custom_headers['X-Custom'] = 'value'

# Use custom_headers for special requests
# Original base_headers unchanged
```

#### 4. Validate After Changes
```python
def validate_headers(headers: dict):
    """Validate required headers are present"""
    required = ['User-Agent', 'Accept', 'Origin']
    
    for header in required:
        if header not in headers:
            print(f"⚠️  Missing required header: {header}")
            return False
    return True

# ✅ GOOD - Validate after changes
client.base_headers['X-Custom'] = 'value'
if validate_headers(client.base_headers):
    print("✅ Headers valid")
```

### ⛔ DON'T:

#### 1. Don't Remove Required Headers
```python
# ❌ BAD - Removes required header
del client.base_headers['User-Agent']  # API may reject requests!
```

#### 2. Don't Use Invalid Values
```python
# ❌ BAD - Invalid values
client.base_headers['Accept'] = 'invalid/type'
client.base_headers['Origin'] = 'not-a-url'
```

#### 3. Don't Expose Sensitive Data in Headers
```python
# ❌ BAD - Sensitive data in custom headers
client.base_headers['X-Password'] = 'mysecret'  # Never do this!
client.base_headers['X-Token'] = 'mytoken'      # Use Authorization header
```

#### 4. Don't Log Full Headers in Production
```python
# ❌ BAD - May expose sensitive info
print(f"Headers: {client.base_headers}")  # Could contain auth data

# ✅ GOOD - Log selectively
print(f"User-Agent: {client.base_headers.get('User-Agent')}")
```

---

## Common Issues

### Issue 1: "403 Forbidden" Errors

**Cause**: Missing or invalid headers

**Solution**:
```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# Verify all required headers are present
required = ['User-Agent', 'Origin', 'Referer']
missing = [h for h in required if h not in client.base_headers]

if missing:
    print(f"❌ Missing headers: {missing}")
    # Restore defaults
    client = AxiomTradeClient()  # Recreate client
else:
    print("✅ All required headers present")
```

### Issue 2: Modified Headers Causing Failures

**Cause**: Accidentally modified critical headers

**Solution**:
```python
from axiomtradeapi import AxiomTradeClient

# Save original headers
client = AxiomTradeClient()
original_headers = client.base_headers.copy()

# If something goes wrong, restore
def restore_headers():
    client.base_headers = original_headers.copy()
    print("✅ Headers restored to defaults")

# Test after modifications
try:
    balance = client.GetBalance("wallet")
except Exception as e:
    print(f"❌ Error: {e}")
    restore_headers()
```

### Issue 3: Headers Not Applied to Requests

**Cause**: Using wrong method to make requests

**Solution**:
```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# ✅ CORRECT - Use client methods (headers applied automatically)
balance = client.GetBalance("wallet")

# ❌ WRONG - Direct requests won't use client headers
import requests
response = requests.get("https://axiom.trade/api/endpoint")  # No headers!

# ✅ CORRECT - If making custom requests, use base_headers
import requests
headers = client.base_headers.copy()
response = requests.get("https://axiom.trade/api/endpoint", headers=headers)
```

### Issue 4: "Invalid Header Value" Errors

**Cause**: Header value contains invalid characters

**Solution**:
```python
def sanitize_header_value(value: str) -> str:
    """Remove invalid characters from header value"""
    # Headers can't contain newlines or special chars
    return value.replace('\n', '').replace('\r', '').strip()

# ✅ GOOD - Sanitize custom values
client.base_headers['X-Custom'] = sanitize_header_value(user_input)
```

### Issue 5: Debugging Header Problems

```python
from axiomtradeapi import AxiomTradeClient
import json

def debug_headers():
    """Comprehensive header debugging"""
    client = AxiomTradeClient()
    
    print("🔍 Header Debug Report")
    print("=" * 60)
    
    # 1. Check all headers present
    print("\n1. All Headers:")
    print(json.dumps(client.base_headers, indent=2))
    
    # 2. Check required headers
    required = ['User-Agent', 'Accept', 'Origin']
    print("\n2. Required Headers Check:")
    for header in required:
        status = "✅" if header in client.base_headers else "❌"
        print(f"   {status} {header}")
    
    # 3. Check header values
    print("\n3. Header Value Check:")
    for key, value in client.base_headers.items():
        if not value:
            print(f"   ⚠️  {key}: Empty value!")
        elif '\n' in value or '\r' in value:
            print(f"   ⚠️  {key}: Contains newlines!")
        else:
            print(f"   ✅ {key}: OK")
    
    # 4. Check header size
    header_size = sum(len(k) + len(v) for k, v in client.base_headers.items())
    print(f"\n4. Total Header Size: {header_size} bytes")
    if header_size > 8192:
        print("   ⚠️  Headers exceed recommended size (8KB)")
    else:
        print("   ✅ Header size OK")

debug_headers()
```

---

## Related Topics

### Authentication Headers

The `base_headers` work in conjunction with authentication headers:

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()
client.login("email@example.com", "password")

# Complete request headers include:
# 1. base_headers (browser emulation)
# 2. Authorization header (Bearer token)
# 3. Cookie header (auth tokens)
# 4. Content-Type (for POST requests)
```

See: [Authentication Attributes Guide](./authentication-attributes-guide.md)

### Custom API Requests

When making custom requests, always include base_headers:

```python
import requests

# Get base headers
headers = client.base_headers.copy()

# Add auth and content type
headers.update({
    'Authorization': f'Bearer {client.access_token}',
    'Content-Type': 'application/json'
})

# Make request
response = requests.post(url, headers=headers, json=data)
```

### HTTP Header Standards

Learn more about HTTP headers:
- [MDN HTTP Headers Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [CORS Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Fetch Metadata](https://web.dev/fetch-metadata/)

---

## Summary

### Key Points

✅ `base_headers` contains standard HTTP headers for all requests  
✅ Headers ensure proper browser emulation and CORS compliance  
✅ Default headers are optimized - rarely need modification  
✅ Add custom headers with `.update()`, don't replace all headers  
✅ Always validate headers after modifications  

### Quick Reference

```python
from axiomtradeapi import AxiomTradeClient

client = AxiomTradeClient()

# View headers
print(client.base_headers)

# Add custom header
client.base_headers['X-Custom'] = 'value'

# Update multiple headers
client.base_headers.update({
    'X-Api-Version': '1.0',
    'X-Client-ID': 'my-bot'
})

# Copy headers for custom requests
custom_headers = client.base_headers.copy()
custom_headers['Authorization'] = 'Bearer token'
```

### Related Documentation

- [Authentication Attributes Guide](./authentication-attributes-guide.md)
- [API Reference](./api-reference.md)
- [Error Handling Guide](./error-handling.md)

---

**Last Updated:** January 14, 2026  
**Package Version:** 1.0.5+  
**Documentation Version:** 1.0
