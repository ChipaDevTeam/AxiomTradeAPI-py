"""
Example: Monitor Active Axiom Users

This example demonstrates how to use the get_active_axiom_users method 
to monitor real-time active user counts on Axiom Trade.
"""

import asyncio
from axiomtradeapi import AxiomTradeClient


async def simple_example():
    """Simple example - monitor for 30 seconds with default callback"""
    # Initialize client with your credentials
    client = AxiomTradeClient(
        username="your_email@example.com",
        password="your_password"
    )
    
    # Login (or use saved tokens)
    if not client.is_authenticated():
        client.login()
    
    print("Monitoring active Axiom users for 30 seconds...")
    print("Press Ctrl+C to stop early\n")
    
    # Monitor for 30 seconds (will print each update)
    await client.get_active_axiom_users(duration=30)


async def custom_callback_example():
    """Example with custom callback for processing user counts"""
    
    # Track user count changes
    user_counts = []
    
    async def handle_user_count(count: int):
        """Custom callback that tracks and analyzes user counts"""
        user_counts.append(count)
        
        # Calculate statistics
        avg = sum(user_counts) / len(user_counts)
        max_users = max(user_counts)
        min_users = min(user_counts)
        
        print(f"Current: {count} users | Avg: {avg:.1f} | Min: {min_users} | Max: {max_users}")
        
        # You could add custom logic here:
        # - Alert when user count exceeds threshold
        # - Store data to database
        # - Trigger actions based on user activity
        
        if count > 100:
            print("🔥 High user activity detected!")
    
    # Initialize client
    client = AxiomTradeClient(
        username="your_email@example.com",
        password="your_password"
    )
    
    if not client.is_authenticated():
        client.login()
    
    print("Monitoring active users with custom analytics...")
    print("Press Ctrl+C to stop\n")
    
    # Monitor indefinitely with custom callback
    try:
        await client.get_active_axiom_users(callback=handle_user_count)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
        print(f"\nFinal statistics:")
        print(f"  Total updates: {len(user_counts)}")
        print(f"  Average users: {sum(user_counts) / len(user_counts):.1f}")
        print(f"  Peak users: {max(user_counts)}")


async def websocket_direct_example():
    """Example using the websocket client directly for more control"""
    from axiomtradeapi import AxiomTradeClient
    
    # Initialize client
    client = AxiomTradeClient(
        username="your_email@example.com",
        password="your_password"
    )
    
    if not client.is_authenticated():
        client.login()
    
    # Get websocket client
    ws_client = client.get_websocket_client()
    
    # Define callback
    async def on_user_count(count: int):
        print(f"Active users: {count}")
    
    # Subscribe to active users
    success = await ws_client.subscribe_active_users(on_user_count)
    
    if success:
        print("Successfully subscribed to active users updates")
        print("Listening for updates...\n")
        
        # Start listening
        await ws_client.start()
    else:
        print("Failed to subscribe to active users")


if __name__ == "__main__":
    print("Active Axiom Users Monitor Examples\n")
    print("Choose an example:")
    print("1. Simple 30-second monitor")
    print("2. Custom analytics callback")
    print("3. Direct websocket usage")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(simple_example())
    elif choice == "2":
        asyncio.run(custom_callback_example())
    elif choice == "3":
        asyncio.run(websocket_direct_example())
    else:
        print("Invalid choice")
