# get_last_transaction() - Complete Guide 📊

## Overview

The `get_last_transaction()` method retrieves the most recent transaction for a specific trading pair on the Solana blockchain. This is essential for:

- 📈 **Real-time Price Discovery** - Get the latest transaction price
- 🔍 **Market Activity Monitoring** - Track trading activity
- ⏱️ **Timestamp Analysis** - Determine last trade time
- 💧 **Liquidity Changes** - Monitor liquidity pool updates
- 🤖 **Trading Bot Logic** - Base decisions on latest market data
- 📊 **Price Feed Updates** - Build real-time price displays
- 🚨 **Activity Alerts** - Detect new transactions for notifications

---

## Method Signature

```python
def get_last_transaction(self, pair_address: str) -> Dict
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pair_address` | `str` | ✅ Yes | The Solana trading pair address to query |

### Return Value

Returns a `Dict` containing the last transaction details:

```python
{
    "signature": str,           # Transaction signature (unique ID)
    "pairAddress": str,         # Trading pair address
    "type": str,                # Transaction type: "buy" or "sell"
    "createdAt": int,           # Unix timestamp (milliseconds)
    "liquiditySol": float,      # SOL liquidity in pool after transaction
    "liquidityToken": float,    # Token liquidity in pool after transaction
    "makerAddress": str,        # Wallet address that initiated the transaction
    "priceSol": float,          # Price in SOL per token
    "priceUsd": float,          # Price in USD per token
    "tokenAmount": float,       # Amount of tokens traded
    "totalSol": float,          # Total SOL amount in transaction
    "totalUsd": float,          # Total USD value of transaction
    "innerIndex": int,          # Inner instruction index
    "outerIndex": int           # Outer instruction index
}
```

---

## Basic Examples

### Example 1: Get Last Transaction
```python
from axiomtradeapi import AxiomClient

client = AxiomClient()
client.login(email="your@email.com", password="your_password")

# Get last transaction for a pair
pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"
last_tx = client.get_last_transaction(pair_address)

print(f"Last transaction: {last_tx['type']}")
print(f"Price: ${last_tx['priceUsd']:.8f}")
print(f"Amount: {last_tx['tokenAmount']:,.0f} tokens")
print(f"Total Value: ${last_tx['totalUsd']:.2f}")
```

### Example 2: Check Transaction Time
```python
from datetime import datetime

last_tx = client.get_last_transaction(pair_address)

# Convert timestamp to readable format
timestamp = last_tx['createdAt'] / 1000  # Convert ms to seconds
tx_time = datetime.fromtimestamp(timestamp)

print(f"Last trade: {tx_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Calculate time since last trade
time_ago = datetime.now() - tx_time
minutes_ago = time_ago.total_seconds() / 60

print(f"Time since last trade: {minutes_ago:.1f} minutes ago")
```

### Example 3: Monitor Buy vs Sell Pressure
```python
# Get last 5 transactions to check sentiment
last_tx = client.get_last_transaction(pair_address)

tx_type = last_tx['type']
if tx_type == "buy":
    print("✅ Last transaction was a BUY")
    print(f"   Amount: ${last_tx['totalUsd']:.2f}")
elif tx_type == "sell":
    print("❌ Last transaction was a SELL")
    print(f"   Amount: ${last_tx['totalUsd']:.2f}")

print(f"Current liquidity: {last_tx['liquiditySol']:.2f} SOL")
```

---

## Advanced Examples

### Example 1: Real-Time Price Monitor
```python
import time
from datetime import datetime
from typing import Dict, List

class PriceMonitor:
    """Monitor price changes using last transaction data"""
    
    def __init__(self, client: AxiomClient, pair_address: str):
        self.client = client
        self.pair_address = pair_address
        self.price_history: List[Dict] = []
        self.last_signature = None
        
    def check_for_new_transaction(self) -> bool:
        """Check if there's a new transaction"""
        try:
            last_tx = self.client.get_last_transaction(self.pair_address)
            
            # Check if this is a new transaction
            if last_tx['signature'] != self.last_signature:
                self.last_signature = last_tx['signature']
                self.price_history.append({
                    'timestamp': last_tx['createdAt'],
                    'price_usd': last_tx['priceUsd'],
                    'price_sol': last_tx['priceSol'],
                    'type': last_tx['type'],
                    'volume_usd': last_tx['totalUsd']
                })
                return True
            return False
            
        except Exception as e:
            print(f"Error checking transaction: {e}")
            return False
    
    def get_price_change(self) -> Dict:
        """Calculate price change from first to last transaction"""
        if len(self.price_history) < 2:
            return {'change_pct': 0, 'change_usd': 0}
        
        first_price = self.price_history[0]['price_usd']
        last_price = self.price_history[-1]['price_usd']
        
        change_usd = last_price - first_price
        change_pct = (change_usd / first_price) * 100
        
        return {
            'change_pct': change_pct,
            'change_usd': change_usd,
            'first_price': first_price,
            'last_price': last_price
        }
    
    def run(self, duration_seconds: int = 300, check_interval: int = 5):
        """Run price monitoring for specified duration"""
        print(f"🔍 Starting price monitor for {self.pair_address}")
        print(f"   Duration: {duration_seconds}s, Check every: {check_interval}s\n")
        
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            if self.check_for_new_transaction():
                last = self.price_history[-1]
                timestamp = datetime.fromtimestamp(last['timestamp'] / 1000)
                
                # Format output based on transaction type
                icon = "📈" if last['type'] == "buy" else "📉"
                color = "BUY" if last['type'] == "buy" else "SELL"
                
                print(f"{icon} New {color} at {timestamp.strftime('%H:%M:%S')}")
                print(f"   Price: ${last['price_usd']:.8f}")
                print(f"   Volume: ${last['volume_usd']:.2f}")
                
                # Show price change if we have history
                if len(self.price_history) > 1:
                    change = self.get_price_change()
                    change_icon = "🟢" if change['change_pct'] > 0 else "🔴"
                    print(f"   {change_icon} Change: {change['change_pct']:.2f}%\n")
            
            time.sleep(check_interval)
        
        # Final summary
        print(f"\n📊 Monitoring Complete")
        print(f"   Total transactions: {len(self.price_history)}")
        if len(self.price_history) > 1:
            change = self.get_price_change()
            print(f"   Price change: {change['change_pct']:.2f}%")
            print(f"   From: ${change['first_price']:.8f}")
            print(f"   To: ${change['last_price']:.8f}")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

monitor = PriceMonitor(client, "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
monitor.run(duration_seconds=300, check_interval=10)
```

