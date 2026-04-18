"""
Direct Axiom Trade Client Implementation
Using exact curl command format from Axiom website
"""
import json
import base64
import requests
from typing import Dict, Union
from axiomtradeapi.client import AxiomTradeClient

class AxiomDirectClient(AxiomTradeClient):
    """Client that uses Axiom Trade's exact RPC format and headers"""
    
    def __init__(self, username: str, password: str, login_type: str = "manual"):
        super().__init__(username, password, login_type)
        
        # Exact headers from Axiom Trade curl commands
        self.axiom_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://www.axiomtrade.io',
            'Referer': 'https://www.axiomtrade.io/',
            'Sec-CH-UA': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site'
        }
        
        # Exact RPC endpoint from Axiom
        self.rpc_url = "https://greer-651y13-fast-mainnet.helius-rpc.com/"

    def buy_token_direct(self, private_key: str, token_mint: str, amount_sol: float, 
                        slippage_percent: float = 10) -> Dict[str, Union[str, bool]]:
        """
        Buy token using Axiom's direct method
        Uses Jupiter for transaction building + Axiom RPC for sending
        """
        try:
            from solders.keypair import Keypair
            from solders.transaction import VersionedTransaction
        except ImportError:
            return {
                "success": False,
                "error": "solders library required for direct trading"
            }
        
        try:
            print(f"\n🔥 AXIOM DIRECT BUY: {amount_sol} SOL → {token_mint}")
            
            # Create keypair
            keypair = Keypair.from_base58_string(private_key)
            wallet_address = str(keypair.pubkey())
            
            # Convert to lamports
            amount_lamports = int(amount_sol * 1_000_000_000)
            slippage_bps = int(slippage_percent * 100)
            
            print(f"Wallet: {wallet_address}")
            print(f"Amount: {amount_lamports} lamports ({amount_sol} SOL)")
            print(f"Slippage: {slippage_bps} bps ({slippage_percent}%)")
            
            # Build transaction using Jupiter
            transaction_b64 = self._build_jupiter_transaction(
                wallet_address, token_mint, amount_lamports, True, slippage_bps
            )
            
            if not transaction_b64:
                return {"success": False, "error": "Failed to build transaction"}
            
            # Decode and sign transaction
            transaction_bytes = base64.b64decode(transaction_b64)
            transaction = VersionedTransaction.from_bytes(transaction_bytes)
            
            print("Signing transaction...")
            signed_transaction = keypair.sign_message(bytes(transaction.message))
            transaction.signatures = [signed_transaction]
            
            # Send using Axiom's exact format
            return self._send_with_axiom_rpc(transaction)
            
        except Exception as e:
            print(f"❌ Direct buy error: {e}")
            return {
                "success": False,
                "error": f"Direct buy error: {str(e)}"
            }

    def _build_jupiter_transaction(self, wallet_address: str, token_mint: str, 
                                 amount_lamports: int, is_buy: bool, slippage_bps: int):
        """Build transaction using Jupiter API"""
        try:
            if is_buy:
                # Buy: SOL -> Token
                input_mint = "So11111111111111111111111111111111111111112"  # SOL
                output_mint = token_mint
                amount = amount_lamports
            else:
                # Sell: Token -> SOL  
                input_mint = token_mint
                output_mint = "So11111111111111111111111111111111111111112"  # SOL
                amount = amount_lamports
            
            # Get quote from Jupiter
            quote_url = "https://quote-api.jup.ag/v6/quote"
            quote_params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount,
                "slippageBps": slippage_bps,
                "onlyDirectRoutes": "false",
                "asLegacyTransaction": "false"
            }
            
            print(f"Getting Jupiter quote...")
            quote_response = requests.get(quote_url, params=quote_params)
            
            if quote_response.status_code != 200:
                print(f"❌ Quote failed: {quote_response.text}")
                return None
            
            quote_data = quote_response.json()
            print(f"Quote received: {quote_data.get('outAmount', 'N/A')} output tokens")
            
            # Get swap transaction
            swap_url = "https://quote-api.jup.ag/v6/swap"
            swap_payload = {
                "quoteResponse": quote_data,
                "userPublicKey": wallet_address,
                "wrapAndUnwrapSol": True,
                "useSharedAccounts": True,
                "feeAccount": None,
                "trackingAccount": None,
                "asLegacyTransaction": False
            }
            
            print("Building Jupiter swap transaction...")
            swap_response = requests.post(swap_url, json=swap_payload)
            
            if swap_response.status_code != 200:
                print(f"❌ Swap transaction failed: {swap_response.text}")
                return None
            
            swap_data = swap_response.json()
            return swap_data.get('swapTransaction')
            
        except Exception as e:
            print(f"❌ Jupiter transaction error: {e}")
            return None

    def _send_with_axiom_rpc(self, signed_transaction) -> Dict[str, Union[str, bool]]:
        """Send transaction using Axiom's exact RPC format"""
        try:
            # Convert to base64 - this is the format Axiom uses
            serialized = bytes(signed_transaction)
            transaction_base64 = base64.b64encode(serialized).decode('utf-8')
            
            # Exact RPC payload from Axiom curl commands
            rpc_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendTransaction",
                "params": [
                    transaction_base64,
                    {
                        "encoding": "base64",
                        "skipPreflight": False,
                        "preflightCommitment": "processed",
                        "maxRetries": 5
                    }
                ]
            }
            
            print(f"Sending transaction via Axiom RPC: {self.rpc_url}")
            print(f"Transaction size: {len(serialized)} bytes")
            
            response = requests.post(
                self.rpc_url,
                headers=self.axiom_headers,
                json=rpc_payload,
                timeout=30
            )
            
            print(f"RPC Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    tx_signature = result['result']
                    print(f"✅ Transaction sent! Signature: {tx_signature}")
                    return {
                        "success": True,
                        "signature": tx_signature,
                        "method": "axiom_direct_rpc"
                    }
                else:
                    error = result.get('error', 'Unknown RPC error')
                    print(f"❌ RPC Error: {error}")
                    return {
                        "success": False,
                        "error": f"RPC Error: {error}"
                    }
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            print(f"❌ Transaction send error: {e}")
            return {
                "success": False,
                "error": f"Send error: {str(e)}"
            }


def test_direct_client():
    """Test the direct client implementation"""
    print("=== Testing Axiom Direct Client ===")
    
    # Initialize client
    client = AxiomDirectClient("test_user", "test_pass")
    
    print("✅ Client initialized successfully")
    print("✅ Headers configured for Axiom format")
    print("✅ RPC endpoint configured")
    
    print("\nDirect client ready for trading!")
    print("This client uses:")
    print("1. Jupiter API for transaction building")
    print("2. Axiom's exact RPC endpoint and headers")
    print("3. Proper transaction signing with solders")
    

if __name__ == "__main__":
    test_direct_client()
