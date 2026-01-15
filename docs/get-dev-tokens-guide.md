# get_dev_tokens() Method - Comprehensive Guide

## Overview

The `get_dev_tokens()` method retrieves all tokens created by a specific developer address on the Solana blockchain. This is essential for analyzing developer track records, identifying patterns in token launches, and performing due diligence before investing in tokens from a particular developer.

This method is particularly useful for:
- 🔍 **Due diligence**: Research developer history before investing
- 📊 **Risk assessment**: Check how many tokens a dev has created
- 🚩 **Rug pull detection**: Identify developers with suspicious patterns
- 📈 **Track record analysis**: See successful vs failed token launches

## Method Signature

```python
def get_dev_tokens(self, dev_address: str) -> Dict
```

## Parameters

### `dev_address` (str, required)
- **Description**: The Solana wallet address of the token developer/creator
- **Format**: Base58-encoded Solana public key (32-44 characters)
- **Example**: `"A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"`
- **Where to find**: 
  - Token metadata on explorers (Solscan, SolanaFM)
  - New pair WebSocket events (`deployer_address` field)
  - DEX Screener token information

## Return Value

Returns a dictionary containing developer token information:

```python
{
    "tokens": [
        {
            "tokenAddress": "TokenMintAddress123...",
            "tokenName": "Example Token",
            "tokenTicker": "EXMPL",
            "initialLiquiditySol": 1.5,
            "createdAt": "2026-01-10T12:30:00Z",
            "currentMarketCap": 25000,
            "priceChange24h": 15.5,
            "status": "active",  # or "rugged", "failed"
            "holders": 150,
            "pairAddress": "PairAddress456..."
        },
        # ... more tokens
    ],
    "counts": {
        "total": 25,
        "active": 10,
        "rugged": 8,
        "failed": 7
    },
    "statistics": {
        "successRate": 40.0,
        "averageInitialLiquidity": 2.5,
        "totalMarketCapCreated": 500000
    }
}
```

### Response Fields

#### `tokens` (Array)
List of all tokens created by the developer.

Each token object contains:
- **tokenAddress**: Token mint address
- **tokenName**: Token name
- **tokenTicker**: Token symbol/ticker
- **initialLiquiditySol**: Initial liquidity in SOL
- **createdAt**: Token creation timestamp
- **currentMarketCap**: Current market cap (if active)
- **priceChange24h**: 24-hour price change percentage
- **status**: Token status (active, rugged, failed)
- **holders**: Number of token holders
- **pairAddress**: DEX pair address

#### `counts` (Object)
Token count breakdown:
- **total**: Total number of tokens created
- **active**: Currently trading tokens
- **rugged**: Suspected rug pulls
- **failed**: Failed launches (no liquidity)

#### `statistics` (Object)
Developer statistics:
- **successRate**: Percentage of successful launches
- **averageInitialLiquidity**: Average initial liquidity
- **totalMarketCapCreated**: Sum of all market caps

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

### Example 1: Get All Developer Tokens
Retrieve complete list of tokens created by a developer.

```python
from axiomtradeapi.client import AxiomTradeClient

client = AxiomTradeClient()
client.login("username", "password")

# Developer address to investigate
dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"

# Get all tokens created by this developer
result = client.get_dev_tokens(dev_address)

print(f"📊 Developer Token Analysis")
print(f"=" * 50)
print(f"Total tokens created: {result['counts']['total']}")
print(f"Active tokens: {result['counts']['active']}")
print(f"Rugged tokens: {result['counts']['rugged']}")
print(f"Failed launches: {result['counts']['failed']}")

print(f"\n📈 Statistics:")
print(f"Success rate: {result['statistics']['successRate']:.1f}%")
print(f"Avg initial liquidity: {result['statistics']['averageInitialLiquidity']:.2f} SOL")
```