### Example 2: Activity Detector with Alerts
```python
import time
from datetime import datetime, timedelta
from typing import Optional

class ActivityDetector:
    """Detect and alert on trading activity patterns"""
    
    def __init__(self, client: AxiomClient, pair_address: str):
        self.client = client
        self.pair_address = pair_address
        self.last_check_time = None
        self.inactivity_threshold_minutes = 5
        self.large_trade_threshold_usd = 1000
        
    def check_activity(self) -> Dict:
        """Check current activity status"""
        try:
            last_tx = self.client.get_last_transaction(self.pair_address)
            
            # Calculate time since last trade
            tx_timestamp = datetime.fromtimestamp(last_tx['createdAt'] / 1000)
            time_since_trade = datetime.now() - tx_timestamp
            minutes_since = time_since_trade.total_seconds() / 60
            
            # Determine activity status
            is_active = minutes_since < self.inactivity_threshold_minutes
            is_large_trade = last_tx['totalUsd'] > self.large_trade_threshold_usd
            
            return {
                'is_active': is_active,
                'is_large_trade': is_large_trade,
                'minutes_since_trade': minutes_since,
                'last_tx': last_tx,
                'timestamp': tx_timestamp
            }
            
        except Exception as e:
            print(f"Error checking activity: {e}")
            return None
    
    def send_alert(self, alert_type: str, data: Dict):
        """Send alert (implement your notification method)"""
        if alert_type == "inactive":
            print(f"\n⚠️  INACTIVITY ALERT")
            print(f"   Pair: {self.pair_address[:8]}...")
            print(f"   No trades for {data['minutes']:.1f} minutes")
            print(f"   Last trade: {data['timestamp'].strftime('%H:%M:%S')}")
            
        elif alert_type == "large_trade":
            tx = data['tx']
            print(f"\n🚨 LARGE TRADE ALERT")
            print(f"   Type: {tx['type'].upper()}")
            print(f"   Amount: ${tx['totalUsd']:,.2f}")
            print(f"   Price: ${tx['priceUsd']:.8f}")
            print(f"   Time: {data['timestamp'].strftime('%H:%M:%S')}")
            
        elif alert_type == "resumed":
            print(f"\n✅ ACTIVITY RESUMED")
            print(f"   After {data['inactive_minutes']:.1f} minutes")
            print(f"   New trade: {data['tx']['type'].upper()}")
            print(f"   Volume: ${data['tx']['totalUsd']:.2f}")
    
    def monitor_with_alerts(self, check_interval: int = 30):
        """Monitor activity and send alerts"""
        print(f"🔔 Activity detector started")
        print(f"   Inactivity threshold: {self.inactivity_threshold_minutes} min")
        print(f"   Large trade threshold: ${self.large_trade_threshold_usd:,}")
        print(f"   Check interval: {check_interval}s\n")
        
        was_inactive = False
        inactive_since = None
        
        while True:
            status = self.check_activity()
            
            if status:
                # Check for large trade
                if status['is_large_trade']:
                    self.send_alert('large_trade', {
                        'tx': status['last_tx'],
                        'timestamp': status['timestamp']
                    })
                
                # Check for inactivity
                if not status['is_active']:
                    if not was_inactive:
                        # First detection of inactivity
                        was_inactive = True
                        inactive_since = datetime.now()
                        self.send_alert('inactive', {
                            'minutes': status['minutes_since_trade'],
                            'timestamp': status['timestamp']
                        })
                else:
                    if was_inactive:
                        # Activity resumed after inactivity
                        inactive_duration = (datetime.now() - inactive_since).total_seconds() / 60
                        self.send_alert('resumed', {
                            'inactive_minutes': inactive_duration,
                            'tx': status['last_tx']
                        })
                        was_inactive = False
                        inactive_since = None
            
            time.sleep(check_interval)

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

detector = ActivityDetector(client, "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
detector.inactivity_threshold_minutes = 3
detector.large_trade_threshold_usd = 500
detector.monitor_with_alerts(check_interval=20)
```

