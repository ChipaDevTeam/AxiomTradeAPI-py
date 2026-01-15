# get_holder_data() Method - Comprehensive Guide

## Overview

The `get_holder_data()` method retrieves detailed information about token holders for a specific trading pair on the Solana blockchain. This data is crucial for analyzing token distribution, identifying whale wallets, detecting smart money movements, and assessing holder concentration risk.

This method is essential for:
- 🐋 **Whale tracking**: Identify large holders and their positions
- 🎯 **Smart money detection**: Track wallets with successful trading history
- 📊 **Distribution analysis**: Understand token concentration
- 🚨 **Risk assessment**: Detect concentration risk and potential dumps
- 📈 **Holder patterns**: Analyze entry/exit timing

## Method Signature

```python
def get_holder_data(
    self, 
    pair_address: str, 
    only_tracked_wallets: bool = False
) -> Dict
```

## Parameters

### `pair_address` (str, required)
- **Description**: The DEX pair address (liquidity pool address) for the token
- **Format**: Base58-encoded Solana public key (32-44 characters)
- **Example**: `"Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"`
- **Where to find**:
  - DEX Screener pair information
  - New pair WebSocket events (`pair_address` field)
  - Token explorers (Solscan, SolanaFM)
  - `get_pair_info()` method

### `only_tracked_wallets` (bool, optional, default=False)
- **Description**: Filter to show only "tracked" wallets (wallets flagged as noteworthy)
- **Values**:
  - `False`: Return all holders (default)
  - `True`: Return only tracked/notable wallets (whales, smart money, influencers)
- **Use Cases**:
  - `False`: Complete distribution analysis
  - `True`: Focus on important wallets only

## Return Value

Returns a dictionary containing comprehensive holder information:

```python
{
    "holders": [
        {
            "walletAddress": "Wallet123...",
            "tokenBalance": 1500000,
            "tokenBalanceFormatted": "1,500,000",
            "percentageOfSupply": 15.5,
            "solValue": 25.5,
            "usdValue": 2850.00,
            "isTracked": true,
            "trackedReason": "Smart Money",
            "entryPrice": 0.00001,
            "currentPnL": 125.50,
            "pnlPercentage": 35.2,
            "holdingTimeHours": 48,
            "lastActivity": "2026-01-14T10:30:00Z"
        },
        # ... more holders
    ],
    "summary": {
        "totalHolders": 1250,
        "trackedWallets": 15,
        "top10HoldingPercentage": 45.5,
        "top20HoldingPercentage": 62.3,
        "averageHoldingSize": 800,
        "medianHoldingSize": 150
    },
    "concentration": {
        "giniCoefficient": 0.75,
        "concentrationRisk": "High",
        "largestHolderPercentage": 12.5,
        "whaleCount": 8
    },
    "smartMoney": {
        "smartMoneyWallets": 12,
        "smartMoneyPercentage": 18.5,
        "avgSmartMoneyWinRate": 65.0
    }
}
```

### Response Fields

#### `holders` (Array)
List of all token holders with detailed information.

Each holder object contains:
- **walletAddress**: Solana wallet address
- **tokenBalance**: Raw token balance
- **tokenBalanceFormatted**: Human-readable balance
- **percentageOfSupply**: Percentage of total supply held
- **solValue**: Value in SOL
- **usdValue**: Value in USD
- **isTracked**: Whether wallet is flagged as tracked
- **trackedReason**: Why wallet is tracked (Smart Money, Whale, Influencer, etc.)
- **entryPrice**: Average entry price
- **currentPnL**: Profit/Loss in USD
- **pnlPercentage**: PnL percentage
- **holdingTimeHours**: Hours since first purchase
- **lastActivity**: Last transaction timestamp

#### `summary` (Object)
Overall holder statistics:
- **totalHolders**: Total number of holders
- **trackedWallets**: Number of tracked wallets
- **top10HoldingPercentage**: % held by top 10 holders
- **top20HoldingPercentage**: % held by top 20 holders
- **averageHoldingSize**: Average tokens per holder
- **medianHoldingSize**: Median holding size

