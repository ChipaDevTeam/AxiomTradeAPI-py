# get_meme_open_positions() - Complete Guide 💼

## Overview

The `get_meme_open_positions()` method retrieves all open (active) meme token positions for a specific wallet address. This is crucial for:

- 💼 **Portfolio Tracking** - Monitor all active token holdings
- 📊 **Position Analysis** - Analyze profit/loss across positions
- 🎯 **Risk Management** - Track exposure across multiple tokens
- 🤖 **Trading Bot Portfolio** - Manage multiple simultaneous positions
- 📈 **Performance Monitoring** - Track unrealized gains/losses
- 💰 **Value Calculation** - Calculate total portfolio value
- 🔍 **Position Discovery** - Find all tokens held by a wallet

---

## Method Signature

```python
def get_meme_open_positions(self, wallet_address: str) -> Dict
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `wallet_address` | `str` | ✅ Yes | The Solana wallet address to query for open positions |

### Return Value

Returns a `Dict` containing open positions data:

```python
{
    "positions": [
        {
            "tokenAddress": str,        # Token mint address
            "tokenSymbol": str,         # Token symbol (e.g., "BONK")
            "tokenName": str,           # Token name
            "pairAddress": str,         # Trading pair address
            "amount": float,            # Token amount held
            "avgBuyPrice": float,       # Average purchase price (USD)
            "currentPrice": float,      # Current market price (USD)
            "value": float,             # Current position value (USD)
            "cost": float,              # Total cost basis (USD)
            "pnl": float,               # Unrealized profit/loss (USD)
            "pnlPercent": float,        # Unrealized PnL percentage
            "buyTransactions": int,     # Number of buy transactions
            "lastBuyTime": int,         # Last purchase timestamp (ms)
            "holdingTime": int          # Time held in seconds
        }
    ],
    "summary": {
        "totalPositions": int,          # Total number of positions
        "totalValue": float,            # Total portfolio value (USD)
        "totalCost": float,             # Total cost basis (USD)
        "totalPnl": float,              # Total unrealized PnL (USD)
        "totalPnlPercent": float,       # Overall PnL percentage
        "winningPositions": int,        # Positions with positive PnL
        "losingPositions": int          # Positions with negative PnL
    }
}
```

---

## Basic Examples

### Example 1: Get All Open Positions
```python
from axiomtradeapi import AxiomClient

client = AxiomClient()
client.login(email="your@email.com", password="your_password")

# Get open positions for a wallet
wallet = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
positions = client.get_meme_open_positions(wallet)

print(f"Total positions: {positions['summary']['totalPositions']}")
print(f"Total value: ${positions['summary']['totalValue']:,.2f}")
print(f"Total PnL: ${positions['summary']['totalPnl']:,.2f} ({positions['summary']['totalPnlPercent']:.2f}%)")
```

### Example 2: List All Positions
```python
wallet = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
positions = client.get_meme_open_positions(wallet)

print("\n📊 Open Positions:\n")
for pos in positions['positions']:
    pnl_icon = "🟢" if pos['pnl'] > 0 else "🔴"
    print(f"{pnl_icon} {pos['tokenSymbol']}")
    print(f"   Amount: {pos['amount']:,.0f} tokens")
    print(f"   Value: ${pos['value']:,.2f}")
    print(f"   PnL: ${pos['pnl']:,.2f} ({pos['pnlPercent']:.2f}%)")
    print()
```

### Example 3: Find Best and Worst Performers
```python
wallet = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
positions = client.get_meme_open_positions(wallet)

if positions['positions']:
    # Sort by PnL percentage
    sorted_positions = sorted(positions['positions'], key=lambda x: x['pnlPercent'], reverse=True)
    
    best = sorted_positions[0]
    worst = sorted_positions[-1]
    
    print(f"🏆 Best Performer: {best['tokenSymbol']}")
    print(f"   PnL: {best['pnlPercent']:.2f}%")
    
    print(f"\n💔 Worst Performer: {worst['tokenSymbol']}")
    print(f"   PnL: {worst['pnlPercent']:.2f}%")
```

---

## Advanced Examples

### Example 1: Portfolio Dashboard
```python
from typing import Dict, List
from datetime import datetime