### Example 3: Liquidity Change Tracker
```python
from typing import List, Dict

class LiquidityTracker:
    """Track liquidity changes from transaction data"""
    
    def __init__(self, client: AxiomClient, pair_address: str):
        self.client = client
        self.pair_address = pair_address
        self.liquidity_history: List[Dict] = []
        self.last_signature = None
        
    def update_liquidity_data(self) -> Optional[Dict]:
        """Update liquidity data if there's a new transaction"""
        try:
            last_tx = self.client.get_last_transaction(self.pair_address)
            
            # Check if this is new data
            if last_tx['signature'] == self.last_signature:
                return None
            
            self.last_signature = last_tx['signature']
            
            liquidity_data = {
                'timestamp': last_tx['createdAt'],
                'sol_liquidity': last_tx['liquiditySol'],
                'token_liquidity': last_tx['liquidityToken'],
                'tx_type': last_tx['type'],
                'tx_size_usd': last_tx['totalUsd']
            }
            
            self.liquidity_history.append(liquidity_data)
            return liquidity_data
            
        except Exception as e:
            print(f"Error updating liquidity: {e}")
            return None
    
    def calculate_liquidity_change(self) -> Dict:
        """Calculate liquidity change metrics"""
        if len(self.liquidity_history) < 2:
            return {'has_data': False}
        
        first = self.liquidity_history[0]
        last = self.liquidity_history[-1]
        
        sol_change = last['sol_liquidity'] - first['sol_liquidity']
        sol_change_pct = (sol_change / first['sol_liquidity']) * 100
        
        token_change = last['token_liquidity'] - first['token_liquidity']
        token_change_pct = (token_change / first['token_liquidity']) * 100
        
        return {
            'has_data': True,
            'sol_change': sol_change,
            'sol_change_pct': sol_change_pct,
            'token_change': token_change,
            'token_change_pct': token_change_pct,
            'initial_sol': first['sol_liquidity'],
            'current_sol': last['sol_liquidity'],
            'initial_token': first['token_liquidity'],
            'current_token': last['token_liquidity']
        }
    
    def analyze_liquidity_trend(self) -> str:
        """Analyze liquidity trend"""
        change = self.calculate_liquidity_change()
        
        if not change['has_data']:
            return "INSUFFICIENT_DATA"
        
        sol_change = change['sol_change_pct']
        
        if sol_change > 10:
            return "STRONG_ADDITION"
        elif sol_change > 5:
            return "MODERATE_ADDITION"
        elif sol_change > 0:
            return "SLIGHT_ADDITION"
        elif sol_change > -5:
            return "SLIGHT_REMOVAL"
        elif sol_change > -10:
            return "MODERATE_REMOVAL"
        else:
            return "STRONG_REMOVAL"
    
    def get_report(self) -> str:
        """Generate liquidity report"""
        if not self.liquidity_history:
            return "No liquidity data collected yet"
        
        change = self.calculate_liquidity_change()
        trend = self.analyze_liquidity_trend()
        
        report = f"💧 Liquidity Report for {self.pair_address[:8]}...\n"
        report += f"{'='*60}\n\n"
        
        if change['has_data']:
            report += f"📊 SOL Liquidity:\n"
            report += f"   Initial:  {change['initial_sol']:,.2f} SOL\n"
            report += f"   Current:  {change['current_sol']:,.2f} SOL\n"
            report += f"   Change:   {change['sol_change']:+,.2f} SOL ({change['sol_change_pct']:+.2f}%)\n\n"
            
            report += f"🪙 Token Liquidity:\n"
            report += f"   Initial:  {change['initial_token']:,.0f} tokens\n"
            report += f"   Current:  {change['current_token']:,.0f} tokens\n"
            report += f"   Change:   {change['token_change']:+,.0f} tokens ({change['token_change_pct']:+.2f}%)\n\n"
            
            report += f"📈 Trend: {trend.replace('_', ' ')}\n"
            report += f"📝 Total transactions tracked: {len(self.liquidity_history)}\n"
        else:
            last = self.liquidity_history[-1]
            report += f"Current SOL Liquidity: {last['sol_liquidity']:,.2f} SOL\n"
            report += f"Current Token Liquidity: {last['token_liquidity']:,.0f} tokens\n"
        
        return report

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

tracker = LiquidityTracker(client, "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")

# Collect data over time
import time
for i in range(10):
    new_data = tracker.update_liquidity_data()
    if new_data:
        print(f"✅ New liquidity data: {new_data['sol_liquidity']:.2f} SOL")
    time.sleep(30)

# Generate report
print("\n" + tracker.get_report())
```

