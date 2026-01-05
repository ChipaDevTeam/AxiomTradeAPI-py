#!/usr/bin/env python3
"""
Test script for new AxiomTradeAPI functions
Tests all the new API10 endpoints added to the client
"""

import os
import sys
from dotenv import load_dotenv

# Add the package to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiomtradeapi.client import AxiomTradeClient

def test_new_api_functions():
    """Test all the new API functions"""
    
    print("🚀 AxiomTradeAPI - New API Functions Test")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize client
    client = AxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    # Test authentication
    print("\n🔐 Testing Authentication")
    print("-" * 40)
    if client.ensure_authenticated():
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed!")
        return
    
    # Example data from your curl commands
    pair_address = "Cr8Qy7quTPDdR3sET6fZk7bRFtiDFLeuwntgZGKJrnAY"
    wallet_address = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
    dev_address = "A3xbhvsma7XYmcouyFBCfzKot5dShxHtTrhyrSfBzyZV"
    token_ticker = "green"
    
    # Test 1: Token Info by Pair
    print("\n📊 Testing Token Info by Pair")
    print("-" * 40)
    try:
        token_info = client.get_token_info_by_pair(pair_address)
        print(f"✅ Token info retrieved for pair: {pair_address}")
        print(f"   Keys in response: {list(token_info.keys()) if isinstance(token_info, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get token info: {e}")
    
    # Test 2: Last Transaction
    print("\n📈 Testing Last Transaction")
    print("-" * 40)
    try:
        last_tx = client.get_last_transaction(pair_address)
        print(f"✅ Last transaction retrieved for pair: {pair_address}")
        print(f"   Keys in response: {list(last_tx.keys()) if isinstance(last_tx, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get last transaction: {e}")
    
    # Test 3: Pair Info
    print("\n🔗 Testing Pair Info")
    print("-" * 40)
    try:
        pair_info = client.get_pair_info(pair_address)
        print(f"✅ Pair info retrieved for pair: {pair_address}")
        print(f"   Keys in response: {list(pair_info.keys()) if isinstance(pair_info, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get pair info: {e}")
    
    # Test 4: Pair Stats
    print("\n📊 Testing Pair Stats")
    print("-" * 40)
    try:
        pair_stats = client.get_pair_stats(pair_address)
        print(f"✅ Pair stats retrieved for pair: {pair_address}")
        print(f"   Keys in response: {list(pair_stats.keys()) if isinstance(pair_stats, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get pair stats: {e}")
    
    # Test 5: Meme Open Positions
    print("\n💰 Testing Meme Open Positions")
    print("-" * 40)
    try:
        positions = client.get_meme_open_positions(wallet_address)
        print(f"✅ Open positions retrieved for wallet: {wallet_address}")
        print(f"   Keys in response: {list(positions.keys()) if isinstance(positions, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get open positions: {e}")
    
    # Test 6: Holder Data
    print("\n👥 Testing Holder Data")
    print("-" * 40)
    try:
        holder_data = client.get_holder_data(pair_address, only_tracked_wallets=False)
        print(f"✅ Holder data retrieved for pair: {pair_address}")
        print(f"   Keys in response: {list(holder_data.keys()) if isinstance(holder_data, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get holder data: {e}")
    
    # Test 7: Dev Tokens
    print("\n🔧 Testing Dev Tokens")
    print("-" * 40)
    try:
        dev_tokens = client.get_dev_tokens(dev_address)
        print(f"✅ Dev tokens retrieved for dev: {dev_address}")
        print(f"   Keys in response: {list(dev_tokens.keys()) if isinstance(dev_tokens, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get dev tokens: {e}")
    
    # Test 8: Token Analysis
    print("\n🔍 Testing Token Analysis")
    print("-" * 40)
    try:
        token_analysis = client.get_token_analysis(dev_address, token_ticker)
        print(f"✅ Token analysis retrieved for dev: {dev_address}, ticker: {token_ticker}")
        print(f"   Keys in response: {list(token_analysis.keys()) if isinstance(token_analysis, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Failed to get token analysis: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 All new API function tests completed!")
    
    print("\n📖 Usage Examples")
    print("-" * 40)
    print("""
# Example usage of new functions:
from axiomtradeapi.client import AxiomTradeClient
import os

client = AxiomTradeClient(
    auth_token=os.getenv('auth-access-token'),
    refresh_token=os.getenv('auth-refresh-token')
)

# Get detailed token information
token_info = client.get_token_info_by_pair("PAIR_ADDRESS")

# Get latest transaction for a pair
last_tx = client.get_last_transaction("PAIR_ADDRESS")

# Get pair information and statistics
pair_info = client.get_pair_info("PAIR_ADDRESS")
pair_stats = client.get_pair_stats("PAIR_ADDRESS")

# Get your open meme positions
positions = client.get_meme_open_positions("YOUR_WALLET_ADDRESS")

# Get holder data for a token
holders = client.get_holder_data("PAIR_ADDRESS", only_tracked_wallets=False)

# Get tokens created by a developer
dev_tokens = client.get_dev_tokens("DEV_ADDRESS")

# Get token analysis
analysis = client.get_token_analysis("DEV_ADDRESS", "TOKEN_TICKER")
""")

if __name__ == "__main__":
    test_new_api_functions()
