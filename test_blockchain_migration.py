#!/usr/bin/env python3
"""
Test script to verify blockchain migration for buy_token, sell_token, and balance methods.
This script tests the migrated functions without requiring actual transactions.
"""

import logging
import sys
from axiomtradeapi import AxiomTradeClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_balance_method():
    """Test GetBalance using Solana RPC"""
    logger.info("=" * 60)
    logger.info("Testing GetBalance with Solana RPC")
    logger.info("=" * 60)
    
    try:
        # Create a minimal client (we don't need auth for balance checks)
        # Using dummy credentials to initialize, but won't actually authenticate
        client = AxiomTradeClient(
            auth_token="dummy_token",  
            refresh_token="dummy_refresh"
        )
        
        # Test with a known Solana address (devnet faucet address)
        test_wallet = "4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY"
        
        logger.info(f"Fetching balance for wallet: {test_wallet}")
        balance = client.GetBalance(test_wallet)
        
        if balance is not None:
            logger.info(f"✅ GetBalance SUCCESS")
            logger.info(f"   Balance: {balance.get('sol', 0)} SOL")
            logger.info(f"   Lamports: {balance.get('lamports', 0)}")
            logger.info(f"   Slot: {balance.get('slot', 0)}")
            return True
        else:
            logger.error(f"❌ GetBalance returned None")
            return False
            
    except Exception as e:
        logger.error(f"❌ GetBalance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_batched_balance_method():
    """Test GetBatchedBalance using Solana RPC"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing GetBatchedBalance with Solana RPC")
    logger.info("=" * 60)
    
    try:
        client = AxiomTradeClient(
            auth_token="dummy_token",
            refresh_token="dummy_refresh"
        )
        
        # Test with multiple known addresses
        test_wallets = [
            "4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY",
            "11111111111111111111111111111111"  # System program address
        ]
        
        logger.info(f"Fetching balances for {len(test_wallets)} wallets")
        balances = client.GetBatchedBalance(test_wallets)
        
        if balances and isinstance(balances, dict):
            logger.info(f"✅ GetBatchedBalance SUCCESS")
            for wallet, balance in balances.items():
                if balance:
                    logger.info(f"   {wallet[:8]}...: {balance.get('sol', 0)} SOL")
                else:
                    logger.info(f"   {wallet[:8]}...: Error or 0 SOL")
            return True
        else:
            logger.error(f"❌ GetBatchedBalance returned invalid data")
            return False
            
    except Exception as e:
        logger.error(f"❌ GetBatchedBalance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_token_balance_method():
    """Test get_token_balance using Solana RPC"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing get_token_balance with Solana RPC")
    logger.info("=" * 60)
    
    try:
        client = AxiomTradeClient(
            auth_token="dummy_token",
            refresh_token="dummy_refresh"
        )
        
        # Test wallet and token (using a common token mint for testing)
        test_wallet = "4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY"
        # USDC mint address on Solana mainnet
        usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        
        logger.info(f"Fetching token balance for wallet: {test_wallet}")
        logger.info(f"Token mint: {usdc_mint}")
        
        balance = client.get_token_balance(test_wallet, usdc_mint)
        
        if balance is not None:
            logger.info(f"✅ get_token_balance SUCCESS")
            logger.info(f"   Token Balance: {balance}")
            return True
        else:
            logger.error(f"❌ get_token_balance returned None")
            return False
            
    except Exception as e:
        logger.error(f"❌ get_token_balance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_buy_sell_methods_structure():
    """Test that buy_token and sell_token have the correct structure (without executing)"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing buy_token and sell_token method structure")
    logger.info("=" * 60)
    
    try:
        client = AxiomTradeClient(
            auth_token="dummy_token",
            refresh_token="dummy_refresh"
        )
        
        # Check if methods exist and have correct signatures
        import inspect
        
        # Check buy_token
        buy_sig = inspect.signature(client.buy_token)
        buy_params = list(buy_sig.parameters.keys())
        logger.info(f"buy_token parameters: {buy_params}")
        
        expected_buy_params = ['private_key', 'token_mint', 'amount_sol', 'slippage_percent', 
                               'priority_fee', 'pool', 'rpc_url']
        
        if all(param in buy_params for param in expected_buy_params[:3]):  # Check required params
            logger.info("✅ buy_token has correct signature")
        else:
            logger.error("❌ buy_token signature mismatch")
            return False
        
        # Check sell_token
        sell_sig = inspect.signature(client.sell_token)
        sell_params = list(sell_sig.parameters.keys())
        logger.info(f"sell_token parameters: {sell_params}")
        
        expected_sell_params = ['private_key', 'token_mint', 'amount_tokens', 'slippage_percent',
                                'priority_fee', 'pool', 'rpc_url']
        
        if all(param in sell_params for param in expected_sell_params[:3]):  # Check required params
            logger.info("✅ sell_token has correct signature")
        else:
            logger.error("❌ sell_token signature mismatch")
            return False
            
        logger.info("✅ Both trading methods have correct structure")
        logger.info("   Note: Actual trading requires valid private key and cannot be tested here")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Method structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting Blockchain Migration Tests")
    logger.info("=" * 60)
    
    results = {
        "GetBalance": test_balance_method(),
        "GetBatchedBalance": test_batched_balance_method(),
        "get_token_balance": test_token_balance_method(),
        "Trading Methods Structure": test_buy_sell_methods_structure()
    }
    
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 60)
    logger.info(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed!")
        return 0
    else:
        logger.warning(f"⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