### Example 4: Transaction Frequency Analyzer
```python
from collections import deque
from datetime import datetime, timedelta

class FrequencyAnalyzer:
    """Analyze transaction frequency and velocity"""
    
    def __init__(self, client: AxiomClient, pair_address: str, window_minutes: int = 60):
        self.client = client
        self.pair_address = pair_address
        self.window_minutes = window_minutes
        self.transactions = deque()  # Store recent transactions
        self.last_signature = None
        
    def add_transaction(self, tx: Dict) -> bool:
        """Add new transaction to the tracking window"""
        if tx['signature'] == self.last_signature:
            return False
        
        self.last_signature = tx['signature']
        tx_time = datetime.fromtimestamp(tx['createdAt'] / 1000)
        
        # Add to deque
        self.transactions.append({
            'signature': tx['signature'],
            'timestamp': tx_time,
            'type': tx['type'],
            'volume_usd': tx['totalUsd']
        })
        
        # Remove transactions outside window
        cutoff_time = datetime.now() - timedelta(minutes=self.window_minutes)
        while self.transactions and self.transactions[0]['timestamp'] < cutoff_time:
            self.transactions.popleft()
        
        return True
    
    def get_frequency_metrics(self) -> Dict:
        """Calculate frequency metrics"""
        if not self.transactions:
            return {'has_data': False}
        
        count = len(self.transactions)
        
        # Calculate average time between transactions
        if count > 1:
            first_time = self.transactions[0]['timestamp']
            last_time = self.transactions[-1]['timestamp']
            time_span = (last_time - first_time).total_seconds()
            avg_interval_seconds = time_span / (count - 1) if count > 1 else 0
        else:
            avg_interval_seconds = 0
        
        # Calculate buy/sell ratio
        buys = sum(1 for tx in self.transactions if tx['type'] == 'buy')
        sells = count - buys
        
        # Calculate total volume
        total_volume = sum(tx['volume_usd'] for tx in self.transactions)
        avg_trade_size = total_volume / count if count > 0 else 0
        
        # Transactions per minute
        tx_per_minute = count / self.window_minutes
        
        return {
            'has_data': True,
            'count': count,
            'buys': buys,
            'sells': sells,
            'buy_sell_ratio': buys / sells if sells > 0 else float('inf'),
            'total_volume_usd': total_volume,
            'avg_trade_size_usd': avg_trade_size,
            'avg_interval_seconds': avg_interval_seconds,
            'tx_per_minute': tx_per_minute,
            'window_minutes': self.window_minutes
        }
    
    def classify_activity_level(self, tx_per_minute: float) -> str:
        """Classify activity level based on frequency"""
        if tx_per_minute > 2:
            return "🔥 VERY_HIGH"
        elif tx_per_minute > 1:
            return "📈 HIGH"
        elif tx_per_minute > 0.5:
            return "📊 MODERATE"
        elif tx_per_minute > 0.1:
            return "📉 LOW"
        else:
            return "💤 VERY_LOW"
    
    def monitor_frequency(self, check_interval: int = 30, duration_minutes: int = 60):
        """Monitor transaction frequency"""
        print(f"⏱️  Frequency Analyzer Started")
        print(f"   Window: {self.window_minutes} minutes")
        print(f"   Check interval: {check_interval}s")
        print(f"   Duration: {duration_minutes} minutes\n")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            try:
                # Get latest transaction
                last_tx = self.client.get_last_transaction(self.pair_address)
                
                # Add to tracker
                if self.add_transaction(last_tx):
                    print(f"📝 New {last_tx['type'].upper()} transaction detected")
                    print(f"   Volume: ${last_tx['totalUsd']:.2f}")
                    
                    # Show current metrics
                    metrics = self.get_frequency_metrics()
                    if metrics['has_data']:
                        activity = self.classify_activity_level(metrics['tx_per_minute'])
                        print(f"   Activity: {activity}")
                        print(f"   Frequency: {metrics['tx_per_minute']:.2f} tx/min")
                        print(f"   Total in window: {metrics['count']} transactions\n")
                
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(check_interval)
        
        # Final report
        print(f"\n{'='*60}")
        print("📊 Final Frequency Report")
        print(f"{'='*60}")
        
        metrics = self.get_frequency_metrics()
        if metrics['has_data']:
            print(f"Total transactions: {metrics['count']}")
            print(f"Buys: {metrics['buys']} | Sells: {metrics['sells']}")
            print(f"Buy/Sell Ratio: {metrics['buy_sell_ratio']:.2f}")
            print(f"Total Volume: ${metrics['total_volume_usd']:,.2f}")
            print(f"Average Trade Size: ${metrics['avg_trade_size_usd']:.2f}")
            print(f"Frequency: {metrics['tx_per_minute']:.2f} tx/min")
            print(f"Avg Interval: {metrics['avg_interval_seconds']:.1f}s between trades")
            print(f"Activity Level: {self.classify_activity_level(metrics['tx_per_minute'])}")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

analyzer = FrequencyAnalyzer(
    client,
    "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY",
    window_minutes=30
)
analyzer.monitor_frequency(check_interval=20, duration_minutes=10)
```

