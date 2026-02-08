"""
Quick test script for the get_active_axiom_users method
"""

import asyncio
import sys
import os

# Add parent directory to path to import axiomtradeapi
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiomtradeapi import AxiomTradeClient


async def test_active_users():
    """Test the active users monitoring"""
    
    print("=" * 60)
    print("Testing get_active_axiom_users method")
    print("=" * 60)
    
    # Initialize client (it will use saved tokens if available)
    client = AxiomTradeClient(use_saved_tokens=True)
    
    # Check authentication
    if not client.is_authenticated():
        print("\n⚠️  Not authenticated. Please provide credentials:")
        username = input("Email: ").strip()
        password = input("Password: ").strip()
        
        client = AxiomTradeClient(username=username, password=password)
        result = client.login()
        
        if not result.get('success'):
            print("❌ Login failed!")
            return
        
        print("✅ Login successful!")
    else:
        print("✅ Using saved authentication tokens")
    
    print("\n" + "=" * 60)
    print("Monitoring active Axiom users for 15 seconds...")
    print("You should see real-time user count updates")
    print("=" * 60 + "\n")
    
    # Count updates received
    update_count = [0]
    
    async def tracking_callback(count: int):
        update_count[0] += 1
        print(f"Update #{update_count[0]}: {count} active users")
    
    try:
        await client.get_active_axiom_users(callback=tracking_callback, duration=15)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during test: {e}")
        return
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print(f"Total updates received: {update_count[0]}")
    
    if update_count[0] > 0:
        print("✅ SUCCESS: Method is working correctly!")
    else:
        print("⚠️  WARNING: No updates received. Check connection or authentication.")
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(test_active_users())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