#### `concentration` (Object)
Token distribution metrics:
- **giniCoefficient**: Measure of inequality (0=equal, 1=concentrated)
- **concentrationRisk**: Risk level (Low, Medium, High)
- **largestHolderPercentage**: Largest single holder percentage
- **whaleCount**: Number of whale wallets

#### `smartMoney` (Object)
Smart money analytics:
- **smartMoneyWallets**: Count of smart money wallets
- **smartMoneyPercentage**: % held by smart money
- **avgSmartMoneyWinRate**: Average win rate of smart money wallets

## Prerequisites

```python
from axiomtradeapi.client import AxiomTradeClient

# Initialize and authenticate
client = AxiomTradeClient()
client.login("username", "password")

# Or use tokens
client = AxiomTradeClient(
    auth_token="your_access_token",
    refresh_token="your_refresh_token"
)
```

---

## Basic Usage Examples

### Example 1: Get All Holders
Retrieve complete holder data for a token pair.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()
client.login("username", "password")

# Pair address to analyze
pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"

# Get all holder data
result = client.get_holder_data(pair_address, only_tracked_wallets=False)

print(f"📊 Token Holder Analysis")
print(f"=" * 50)
print(f"Total holders: {result['summary']['totalHolders']}")
print(f"Tracked wallets: {result['summary']['trackedWallets']}")
print(f"Top 10 holders own: {result['summary']['top10HoldingPercentage']:.1f}%")
print(f"Top 20 holders own: {result['summary']['top20HoldingPercentage']:.1f}%")

print(f"\n🔒 Concentration Risk")
print(f"Risk Level: {result['concentration']['concentrationRisk']}")
print(f"Gini Coefficient: {result['concentration']['giniCoefficient']:.2f}")
print(f"Largest holder: {result['concentration']['largestHolderPercentage']:.1f}%")
```

**Output:**
```
📊 Token Holder Analysis
==================================================
Total holders: 1250
Tracked wallets: 15
Top 10 holders own: 45.5%
Top 20 holders own: 62.3%

🔒 Concentration Risk
Risk Level: High
Gini Coefficient: 0.75
Largest holder: 12.5%
```

### Example 2: Track Smart Money Wallets
Focus on tracked wallets only (smart money, whales, influencers).

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()
client.login("username", "password")

pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"

# Get only tracked wallets
result = client.get_holder_data(pair_address, only_tracked_wallets=True)

print("🎯 Tracked Wallets Analysis\n")

# Display tracked wallets
for holder in result['holders'][:10]:  # Top 10 tracked wallets
    wallet = holder['walletAddress'][:8] + "..."
    percentage = holder['percentageOfSupply']
    reason = holder.get('trackedReason', 'Unknown')
    pnl = holder.get('pnlPercentage', 0)
    
    pnl_emoji = "🟢" if pnl > 0 else "🔴"
    
    print(f"{reason:15} | {wallet} | {percentage:5.2f}% | {pnl_emoji} {pnl:+.1f}%")

print(f"\n💰 Smart Money Summary:")
print(f"   Smart money wallets: {result['smartMoney']['smartMoneyWallets']}")
print(f"   Smart money owns: {result['smartMoney']['smartMoneyPercentage']:.1f}%")
print(f"   Avg win rate: {result['smartMoney']['avgSmartMoneyWinRate']:.1f}%")
```

**Output:**
```
🎯 Tracked Wallets Analysis

Smart Money      | Wallet12... |  8.50% | 🟢 +45.2%
Whale           | Wallet34... | 12.30% | 🟢 +28.5%
Smart Money      | Wallet56... |  5.20% | 🟢 +62.1%
Influencer      | Wallet78... |  3.40% | 🟢 +15.8%
Smart Money      | Wallet90... |  4.10% | 🔴 -12.3%

💰 Smart Money Summary:
   Smart money wallets: 12
   Smart money owns: 18.5%
   Avg win rate: 65.0%
```

### Example 3: Identify Whale Wallets
Find and analyze whale holders.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()
client.login("username", "password")

pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"
result = client.get_holder_data(pair_address)

print("🐋 Whale Wallet Analysis\n")