**Output:**
```
📊 Developer Token Analysis
==================================================
Total tokens created: 25
Active tokens: 10
Rugged tokens: 8
Failed launches: 7

📈 Statistics:
Success rate: 40.0%
Avg initial liquidity: 2.50 SOL
```

### Example 2: List Recent Tokens
Display the most recent tokens created by a developer.

```python
from axiomtradeapi.client import AxiomTradeClient
from datetime import datetime

client = AxiomTradeClient()
client.login("username", "password")

dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"
result = client.get_dev_tokens(dev_address)

print("🆕 Recent Tokens by Developer\n")

# Sort tokens by creation date (most recent first)
tokens = sorted(
    result['tokens'], 
    key=lambda x: x.get('createdAt', ''), 
    reverse=True
)

# Show last 5 tokens
for token in tokens[:5]:
    created_date = datetime.fromisoformat(token['createdAt'].replace('Z', '+00:00'))
    status_emoji = {
        'active': '✅',
        'rugged': '🚩',
        'failed': '❌'
    }.get(token.get('status'), '❓')
    
    print(f"{status_emoji} {token['tokenName']} ({token['tokenTicker']})")
    print(f"   Created: {created_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Initial liquidity: {token['initialLiquiditySol']} SOL")
    print(f"   Holders: {token.get('holders', 0)}")
    print(f"   Status: {token.get('status', 'unknown')}")
    print()
```

**Output:**
```
🆕 Recent Tokens by Developer

✅ Moon Token (MOON)
   Created: 2026-01-13 14:30
   Initial liquidity: 5.0 SOL
   Holders: 245
   Status: active

🚩 Rug Token (RUG)
   Created: 2026-01-12 09:15
   Initial liquidity: 1.0 SOL
   Holders: 12
   Status: rugged

❌ Failed Token (FAIL)
   Created: 2026-01-11 16:45
   Initial liquidity: 0.5 SOL
   Holders: 3
   Status: failed
```

### Example 3: Calculate Risk Score
Assess developer risk based on their token history.

```python
from axiomtradeapi.client import AxiomTradeClient

def calculate_dev_risk_score(dev_address: str) -> dict:
    """
    Calculate developer risk score based on token history
    
    Returns:
        dict with risk_score (0-100), risk_level, and reasons
    """
    client = AxiomTradeClient()
    client.login("username", "password")
    
    result = client.get_dev_tokens(dev_address)
    counts = result['counts']
    stats = result['statistics']
    
    # Calculate risk factors
    risk_score = 0
    risk_factors = []
    
    # High rug count
    rug_rate = (counts['rugged'] / counts['total']) * 100 if counts['total'] > 0 else 0
    if rug_rate > 50:
        risk_score += 40
        risk_factors.append(f"High rug rate: {rug_rate:.1f}%")
    elif rug_rate > 30:
        risk_score += 25
        risk_factors.append(f"Moderate rug rate: {rug_rate:.1f}%")
    
    # Many failed launches
    fail_rate = (counts['failed'] / counts['total']) * 100 if counts['total'] > 0 else 0
    if fail_rate > 40:
        risk_score += 20
        risk_factors.append(f"High failure rate: {fail_rate:.1f}%")
    
    # Low success rate
    if stats['successRate'] < 30:
        risk_score += 20
        risk_factors.append(f"Low success rate: {stats['successRate']:.1f}%")
    
    # Too many tokens (pump and dump pattern)
    if counts['total'] > 20:
        risk_score += 15
        risk_factors.append(f"Excessive tokens: {counts['total']}")
    
    # Low average liquidity
    if stats['averageInitialLiquidity'] < 1.0:
        risk_score += 15
        risk_factors.append(f"Low avg liquidity: {stats['averageInitialLiquidity']:.2f} SOL")
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "🔴 HIGH RISK"
    elif risk_score >= 40:
        risk_level = "🟡 MEDIUM RISK"
    else:
        risk_level = "🟢 LOW RISK"
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "developer_stats": {
            "total_tokens": counts['total'],
            "success_rate": stats['successRate'],
            "rug_rate": rug_rate,
            "fail_rate": fail_rate
        }
    }

# Usage
dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"
risk_assessment = calculate_dev_risk_score(dev_address)

print("🛡️  Developer Risk Assessment")
print("=" * 50)
print(f"Risk Level: {risk_assessment['risk_level']}")
print(f"Risk Score: {risk_assessment['risk_score']}/100")
print(f"\n⚠️  Risk Factors:")
for factor in risk_assessment['risk_factors']:
    print(f"   - {factor}")
```