### Example 5: Price Feed Generator
```python
import time
from typing import Optional, Dict
from datetime import datetime

class PriceFeed:
    """Generate real-time price feed from last transaction"""
    
    def __init__(self, client: AxiomClient, pair_address: str):
        self.client = client
        self.pair_address = pair_address
        self.current_price_usd = None
        self.current_price_sol = None
        self.last_update = None
        self.last_signature = None
        self.update_count = 0
        
    def update(self) -> bool:
        """Update price from latest transaction"""
        try:
            last_tx = self.client.get_last_transaction(self.pair_address)
            
            # Check if this is new data
            if last_tx['signature'] == self.last_signature:
                return False
            
            # Update price data
            self.last_signature = last_tx['signature']
            self.current_price_usd = last_tx['priceUsd']
            self.current_price_sol = last_tx['priceSol']
            self.last_update = datetime.fromtimestamp(last_tx['createdAt'] / 1000)
            self.update_count += 1
            
            return True
            
        except Exception as e:
            print(f"Error updating price: {e}")
            return False
    
    def get_price(self, currency: str = "USD") -> Optional[float]:
        """Get current price in specified currency"""
        if currency.upper() == "USD":
            return self.current_price_usd
        elif currency.upper() == "SOL":
            return self.current_price_sol
        else:
            return None
    
    def get_age_seconds(self) -> Optional[float]:
        """Get age of current price in seconds"""
        if not self.last_update:
            return None
        return (datetime.now() - self.last_update).total_seconds()
    
    def is_stale(self, threshold_seconds: int = 300) -> bool:
        """Check if price data is stale"""
        age = self.get_age_seconds()
        return age is None or age > threshold_seconds
    
    def format_price_display(self) -> str:
        """Format price for display"""
        if self.current_price_usd is None:
            return "No price data available"
        
        age = self.get_age_seconds()
        age_str = f"{age:.0f}s ago" if age else "Unknown age"
        
        stale_indicator = " ⚠️ STALE" if self.is_stale() else " ✅"
        
        display = f"💰 Price Feed{stale_indicator}\n"
        display += f"   USD: ${self.current_price_usd:.8f}\n"
        display += f"   SOL: {self.current_price_sol:.6f} SOL\n"
        display += f"   Updated: {age_str}\n"
        display += f"   Updates: {self.update_count}"
        
        return display
    
    def run_feed(self, check_interval: int = 10, display_always: bool = False):
        """Run continuous price feed"""
        print(f"💰 Starting Price Feed")
        print(f"   Pair: {self.pair_address[:8]}...")
        print(f"   Check interval: {check_interval}s\n")
        
        while True:
            updated = self.update()
            
            # Display price (always or only on update)
            if updated or display_always:
                print(f"\r{self.format_price_display()}", end='\n\n')
            
            time.sleep(check_interval)

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

feed = PriceFeed(client, "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
feed.run_feed(check_interval=15, display_always=True)
```

### Example 6: Multi-Pair Comparison Dashboard
```python
from typing import List, Dict
from datetime import datetime
import time

class MultiPairDashboard:
    """Monitor multiple pairs simultaneously"""
    
    def __init__(self, client: AxiomClient, pair_addresses: List[str]):
        self.client = client
        self.pairs = {addr: self._init_pair_data(addr) for addr in pair_addresses}
        
    def _init_pair_data(self, pair_address: str) -> Dict:
        """Initialize tracking data for a pair"""
        return {
            'address': pair_address,
            'last_signature': None,
            'price_usd': None,
            'price_sol': None,
            'last_tx_type': None,
            'last_tx_time': None,
            'last_tx_volume': None,
            'update_count': 0
        }
    
    def update_pair(self, pair_address: str) -> bool:
        """Update data for a specific pair"""
        try:
            last_tx = self.client.get_last_transaction(pair_address)
            pair_data = self.pairs[pair_address]
            
            # Check if new data
            if last_tx['signature'] == pair_data['last_signature']:
                return False
            
            # Update data
            pair_data['last_signature'] = last_tx['signature']
            pair_data['price_usd'] = last_tx['priceUsd']
            pair_data['price_sol'] = last_tx['priceSol']
            pair_data['last_tx_type'] = last_tx['type']
            pair_data['last_tx_time'] = datetime.fromtimestamp(last_tx['createdAt'] / 1000)
            pair_data['last_tx_volume'] = last_tx['totalUsd']
            pair_data['update_count'] += 1
            
            return True
            
        except Exception as e:
            print(f"Error updating {pair_address[:8]}: {e}")
            return False
    
    def update_all(self) -> int:
        """Update all pairs, return count of updated pairs"""
        updated_count = 0
        for pair_address in self.pairs.keys():
            if self.update_pair(pair_address):
                updated_count += 1
        return updated_count
    
    def get_dashboard_display(self) -> str:
        """Generate dashboard display"""
        display = f"\n{'='*80}\n"
        display += f"📊 Multi-Pair Dashboard - {datetime.now().strftime('%H:%M:%S')}\n"
        display += f"{'='*80}\n\n"
        
        for pair_data in self.pairs.values():
            addr_short = pair_data['address'][:8] + "..."
            
            if pair_data['price_usd'] is None:
                display += f"❓ {addr_short} - No data yet\n\n"
                continue
            
            # Calculate time since last trade
            time_ago = (datetime.now() - pair_data['last_tx_time']).total_seconds()
            time_str = f"{time_ago:.0f}s ago" if time_ago < 60 else f"{time_ago/60:.1f}m ago"
            
            # Transaction type indicator
            tx_icon = "📈" if pair_data['last_tx_type'] == "buy" else "📉"
            
            display += f"{tx_icon} {addr_short}\n"
            display += f"   Price: ${pair_data['price_usd']:.8f} ({pair_data['price_sol']:.6f} SOL)\n"
            display += f"   Last: {pair_data['last_tx_type'].upper()} ${pair_data['last_tx_volume']:.2f} - {time_str}\n"
            display += f"   Updates: {pair_data['update_count']}\n\n"
        
        return display
    
    def find_most_active(self) -> Optional[str]:
        """Find the most active pair (most recent transaction)"""
        most_recent_pair = None
        most_recent_time = None
        
        for pair_address, pair_data in self.pairs.items():
            if pair_data['last_tx_time']:
                if most_recent_time is None or pair_data['last_tx_time'] > most_recent_time:
                    most_recent_time = pair_data['last_tx_time']
                    most_recent_pair = pair_address
        
        return most_recent_pair
    
    def find_best_performer(self) -> Optional[str]:
        """Find pair with highest price (simple comparison)"""
        best_pair = None
        highest_price = 0
        
        for pair_address, pair_data in self.pairs.items():
            if pair_data['price_usd'] and pair_data['price_usd'] > highest_price:
                highest_price = pair_data['price_usd']
                best_pair = pair_address
        
        return best_pair
    
    def run_dashboard(self, update_interval: int = 20):
        """Run the dashboard with periodic updates"""
        print("🚀 Multi-Pair Dashboard Started")
        print(f"   Monitoring {len(self.pairs)} pairs")
        print(f"   Update interval: {update_interval}s\n")
        
        while True:
            # Update all pairs
            updated_count = self.update_all()
            
            # Display dashboard
            print(self.get_dashboard_display())
            
            # Show insights
            if updated_count > 0:
                most_active = self.find_most_active()
                if most_active:
                    print(f"🔥 Most Active: {most_active[:8]}...")
            
            print(f"⏱️  Next update in {update_interval}s...\n")
            time.sleep(update_interval)

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

# Monitor multiple pairs
pairs = [
    "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY",
    "AnotherPairAddress123456789",
    "YetAnotherPairAddress987654"
]

dashboard = MultiPairDashboard(client, pairs)
dashboard.run_dashboard(update_interval=30)
```