# Define whale threshold (e.g., > 5% of supply)
WHALE_THRESHOLD = 5.0

whales = [
    holder for holder in result['holders']
    if holder['percentageOfSupply'] >= WHALE_THRESHOLD
]

print(f"Found {len(whales)} whale wallets (≥{WHALE_THRESHOLD}% of supply)\n")

for i, whale in enumerate(whales, 1):
    wallet = whale['walletAddress'][:8] + "..."
    percentage = whale['percentageOfSupply']
    usd_value = whale.get('usdValue', 0)
    holding_hours = whale.get('holdingTimeHours', 0)
    
    print(f"{i}. {wallet}")
    print(f"   Holding: {percentage:.2f}% (${usd_value:,.0f})")
    print(f"   Holding time: {holding_hours} hours ({holding_hours/24:.1f} days)")
    print()
```

**Output:**
```
🐋 Whale Wallet Analysis

Found 8 whale wallets (≥5.0% of supply)

1. Wallet12...
   Holding: 12.50% ($35,000)
   Holding time: 120 hours (5.0 days)

2. Wallet34...
   Holding: 8.30% ($23,000)
   Holding time: 96 hours (4.0 days)

3. Wallet56...
   Holding: 7.20% ($20,100)
   Holding time: 48 hours (2.0 days)
```

---

## Advanced Examples

### Example 4: Real-Time Holder Monitoring
Monitor holder changes over time to detect accumulation/distribution.

```python
from axiomtradeapi.client import AxiomTradeClient
import time
from datetime import datetime
from typing import Dict, List