**Output:**
```
🛡️  Developer Risk Assessment
==================================================
Risk Level: 🔴 HIGH RISK
Risk Score: 75/100

⚠️  Risk Factors:
   - High rug rate: 52.0%
   - Excessive tokens: 25
   - Low avg liquidity: 0.85 SOL
```

---

## Advanced Examples

### Example 4: Developer Comparison Tool
Compare multiple developers side-by-side.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import List, Dict

class DeveloperComparison:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
    
    def compare_developers(self, dev_addresses: List[str]) -> Dict:
        """
        Compare multiple developers
        
        Args:
            dev_addresses: List of developer addresses to compare
            
        Returns:
            Comparison data with rankings
        """
        print("📊 Comparing Developers...\n")
        
        comparisons = []
        
        for dev_addr in dev_addresses:
            try:
                result = self.client.get_dev_tokens(dev_addr)
                counts = result['counts']
                stats = result['statistics']
                
                comparisons.append({
                    "address": dev_addr[:8] + "...",
                    "total_tokens": counts['total'],
                    "success_rate": stats['successRate'],
                    "rug_rate": (counts['rugged'] / counts['total'] * 100) if counts['total'] > 0 else 0,
                    "avg_liquidity": stats['averageInitialLiquidity'],
                    "total_market_cap": stats['totalMarketCapCreated']
                })
            except Exception as e:
                print(f"   ❌ Error fetching data for {dev_addr[:8]}...: {e}")
        
        # Sort by success rate (descending)
        comparisons.sort(key=lambda x: x['success_rate'], reverse=True)
        
        return comparisons
    
    def display_comparison(self, comparisons: List[Dict]):
        """Display comparison table"""
        print("🏆 Developer Rankings (by Success Rate)")
        print("=" * 80)
        print(f"{'Rank':<6} {'Developer':<15} {'Success':<10} {'Rug Rate':<10} {'Tokens':<8} {'Avg Liq':<10}")
        print("-" * 80)
        
        for i, comp in enumerate(comparisons, 1):
            print(f"{i:<6} {comp['address']:<15} {comp['success_rate']:<9.1f}% "
                  f"{comp['rug_rate']:<9.1f}% {comp['total_tokens']:<8} "
                  f"{comp['avg_liquidity']:<9.2f} SOL")
        
        print("\n📈 Best Developer:")
        best = comparisons[0]
        print(f"   {best['address']} - {best['success_rate']:.1f}% success rate")
        
        print("\n⚠️  Worst Developer:")
        worst = comparisons[-1]
        print(f"   {worst['address']} - {worst['success_rate']:.1f}% success rate")

# Usage
comparator = DeveloperComparison()

devs_to_compare = [
    "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV",
    "B8yjZ4nL3mN2oP1qR5sT6uV7wX8yZ9aA1bC2dE3fG4hH",
    "C2zY1xW3vU4tS5rQ6pO7nM8lK9jI0hG1fE2dC3bA4ZXY"
]

comparisons = comparator.compare_developers(devs_to_compare)
comparator.display_comparison(comparisons)
```

**Output:**
```
📊 Comparing Developers...

🏆 Developer Rankings (by Success Rate)
================================================================================
Rank   Developer       Success    Rug Rate   Tokens   Avg Liq   
--------------------------------------------------------------------------------
1      B8yjZ4nL...     65.0%      15.0%      20       3.50 SOL
2      A3xbhvsm...     40.0%      32.0%      25       2.50 SOL
3      C2zY1xW3...     25.0%      55.0%      30       1.20 SOL