class PortfolioDashboard:
    """Comprehensive portfolio dashboard for meme positions"""
    
    def __init__(self, client: AxiomClient, wallet_address: str):
        self.client = client
        self.wallet_address = wallet_address
        self.positions_data = None
        
    def refresh(self) -> bool:
        """Refresh portfolio data"""
        try:
            self.positions_data = self.client.get_meme_open_positions(self.wallet_address)
            return True
        except Exception as e:
            print(f"Error refreshing portfolio: {e}")
            return False
    
    def get_position_categories(self) -> Dict:
        """Categorize positions by performance"""
        if not self.positions_data:
            return {}
        
        categories = {
            'moon_shots': [],      # >100% gain
            'winners': [],         # 20-100% gain
            'slight_winners': [],  # 0-20% gain
            'slight_losers': [],   # 0 to -20% loss
            'losers': [],          # -20 to -50% loss
            'dead': []             # <-50% loss
        }
        
        for pos in self.positions_data['positions']:
            pnl_pct = pos['pnlPercent']
            
            if pnl_pct > 100:
                categories['moon_shots'].append(pos)
            elif pnl_pct > 20:
                categories['winners'].append(pos)
            elif pnl_pct > 0:
                categories['slight_winners'].append(pos)
            elif pnl_pct > -20:
                categories['slight_losers'].append(pos)
            elif pnl_pct > -50:
                categories['losers'].append(pos)
            else:
                categories['dead'].append(pos)
        
        return categories
    
    def get_concentration_risk(self) -> List[Dict]:
        """Calculate position concentration"""
        if not self.positions_data:
            return []
        
        total_value = self.positions_data['summary']['totalValue']
        
        concentration = []
        for pos in self.positions_data['positions']:
            pct_of_portfolio = (pos['value'] / total_value * 100) if total_value > 0 else 0
            concentration.append({
                'symbol': pos['tokenSymbol'],
                'value': pos['value'],
                'percentage': pct_of_portfolio
            })
        
        return sorted(concentration, key=lambda x: x['percentage'], reverse=True)
    
    def get_risk_metrics(self) -> Dict:
        """Calculate portfolio risk metrics"""
        if not self.positions_data:
            return {}
        
        positions = self.positions_data['positions']
        summary = self.positions_data['summary']
        
        # Calculate average position size
        avg_position_size = summary['totalValue'] / summary['totalPositions'] if summary['totalPositions'] > 0 else 0
        
        # Find largest position
        largest_pos = max(positions, key=lambda x: x['value']) if positions else None
        largest_pos_pct = (largest_pos['value'] / summary['totalValue'] * 100) if largest_pos and summary['totalValue'] > 0 else 0
        
        # Calculate win rate
        win_rate = (summary['winningPositions'] / summary['totalPositions'] * 100) if summary['totalPositions'] > 0 else 0
        
        # Calculate average holding time
        avg_holding_time = sum(p['holdingTime'] for p in positions) / len(positions) if positions else 0
        avg_holding_days = avg_holding_time / 86400
        
        return {
            'avg_position_size': avg_position_size,
            'largest_position_pct': largest_pos_pct,
            'win_rate': win_rate,
            'avg_holding_days': avg_holding_days,
            'diversification': summary['totalPositions']
        }
    
    def display_dashboard(self):
        """Display comprehensive dashboard"""
        if not self.positions_data:
            print("No portfolio data. Call refresh() first.")
            return
        
        summary = self.positions_data['summary']
        
        print(f"\n{'='*80}")
        print(f"💼 PORTFOLIO DASHBOARD")
        print(f"{'='*80}")
        print(f"Wallet: {self.wallet_address[:8]}...{self.wallet_address[-8:]}")
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Summary section
        print("📊 SUMMARY")
        print(f"   Total Positions: {summary['totalPositions']}")
        print(f"   Portfolio Value: ${summary['totalValue']:,.2f}")
        print(f"   Cost Basis: ${summary['totalCost']:,.2f}")
        
        pnl_icon = "🟢" if summary['totalPnl'] > 0 else "🔴"
        print(f"   {pnl_icon} Total PnL: ${summary['totalPnl']:,.2f} ({summary['totalPnlPercent']:.2f}%)")
        print(f"   Winning: {summary['winningPositions']} | Losing: {summary['losingPositions']}\n")
        
        # Risk metrics
        risk = self.get_risk_metrics()
        print("⚠️  RISK METRICS")
        print(f"   Average Position: ${risk['avg_position_size']:,.2f}")
        print(f"   Largest Position: {risk['largest_position_pct']:.1f}% of portfolio")
        print(f"   Win Rate: {risk['win_rate']:.1f}%")
        print(f"   Avg Holding Time: {risk['avg_holding_days']:.1f} days")
        print(f"   Diversification: {risk['diversification']} positions\n")
        
        # Position categories
        categories = self.get_position_categories()
        print("🎯 POSITION BREAKDOWN")
        if categories['moon_shots']:
            print(f"   🚀 Moon Shots (>100%): {len(categories['moon_shots'])}")
        if categories['winners']:
            print(f"   🟢 Winners (20-100%): {len(categories['winners'])}")
        if categories['slight_winners']:
            print(f"   🟩 Slight Winners (0-20%): {len(categories['slight_winners'])}")
        if categories['slight_losers']:
            print(f"   🟨 Slight Losers (0 to -20%): {len(categories['slight_losers'])}")
        if categories['losers']:
            print(f"   🔴 Losers (-20 to -50%): {len(categories['losers'])}")
        if categories['dead']:
            print(f"   💀 Dead (<-50%): {len(categories['dead'])}")
        print()
        
        # Top 5 positions by value
        concentration = self.get_concentration_risk()
        print("💎 TOP 5 POSITIONS BY VALUE")
        for i, pos in enumerate(concentration[:5], 1):
            print(f"   {i}. {pos['symbol']}: ${pos['value']:,.2f} ({pos['percentage']:.1f}%)")
        print()
        
        # Detailed positions
        print("📋 ALL POSITIONS")
        print(f"{'='*80}")
        
        for pos in sorted(self.positions_data['positions'], key=lambda x: x['pnlPercent'], reverse=True):
            pnl_icon = "🟢" if pos['pnl'] > 0 else "🔴"
            holding_days = pos['holdingTime'] / 86400
            
            print(f"\n{pnl_icon} {pos['tokenSymbol']} ({pos['tokenName']})")
            print(f"   Amount: {pos['amount']:,.0f} tokens")
            print(f"   Avg Buy Price: ${pos['avgBuyPrice']:.8f}")
            print(f"   Current Price: ${pos['currentPrice']:.8f}")
            print(f"   Value: ${pos['value']:,.2f}")
            print(f"   PnL: ${pos['pnl']:,.2f} ({pos['pnlPercent']:.2f}%)")
            print(f"   Holding: {holding_days:.1f} days | Buys: {pos['buyTransactions']}")
            print(f"   Pair: {pos['pairAddress'][:8]}...")
        
        print(f"\n{'='*80}\n")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

