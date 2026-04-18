"""
PumpPortal API Investigation - Check if they've changed requirements
"""

import requests
import json

print("🔍 PumpPortal API Investigation")
print("=" * 50)

# Test if PumpPortal API is responding at all
print("1️⃣ Testing basic API connectivity...")

try:
    # Try a simple GET request to see if the endpoint exists
    response = requests.get("https://pumpportal.fun/api/trade-local", timeout=10)
    print(f"GET request status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"GET request failed: {e}")

print("\n2️⃣ Testing with different headers...")

# Test with common headers that might be required
headers_tests = [
    {
        "name": "Basic headers",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    },
    {
        "name": "Form headers",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    },
    {
        "name": "PumpPortal specific headers",
        "headers": {
            "Content-Type": "application/json",
            "Origin": "https://pump.fun",
            "Referer": "https://pump.fun/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    }
]

test_data = {
    "publicKey": "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh",
    "action": "buy",
    "mint": "9SkhnfNU5kx3VhngR9F2X7YSKnRZsNxGzcipHoCNGakK",
    "amount": 1000000,
    "denominatedInSol": "true",
    "slippage": 20,
    "priorityFee": 0.005,
    "pool": "pump"
}

for test in headers_tests:
    print(f"\n   {test['name']}:")
    try:
        # Try with JSON payload
        response = requests.post(
            "https://pumpportal.fun/api/trade-local",
            headers=test['headers'],
            json=test_data,
            timeout=10
        )
        print(f"   JSON - Status: {response.status_code}, Response: {response.text[:100]}")
        
        # Try with form data
        response2 = requests.post(
            "https://pumpportal.fun/api/trade-local", 
            headers=test['headers'],
            data=test_data,
            timeout=10
        )
        print(f"   FORM - Status: {response2.status_code}, Response: {response2.text[:100]}")
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")

print("\n3️⃣ Checking PumpPortal documentation/status...")

# Check if there's an API status endpoint
try:
    status_response = requests.get("https://pumpportal.fun/api/status", timeout=5)
    print(f"Status endpoint: {status_response.status_code}")
    if status_response.status_code == 200:
        print(f"Status response: {status_response.text}")
except:
    print("No status endpoint found")

try:
    # Check if there's a different API base
    health_response = requests.get("https://pumpportal.fun/health", timeout=5)
    print(f"Health endpoint: {health_response.status_code}")
    if health_response.status_code == 200:
        print(f"Health response: {health_response.text}")
except:
    print("No health endpoint found")

print(f"\n4️⃣ Alternative approach - Check pump.fun directly...")

# Sometimes APIs require checking the main site first
try:
    main_site = requests.get("https://pump.fun", timeout=10)
    print(f"Main pump.fun site: {main_site.status_code}")
    
    # Look for API documentation in the response
    if "api" in main_site.text.lower():
        print("Found 'api' references in main site")
        
except Exception as e:
    print(f"Main site check failed: {e}")

print(f"\n📋 Conclusions:")
print("Based on consistent 400 errors across all requests:")
print("1. PumpPortal may have changed their API")
print("2. Authentication might now be required") 
print("3. Rate limiting could be very strict")
print("4. The API might be temporarily disabled")
print("5. Regional restrictions might apply")
print("\nRecommendation: Check PumpPortal documentation for recent changes")
