#!/usr/bin/env python3
"""
Test script for token refresh functionality
Tests the new automatic token refresh using the correct API endpoint
"""

import os
import sys
import time
import logging
from pathlib import Path
import dotenv

dotenv.load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from axiomtradeapi.auth.auth_manager import AuthManager
from axiomtradeapi.client import AxiomTradeClient

# Configure logging to see what's happening
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_token_refresh():
    """Test the token refresh functionality"""
    print("🧪 Testing Token Refresh Functionality")
    print("=" * 50)
    
    # You can set these from environment variables or replace with your tokens
    access_token = os.getenv('auth-access-token', 'your_access_token_here')
    refresh_token = os.getenv('auth-refresh-token', 'your_refresh_token_here')

    if access_token == 'your_access_token_here' or refresh_token == 'your_refresh_token_here':
        print("❌ Please set ACCESS_TOKEN and REFRESH_TOKEN environment variables")
        print("   Or replace the tokens in this script with real ones")
        print("\nExample:")
        print("   set ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        print("   set REFRESH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        return False
    
    try:
        # Test 1: Create AuthManager with tokens
        print("\n1️⃣ Creating AuthManager with existing tokens...")
        auth_manager = AuthManager(
            auth_token=access_token,
            refresh_token=refresh_token,
            use_saved_tokens=False  # Don't save for testing
        )
        
        # Test 2: Check current token status
        print("\n2️⃣ Checking current token status...")
        token_info = auth_manager.get_token_info()
        print(f"   Authenticated: {token_info.get('authenticated')}")
        print(f"   Is Expired: {token_info.get('is_expired')}")
        print(f"   Needs Refresh: {token_info.get('needs_refresh')}")
        
        # Test 3: Force a token refresh
        print("\n3️⃣ Testing token refresh...")
        refresh_success = auth_manager.refresh_tokens()
        
        if refresh_success:
            print("   ✅ Token refresh successful!")
            
            # Check new token info
            new_token_info = auth_manager.get_token_info()
            print(f"   New access token preview: {new_token_info.get('access_token_preview')}")
            print(f"   New expiry time: {new_token_info.get('expires_at')}")
            
        else:
            print("   ❌ Token refresh failed!")
            return False
        
        # Test 4: Test with AxiomTradeClient
        print("\n4️⃣ Testing with AxiomTradeClient...")
        client = AxiomTradeClient(
            auth_token=access_token,
            refresh_token=refresh_token,
            use_saved_tokens=False
        )
        
        if client.ensure_authenticated():
            print("   ✅ Client authentication successful!")
            
            # Try to make an API call
            try:
                trending = client.get_trending_tokens()
                if isinstance(trending, list):
                    print(f"   ✅ API call successful! Got {len(trending)} trending tokens")
                elif isinstance(trending, dict):
                    tokens = trending.get('tokens', trending.get('data', []))
                    if isinstance(tokens, list):
                        print(f"   ✅ API call successful! Got {len(tokens)} trending tokens")
                    else:
                        print(f"   ✅ API call successful! Response: {type(trending)}")
                else:
                    print(f"   ✅ API call successful! Response type: {type(trending)}")
            except Exception as e:
                print(f"   ⚠️ API call failed (but auth worked): {e}")
        else:
            print("   ❌ Client authentication failed!")
            return False
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logger.exception("Full error details:")
        return False


def test_secure_storage():
    """Test secure token storage"""
    print("\n🔒 Testing Secure Token Storage")
    print("=" * 40)
    
    try:
        # Create a test auth manager with secure storage
        auth_manager = AuthManager(use_saved_tokens=True)
        
        # Test tokens (fake ones for testing)
        test_access_token = "test_access_token_123"
        test_refresh_token = "test_refresh_token_456"
        
        print("1️⃣ Setting test tokens...")
        auth_manager._set_tokens(test_access_token, test_refresh_token)
        
        print("2️⃣ Creating new AuthManager to test loading...")
        new_auth_manager = AuthManager(use_saved_tokens=True)
        
        if (new_auth_manager.tokens and 
            new_auth_manager.tokens.access_token == test_access_token and
            new_auth_manager.tokens.refresh_token == test_refresh_token):
            print("   ✅ Secure storage test passed!")
            
            # Clean up
            print("3️⃣ Cleaning up test tokens...")
            new_auth_manager.clear_saved_tokens()
            print("   ✅ Test tokens cleared!")
            
            return True
        else:
            print("   ❌ Secure storage test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Secure storage test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Axiom Trade API - Token Refresh Tests")
    print("=" * 60)
    
    success = True
    
    # Test token refresh
    if not test_token_refresh():
        success = False
    
    # Test secure storage
    if not test_secure_storage():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
    else:
        print("❌ Some tests failed!")
    
    print("\n📝 Usage Notes:")
    print("   - Set your real tokens as environment variables to test refresh")
    print("   - Tokens are automatically refreshed when they expire")
    print("   - Secure storage uses encryption to protect your tokens")
    print("   - Use use_saved_tokens=False to disable automatic storage")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