class HolderMonitor:
    """Monitor holder changes over time"""
    
    def __init__(self, pair_address: str):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
        self.pair_address = pair_address
        self.previous_snapshot = None
    
    def take_snapshot(self) -> Dict:
        """Take snapshot of current holder data"""
        return self.client.get_holder_data(self.pair_address)
    
    def detect_changes(self, current: Dict) -> Dict:
        """Detect changes since last snapshot"""
        if not self.previous_snapshot:
            return {"first_run": True}
        
        prev_holders = {h['walletAddress']: h for h in self.previous_snapshot['holders']}
        curr_holders = {h['walletAddress']: h for h in current['holders']}
        
        changes = {
            "new_holders": [],
            "exited_holders": [],
            "increased_positions": [],
            "decreased_positions": [],
            "whale_movements": []
        }
        
        # Find new holders
        for wallet, holder in curr_holders.items():
            if wallet not in prev_holders:
                changes["new_holders"].append(holder)
        
        # Find exited holders
        for wallet, holder in prev_holders.items():
            if wallet not in curr_holders:
                changes["exited_holders"].append(holder)
        
        # Find position changes
        for wallet in set(prev_holders.keys()) & set(curr_holders.keys()):
            prev_balance = prev_holders[wallet]['tokenBalance']
            curr_balance = curr_holders[wallet]['tokenBalance']
            
            if curr_balance > prev_balance:
                change_pct = ((curr_balance - prev_balance) / prev_balance) * 100
                changes["increased_positions"].append({
                    "wallet": wallet,
                    "change_pct": change_pct,
                    "holder_data": curr_holders[wallet]
                })
            elif curr_balance < prev_balance:
                change_pct = ((prev_balance - curr_balance) / prev_balance) * 100
                changes["decreased_positions"].append({
                    "wallet": wallet,
                    "change_pct": change_pct,
                    "holder_data": curr_holders[wallet]
                })
        
        # Detect whale movements
        for position in changes["increased_positions"] + changes["decreased_positions"]:
            if position['holder_data']['percentageOfSupply'] >= 5.0:
                changes["whale_movements"].append(position)
        
        return changes
    
    def start_monitoring(self, interval_seconds: int = 300):
        """
        Start monitoring loop
        
        Args:
            interval_seconds: Seconds between checks (default: 5 minutes)
        """
        print(f"👀 Monitoring holder changes for pair: {self.pair_address[:8]}...")
        print(f"   Check interval: {interval_seconds}s ({interval_seconds/60:.1f} minutes)\n")
        
        try:
            while True:
                current = self.take_snapshot()
                changes = self.detect_changes(current)
                
                if not changes.get('first_run'):
                    self.report_changes(changes)
                else:
                    print(f"✅ Initial snapshot taken at {datetime.now()}")
                
                self.previous_snapshot = current
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n⏹️  Monitoring stopped")
    
    def report_changes(self, changes: Dict):
        """Report detected changes"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n📊 Holder Update at {timestamp}")
        print("=" * 60)
        
        if changes["new_holders"]:
            print(f"🆕 New holders: {len(changes['new_holders'])}")
            for holder in changes["new_holders"][:5]:
                print(f"   {holder['walletAddress'][:8]}... - {holder['percentageOfSupply']:.2f}%")
        
        if changes["exited_holders"]:
            print(f"🚪 Exited holders: {len(changes['exited_holders'])}")
            for holder in changes["exited_holders"][:5]:
                print(f"   {holder['walletAddress'][:8]}... - was {holder['percentageOfSupply']:.2f}%")
        
        if changes["whale_movements"]:
            print(f"🐋 Whale movements: {len(changes['whale_movements'])}")
            for movement in changes["whale_movements"]:
                action = "increased" if movement in changes["increased_positions"] else "decreased"
                print(f"   {movement['wallet'][:8]}... {action} by {movement['change_pct']:.1f}%")

# Usage
monitor = HolderMonitor("Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY")
monitor.start_monitoring(interval_seconds=300)  # Check every 5 minutes
```

**Output:**
```
👀 Monitoring holder changes for pair: Cr8Qy7q...
   Check interval: 300s (5.0 minutes)

✅ Initial snapshot taken at 2026-01-14 10:30:00

📊 Holder Update at 2026-01-14 10:35:00
============================================================
🆕 New holders: 8
   Wallet12... - 0.15%
   Wallet34... - 0.08%
🐋 Whale movements: 2
   Wallet56... increased by 12.5%
   Wallet78... decreased by 8.2%
```

### Example 5: Concentration Risk Calculator
Calculate detailed concentration risk metrics.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import Dict

class ConcentrationAnalyzer:
    """Analyze token holder concentration risk"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
    
    def analyze_concentration(self, pair_address: str) -> Dict:
        """
        Comprehensive concentration analysis
        
        Returns:
            Dict with risk assessment and metrics
        """
        result = self.client.get_holder_data(pair_address)
        holders = sorted(result['holders'], key=lambda x: x['percentageOfSupply'], reverse=True)
        
        # Calculate various metrics
        top1_pct = holders[0]['percentageOfSupply'] if holders else 0
        top5_pct = sum(h['percentageOfSupply'] for h in holders[:5])
        top10_pct = result['summary']['top10HoldingPercentage']
        top20_pct = result['summary']['top20HoldingPercentage']
        
        # Herfindahl-Hirschman Index (HHI)
        hhi = sum((h['percentageOfSupply'] / 100) ** 2 for h in holders) * 10000
        
        # Risk scoring
        risk_score = 0
        risk_factors = []
        
        if top1_pct > 15:
            risk_score += 30
            risk_factors.append(f"Single holder owns {top1_pct:.1f}% (very dangerous)")
        elif top1_pct > 10:
            risk_score += 20
            risk_factors.append(f"Single holder owns {top1_pct:.1f}% (dangerous)")
        
        if top10_pct > 60:
            risk_score += 25
            risk_factors.append(f"Top 10 own {top10_pct:.1f}% (high concentration)")
        elif top10_pct > 50:
            risk_score += 15
            risk_factors.append(f"Top 10 own {top10_pct:.1f}% (moderate concentration)")
        
        if top20_pct > 80:
            risk_score += 20
            risk_factors.append(f"Top 20 own {top20_pct:.1f}% (extreme concentration)")
        
        if result['concentration']['giniCoefficient'] > 0.8:
            risk_score += 15
            risk_factors.append(f"High Gini coefficient ({result['concentration']['giniCoefficient']:.2f})")
        
        if hhi > 2500:
            risk_score += 10
            risk_factors.append(f"High HHI ({hhi:.0f} - highly concentrated)")
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "🔴 EXTREME RISK"
            recommendation = "DO NOT INVEST - Highly concentrated, high dump risk"
        elif risk_score >= 50:
            risk_level = "🟠 HIGH RISK"
            recommendation = "Avoid or invest very small amounts only"
        elif risk_score >= 30:
            risk_level = "🟡 MEDIUM RISK"
            recommendation = "Proceed with caution, monitor closely"
        else:
            risk_level = "🟢 LOW RISK"
            recommendation = "Relatively safe distribution"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'metrics': {
                'top1_percentage': top1_pct,
                'top5_percentage': top5_pct,
                'top10_percentage': top10_pct,
                'top20_percentage': top20_pct,
                'gini_coefficient': result['concentration']['giniCoefficient'],
                'hhi': hhi,
                'total_holders': result['summary']['totalHolders']
            },
            'risk_factors': risk_factors
        }
    
    def display_analysis(self, analysis: Dict):
        """Display concentration analysis"""
        print("🔒 Token Concentration Risk Analysis")
        print("=" * 60)
        print(f"Risk Level: {analysis['risk_level']}")
        print(f"Risk Score: {analysis['risk_score']}/100")
        print(f"Recommendation: {analysis['recommendation']}")
        
        print(f"\n📊 Distribution Metrics:")
        metrics = analysis['metrics']
        print(f"   Top 1 holder: {metrics['top1_percentage']:.2f}%")
        print(f"   Top 5 holders: {metrics['top5_percentage']:.2f}%")
        print(f"   Top 10 holders: {metrics['top10_percentage']:.2f}%")
        print(f"   Top 20 holders: {metrics['top20_percentage']:.2f}%")
        print(f"   Total holders: {metrics['total_holders']}")
        print(f"   Gini Coefficient: {metrics['gini_coefficient']:.3f}")
        print(f"   HHI: {metrics['hhi']:.0f}")
        
        if analysis['risk_factors']:
            print(f"\n⚠️  Risk Factors:")
            for factor in analysis['risk_factors']:
                print(f"   - {factor}")