### Example 7: Smart Entry Signal Generator
```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

class EntrySignalGenerator:
    """Generate buy signals based on last transaction analysis"""
    
    def __init__(self, client: AxiomClient, pair_address: str):
        self.client = client
        self.pair_address = pair_address
        self.price_history: List[Dict] = []
        self.last_signature = None
        
        # Signal parameters
        self.dip_threshold_pct = -5  # Look for 5% dips
        self.volume_spike_multiplier = 2  # Volume 2x average
        self.min_liquidity_sol = 50  # Minimum liquidity
        
    def update_history(self) -> bool:
        """Update price history from last transaction"""
        try:
            last_tx = self.client.get_last_transaction(self.pair_address)
            
            if last_tx['signature'] == self.last_signature:
                return False
            
            self.last_signature = last_tx['signature']
            
            self.price_history.append({
                'timestamp': datetime.fromtimestamp(last_tx['createdAt'] / 1000),
                'price_usd': last_tx['priceUsd'],
                'price_sol': last_tx['priceSol'],
                'volume_usd': last_tx['totalUsd'],
                'type': last_tx['type'],
                'liquidity_sol': last_tx['liquiditySol']
            })
            
            # Keep only last hour of data
            cutoff = datetime.now() - timedelta(hours=1)
            self.price_history = [p for p in self.price_history if p['timestamp'] > cutoff]
            
            return True
            
        except Exception as e:
            print(f"Error updating history: {e}")
            return False
    
    def calculate_average_volume(self) -> float:
        """Calculate average volume from history"""
        if not self.price_history:
            return 0
        return sum(p['volume_usd'] for p in self.price_history) / len(self.price_history)
    
    def get_price_change_pct(self, lookback_minutes: int = 15) -> Optional[float]:
        """Calculate price change over lookback period"""
        if not self.price_history:
            return None
        
        cutoff = datetime.now() - timedelta(minutes=lookback_minutes)
        recent_prices = [p for p in self.price_history if p['timestamp'] > cutoff]
        
        if len(recent_prices) < 2:
            return None
        
        first_price = recent_prices[0]['price_usd']
        last_price = recent_prices[-1]['price_usd']
        
        return ((last_price - first_price) / first_price) * 100
    
    def check_dip_signal(self) -> Dict:
        """Check for price dip entry signal"""
        change_pct = self.get_price_change_pct(lookback_minutes=15)
        
        if change_pct is None or change_pct > self.dip_threshold_pct:
            return {'signal': False, 'reason': 'No significant dip'}
        
        # Check if liquidity is sufficient
        if self.price_history:
            current_liquidity = self.price_history[-1]['liquidity_sol']
            if current_liquidity < self.min_liquidity_sol:
                return {'signal': False, 'reason': 'Insufficient liquidity'}
        
        return {
            'signal': True,
            'type': 'DIP_BUY',
            'reason': f'Price dipped {change_pct:.2f}%',
            'current_price': self.price_history[-1]['price_usd'],
            'liquidity_sol': self.price_history[-1]['liquidity_sol']
        }
    
    def check_volume_spike_signal(self) -> Dict:
        """Check for volume spike signal"""
        if len(self.price_history) < 5:
            return {'signal': False, 'reason': 'Insufficient history'}
        
        avg_volume = self.calculate_average_volume()
        current_volume = self.price_history[-1]['volume_usd']
        
        if current_volume < avg_volume * self.volume_spike_multiplier:
            return {'signal': False, 'reason': 'No volume spike'}
        
        # Check if it's a buy transaction (bullish)
        if self.price_history[-1]['type'] != 'buy':
            return {'signal': False, 'reason': 'Volume spike on sell'}
        
        return {
            'signal': True,
            'type': 'VOLUME_SPIKE',
            'reason': f'Buy volume {current_volume/avg_volume:.1f}x average',
            'current_price': self.price_history[-1]['price_usd'],
            'volume': current_volume,
            'avg_volume': avg_volume
        }
    
    def check_momentum_signal(self) -> Dict:
        """Check for positive momentum signal"""
        if len(self.price_history) < 3:
            return {'signal': False, 'reason': 'Insufficient history'}
        
        # Check last 3 transactions
        last_three = self.price_history[-3:]
        
        # All three should be buys
        all_buys = all(tx['type'] == 'buy' for tx in last_three)
        if not all_buys:
            return {'signal': False, 'reason': 'Not all recent transactions are buys'}
        
        # Price should be trending up
        prices = [tx['price_usd'] for tx in last_three]
        is_uptrend = prices[0] < prices[1] < prices[2]
        
        if not is_uptrend:
            return {'signal': False, 'reason': 'No clear uptrend'}
        
        price_increase = ((prices[-1] - prices[0]) / prices[0]) * 100
        
        return {
            'signal': True,
            'type': 'MOMENTUM',
            'reason': f'3 consecutive buys, price up {price_increase:.2f}%',
            'current_price': prices[-1]
        }
    
    def check_all_signals(self) -> List[Dict]:
        """Check all signal types"""
        signals = []
        
        dip_signal = self.check_dip_signal()
        if dip_signal['signal']:
            signals.append(dip_signal)
        
        volume_signal = self.check_volume_spike_signal()
        if volume_signal['signal']:
            signals.append(volume_signal)
        
        momentum_signal = self.check_momentum_signal()
        if momentum_signal['signal']:
            signals.append(momentum_signal)
        
        return signals
    
    def run_signal_generator(self, check_interval: int = 30):
        """Run continuous signal generation"""
        print(f"🎯 Entry Signal Generator Started")
        print(f"   Pair: {self.pair_address[:8]}...")
        print(f"   Check interval: {check_interval}s")
        print(f"   Dip threshold: {self.dip_threshold_pct}%")
        print(f"   Volume spike: {self.volume_spike_multiplier}x")
        print(f"   Min liquidity: {self.min_liquidity_sol} SOL\n")
        
        while True:
            if self.update_history():
                # Check for signals
                signals = self.check_all_signals()
                
                if signals:
                    print(f"\n🚨 {'='*60}")
                    print(f"   ENTRY SIGNALS DETECTED - {datetime.now().strftime('%H:%M:%S')}")
                    print(f"{'='*60}")
                    
                    for signal in signals:
                        print(f"\n📊 {signal['type']}")
                        print(f"   Reason: {signal['reason']}")
                        print(f"   Price: ${signal['current_price']:.8f}")
                        
                        if 'liquidity_sol' in signal:
                            print(f"   Liquidity: {signal['liquidity_sol']:.2f} SOL")
                        
                        if 'volume' in signal:
                            print(f"   Volume: ${signal['volume']:.2f}")
                    
                    print(f"\n{'='*60}\n")
            
            time.sleep(check_interval)

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

generator = EntrySignalGenerator(client, "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
generator.dip_threshold_pct = -3  # More sensitive to dips
generator.volume_spike_multiplier = 1.5  # Lower threshold for volume
generator.run_signal_generator(check_interval=20)
```