dashboard = PortfolioDashboard(client, "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
dashboard.refresh()
dashboard.display_dashboard()
```

### Example 2: Position Rebalancer
```python
from typing import List, Dict

class PositionRebalancer:
    """Rebalance portfolio based on position sizes"""
    
    def __init__(self, client: AxiomClient, wallet_address: str):
        self.client = client
        self.wallet_address = wallet_address
        self.target_position_pct = 10  # Target 10% per position
        self.max_position_pct = 20     # Max 20% per position
        
    def get_rebalancing_actions(self) -> List[Dict]:
        """Calculate needed rebalancing actions"""
        try:
            positions_data = self.client.get_meme_open_positions(self.wallet_address)
        except Exception as e:
            print(f"Error getting positions: {e}")
            return []
        
        total_value = positions_data['summary']['totalValue']
        actions = []
        
        for pos in positions_data['positions']:
            current_pct = (pos['value'] / total_value * 100) if total_value > 0 else 0
            
            # Position too large - recommend selling
            if current_pct > self.max_position_pct:
                excess_pct = current_pct - self.target_position_pct
                excess_value = (excess_pct / 100) * total_value
                
                actions.append({
                    'action': 'SELL',
                    'symbol': pos['tokenSymbol'],
                    'reason': f'Position too large ({current_pct:.1f}% > {self.max_position_pct}%)',
                    'current_value': pos['value'],
                    'current_pct': current_pct,
                    'target_pct': self.target_position_pct,
                    'suggested_sell_value': excess_value,
                    'pair_address': pos['pairAddress']
                })
        
        return actions
    
    def display_rebalancing_plan(self):
        """Display rebalancing recommendations"""
        actions = self.get_rebalancing_actions()
        
        if not actions:
            print("✅ Portfolio is well balanced. No rebalancing needed.")
            return
        
        print(f"\n⚖️  REBALANCING PLAN")
        print(f"{'='*80}")
        print(f"Target Position Size: {self.target_position_pct}%")
        print(f"Maximum Position Size: {self.max_position_pct}%")
        print(f"{'='*80}\n")
        
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action['action']} {action['symbol']}")
            print(f"   Reason: {action['reason']}")
            print(f"   Current: ${action['current_value']:,.2f} ({action['current_pct']:.1f}%)")
            print(f"   Suggested Sell: ${action['suggested_sell_value']:,.2f}")
            print(f"   Pair: {action['pair_address'][:8]}...\n")
    
    def execute_rebalancing(self, dry_run: bool = True):
        """Execute rebalancing actions"""
        actions = self.get_rebalancing_actions()
        
        if not actions:
            print("No rebalancing needed.")
            return
        
        print(f"{'DRY RUN - ' if dry_run else ''}Executing {len(actions)} rebalancing actions...\n")
        
        for action in actions:
            if action['action'] == 'SELL':
                print(f"Selling ${action['suggested_sell_value']:,.2f} of {action['symbol']}...")
                
                if not dry_run:
                    try:
                        # Calculate amount to sell based on current price
                        # Note: You'd need to calculate the actual token amount
                        # result = self.client.sell_token(
                        #     pair_address=action['pair_address'],
                        #     amount=calculated_amount,
                        #     slippage=1.0
                        # )
                        print(f"   ✅ Sell order executed")
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
                else:
                    print(f"   [DRY RUN] Would sell here")
        
        print("\nRebalancing complete!")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