📈 Best Developer:
   B8yjZ4nL... - 65.0% success rate

⚠️  Worst Developer:
   C2zY1xW3... - 25.0% success rate
```

### Example 5: Token Launch Monitor
Monitor when a developer creates new tokens.

```python
from axiomtradeapi.client import AxiomTradeClient
import time
from datetime import datetime

class DeveloperMonitor:
    """Monitor developers for new token launches"""
    
    def __init__(self, dev_addresses: List[str]):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
        self.dev_addresses = dev_addresses
        self.known_tokens = {}  # Track known tokens per developer
        
        # Initialize known tokens
        for dev_addr in dev_addresses:
            self.update_known_tokens(dev_addr)
    
    def update_known_tokens(self, dev_addr: str):
        """Update list of known tokens for a developer"""
        try:
            result = self.client.get_dev_tokens(dev_addr)
            token_addresses = [t['tokenAddress'] for t in result['tokens']]
            self.known_tokens[dev_addr] = set(token_addresses)
        except Exception as e:
            print(f"❌ Error updating tokens for {dev_addr[:8]}...: {e}")
    
    def check_for_new_tokens(self, dev_addr: str) -> List[Dict]:
        """Check if developer has launched new tokens"""
        try:
            result = self.client.get_dev_tokens(dev_addr)
            current_tokens = {t['tokenAddress']: t for t in result['tokens']}
            
            # Find new tokens
            new_tokens = []
            for token_addr, token_data in current_tokens.items():
                if token_addr not in self.known_tokens[dev_addr]:
                    new_tokens.append(token_data)
                    self.known_tokens[dev_addr].add(token_addr)
            
            return new_tokens
        except Exception as e:
            print(f"❌ Error checking {dev_addr[:8]}...: {e}")
            return []
    
    def start_monitoring(self, check_interval: int = 60):
        """
        Start monitoring loop
        
        Args:
            check_interval: Seconds between checks
        """
        print(f"👀 Monitoring {len(self.dev_addresses)} developers for new launches")
        print(f"   Check interval: {check_interval}s\n")
        
        try:
            while True:
                for dev_addr in self.dev_addresses:
                    new_tokens = self.check_for_new_tokens(dev_addr)
                    
                    if new_tokens:
                        self.notify_new_tokens(dev_addr, new_tokens)
                
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n⏹️  Monitoring stopped")
    
    def notify_new_tokens(self, dev_addr: str, new_tokens: List[Dict]):
        """Notify about new token launches"""
        print(f"\n🚨 NEW TOKEN LAUNCH DETECTED!")
        print(f"   Developer: {dev_addr[:8]}...")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for token in new_tokens:
            print(f"\n   Token: {token['tokenName']} ({token['tokenTicker']})")
            print(f"   Address: {token['tokenAddress']}")
            print(f"   Initial Liquidity: {token['initialLiquiditySol']} SOL")
            print(f"   Pair: {token.get('pairAddress', 'N/A')}")

# Usage
monitor = DeveloperMonitor([
    "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV",
    "B8yjZ4nL3mN2oP1qR5sT6uV7wX8yZ9aA1bC2dE3fG4hH"
])

# Start monitoring (checks every 60 seconds)
monitor.start_monitoring(check_interval=60)
```

**Output:**
```
👀 Monitoring 2 developers for new launches
   Check interval: 60s

🚨 NEW TOKEN LAUNCH DETECTED!
   Developer: A3xbhvsm...
   Time: 2026-01-14 15:42:30

   Token: SafeMoon 2.0 (SAFE2)
   Address: TokenAddress789...
   Initial Liquidity: 3.5 SOL
   Pair: PairAddress123...