---

## Best Practices

### 1. **Handle Rate Limits** ⚠️
```python
import time
from requests.exceptions import HTTPError

def get_last_tx_with_retry(client, pair_address, max_retries=3):
    """Get last transaction with retry logic"""
    for attempt in range(max_retries):
        try:
            return client.get_last_transaction(pair_address)
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = (attempt + 1) * 2
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### 2. **Cache Transaction Data** 💾
```python
# Don't poll too frequently
last_check = None
cache_duration = 10  # seconds

def get_cached_transaction(client, pair_address):
    global last_check, cached_data
    
    now = time.time()
    if last_check and (now - last_check) < cache_duration:
        return cached_data
    
    cached_data = client.get_last_transaction(pair_address)
    last_check = now
    return cached_data
```

### 3. **Validate Pair Address** ✅
```python
def is_valid_solana_address(address: str) -> bool:
    """Basic validation for Solana address"""
    return len(address) >= 32 and len(address) <= 44 and address.isalnum()

# Use before API call
if not is_valid_solana_address(pair_address):
    raise ValueError("Invalid pair address format")
```

### 4. **Monitor Data Freshness** 🕐
```python
from datetime import datetime, timedelta

def is_data_fresh(last_tx, max_age_minutes=5):
    """Check if transaction data is recent"""
    tx_time = datetime.fromtimestamp(last_tx['createdAt'] / 1000)
    age = datetime.now() - tx_time
    return age < timedelta(minutes=max_age_minutes)

# Usage
last_tx = client.get_last_transaction(pair_address)
if not is_data_fresh(last_tx):
    print("⚠️  Warning: Data may be stale")
```

### 5. **Handle Missing Data Gracefully** 🛡️
```python
def safe_get_last_transaction(client, pair_address):
    """Safely get last transaction with error handling"""
    try:
        last_tx = client.get_last_transaction(pair_address)
        
        # Validate essential fields
        required_fields = ['signature', 'priceUsd', 'type']
        for field in required_fields:
            if field not in last_tx:
                raise ValueError(f"Missing field: {field}")
        
        return last_tx
        
    except Exception as e:
        print(f"Error getting transaction: {e}")
        return None
```

### 6. **Use Appropriate Polling Intervals** ⏱️
```python
# For high-frequency monitoring
high_frequency_interval = 5  # seconds (active trading)

