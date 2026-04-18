"""
Enhanced AxiomTradeAPI with Multiple Trading SDKs
================================================

This enhanced version supports:
1. PumpPortal API (current working method)
2. Jupiter API (universal Solana token swapping)
3. Direct Raydium integration
4. Direct Pump.fun integration

Automatically chooses the best method for each token.
"""

from axiomtradeapi.client import AxiomTradeClient
import requests
import json
from typing import Dict, Union, Optional
import dotenv
import os

class EnhancedAxiomTradeClient(AxiomTradeClient):
    """Enhanced client with multiple trading SDK support"""
    
    def __init__(self, auth_token: str = None, refresh_token: str = None):
        super().__init__(auth_token=auth_token, refresh_token=refresh_token)
        self.jupiter_url = "https://quote-api.jup.ag/v6"
        self.sol_mint = "So11111111111111111111111111111111111111112"
        
    def smart_buy_token(self, private_key: str, token_mint: str, amount_sol: float, 
                       slippage_percent: float = 10) -> Dict[str, Union[str, bool]]:
        """
        Smart buy function that tries multiple methods:
        1. PumpPortal (fastest for supported tokens)
        2. Jupiter API (universal support)
        3. Direct Raydium (if needed)
        """
        
        print(f"🔍 Finding best trading method for token: {token_mint}")
        
        # Method 1: Try PumpPortal first (works for pump.fun tokens)
        print("1️⃣ Trying PumpPortal...")
        try:
            pumpportal_result = self.buy_token(
                private_key=private_key,
                token_mint=token_mint,
                amount=amount_sol,
                slippage_percent=slippage_percent,
                pool="auto",
                denominated_in_sol=True
            )
            
            if pumpportal_result["success"]:
                print("✅ PumpPortal successful!")
                pumpportal_result["method"] = "PumpPortal"
                return pumpportal_result
            else:
                print(f"❌ PumpPortal failed: {pumpportal_result['error'][:50]}...")
        except Exception as e:
            print(f"❌ PumpPortal error: {str(e)[:50]}...")
        
        # Method 2: Try Jupiter API (universal Solana DEX aggregator)
        print("2️⃣ Trying Jupiter API...")
        try:
            jupiter_result = self.jupiter_buy_token(
                private_key=private_key,
                token_mint=token_mint,
                amount_sol=amount_sol,
                slippage_percent=slippage_percent
            )
            
            if jupiter_result["success"]:
                print("✅ Jupiter API successful!")
                jupiter_result["method"] = "Jupiter"
                return jupiter_result
            else:
                print(f"❌ Jupiter failed: {jupiter_result['error'][:50]}...")
        except Exception as e:
            print(f"❌ Jupiter error: {str(e)[:50]}...")
        
        # Method 3: Try direct Raydium
        print("3️⃣ Trying Raydium direct...")
        try:
            raydium_result = self.raydium_buy_token(
                private_key=private_key,
                token_mint=token_mint,
                amount_sol=amount_sol,
                slippage_percent=slippage_percent
            )
            
            if raydium_result["success"]:
                print("✅ Raydium successful!")
                raydium_result["method"] = "Raydium"
                return raydium_result
            else:
                print(f"❌ Raydium failed: {raydium_result['error'][:50]}...")
        except Exception as e:
            print(f"❌ Raydium error: {str(e)[:50]}...")
        
        return {
            "success": False,
            "error": "All trading methods failed. Token may not be tradeable or insufficient liquidity.",
            "method": "None"
        }
    
    def jupiter_buy_token(self, private_key: str, token_mint: str, amount_sol: float, 
                         slippage_percent: float = 10) -> Dict[str, Union[str, bool]]:
        """
        Buy tokens using Jupiter API (universal Solana DEX aggregator)
        Jupiter supports almost all Solana tokens across all DEXs
        """
        try:
            amount_lamports = int(amount_sol * 1_000_000_000)
            
            # Step 1: Get quote from Jupiter
            quote_url = f"{self.jupiter_url}/quote"
            quote_params = {
                "inputMint": self.sol_mint,  # SOL
                "outputMint": token_mint,    # Target token
                "amount": amount_lamports,   # Amount in lamports
                "slippageBps": int(slippage_percent * 100),  # Slippage in basis points
                "onlyDirectRoutes": "false"  # Allow multi-hop routes
            }
            
            print(f"   Getting quote for {amount_sol} SOL → {token_mint}")
            quote_response = requests.get(quote_url, params=quote_params, timeout=10)
            
            if quote_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Jupiter quote failed: {quote_response.status_code} - {quote_response.text}"
                }
            
            quote_data = quote_response.json()
            
            if "routePlan" not in quote_data:
                return {
                    "success": False,
                    "error": "No route found for this token pair"
                }
            
            print(f"   ✅ Quote received: {quote_data.get('outAmount', 'Unknown')} tokens")
            
            # Step 2: Get swap transaction from Jupiter
            from solders.keypair import Keypair
            keypair = Keypair.from_base58_string(private_key)
            user_public_key = str(keypair.pubkey())
            
            swap_url = f"{self.jupiter_url}/swap"
            swap_payload = {
                "quoteResponse": quote_data,
                "userPublicKey": user_public_key,
                "wrapAndUnwrapSol": True,  # Handle SOL wrapping automatically
                "dynamicComputeUnitLimit": True,  # Optimize compute units
                "prioritizationFeeLamports": 1000  # Priority fee
            }
            
            print(f"   Creating swap transaction...")
            swap_response = requests.post(
                swap_url, 
                json=swap_payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if swap_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Jupiter swap failed: {swap_response.status_code} - {swap_response.text}"
                }
            
            swap_data = swap_response.json()
            
            if "swapTransaction" not in swap_data:
                return {
                    "success": False,
                    "error": "No swap transaction received from Jupiter"
                }
            
            # Step 3: Sign and send transaction
            print(f"   Signing and sending transaction...")
            
            import base64
            from solders.transaction import VersionedTransaction
            from solders.commitment_config import CommitmentLevel
            from solders.rpc.requests import SendVersionedTransaction
            from solders.rpc.config import RpcSendTransactionConfig
            
            # Decode transaction
            swap_transaction_b64 = swap_data["swapTransaction"]
            swap_transaction_bytes = base64.b64decode(swap_transaction_b64)
            
            # Create versioned transaction and sign
            transaction = VersionedTransaction.from_bytes(swap_transaction_bytes)
            signed_tx = VersionedTransaction(transaction.message, [keypair])
            
            # Send to RPC
            commitment = CommitmentLevel.Confirmed
            config = RpcSendTransactionConfig(preflight_commitment=commitment)
            
            rpc_response = requests.post(
                url="https://api.mainnet-beta.solana.com/",
                headers={"Content-Type": "application/json"},
                data=SendVersionedTransaction(signed_tx, config).to_json(),
                timeout=30
            )
            
            if rpc_response.status_code == 200:
                result = rpc_response.json()
                if "result" in result:
                    signature = result["result"]
                    return {
                        "success": True,
                        "signature": signature,
                        "transactionId": signature,
                        "explorer_url": f"https://solscan.io/tx/{signature}",
                        "method": "Jupiter",
                        "route": quote_data.get("routePlan", [])
                    }
                else:
                    return {
                        "success": False,
                        "error": f"RPC error: {result.get('error', 'Unknown error')}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"RPC failed: {rpc_response.status_code} - {rpc_response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Jupiter trading error: {str(e)}"
            }
    
    def raydium_buy_token(self, private_key: str, token_mint: str, amount_sol: float, 
                         slippage_percent: float = 10) -> Dict[str, Union[str, bool]]:
        """
        Buy tokens using direct Raydium integration
        This is a placeholder for direct Raydium SDK integration
        """
        # TODO: Implement direct Raydium SDK integration
        # For now, return a placeholder response
        return {
            "success": False,
            "error": "Direct Raydium integration not yet implemented. Use Jupiter for Raydium tokens."
        }
    
    def smart_sell_token(self, private_key: str, token_mint: str, amount_tokens: float, 
                        slippage_percent: float = 10) -> Dict[str, Union[str, bool]]:
        """
        Smart sell function that tries multiple methods
        """
        print(f"🔍 Finding best selling method for token: {token_mint}")
        
        # Try PumpPortal first
        print("1️⃣ Trying PumpPortal...")
        try:
            pumpportal_result = self.sell_token(
                private_key=private_key,
                token_mint=token_mint,
                amount=amount_tokens,
                slippage_percent=slippage_percent,
                pool="auto",
                denominated_in_sol=False
            )
            
            if pumpportal_result["success"]:
                print("✅ PumpPortal successful!")
                pumpportal_result["method"] = "PumpPortal"
                return pumpportal_result
            else:
                print(f"❌ PumpPortal failed: {pumpportal_result['error'][:50]}...")
        except Exception as e:
            print(f"❌ PumpPortal error: {str(e)[:50]}...")
        
        # Try Jupiter API
        print("2️⃣ Trying Jupiter API...")
        try:
            jupiter_result = self.jupiter_sell_token(
                private_key=private_key,
                token_mint=token_mint,
                amount_tokens=amount_tokens,
                slippage_percent=slippage_percent
            )
            
            if jupiter_result["success"]:
                print("✅ Jupiter API successful!")
                jupiter_result["method"] = "Jupiter"
                return jupiter_result
            else:
                print(f"❌ Jupiter failed: {jupiter_result['error'][:50]}...")
        except Exception as e:
            print(f"❌ Jupiter error: {str(e)[:50]}...")
        
        return {
            "success": False,
            "error": "All selling methods failed.",
            "method": "None"
        }
    
    def jupiter_sell_token(self, private_key: str, token_mint: str, amount_tokens: float, 
                          slippage_percent: float = 10) -> Dict[str, Union[str, bool]]:
        """
        Sell tokens using Jupiter API (swap tokens for SOL)
        """
        try:
            # For selling, we swap token → SOL
            amount_tokens_int = int(amount_tokens)
            
            # Get quote
            quote_url = f"{self.jupiter_url}/quote"
            quote_params = {
                "inputMint": token_mint,        # Token we're selling
                "outputMint": self.sol_mint,    # SOL
                "amount": amount_tokens_int,    # Amount of tokens
                "slippageBps": int(slippage_percent * 100),
                "onlyDirectRoutes": "false"
            }
            
            print(f"   Getting quote for {amount_tokens} tokens → SOL")
            quote_response = requests.get(quote_url, params=quote_params, timeout=10)
            
            if quote_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Jupiter quote failed: {quote_response.status_code}"
                }
            
            quote_data = quote_response.json()
            
            if "routePlan" not in quote_data:
                return {
                    "success": False,
                    "error": "No route found for selling this token"
                }
            
            # Create swap transaction (same process as buying)
            from solders.keypair import Keypair
            keypair = Keypair.from_base58_string(private_key)
            user_public_key = str(keypair.pubkey())
            
            swap_url = f"{self.jupiter_url}/swap"
            swap_payload = {
                "quoteResponse": quote_data,
                "userPublicKey": user_public_key,
                "wrapAndUnwrapSol": True,
                "dynamicComputeUnitLimit": True,
                "prioritizationFeeLamports": 1000
            }
            
            swap_response = requests.post(
                swap_url,
                json=swap_payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if swap_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Jupiter swap failed: {swap_response.status_code}"
                }
            
            swap_data = swap_response.json()
            
            # Sign and send (same as buy process)
            import base64
            from solders.transaction import VersionedTransaction
            from solders.commitment_config import CommitmentLevel
            from solders.rpc.requests import SendVersionedTransaction
            from solders.rpc.config import RpcSendTransactionConfig
            
            swap_transaction_b64 = swap_data["swapTransaction"]
            swap_transaction_bytes = base64.b64decode(swap_transaction_b64)
            
            transaction = VersionedTransaction.from_bytes(swap_transaction_bytes)
            signed_tx = VersionedTransaction(transaction.message, [keypair])
            
            commitment = CommitmentLevel.Confirmed
            config = RpcSendTransactionConfig(preflight_commitment=commitment)
            
            rpc_response = requests.post(
                url="https://api.mainnet-beta.solana.com/",
                headers={"Content-Type": "application/json"},
                data=SendVersionedTransaction(signed_tx, config).to_json(),
                timeout=30
            )
            
            if rpc_response.status_code == 200:
                result = rpc_response.json()
                if "result" in result:
                    signature = result["result"]
                    expected_sol = float(quote_data.get("outAmount", 0)) / 1_000_000_000
                    return {
                        "success": True,
                        "signature": signature,
                        "transactionId": signature,
                        "explorer_url": f"https://solscan.io/tx/{signature}",
                        "method": "Jupiter",
                        "expected_sol": expected_sol
                    }
                else:
                    return {
                        "success": False,
                        "error": f"RPC error: {result.get('error', 'Unknown')}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"RPC failed: {rpc_response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Jupiter sell error: {str(e)}"
            }

def test_enhanced_client():
    """Test the enhanced client with multiple trading methods"""
    
    print("🚀 Enhanced AxiomTradeAPI Multi-SDK Test")
    print("=" * 50)
    
    dotenv.load_dotenv()
    
    # Initialize enhanced client
    client = EnhancedAxiomTradeClient(
        auth_token=os.getenv('auth-access-token'),
        refresh_token=os.getenv('auth-refresh-token')
    )
    
    private_key = os.getenv('PRIVATE_KEY')
    
    # Test with a token that failed on PumpPortal
    test_token = "972LTtg2krARR7ysu6jHWLmdKqeVw7xT5Hs1Mt413dR9"
    amount_sol = 0.001  # Small test amount
    
    print(f"\n🎯 Testing with problematic token:")
    print(f"   Token: {test_token}")
    print(f"   Amount: {amount_sol} SOL")
    
    # Test smart buy
    result = client.smart_buy_token(
        private_key=private_key,
        token_mint=test_token,
        amount_sol=amount_sol,
        slippage_percent=15
    )
    
    print(f"\n📊 Result:")
    print(f"   Success: {result['success']}")
    print(f"   Method: {result.get('method', 'None')}")
    
    if result["success"]:
        print(f"   ✅ Transaction: {result['signature']}")
        print(f"   🔗 Explorer: {result['explorer_url']}")
    else:
        print(f"   ❌ Error: {result['error']}")

if __name__ == "__main__":
    test_enhanced_client()