```

### Example 6: Developer Reputation System
Build a reputation score for developers based on multiple factors.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import Dict
import json

class DeveloperReputation:
    """Calculate comprehensive developer reputation"""
    
    def __init__(self):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
    
    def calculate_reputation(self, dev_address: str) -> Dict:
        """
        Calculate comprehensive reputation score (0-100)
        
        Factors considered:
        - Success rate (40 points)
        - Token longevity (20 points)
        - Average liquidity (15 points)
        - Holder retention (15 points)
        - Rug history (10 points penalty)
        """
        result = self.client.get_dev_tokens(dev_address)
        counts = result['counts']
        stats = result['statistics']
        tokens = result['tokens']
        
        score = 0
        breakdown = {}
        
        # 1. Success Rate (0-40 points)
        success_points = (stats['successRate'] / 100) * 40
        score += success_points
        breakdown['success_rate'] = {
            'points': round(success_points, 1),
            'max': 40,
            'value': stats['successRate']
        }
        
        # 2. Token Longevity (0-20 points)
        active_tokens = [t for t in tokens if t.get('status') == 'active']
        if active_tokens:
            # Average age of active tokens (simplified)
            avg_age_score = min(len(active_tokens) / counts['total'], 1.0) * 20
        else:
            avg_age_score = 0
        score += avg_age_score
        breakdown['longevity'] = {
            'points': round(avg_age_score, 1),
            'max': 20,
            'active_tokens': len(active_tokens)
        }
        
        # 3. Average Liquidity (0-15 points)
        liq_score = min(stats['averageInitialLiquidity'] / 5.0, 1.0) * 15
        score += liq_score
        breakdown['liquidity'] = {
            'points': round(liq_score, 1),
            'max': 15,
            'avg_liquidity': stats['averageInitialLiquidity']
        }
        
        # 4. Holder Retention (0-15 points)
        if active_tokens:
            avg_holders = sum(t.get('holders', 0) for t in active_tokens) / len(active_tokens)
            holder_score = min(avg_holders / 100, 1.0) * 15
        else:
            holder_score = 0
        score += holder_score
        breakdown['holder_retention'] = {
            'points': round(holder_score, 1),
            'max': 15,
            'avg_holders': round(avg_holders, 0) if active_tokens else 0
        }
        
        # 5. Rug Penalty (-10 points per rug, max -30)
        rug_penalty = min(counts['rugged'] * 10, 30)
        score -= rug_penalty
        breakdown['rug_penalty'] = {
            'points': -rug_penalty,
            'max': -30,
            'rug_count': counts['rugged']
        }
        
        # Ensure score is between 0-100
        final_score = max(0, min(100, score))
        
        # Determine reputation tier
        if final_score >= 80:
            tier = "🏆 LEGENDARY"
            recommendation = "Highly trusted developer"
        elif final_score >= 60:
            tier = "⭐ REPUTABLE"
            recommendation = "Generally reliable developer"
        elif final_score >= 40:
            tier = "⚠️  AVERAGE"
            recommendation = "Proceed with caution"
        elif final_score >= 20:
            tier = "🚩 RISKY"
            recommendation = "High risk, be very careful"
        else:
            tier = "🔴 DANGEROUS"
            recommendation = "Avoid - high rug risk"
        
        return {
            'score': round(final_score, 1),
            'tier': tier,
            'recommendation': recommendation,
            'breakdown': breakdown,
            'developer_address': dev_address
        }
    
    def display_reputation(self, reputation: Dict):
        """Display reputation report"""
        print(f"👤 Developer Reputation Report")
        print("=" * 60)
        print(f"Developer: {reputation['developer_address'][:16]}...")
        print(f"Reputation Score: {reputation['score']}/100")
        print(f"Tier: {reputation['tier']}")
        print(f"Recommendation: {reputation['recommendation']}")
        
        print(f"\n📊 Score Breakdown:")
        for factor, data in reputation['breakdown'].items():
            print(f"   {factor.replace('_', ' ').title()}: "
                  f"{data['points']}/{data['max']} points")
            if 'value' in data:
                print(f"      ({data['value']})")
            elif 'rug_count' in data:
                print(f"      ({data['rug_count']} rugs)")

# Usage
reputation_system = DeveloperReputation()

dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"
reputation = reputation_system.calculate_reputation(dev_address)
reputation_system.display_reputation(reputation)

# Save reputation to file
with open(f"dev_reputation_{dev_address[:8]}.json", 'w') as f:
    json.dump(reputation, f, indent=2)
print(f"\n💾 Reputation saved to file")
```