# Usage
analyzer = ConcentrationAnalyzer()
pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"

analysis = analyzer.analyze_concentration(pair_address)
analyzer.display_analysis(analysis)
```

**Output:**
```
🔒 Token Concentration Risk Analysis
============================================================
Risk Level: 🟠 HIGH RISK
Risk Score: 65/100
Recommendation: Avoid or invest very small amounts only

📊 Distribution Metrics:
   Top 1 holder: 12.50%
   Top 5 holders: 38.20%
   Top 10 holders: 45.50%
   Top 20 holders: 62.30%
   Total holders: 1250
   Gini Coefficient: 0.750
   HHI: 2850

⚠️  Risk Factors:
   - Single holder owns 12.5% (dangerous)
   - Top 20 own 62.3% (moderate concentration)
   - High HHI (2850 - highly concentrated)
```

### Example 6: Smart Money Tracker
Track and copy smart money wallet movements.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import List, Dict

class SmartMoneyTracker:
    """Track smart money wallet activity"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
        self.tracked_wallets = set()
    
    def find_smart_money_wallets(self, pair_address: str) -> List[Dict]:
        """
        Find smart money wallets holding this token
        
        Returns:
            List of smart money holders with their positions
        """
        result = self.client.get_holder_data(pair_address, only_tracked_wallets=True)
        
        smart_money = [
            holder for holder in result['holders']
            if holder.get('trackedReason') == 'Smart Money'
        ]
        
        return smart_money
    
    def analyze_smart_money_sentiment(self, pair_address: str) -> Dict:
        """
        Analyze overall smart money sentiment on a token
        
        Returns:
            Dict with sentiment analysis
        """
        smart_money = self.find_smart_money_wallets(pair_address)
        
        if not smart_money:
            return {
                'sentiment': 'NEUTRAL',
                'confidence': 0,
                'reason': 'No smart money positions detected'
            }
        
        # Analyze PnL
        in_profit = sum(1 for w in smart_money if w.get('pnlPercentage', 0) > 0)
        total = len(smart_money)
        
        # Analyze holding time
        avg_holding_hours = sum(w.get('holdingTimeHours', 0) for w in smart_money) / total
        
        # Analyze position sizes
        total_smart_money_pct = sum(w['percentageOfSupply'] for w in smart_money)
        
        # Calculate sentiment
        profit_ratio = in_profit / total
        
        if profit_ratio >= 0.7 and avg_holding_hours > 24:
            sentiment = '🟢 BULLISH'
            confidence = 85
            reason = f"{in_profit}/{total} smart money wallets profitable, holding avg {avg_holding_hours:.1f}h"
        elif profit_ratio >= 0.5:
            sentiment = '🟡 NEUTRAL/BULLISH'
            confidence = 60
            reason = f"{in_profit}/{total} profitable, mixed signals"
        elif profit_ratio <= 0.3:
            sentiment = '🔴 BEARISH'
            confidence = 75
            reason = f"Only {in_profit}/{total} profitable, likely exiting"
        else:
            sentiment = '🟡 NEUTRAL'
            confidence = 40
            reason = "Mixed smart money positions"
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reason': reason,
            'details': {
                'smart_money_count': total,
                'profitable_count': in_profit,
                'profit_ratio': profit_ratio,
                'avg_holding_hours': avg_holding_hours,
                'total_percentage': total_smart_money_pct
            }
        }
    
    def display_smart_money_analysis(self, pair_address: str):
        """Display comprehensive smart money analysis"""
        print("🎯 Smart Money Analysis")
        print("=" * 60)
        
        # Get smart money positions
        smart_money = self.find_smart_money_wallets(pair_address)
        
        if not smart_money:
            print("ℹ️  No smart money positions detected")
            return
        
        print(f"Found {len(smart_money)} smart money wallets\n")
        
        # Display individual positions
        print("📊 Smart Money Positions:")
        for i, wallet in enumerate(smart_money[:10], 1):
            addr = wallet['walletAddress'][:8] + "..."
            pct = wallet['percentageOfSupply']
            pnl = wallet.get('pnlPercentage', 0)
            hours = wallet.get('holdingTimeHours', 0)
            
            pnl_emoji = "🟢" if pnl > 0 else "🔴"
            print(f"{i:2}. {addr} | {pct:5.2f}% | {pnl_emoji} {pnl:+6.1f}% | {hours:4.0f}h")
        
        # Get sentiment
        sentiment = self.analyze_smart_money_sentiment(pair_address)
        
        print(f"\n💡 Smart Money Sentiment: {sentiment['sentiment']}")
        print(f"   Confidence: {sentiment['confidence']}%")
        print(f"   Reason: {sentiment['reason']}")

# Usage
tracker = SmartMoneyTracker()
pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"

tracker.display_smart_money_analysis(pair_address)
```