# For price displays
medium_frequency_interval = 15  # seconds (dashboards)

# For background monitoring
low_frequency_interval = 60  # seconds (alerts)

# Choose based on your use case
time.sleep(medium_frequency_interval)
```

### 7. **Log Transaction Signatures** 📝
```python
def track_transactions(client, pair_address, log_file="transactions.log"):
    """Log transactions for audit trail"""
    last_tx = client.get_last_transaction(pair_address)
    
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()},{last_tx['signature']},{last_tx['type']},{last_tx['priceUsd']}\n")
```

---

## Troubleshooting

### Issue: "Authentication failed"
**Solution**: Ensure you're logged in before calling the method
```python
client = AxiomClient()
if not client.is_authenticated():
    client.login(email="your@email.com", password="your_password")

last_tx = client.get_last_transaction(pair_address)
```

### Issue: "Failed to get last transaction"
**Solution**: Verify the pair address is correct and active
```python
# Test with a known active pair first
test_pair = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"
try:
    test_tx = client.get_last_transaction(test_pair)
    print("API working correctly")
except Exception as e:
    print(f"API issue: {e}")
```

### Issue: Rate limiting (429 errors)
**Solution**: Implement exponential backoff and reduce polling frequency
```python
import time
from requests.exceptions import HTTPError

def get_tx_with_backoff(client, pair_address):
    backoff = 1
    max_backoff = 32
    
    while True:
        try:
            return client.get_last_transaction(pair_address)
        except HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limited. Waiting {backoff}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)
            else:
                raise
```

### Issue: Stale data (old transaction)
**Solution**: Check transaction timestamp and handle appropriately
```python
last_tx = client.get_last_transaction(pair_address)
tx_age_seconds = (time.time() * 1000 - last_tx['createdAt']) / 1000

if tx_age_seconds > 300:  # 5 minutes
    print(f"⚠️  Data is {tx_age_seconds/60:.1f} minutes old")
    print("Pair may have low trading activity")
```

### Issue: Incomplete data in response
**Solution**: Validate response structure before using
```python
def validate_transaction_data(tx_data):
    """Validate transaction has required fields"""
    required_fields = [
        'signature', 'pairAddress', 'type', 'createdAt',
        'priceUsd', 'priceSol', 'liquiditySol'
    ]
    
    missing = [f for f in required_fields if f not in tx_data]
    if missing:
        raise ValueError(f"Missing fields: {missing}")
    
    return True

# Usage
last_tx = client.get_last_transaction(pair_address)
validate_transaction_data(last_tx)
```

### Issue: Network timeouts
**Solution**: Configure timeout settings and implement retry logic
```python
from requests.exceptions import Timeout

def get_tx_with_timeout(client, pair_address, timeout=10, retries=3):
    """Get transaction with timeout handling"""
    for attempt in range(retries):
        try:
            # Note: You may need to modify client's request timeout
            return client.get_last_transaction(pair_address)
        except Timeout:
            if attempt < retries - 1:
                print(f"Timeout. Retry {attempt + 1}/{retries}")
                time.sleep(2)
            else:
                raise Exception("Request timed out after retries")
```

---

## Related Methods

- **[`get_pair_info()`](./get-pair-info-guide.md)** - Get comprehensive pair information including liquidity, volume, and holder data
- **[`get_pair_stats()`](./get-pair-stats-guide.md)** - Get statistical data and trends for a trading pair
- **[`get_token_info()`](./get-token-info-guide.md)** - Get detailed token information by mint address
- **[`get_token_info_by_pair()`](./get-token-info-by-pair-guide.md)** - Get token information using pair address
- **[`buy_token()`](./buy-token-guide.md)** - Execute a token purchase based on latest price data
- **[`sell_token()`](./sell-token-guide.md)** - Execute a token sale based on latest price data

---

## Summary

The `get_last_transaction()` method is essential for:

✅ **Real-Time Price Tracking** - Get the most current transaction price  
✅ **Activity Monitoring** - Detect trading activity and patterns  
✅ **Liquidity Analysis** - Monitor pool liquidity changes over time  
✅ **Trading Bot Logic** - Base automated decisions on latest market data  
✅ **Alert Systems** - Trigger notifications on specific transaction events  
✅ **Price Feeds** - Build real-time price display systems  
✅ **Market Analysis** - Track transaction frequency and volume patterns

### Key Features:
- 📊 Complete transaction details (price, volume, liquidity)
- 🕐 Millisecond precision timestamps
- 💰 USD and SOL price values
- 📈 Buy/sell transaction type
- 💧 Post-transaction liquidity levels
- 🔗 Blockchain signature for verification

### Important Notes:
⚠️ **Data Freshness**: Transaction data reflects the last trade, which may be minutes or hours old for low-activity pairs  
⚠️ **Rate Limiting**: Don't poll too frequently; implement caching and reasonable intervals  
⚠️ **Validation**: Always validate pair address format before making requests  
⚠️ **Error Handling**: Implement robust retry logic for network issues  
⚠️ **Liquidity**: Low liquidity pairs may have infrequent transactions

---

**💡 Pro Tip**: Combine `get_last_transaction()` with `get_pair_info()` for a complete market picture. The last transaction gives you real-time price action, while pair info provides context like total liquidity, holder count, and 24h volume!