**Output:**
```
👤 Developer Reputation Report
============================================================
Developer: A3xbhvsma7XYmc...
Reputation Score: 42.5/100
Tier: ⚠️  AVERAGE
Recommendation: Proceed with caution

📊 Score Breakdown:
   Success Rate: 16.0/40 points
      (40.0%)
   Longevity: 8.0/20 points
      (10 active tokens)
   Liquidity: 7.5/15 points
      (2.5 SOL avg)
   Holder Retention: 11.0/15 points
      (73 avg holders)
   Rug Penalty: -30/-30 points
      (8 rugs)

💾 Reputation saved to file
```

### Example 7: Automated Investment Filter
Filter investment opportunities based on developer reputation.

```python
from axiomtradeapi.client import AxiomTradeClient
from typing import List, Dict

class InvestmentFilter:
    """Filter tokens based on developer criteria"""
    
    def __init__(self, min_success_rate: float = 50.0, max_rug_rate: float = 20.0):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
        self.min_success_rate = min_success_rate
        self.max_rug_rate = max_rug_rate
    
    def evaluate_developer(self, dev_address: str) -> Dict:
        """Evaluate if developer meets investment criteria"""
        result = self.client.get_dev_tokens(dev_address)
        counts = result['counts']
        stats = result['statistics']
        
        rug_rate = (counts['rugged'] / counts['total'] * 100) if counts['total'] > 0 else 0
        
        # Check criteria
        passes_success = stats['successRate'] >= self.min_success_rate
        passes_rug = rug_rate <= self.max_rug_rate
        passes_overall = passes_success and passes_rug
        
        return {
            'dev_address': dev_address,
            'passes': passes_overall,
            'success_rate': stats['successRate'],
            'rug_rate': rug_rate,
            'total_tokens': counts['total'],
            'active_tokens': counts['active'],
            'criteria': {
                'success_rate': {
                    'required': self.min_success_rate,
                    'actual': stats['successRate'],
                    'passes': passes_success
                },
                'rug_rate': {
                    'max_allowed': self.max_rug_rate,
                    'actual': rug_rate,
                    'passes': passes_rug
                }
            }
        }
    
    def should_invest_in_token(self, token_info: Dict) -> bool:
        """
        Determine if a token is worth investing based on developer
        
        Args:
            token_info: Token information with deployer_address field
            
        Returns:
            True if token passes developer criteria, False otherwise
        """
        dev_address = token_info.get('deployer_address')
        if not dev_address:
            print("⚠️  No developer address available")
            return False
        
        evaluation = self.evaluate_developer(dev_address)
        
        if evaluation['passes']:
            print(f"✅ PASS - Developer meets criteria")
            print(f"   Success Rate: {evaluation['success_rate']:.1f}% (min: {self.min_success_rate}%)")
            print(f"   Rug Rate: {evaluation['rug_rate']:.1f}% (max: {self.max_rug_rate}%)")
            return True
        else:
            print(f"❌ FAIL - Developer doesn't meet criteria")
            for criterion, data in evaluation['criteria'].items():
                status = "✅" if data['passes'] else "❌"
                print(f"   {status} {criterion}: {data['actual']:.1f}%")
            return False

# Usage
investment_filter = InvestmentFilter(
    min_success_rate=50.0,  # Require 50%+ success rate
    max_rug_rate=20.0       # Allow max 20% rug rate
)

# Example: Evaluating a token from WebSocket
new_token = {
    'token_name': 'NewCoin',
    'token_address': 'TokenAddr123...',
    'deployer_address': 'A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV',
    'initial_liquidity_sol': 2.5
}

print(f"🔍 Evaluating: {new_token['token_name']}")
print(f"   Liquidity: {new_token['initial_liquidity_sol']} SOL\n")

should_invest = investment_filter.should_invest_in_token(new_token)

if should_invest:
    print(f"\n💰 Recommendation: CONSIDER INVESTING")
else:
    print(f"\n🚫 Recommendation: SKIP THIS TOKEN")
```

