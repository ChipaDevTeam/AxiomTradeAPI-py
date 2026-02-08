# Active Axiom Users Monitoring

This guide explains how to use the `get_active_axiom_users` method to monitor real-time active user counts on Axiom Trade.

## Overview

The `get_active_axiom_users` method subscribes to a WebSocket stream that provides real-time updates about the number of active users on the Axiom Trade platform. This can be useful for:

- Monitoring platform activity
- Tracking peak usage times
- Building activity-based alerts or automations
- Analyzing user engagement patterns

## Quick Start

### Basic Usage

```python
import asyncio
from axiomtradeapi import AxiomTradeClient

async def monitor_users():
    # Initialize client
    client = AxiomTradeClient(
        username="your_email@example.com",
        password="your_password"
    )
    
    # Monitor for 60 seconds (prints updates to console)
    await client.get_active_axiom_users(duration=60)

asyncio.run(monitor_users())
```

### Custom Callback

```python
async def custom_handler(count: int):
    print(f"There are currently {count} active users on Axiom")
    
    # Add your custom logic
    if count > 100:
        print("High activity detected!")

async def main():
    client = AxiomTradeClient(username="...", password="...")
    await client.get_active_axiom_users(callback=custom_handler, duration=120)

asyncio.run(main())
```

## Method Signature

```python
async def get_active_axiom_users(
    self, 
    callback=None, 
    duration: int = None
) -> None
```

### Parameters

- **callback** (optional): An async function that receives the user count as an integer
  - If not provided, a default callback prints the count to console
  - Must be an async function: `async def callback(count: int): ...`

- **duration** (optional): Duration in seconds to monitor for updates
  - If `None`, monitors indefinitely until interrupted (Ctrl+C)
  - If specified, stops after the given number of seconds

### Returns

- None - The method runs continuously until stopped

## WebSocket Protocol

The method subscribes to the following WebSocket room:

```json
{
  "action": "join",
  "room": "e-FFcYgSSgWHforA9rXXkA48p8YFoz8TSW85Jpo3CQHDyS"
}
```

And receives messages in this format:

```json
{
  "room": "e-FFcYgSSgWHforA9rXXkA48p8YFoz8TSW85Jpo3CQHDyS",
  "content": "49"
}
```

Where `content` is a string containing the active user count.

## Advanced Usage

### Using WebSocket Client Directly

For more control over the WebSocket connection:

```python
from axiomtradeapi import AxiomTradeClient

async def main():
    client = AxiomTradeClient(username="...", password="...")
    
    # Get the websocket client
    ws_client = client.get_websocket_client()
    
    # Define callback
    async def on_user_count(count: int):
        print(f"Users: {count}")
    
    # Subscribe
    await ws_client.subscribe_active_users(on_user_count)
    
    # Start listening
    await ws_client.start()

asyncio.run(main())
```

### Tracking Statistics

```python
import asyncio
from datetime import datetime

class UserActivityTracker:
    def __init__(self):
        self.counts = []
        self.timestamps = []
    
    async def track(self, count: int):
        self.counts.append(count)
        self.timestamps.append(datetime.now())
        
        # Calculate stats
        avg = sum(self.counts) / len(self.counts)
        max_count = max(self.counts)
        min_count = min(self.counts)
        
        print(f"Current: {count} | Avg: {avg:.1f} | Min: {min_count} | Max: {max_count}")

async def main():
    tracker = UserActivityTracker()
    client = AxiomTradeClient(username="...", password="...")
    
    try:
        await client.get_active_axiom_users(callback=tracker.track)
    except KeyboardInterrupt:
        print("\nStopped by user")
        print(f"Total updates: {len(tracker.counts)}")

asyncio.run(main())
```

### Storing Data to Database

```python
import asyncio
from datetime import datetime
import sqlite3

async def store_to_db(count: int):
    conn = sqlite3.connect('user_activity.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO user_counts (timestamp, count) 
        VALUES (?, ?)
    ''', (datetime.now(), count))
    
    conn.commit()
    conn.close()
    
    print(f"Stored: {count} users at {datetime.now()}")

async def main():
    # Create table
    conn = sqlite3.connect('user_activity.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_counts (
            timestamp TEXT,
            count INTEGER
        )
    ''')
    conn.close()
    
    # Start monitoring
    client = AxiomTradeClient(username="...", password="...")
    await client.get_active_axiom_users(callback=store_to_db)

asyncio.run(main())
```

## Error Handling

```python
async def safe_monitor():
    client = AxiomTradeClient(username="...", password="...")
    
    try:
        await client.get_active_axiom_users(duration=300)
    except ValueError as e:
        print(f"Authentication error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

asyncio.run(safe_monitor())
```

## Authentication

The method requires valid authentication. It will automatically:

1. Check for existing valid tokens
2. Refresh expired tokens if possible
3. Use saved tokens if available
4. Raise `ValueError` if authentication fails

Make sure to either:
- Provide credentials when initializing the client
- Have valid saved tokens
- Call `login()` before using this method

## Notes

- The method is asynchronous and must be called with `await`
- Updates are received in real-time as users connect/disconnect
- The WebSocket connection is authenticated using your access tokens
- Press Ctrl+C to stop monitoring when running indefinitely
- The callback function must be async (use `async def`)

## Example Files

Check these example files in the `examples/` directory:

- **active_users_example.py** - Complete examples with different use cases
- **test_active_users.py** - Simple test script to verify the functionality

## Troubleshooting

**No updates received:**
- Check your authentication is valid
- Ensure you have a stable internet connection
- Verify the WebSocket server is accessible

**"Authentication failed" error:**
- Verify your credentials are correct
- Try logging in again with `client.login()`
- Check if tokens need to be refreshed

**Connection closed unexpectedly:**
- The WebSocket connection may have timed out
- Try reconnecting by calling the method again
- Check for network issues

## See Also

- [WebSocket Guide](websocket-guide.md) - General WebSocket usage
- [Authentication Guide](authentication.md) - Authentication setup
- [Getting Started](getting-started.md) - Basic setup and usage