**Output:**
```
🎯 Smart Money Analysis
============================================================
Found 12 smart money wallets

📊 Smart Money Positions:
 1. Wallet12... |  8.50% | 🟢 +45.2% |   96h
 2. Wallet34... |  5.20% | 🟢 +62.1% |  120h
 3. Wallet56... |  4.10% | 🔴 -12.3% |   24h
 4. Wallet78... |  3.80% | 🟢 +28.7% |   72h
 5. Wallet90... |  2.90% | 🟢 +15.4% |   48h

💡 Smart Money Sentiment: 🟢 BULLISH
   Confidence: 85%
   Reason: 10/12 smart money wallets profitable, holding avg 72.5h
```

### Example 7: Holder Distribution Visualizer
Generate distribution statistics and insights.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import Dict, List
from collections import defaultdict

class DistributionAnalyzer:
    """Analyze and visualize token holder distribution"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
    
    def categorize_holders(self, pair_address: str) -> Dict:
        """
        Categorize holders into tiers based on holding size
        
        Returns:
            Dict with holder categories and statistics
        """
        result = self.client.get_holder_data(pair_address)
        holders = result['holders']
        
        categories = {
            'mega_whales': [],   # > 10%
            'whales': [],        # 5-10%
            'large': [],         # 1-5%
            'medium': [],        # 0.1-1%
            'small': [],         # < 0.1%
        }
        
        for holder in holders:
            pct = holder['percentageOfSupply']
            
            if pct >= 10:
                categories['mega_whales'].append(holder)
            elif pct >= 5:
                categories['whales'].append(holder)
            elif pct >= 1:
                categories['large'].append(holder)
            elif pct >= 0.1:
                categories['medium'].append(holder)
            else:
                categories['small'].append(holder)
        
        return {
            'categories': categories,
            'summary': result['summary'],
            'total_holders': len(holders)
        }
    
    def display_distribution(self, pair_address: str):
        """Display distribution chart"""
        data = self.categorize_holders(pair_address)
        categories = data['categories']
        
        print("📊 Token Holder Distribution")
        print("=" * 70)
        
        # Calculate percentages
        total = data['total_holders']
        
        print(f"{'Category':<15} {'Count':>8} {'% of Total':>12} {'Holds':>12}")
        print("-" * 70)
        
        for name, holders in categories.items():
            count = len(holders)
            pct_of_holders = (count / total * 100) if total > 0 else 0
            total_held = sum(h['percentageOfSupply'] for h in holders)
            
            display_name = {
                'mega_whales': '🐋 Mega Whales',
                'whales': '🐋 Whales',
                'large': '🐟 Large Fish',
                'medium': '🐠 Medium Fish',
                'small': '🦐 Shrimp'
            }.get(name, name)
            
            print(f"{display_name:<15} {count:>8} {pct_of_holders:>11.1f}% {total_held:>11.1f}%")
        
        print(f"{'-'*70}")
        print(f"{'TOTAL':<15} {total:>8} {100.0:>11.1f}% {100.0:>11.1f}%")
        
        # Health assessment
        print(f"\n💊 Distribution Health:")
        mega_whale_pct = sum(h['percentageOfSupply'] for h in categories['mega_whales'])
        whale_pct = sum(h['percentageOfSupply'] for h in categories['whales'])
        
        if mega_whale_pct > 30:
            print("   🔴 UNHEALTHY - Mega whales control too much")
        elif mega_whale_pct + whale_pct > 50:
            print("   🟡 MODERATE - High whale concentration")
        else:
            print("   🟢 HEALTHY - Good distribution")

# Usage
analyzer = DistributionAnalyzer()
pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"

analyzer.display_distribution(pair_address)
```

**Output:**
```
📊 Token Holder Distribution
======================================================================
Category            Count  % of Total        Holds
----------------------------------------------------------------------
🐋 Mega Whales          2        0.2%        22.8%
🐋 Whales               6        0.5%        22.7%
🐟 Large Fish          45        3.6%        35.2%
🐠 Medium Fish        287       23.0%        18.1%
🦐 Shrimp            910       72.8%         1.2%
----------------------------------------------------------------------
TOTAL               1250      100.0%       100.0%

💊 Distribution Health:
   🟡 MODERATE - High whale concentration
```

---

## Best Practices

### 1. Filter by Tracked Wallets for Efficiency
```python
# ✅ Good: Use filter when you only need tracked wallets
tracked_only = client.get_holder_data(pair_address, only_tracked_wallets=True)

# ❌ Inefficient: Getting all then filtering manually
all_holders = client.get_holder_data(pair_address, only_tracked_wallets=False)
tracked = [h for h in all_holders['holders'] if h.get('isTracked')]
```

### 2. Cache Results for Multiple Analyses
```python
# Get once, use multiple times
holder_data = client.get_holder_data(pair_address)

# Multiple analyses
concentration_risk = analyze_concentration(holder_data)
whale_count = count_whales(holder_data)
distribution = analyze_distribution(holder_data)
```

### 3. Handle Large Holder Lists
```python
# Process in batches
holder_data = client.get_holder_data(pair_address)
holders = holder_data['holders']

BATCH_SIZE = 100
for i in range(0, len(holders), BATCH_SIZE):
    batch = holders[i:i + BATCH_SIZE]
    process_batch(batch)
```

### 4. Set Realistic Thresholds
```python
# Define thresholds based on market cap
def get_whale_threshold(market_cap: float) -> float:
    """Adjust whale threshold based on market cap"""
    if market_cap > 10_000_000:  # > $10M
        return 2.0  # 2%
    elif market_cap > 1_000_000:  # > $1M
        return 5.0  # 5%
    else:
        return 10.0  # 10% for small caps
```

### 5. Monitor Over Time
```python
# Take snapshots periodically
snapshots = []

for _ in range(10):  # Take 10 snapshots
    holder_data = client.get_holder_data(pair_address)
    snapshots.append({
        'timestamp': datetime.now(),
        'data': holder_data
    })
    time.sleep(300)  # 5 minutes between snapshots

# Analyze trends
analyze_holder_trends(snapshots)
```

---

## Troubleshooting

### Issue: "Authentication failed"

**Solution**:
```python
# Ensure authenticated before calling
if not client.ensure_authenticated():
    client.login("username", "password")

holder_data = client.get_holder_data(pair_address)
```

### Issue: Empty Holder List

**Possible Causes**:
1. Invalid pair address
2. Very new token (data not indexed yet)
3. Token has no holders yet

**Solution**:
```python
holder_data = client.get_holder_data(pair_address)

if holder_data['summary']['totalHolders'] == 0:
    print("No holders found - check pair address or wait for indexing")
```

### Issue: Slow Performance with Large Holder Lists

**Solution**:
```python
# Use tracked wallets only when possible
if need_whale_data_only:
    holder_data = client.get_holder_data(pair_address, only_tracked_wallets=True)
else:
    holder_data = client.get_holder_data(pair_address, only_tracked_wallets=False)
```

---

## Related Methods

### `get_pair_info()`
Get pair information including the pair address needed for holder data.

```python
pair_info = client.get_pair_info(pair_address)
holder_data = client.get_holder_data(pair_address)
```

### `get_token_info_by_pair()`
Get token information which includes holder count.

```python
token_info = client.get_token_info_by_pair(pair_address)
print(f"Total holders: {token_info['numHolders']}")

# Then get detailed holder data
holder_data = client.get_holder_data(pair_address)
```

---

## Additional Resources

- **Token Analysis**: [NEW_API_FUNCTIONS.md](./NEW_API_FUNCTIONS.md)
- **Developer Analysis**: [get-dev-tokens-guide.md](./get-dev-tokens-guide.md)
- **API Reference**: [api-reference.md](./api-reference.md)
- **Trading Guide**: [TRADING_GUIDE.md](./TRADING_GUIDE.md)

---

## Summary

The `get_holder_data()` method is essential for:
- ✅ **Risk assessment**: Identify concentration risk
- ✅ **Whale tracking**: Monitor large holders
- ✅ **Smart money analysis**: Follow successful traders
- ✅ **Distribution analysis**: Understand token spread
- ✅ **Sentiment analysis**: Gauge holder confidence

**Key Takeaways**:
1. Top 10 holders > 60% = High risk
2. Single holder > 15% = Extreme risk
3. Gini coefficient > 0.8 = Very concentrated
4. Monitor smart money for entry/exit signals
5. Use `only_tracked_wallets=True` to focus on key players

**Risk Indicators**:
- 🚩 Top holder > 15%
- 🚩 Top 10 > 60%
- 🚩 Top 20 > 80%
- 🚩 Gini coefficient > 0.8
- 🚩 Smart money exiting (negative PnL)

**Usage Pattern**:
```python
# Get holder data
holder_data = client.get_holder_data(pair_address)

# Check concentration risk
if holder_data['summary']['top10HoldingPercentage'] > 60:
    print("🚩 HIGH CONCENTRATION RISK")

# Check smart money sentiment
tracked = client.get_holder_data(pair_address, only_tracked_wallets=True)
smart_money = [h for h in tracked['holders'] if h.get('trackedReason') == 'Smart Money']

if len(smart_money) > 5:
    profitable = sum(1 for h in smart_money if h.get('pnlPercentage', 0) > 0)
    if profitable / len(smart_money) > 0.7:
        print("🟢 Smart money bullish")
```

For questions or issues, refer to the [troubleshooting guide](./troubleshooting.md) or open an issue on GitHub.