**Output:**
```
🔍 Evaluating: NewCoin
   Liquidity: 2.5 SOL

❌ FAIL - Developer doesn't meet criteria
   ❌ success_rate: 40.0%
   ❌ rug_rate: 32.0%

🚫 Recommendation: SKIP THIS TOKEN
```

---

## Best Practices

### 1. Cache Results for Performance
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedDevTokens:
    def __init__(self):
        self.client = AxiomTradeClient()
        self.client.login("username", "password")
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    def get_dev_tokens_cached(self, dev_address: str):
        """Get developer tokens with caching"""
        now = datetime.now()
        
        if dev_address in self.cache:
            cached_data, cached_time = self.cache[dev_address]
            if now - cached_time < self.cache_duration:
                print(f"📦 Using cached data (age: {(now - cached_time).seconds}s)")
                return cached_data
        
        # Fetch fresh data
        print(f"🔄 Fetching fresh data for {dev_address[:8]}...")
        result = self.client.get_dev_tokens(dev_address)
        self.cache[dev_address] = (result, now)
        return result
```

### 2. Handle Large Token Lists
```python
def process_dev_tokens_in_batches(dev_address: str, batch_size: int = 10):
    """Process large token lists in batches"""
    result = client.get_dev_tokens(dev_address)
    tokens = result['tokens']
    
    for i in range(0, len(tokens), batch_size):
        batch = tokens[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}...")
        
        for token in batch:
            # Process each token
            analyze_token(token)
        
        # Optional: Add delay between batches
        time.sleep(1)
```

### 3. Combine with Other Analysis Methods
```python
def comprehensive_token_analysis(dev_address: str, token_ticker: str):
    """Combine multiple API methods for complete analysis"""
    # Get all developer tokens
    dev_tokens = client.get_dev_tokens(dev_address)
    
    # Get specific token analysis
    token_analysis = client.get_token_analysis(dev_address, token_ticker)
    
    # Combine results
    return {
        'developer_history': dev_tokens,
        'token_specific_analysis': token_analysis,
        'combined_risk_score': calculate_risk(dev_tokens, token_analysis)
    }
```

### 4. Log Developer Investigations
```python
import logging
from datetime import datetime