rebalancer = PositionRebalancer(client, "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
rebalancer.target_position_pct = 10
rebalancer.max_position_pct = 15
rebalancer.display_rebalancing_plan()

# Execute with dry run first
rebalancer.execute_rebalancing(dry_run=True)
```

### Example 3: Stop-Loss Monitor
```python
import time
from datetime import datetime
from typing import Dict, List

class StopLossMonitor:
    """Monitor positions and trigger stop-loss alerts"""
    
    def __init__(self, client: AxiomClient, wallet_address: str):
        self.client = client
        self.wallet_address = wallet_address
        self.stop_loss_pct = -20  # Default 20% stop loss
        self.take_profit_pct = 50  # Default 50% take profit
        self.positions_cache = {}
        
    def check_positions(self) -> List[Dict]:
        """Check all positions against stop-loss and take-profit levels"""
        try:
            positions_data = self.client.get_meme_open_positions(self.wallet_address)
        except Exception as e:
            print(f"Error checking positions: {e}")
            return []
        
        alerts = []
        
        for pos in positions_data['positions']:
            pnl_pct = pos['pnlPercent']
            
            # Stop-loss triggered
            if pnl_pct <= self.stop_loss_pct:
                alerts.append({
                    'type': 'STOP_LOSS',
                    'symbol': pos['tokenSymbol'],
                    'pnl_pct': pnl_pct,
                    'value': pos['value'],
                    'pnl': pos['pnl'],
                    'pair_address': pos['pairAddress'],
                    'severity': 'HIGH'
                })
            
            # Take-profit triggered
            elif pnl_pct >= self.take_profit_pct:
                alerts.append({
                    'type': 'TAKE_PROFIT',
                    'symbol': pos['tokenSymbol'],
                    'pnl_pct': pnl_pct,
                    'value': pos['value'],
                    'pnl': pos['pnl'],
                    'pair_address': pos['pairAddress'],
                    'severity': 'MEDIUM'
                })
            
            # Approaching stop-loss (within 5%)
            elif self.stop_loss_pct + 5 >= pnl_pct > self.stop_loss_pct:
                alerts.append({
                    'type': 'APPROACHING_STOP_LOSS',
                    'symbol': pos['tokenSymbol'],
                    'pnl_pct': pnl_pct,
                    'value': pos['value'],
                    'pnl': pos['pnl'],
                    'pair_address': pos['pairAddress'],
                    'severity': 'LOW'
                })
        
        return alerts
    
    def send_alert(self, alert: Dict):
        """Send alert (implement your notification method)"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if alert['type'] == 'STOP_LOSS':
            print(f"\n🚨 STOP-LOSS ALERT - {timestamp}")
            print(f"   {alert['symbol']}: {alert['pnl_pct']:.2f}%")
            print(f"   Loss: ${alert['pnl']:,.2f}")
            print(f"   Current Value: ${alert['value']:,.2f}")
            print(f"   RECOMMENDATION: SELL IMMEDIATELY")
            
        elif alert['type'] == 'TAKE_PROFIT':
            print(f"\n🎯 TAKE-PROFIT ALERT - {timestamp}")
            print(f"   {alert['symbol']}: +{alert['pnl_pct']:.2f}%")
            print(f"   Profit: ${alert['pnl']:,.2f}")
            print(f"   Current Value: ${alert['value']:,.2f}")
            print(f"   RECOMMENDATION: Consider taking profits")
            
        elif alert['type'] == 'APPROACHING_STOP_LOSS':
            print(f"\n⚠️  WARNING - {timestamp}")
            print(f"   {alert['symbol']}: {alert['pnl_pct']:.2f}%")
            print(f"   Approaching stop-loss threshold")
    
    def monitor(self, check_interval: int = 60):
        """Monitor positions continuously"""
        print(f"🔍 Stop-Loss Monitor Started")
        print(f"   Wallet: {self.wallet_address[:8]}...")
        print(f"   Stop-Loss: {self.stop_loss_pct}%")
        print(f"   Take-Profit: {self.take_profit_pct}%")
        print(f"   Check interval: {check_interval}s\n")
        
        while True:
            alerts = self.check_positions()
            
            # Send alerts for new or changed positions
            for alert in alerts:
                alert_key = f"{alert['symbol']}_{alert['type']}"
                
                # Check if this is a new alert
                if alert_key not in self.positions_cache:
                    self.send_alert(alert)
                    self.positions_cache[alert_key] = alert
            
            # Clean up resolved alerts
            current_alerts = {f"{a['symbol']}_{a['type']}" for a in alerts}
            resolved = set(self.positions_cache.keys()) - current_alerts
            
            for key in resolved:
                symbol = self.positions_cache[key]['symbol']
                alert_type = self.positions_cache[key]['type']
                print(f"✅ Resolved: {symbol} {alert_type}")
                del self.positions_cache[key]
            
            time.sleep(check_interval)

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

monitor = StopLossMonitor(client, "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
monitor.stop_loss_pct = -15  # 15% stop loss
monitor.take_profit_pct = 100  # 100% take profit
monitor.monitor(check_interval=30)
```

### Example 4: Performance Tracker
```python
import json
from datetime import datetime
from typing import Dict, List

class PerformanceTracker:
    """Track portfolio performance over time"""
    
    def __init__(self, client: AxiomClient, wallet_address: str, log_file: str = "performance.json"):
        self.client = client
        self.wallet_address = wallet_address
        self.log_file = log_file
        self.history = self._load_history()
        
    def _load_history(self) -> List[Dict]:
        """Load historical performance data"""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_history(self):
        """Save performance history"""
        with open(self.log_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def record_snapshot(self):
        """Record current portfolio snapshot"""
        try:
            positions_data = self.client.get_meme_open_positions(self.wallet_address)
            
            snapshot = {
                'timestamp': datetime.now().isoformat(),
                'total_value': positions_data['summary']['totalValue'],
                'total_cost': positions_data['summary']['totalCost'],
                'total_pnl': positions_data['summary']['totalPnl'],
                'total_pnl_pct': positions_data['summary']['totalPnlPercent'],
                'position_count': positions_data['summary']['totalPositions'],
                'winning_count': positions_data['summary']['winningPositions'],
                'losing_count': positions_data['summary']['losingPositions']
            }
            
            self.history.append(snapshot)
            self._save_history()
            
            print(f"✅ Snapshot recorded: ${snapshot['total_value']:,.2f} portfolio value")
            
        except Exception as e:
            print(f"Error recording snapshot: {e}")
    
    def get_performance_metrics(self) -> Dict:
        """Calculate performance metrics from history"""
        if len(self.history) < 2:
            return {'has_data': False}
        
        first = self.history[0]
        last = self.history[-1]
        
        # Calculate overall change
        value_change = last['total_value'] - first['total_value']
        value_change_pct = (value_change / first['total_value'] * 100) if first['total_value'] > 0 else 0
        
        # Calculate max drawdown
        peak_value = first['total_value']
        max_drawdown = 0
        
        for snapshot in self.history:
            if snapshot['total_value'] > peak_value:
                peak_value = snapshot['total_value']
            
            drawdown = ((peak_value - snapshot['total_value']) / peak_value * 100) if peak_value > 0 else 0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Calculate average daily PnL
        time_span_days = (datetime.fromisoformat(last['timestamp']) - 
                         datetime.fromisoformat(first['timestamp'])).days
        avg_daily_pnl = value_change / time_span_days if time_span_days > 0 else 0
        
        return {
            'has_data': True,
            'initial_value': first['total_value'],
            'current_value': last['total_value'],
            'value_change': value_change,
            'value_change_pct': value_change_pct,
            'max_drawdown': max_drawdown,
            'avg_daily_pnl': avg_daily_pnl,
            'days_tracked': time_span_days,
            'snapshots_count': len(self.history)
        }
    
    def generate_report(self):
        """Generate performance report"""
        metrics = self.get_performance_metrics()
        
        if not metrics['has_data']:
            print("Insufficient data for performance report. Need at least 2 snapshots.")
            return
        
        print(f"\n{'='*80}")
        print(f"📈 PERFORMANCE REPORT")
        print(f"{'='*80}")
        print(f"Wallet: {self.wallet_address[:8]}...{self.wallet_address[-8:]}")
        print(f"Tracking Period: {metrics['days_tracked']} days")
        print(f"Snapshots: {metrics['snapshots_count']}")
        print(f"{'='*80}\n")
        
        print("💰 VALUE METRICS")
        print(f"   Initial Value: ${metrics['initial_value']:,.2f}")
        print(f"   Current Value: ${metrics['current_value']:,.2f}")
        
        change_icon = "🟢" if metrics['value_change'] > 0 else "🔴"
        print(f"   {change_icon} Change: ${metrics['value_change']:,.2f} ({metrics['value_change_pct']:.2f}%)")
        print(f"   Avg Daily PnL: ${metrics['avg_daily_pnl']:,.2f}\n")
        
        print("⚠️  RISK METRICS")
        print(f"   Max Drawdown: {metrics['max_drawdown']:.2f}%\n")
        
        # Show recent trend
        print("📊 RECENT TREND (Last 5 snapshots)")
        recent = self.history[-5:]
        for snapshot in recent:
            timestamp = datetime.fromisoformat(snapshot['timestamp']).strftime('%Y-%m-%d %H:%M')
            pnl_icon = "🟢" if snapshot['total_pnl'] > 0 else "🔴"
            print(f"   {timestamp}: ${snapshot['total_value']:,.2f} {pnl_icon} {snapshot['total_pnl_pct']:.2f}%")
        
        print(f"\n{'='*80}\n")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

tracker = PerformanceTracker(client, "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")

# Record snapshots periodically
import time
for i in range(5):
    tracker.record_snapshot()
    time.sleep(60)  # Wait 1 minute between snapshots

# Generate report
tracker.generate_report()
```

### Example 5: Tax Reporting Helper
```python
from datetime import datetime
from typing import Dict, List

class TaxReportHelper:
    """Generate tax reporting data from open positions"""
    
    def __init__(self, client: AxiomClient, wallet_address: str):
        self.client = client
        self.wallet_address = wallet_address
        
    def generate_unrealized_gains_report(self) -> Dict:
        """Generate unrealized gains/losses report"""
        try:
            positions_data = self.client.get_meme_open_positions(self.wallet_address)
        except Exception as e:
            print(f"Error getting positions: {e}")
            return {}
        
        report = {
            'report_date': datetime.now().isoformat(),
            'wallet_address': self.wallet_address,
            'positions': [],
            'summary': {
                'total_unrealized_gains': 0,
                'total_unrealized_losses': 0,
                'total_cost_basis': 0,
                'total_current_value': 0
            }
        }
        
        for pos in positions_data['positions']:
            position_report = {
                'token_symbol': pos['tokenSymbol'],
                'token_name': pos['tokenName'],
                'token_address': pos['tokenAddress'],
                'quantity': pos['amount'],
                'cost_basis': pos['cost'],
                'current_value': pos['value'],
                'unrealized_pnl': pos['pnl'],
                'pnl_percentage': pos['pnlPercent'],
                'acquisition_date': datetime.fromtimestamp(pos['lastBuyTime'] / 1000).isoformat(),
                'holding_period_days': pos['holdingTime'] / 86400
            }
            
            report['positions'].append(position_report)
            
            # Update summary
            if pos['pnl'] > 0:
                report['summary']['total_unrealized_gains'] += pos['pnl']
            else:
                report['summary']['total_unrealized_losses'] += abs(pos['pnl'])
            
            report['summary']['total_cost_basis'] += pos['cost']
            report['summary']['total_current_value'] += pos['value']
        
        return report
    
    def identify_long_term_holdings(self, days_threshold: int = 365) -> List[Dict]:
        """Identify positions held for long-term (>1 year)"""
        try:
            positions_data = self.client.get_meme_open_positions(self.wallet_address)
        except Exception as e:
            print(f"Error getting positions: {e}")
            return []
        
        long_term = []
        
        for pos in positions_data['positions']:
            holding_days = pos['holdingTime'] / 86400
            
            if holding_days >= days_threshold:
                long_term.append({
                    'symbol': pos['tokenSymbol'],
                    'holding_days': holding_days,
                    'value': pos['value'],
                    'pnl': pos['pnl'],
                    'pnl_pct': pos['pnlPercent']
                })
        
        return sorted(long_term, key=lambda x: x['holding_days'], reverse=True)
    
    def display_tax_summary(self):
        """Display tax summary for current positions"""
        report = self.generate_unrealized_gains_report()
        
        if not report:
            print("Unable to generate tax report")
            return
        
        print(f"\n{'='*80}")
        print(f"📋 TAX REPORTING SUMMARY")
        print(f"{'='*80}")
        print(f"Report Date: {datetime.fromisoformat(report['report_date']).strftime('%Y-%m-%d')}")
        print(f"Wallet: {self.wallet_address[:8]}...{self.wallet_address[-8:]}")
        print(f"{'='*80}\n")
        
        summary = report['summary']
        print("💰 UNREALIZED GAINS/LOSSES")
        print(f"   Total Cost Basis: ${summary['total_cost_basis']:,.2f}")
        print(f"   Current Value: ${summary['total_current_value']:,.2f}")
        print(f"   Unrealized Gains: ${summary['total_unrealized_gains']:,.2f}")
        print(f"   Unrealized Losses: ${summary['total_unrealized_losses']:,.2f}")
        
        net_unrealized = summary['total_unrealized_gains'] - summary['total_unrealized_losses']
        net_icon = "🟢" if net_unrealized > 0 else "🔴"
        print(f"   {net_icon} Net Unrealized: ${net_unrealized:,.2f}\n")
        
        # Long-term holdings
        long_term = self.identify_long_term_holdings()
        if long_term:
            print(f"📅 LONG-TERM HOLDINGS (>365 days)")
            for pos in long_term:
                print(f"   {pos['symbol']}: {pos['holding_days']:.0f} days, ${pos['value']:,.2f} ({pos['pnl_pct']:.2f}%)")
            print()
        
        # Detailed positions
        print("📊 POSITION DETAILS")
        print(f"{'='*80}")
        
        for pos in sorted(report['positions'], key=lambda x: abs(x['unrealized_pnl']), reverse=True):
            pnl_icon = "🟢" if pos['unrealized_pnl'] > 0 else "🔴"
            holding_days = pos['holding_period_days']
            term = "Long-term" if holding_days >= 365 else "Short-term"
            
            print(f"\n{pnl_icon} {pos['token_symbol']} ({pos['token_name']})")
            print(f"   Quantity: {pos['quantity']:,.0f}")
            print(f"   Cost Basis: ${pos['cost_basis']:,.2f}")
            print(f"   Current Value: ${pos['current_value']:,.2f}")
            print(f"   Unrealized PnL: ${pos['unrealized_pnl']:,.2f} ({pos['pnl_percentage']:.2f}%)")
            print(f"   Holding Period: {holding_days:.0f} days ({term})")
        
        print(f"\n{'='*80}")
        print("⚠️  Note: This is for informational purposes only. Consult a tax professional.")
        print(f"{'='*80}\n")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

tax_helper = TaxReportHelper(client, "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
tax_helper.display_tax_summary()

# Export to JSON for tax software
report = tax_helper.generate_unrealized_gains_report()
import json
with open('unrealized_gains_report.json', 'w') as f:
    json.dump(report, f, indent=2)
print("Report exported to unrealized_gains_report.json")
```

### Example 6: Position Comparison Tool
```python
from typing import Dict, List

class PositionComparator:
    """Compare positions across multiple wallets"""
    
    def __init__(self, client: AxiomClient):
        self.client = client
        self.wallets_data = {}
        
    def add_wallet(self, wallet_address: str, label: str = None):
        """Add a wallet to comparison"""
        try:
            positions = self.client.get_meme_open_positions(wallet_address)
            self.wallets_data[wallet_address] = {
                'label': label or wallet_address[:8],
                'positions': positions
            }
            print(f"✅ Added wallet: {label or wallet_address[:8]}")
        except Exception as e:
            print(f"❌ Error adding wallet: {e}")
    
    def find_common_positions(self) -> List[str]:
        """Find tokens held by all wallets"""
        if not self.wallets_data:
            return []
        
        # Get all token symbols from first wallet
        all_tokens = []
        for wallet_data in self.wallets_data.values():
            tokens = {pos['tokenSymbol'] for pos in wallet_data['positions']['positions']}
            all_tokens.append(tokens)
        
        # Find intersection
        if all_tokens:
            common = all_tokens[0]
            for tokens in all_tokens[1:]:
                common = common.intersection(tokens)
            return list(common)
        
        return []
    
    def compare_performance(self) -> Dict:
        """Compare performance across wallets"""
        comparison = {}
        
        for wallet_addr, wallet_data in self.wallets_data.items():
            summary = wallet_data['positions']['summary']
            comparison[wallet_data['label']] = {
                'total_value': summary['totalValue'],
                'total_pnl': summary['totalPnl'],
                'total_pnl_pct': summary['totalPnlPercent'],
                'position_count': summary['totalPositions'],
                'win_rate': (summary['winningPositions'] / summary['totalPositions'] * 100) 
                           if summary['totalPositions'] > 0 else 0
            }
        
        return comparison
    
    def display_comparison(self):
        """Display wallet comparison"""
        if not self.wallets_data:
            print("No wallets added for comparison")
            return
        
        print(f"\n{'='*80}")
        print(f"🔍 WALLET COMPARISON")
        print(f"{'='*80}")
        print(f"Comparing {len(self.wallets_data)} wallets\n")
        
        # Performance comparison
        comparison = self.compare_performance()
        
        print("📊 PERFORMANCE COMPARISON")
        print(f"{'='*80}")
        print(f"{'Wallet':<15} {'Value':<15} {'PnL %':<12} {'Positions':<12} {'Win Rate':<10}")
        print(f"{'-'*80}")
        
        for label, metrics in comparison.items():
            pnl_icon = "🟢" if metrics['total_pnl'] > 0 else "🔴"
            print(f"{label:<15} ${metrics['total_value']:>12,.0f} "
                  f"{pnl_icon} {metrics['total_pnl_pct']:>7.1f}% "
                  f"{metrics['position_count']:>10} "
                  f"{metrics['win_rate']:>8.1f}%")
        
        print()
        
        # Common positions
        common = self.find_common_positions()
        if common:
            print(f"🤝 COMMON POSITIONS ({len(common)} tokens)")
            print(f"{'='*80}")
            
            for symbol in common:
                print(f"\n{symbol}:")
                for wallet_addr, wallet_data in self.wallets_data.items():
                    label = wallet_data['label']
                    positions = wallet_data['positions']['positions']
                    
                    # Find this token in positions
                    pos = next((p for p in positions if p['tokenSymbol'] == symbol), None)
                    if pos:
                        pnl_icon = "🟢" if pos['pnl'] > 0 else "🔴"
                        print(f"   {label}: ${pos['value']:>10,.2f} {pnl_icon} {pos['pnlPercent']:>6.1f}%")
        
        print(f"\n{'='*80}\n")

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

comparator = PositionComparator(client)

# Add multiple wallets
comparator.add_wallet("BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh", "Main Wallet")
comparator.add_wallet("AnotherWalletAddress123456789", "Trading Bot")
comparator.add_wallet("YetAnotherWallet987654321", "Long-term Hold")

# Display comparison
comparator.display_comparison()
```

### Example 7: Automated Position Reporter
```python
import time
from datetime import datetime, timedelta
from typing import Dict

class AutomatedReporter:
    """Generate automated portfolio reports"""
    
    def __init__(self, client: AxiomClient, wallet_address: str):
        self.client = client
        self.wallet_address = wallet_address
        self.report_interval_hours = 24
        self.last_report_time = None
        
    def generate_daily_report(self) -> str:
        """Generate daily portfolio report"""
        try:
            positions_data = self.client.get_meme_open_positions(self.wallet_address)
        except Exception as e:
            return f"Error generating report: {e}"
        
        summary = positions_data['summary']
        positions = positions_data['positions']
        
        # Build report
        report = []
        report.append("=" * 80)
        report.append("📧 DAILY PORTFOLIO REPORT")
        report.append("=" * 80)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Wallet: {self.wallet_address[:8]}...{self.wallet_address[-8:]}")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append("📊 PORTFOLIO SUMMARY")
        report.append(f"   Total Positions: {summary['totalPositions']}")
        report.append(f"   Portfolio Value: ${summary['totalValue']:,.2f}")
        report.append(f"   Cost Basis: ${summary['totalCost']:,.2f}")
        
        pnl_icon = "🟢" if summary['totalPnl'] > 0 else "🔴"
        report.append(f"   {pnl_icon} Total PnL: ${summary['totalPnl']:,.2f} ({summary['totalPnlPercent']:.2f}%)")
        report.append(f"   Winning: {summary['winningPositions']} | Losing: {summary['losingPositions']}")
        report.append("")
        
        # Top performers
        if positions:
            sorted_positions = sorted(positions, key=lambda x: x['pnlPercent'], reverse=True)
            
            report.append("🏆 TOP 3 PERFORMERS")
            for i, pos in enumerate(sorted_positions[:3], 1):
                report.append(f"   {i}. {pos['tokenSymbol']}: {pos['pnlPercent']:.2f}% (${pos['pnl']:,.2f})")
            report.append("")
            
            # Worst performers
            report.append("💔 BOTTOM 3 PERFORMERS")
            for i, pos in enumerate(sorted_positions[-3:], 1):
                report.append(f"   {i}. {pos['tokenSymbol']}: {pos['pnlPercent']:.2f}% (${pos['pnl']:,.2f})")
            report.append("")
        
        # Risk alerts
        report.append("⚠️  RISK ALERTS")
        alerts = []
        
        for pos in positions:
            # Large loss alert
            if pos['pnlPercent'] < -20:
                alerts.append(f"   🔴 {pos['tokenSymbol']} down {abs(pos['pnlPercent']):.1f}% (${abs(pos['pnl']):,.2f} loss)")
            
            # Concentration risk
            pos_pct = (pos['value'] / summary['totalValue'] * 100) if summary['totalValue'] > 0 else 0
            if pos_pct > 25:
                alerts.append(f"   ⚠️  {pos['tokenSymbol']} is {pos_pct:.1f}% of portfolio (concentration risk)")
        
        if alerts:
            report.extend(alerts)
        else:
            report.append("   ✅ No risk alerts")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def should_send_report(self) -> bool:
        """Check if it's time to send report"""
        if self.last_report_time is None:
            return True
        
        time_since_report = datetime.now() - self.last_report_time
        return time_since_report >= timedelta(hours=self.report_interval_hours)
    
    def send_report(self, report: str):
        """Send report (implement your delivery method)"""
        # Print to console (you could email, post to Telegram, etc.)
        print("\n" + report + "\n")
        
        # Example: Save to file
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Report saved to {filename}")
    
    def run(self, check_interval_minutes: int = 60):
        """Run automated reporter"""
        print(f"🤖 Automated Reporter Started")
        print(f"   Report interval: {self.report_interval_hours} hours")
        print(f"   Check interval: {check_interval_minutes} minutes\n")
        
        while True:
            if self.should_send_report():
                print("Generating report...")
                report = self.generate_daily_report()
                self.send_report(report)
                self.last_report_time = datetime.now()
            else:
                time_until_next = self.report_interval_hours * 3600 - (datetime.now() - self.last_report_time).total_seconds()
                print(f"Next report in {time_until_next/3600:.1f} hours")
            
            time.sleep(check_interval_minutes * 60)

# Usage
client = AxiomClient()
client.login(email="your@email.com", password="your_password")

reporter = AutomatedReporter(client, "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh")
reporter.report_interval_hours = 12  # Report every 12 hours

# Run in background
reporter.run(check_interval_minutes=30)
```

---

## Best Practices

### 1. **Cache Position Data** 💾
```python
import time

class PositionCache:
    def __init__(self, client, wallet, ttl_seconds=60):
        self.client = client
        self.wallet = wallet
        self.ttl = ttl_seconds
        self.cache = None
        self.cache_time = 0
    
    def get_positions(self):
        now = time.time()
        if self.cache is None or (now - self.cache_time) > self.ttl:
            self.cache = self.client.get_meme_open_positions(self.wallet)
            self.cache_time = now
        return self.cache

# Use cached data to avoid rate limits
cache = PositionCache(client, wallet_address, ttl_seconds=30)
positions = cache.get_positions()
```

### 2. **Handle Empty Portfolios** 🛡️
```python
positions = client.get_meme_open_positions(wallet_address)

if not positions['positions']:
    print("No open positions found")
else:
    # Process positions
    for pos in positions['positions']:
        print(f"{pos['tokenSymbol']}: ${pos['value']:,.2f}")
```

### 3. **Monitor Position Changes** 📊
```python
def track_position_changes(client, wallet, check_interval=300):
    """Track when positions are opened or closed"""
    last_positions = set()
    
    while True:
        current_data = client.get_meme_open_positions(wallet)
        current_positions = {pos['tokenAddress'] for pos in current_data['positions']}
        
        # Detect new positions
        new_positions = current_positions - last_positions
        if new_positions:
            print(f"🆕 New position(s) opened: {len(new_positions)}")
        
        # Detect closed positions
        closed_positions = last_positions - current_positions
        if closed_positions:
            print(f"✅ Position(s) closed: {len(closed_positions)}")
        
        last_positions = current_positions
        time.sleep(check_interval)
```

### 4. **Calculate Position Sizing** 📏
```python
def calculate_position_sizes(positions_data):
    """Calculate position sizes as percentage of portfolio"""
    total_value = positions_data['summary']['totalValue']
    
    position_sizes = []
    for pos in positions_data['positions']:
        size_pct = (pos['value'] / total_value * 100) if total_value > 0 else 0
        position_sizes.append({
            'symbol': pos['tokenSymbol'],
            'value': pos['value'],
            'percentage': size_pct
        })
    
    return sorted(position_sizes, key=lambda x: x['percentage'], reverse=True)
```

### 5. **Validate Wallet Addresses** ✅
```python
def is_valid_solana_address(address: str) -> bool:
    """Basic Solana address validation"""
    return len(address) >= 32 and len(address) <= 44 and address.isalnum()

# Use before API calls
if not is_valid_solana_address(wallet_address):
    raise ValueError("Invalid wallet address format")

positions = client.get_meme_open_positions(wallet_address)
```

### 6. **Set PnL Thresholds** 🎯
```python
# Define thresholds for decision making
TAKE_PROFIT_THRESHOLD = 50  # Take profits at 50%
STOP_LOSS_THRESHOLD = -20    # Stop loss at -20%
REBALANCE_THRESHOLD = 25     # Rebalance if position >25% of portfolio

positions = client.get_meme_open_positions(wallet_address)

for pos in positions['positions']:
    if pos['pnlPercent'] >= TAKE_PROFIT_THRESHOLD:
        print(f"🎯 Consider taking profits on {pos['tokenSymbol']}")
    elif pos['pnlPercent'] <= STOP_LOSS_THRESHOLD:
        print(f"🚨 Consider stop-loss on {pos['tokenSymbol']}")
```

### 7. **Export Portfolio Data** 📤
```python
import json
from datetime import datetime

def export_portfolio(positions_data, filename=None):
    """Export portfolio to JSON file"""
    if filename is None:
        filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(positions_data, f, indent=2)
    
    print(f"Portfolio exported to {filename}")

# Usage
positions = client.get_meme_open_positions(wallet_address)
export_portfolio(positions)
```

---

## Troubleshooting

### Issue: "Authentication failed"
**Solution**: Ensure you're logged in before calling the method
```python
client = AxiomClient()
if not client.is_authenticated():
    client.login(email="your@email.com", password="your_password")

positions = client.get_meme_open_positions(wallet_address)
```

### Issue: "Failed to get open positions"
**Solution**: Verify the wallet address is correct
```python
# Test with your own wallet address first
my_wallet = "YourWalletAddressHere"
try:
    positions = client.get_meme_open_positions(my_wallet)
    print(f"Found {len(positions['positions'])} positions")
except Exception as e:
    print(f"Error: {e}")
```

### Issue: Empty positions array
**Solution**: This wallet may not have any open meme token positions
```python
positions = client.get_meme_open_positions(wallet_address)

if not positions['positions']:
    print("No open positions found for this wallet")
    print("This could mean:")
    print("- Wallet has no meme token holdings")
    print("- All positions have been closed")
    print("- Wallet only holds non-meme tokens")
```

### Issue: Outdated position data
**Solution**: Position data is real-time but prices may lag slightly
```python
# Refresh data periodically for monitoring
import time

def get_fresh_positions(client, wallet, max_age_seconds=60):
    """Get positions and ensure data is fresh"""
    positions = client.get_meme_open_positions(wallet)
    
    # You could add timestamp checking here if the API returns it
    # For now, just return the data
    return positions

# Use in monitoring loop
while True:
    positions = get_fresh_positions(client, wallet_address)
    # Process positions...
    time.sleep(30)
```

### Issue: Rate limiting (429 errors)
**Solution**: Implement caching and reduce request frequency
```python
import time
from requests.exceptions import HTTPError

def get_positions_with_retry(client, wallet, max_retries=3):
    """Get positions with retry logic"""
    backoff = 1
    
    for attempt in range(max_retries):
        try:
            return client.get_meme_open_positions(wallet)
        except HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limited. Waiting {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                raise
    
    raise Exception("Max retries exceeded")
```

### Issue: Missing fields in position data
**Solution**: Validate data structure before processing
```python
def validate_position_data(positions_data):
    """Validate position data structure"""
    required_fields = ['positions', 'summary']
    
    for field in required_fields:
        if field not in positions_data:
            raise ValueError(f"Missing field: {field}")
    
    # Validate summary fields
    summary_fields = ['totalPositions', 'totalValue', 'totalPnl']
    for field in summary_fields:
        if field not in positions_data['summary']:
            raise ValueError(f"Missing summary field: {field}")
    
    return True

# Usage
positions = client.get_meme_open_positions(wallet_address)
validate_position_data(positions)
```

### Issue: PnL calculations seem incorrect
**Solution**: Understand that PnL is unrealized and based on current market prices
```python
# PnL is calculated as: (current_price - avg_buy_price) * amount
# This is unrealized until you sell

for pos in positions['positions']:
    print(f"{pos['tokenSymbol']}:")
    print(f"  Avg Buy: ${pos['avgBuyPrice']:.8f}")
    print(f"  Current: ${pos['currentPrice']:.8f}")
    print(f"  Amount: {pos['amount']:,.0f}")
    print(f"  Unrealized PnL: ${pos['pnl']:,.2f}")
    print(f"  Note: This will change as price moves")
```

---

## Related Methods

- **[`get_user_portfolio()`](./get-user-portfolio-guide.md)** - Get complete portfolio including closed positions and realized PnL
- **[`get_token_balance()`](./get-token-balance-guide.md)** - Get balance for a specific token
- **[`get_sol_balance()`](./get-sol-balance-guide.md)** - Get SOL balance for wallet
- **[`buy_token()`](./buy-token-guide.md)** - Open new positions by buying tokens
- **[`sell_token()`](./sell-token-guide.md)** - Close positions by selling tokens
- **[`get_token_info()`](./get-token-info-guide.md)** - Get detailed information about tokens in your positions

---

## Summary

The `get_meme_open_positions()` method is essential for:

✅ **Portfolio Management** - Track all active token holdings in one call  
✅ **Performance Monitoring** - Monitor unrealized gains/losses across positions  
✅ **Risk Management** - Identify concentration risk and stop-loss needs  
✅ **Position Sizing** - Calculate and rebalance position sizes  
✅ **Trading Automation** - Build bots that manage multiple positions  
✅ **Tax Reporting** - Track unrealized gains for tax planning  
✅ **Analytics** - Analyze portfolio composition and performance trends

### Key Features:
- 💼 Complete position details (amount, value, PnL, avg buy price)
- 📊 Portfolio-level summary statistics
- 🎯 Win/loss position counts
- ⏱️ Holding time for each position
- 💰 Cost basis and current value tracking
- 📈 Percentage-based PnL calculations

### Important Notes:
⚠️ **Unrealized PnL**: All profits/losses are unrealized until positions are closed  
⚠️ **Real-time Prices**: Current prices may lag slightly from latest market data  
⚠️ **Meme Tokens Only**: Only includes meme tokens, not all wallet holdings  
⚠️ **Open Positions**: Closed positions are not included (use `get_user_portfolio()` for full history)  
⚠️ **Rate Limits**: Implement caching for frequent monitoring

---

**💡 Pro Tip**: Combine `get_meme_open_positions()` with `get_last_transaction()` for each pair to build a comprehensive portfolio monitor with real-time price updates and alerts!
