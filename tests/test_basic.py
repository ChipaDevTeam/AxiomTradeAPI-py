#!/usr/bin/env python3
"""
Quick test script to verify the new functionality works
"""

from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.auth.auth_manager import AuthManager

def test_basic_functionality():
    print("🧪 Testing Basic Functionality")
    print("=" * 40)
    
    try:
        # Test basic client creation
        client = AxiomTradeClient(use_saved_tokens=False)
        print("✅ Client created successfully")
        
        # Test auth manager creation
        auth = AuthManager(use_saved_tokens=False)
        print("✅ AuthManager created successfully")
        
        # Test token info
        token_info = auth.get_token_info()
        print(f"✅ Token info: authenticated={token_info['authenticated']}")
        
        # Test secure storage check
        print(f"✅ Has saved tokens: {auth.has_saved_tokens()}")
        
        # Test client methods
        print(f"✅ Client authenticated: {client.is_authenticated()}")
        print(f"✅ Client tokens: {client.get_tokens()}")
        
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)