logging.basicConfig(
    filename='dev_investigations.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log_dev_investigation(dev_address: str, result: Dict):
    """Log developer investigations for audit trail"""
    logging.info(f"Developer: {dev_address}")
    logging.info(f"Total tokens: {result['counts']['total']}")
    logging.info(f"Success rate: {result['statistics']['successRate']}%")
    logging.info(f"Rug count: {result['counts']['rugged']}")
    logging.info("=" * 50)
```

### 5. Validate Developer Addresses
```python
def validate_dev_address(address: str) -> bool:
    """Validate Solana address format"""
    import base58
    
    try:
        # Solana addresses are base58 encoded and 32-44 characters
        if len(address) < 32 or len(address) > 44:
            return False
        
        # Try to decode as base58
        decoded = base58.b58decode(address)
        return len(decoded) == 32
    except:
        return False

# Usage
if validate_dev_address(dev_address):
    result = client.get_dev_tokens(dev_address)
else:
    print("Invalid developer address format")
```

---

## Troubleshooting

### Issue: "Authentication failed"

**Problem**: Method returns authentication error.

**Solution**:
```python
# Ensure you're authenticated
if not client.ensure_authenticated():
    client.login("username", "password")

# Then retry
result = client.get_dev_tokens(dev_address)
```

### Issue: Empty or No Token Data

**Problem**: Returns empty token list or minimal data.

**Possible Causes**:
1. Developer hasn't created any tokens yet
2. Invalid developer address
3. Tokens not indexed yet (very recent launches)

**Solution**:
```python
result = client.get_dev_tokens(dev_address)

if result['counts']['total'] == 0:
    print("This developer hasn't created any tokens yet")
elif len(result['tokens']) == 0:
    print("Developer address may be invalid or not indexed")
```

### Issue: Rate Limiting

**Problem**: Too many requests in short time period.

**Solution**:
```python
import time

dev_addresses = ["Dev1...", "Dev2...", "Dev3..."]

for dev_addr in dev_addresses:
    result = client.get_dev_tokens(dev_addr)
    # Process result...
    
    # Add delay between requests
    time.sleep(2)  # 2 second delay
```

### Issue: Slow Performance

**Problem**: Method takes long time to return results.

**Solutions**:
1. Use caching (see Best Practices)
2. Fetch during off-peak hours
3. Process token lists in batches
4. Consider using background tasks

---

## Related Methods

### `get_token_analysis()`
Get detailed analysis for a specific token from a developer.

```python
# Get all developer tokens
dev_tokens = client.get_dev_tokens(dev_address)

# Then analyze a specific token
token_analysis = client.get_token_analysis(dev_address, "TOKENTICKER")
```

### `get_holder_data()`
Get holder information for tokens created by developer.

```python
# Get developer's tokens
dev_tokens = client.get_dev_tokens(dev_address)

# Get holder data for each token
for token in dev_tokens['tokens']:
    holders = client.get_holder_data(token['pairAddress'])
```

### `get_pair_info()`
Get detailed pair information for developer's tokens.

```python
dev_tokens = client.get_dev_tokens(dev_address)

for token in dev_tokens['tokens']:
    if token.get('pairAddress'):
        pair_info = client.get_pair_info(token['pairAddress'])
```

---

## Additional Resources

- **Token Analysis**: [NEW_API_FUNCTIONS.md](./NEW_API_FUNCTIONS.md)
- **WebSocket Monitoring**: [websocket-guide.md](./websocket-guide.md)
- **Trading Guide**: [TRADING_GUIDE.md](./TRADING_GUIDE.md)
- **Authentication**: [authentication.md](./authentication.md)
- **API Reference**: [api-reference.md](./api-reference.md)

---

## Summary

The `get_dev_tokens()` method is essential for:
- ✅ **Developer due diligence**: Research before investing
- ✅ **Risk assessment**: Identify high-risk developers
- ✅ **Pattern recognition**: Spot pump-and-dump schemes
- ✅ **Track record analysis**: Evaluate developer history
- ✅ **Investment filtering**: Automate token screening

**Key Takeaways**:
1. Always check developer history before investing
2. High rug count = major red flag
3. Success rate < 30% = avoid
4. Too many tokens (20+) = potential pump-and-dump
5. Low average liquidity = higher risk
6. Combine with `get_token_analysis()` for comprehensive view

**Risk Indicators**:
- 🚩 Rug rate > 30%
- 🚩 Success rate < 30%
- 🚩 More than 20 tokens created
- 🚩 Average liquidity < 1 SOL
- 🚩 Many recent failures

**Usage Pattern**:
```python
# Initialize
client = AxiomTradeClient()
client.login("username", "password")

# Get developer tokens
result = client.get_dev_tokens(dev_address)

# Check risk
if result['counts']['rugged'] > result['counts']['total'] * 0.3:
    print("🚩 HIGH RUG RISK - Avoid this developer")
elif result['statistics']['successRate'] < 30:
    print("⚠️  Low success rate - Be cautious")
else:
    print("✅ Developer looks relatively safe")
```

For questions or issues, refer to the [troubleshooting guide](./troubleshooting.md) or open an issue on GitHub.
