"""
Direct Axiom Trade Implementation
Based on the exact curl commands from Axiom Trade website
"""

import requests
import json
import base64
from typing import Dict, Union
import dotenv
import os

class DirectAxiomTradeClient:
    """
    Direct implementation that mimics exactly what Axiom Trade website does
    Based on the provided curl commands
    """
    
    def __init__(self):
        self.rpc_url = "https://greer-651y13-fast-mainnet.helius-rpc.com/"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5",
            "content-type": "application/json",
            "origin": "https://axiom.trade",
            "priority": "u=1, i",
            "referer": "https://axiom.trade/",
            "sec-ch-ua": '"Opera GX";v="120", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0"
        }
    
    def send_axiom_transaction(self, transaction_base64: str) -> Dict[str, Union[str, bool]]:
        """
        Send a transaction using the exact format from Axiom Trade curl commands
        
        Args:
            transaction_base64 (str): Base64 encoded transaction
            
        Returns:
            Dict with transaction result
        """
        try:
            # Exact payload format from curl command
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendTransaction",
                "params": [
                    transaction_base64,
                    {
                        "encoding": "base64",
                        "skipPreflight": True,
                        "preflightCommitment": "confirmed",
                        "maxRetries": 0
                    }
                ]
            }
            
            print(f"🚀 Sending transaction to Axiom RPC...")
            print(f"   RPC: {self.rpc_url}")
            print(f"   Transaction length: {len(transaction_base64)} chars")
            
            response = requests.post(
                self.rpc_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            print(f"   Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
                
                if "result" in result:
                    signature = result["result"]
                    return {
                        "success": True,
                        "signature": signature,
                        "transactionId": signature,
                        "explorer_url": f"https://solscan.io/tx/{signature}",
                        "method": "Direct Axiom RPC"
                    }
                elif "error" in result:
                    return {
                        "success": False,
                        "error": f"RPC Error: {result['error']}",
                        "full_response": result
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Unexpected response format: {result}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def test_buy_transaction(self):
        """Test the buy transaction from your curl command"""
        
        print("🛒 Testing BUY transaction from curl command")
        print("=" * 50)
        
        # This is the exact transaction from your buy curl command
        buy_transaction = "AW84w5CYMZQPWj1uOwEbOgNkzvN2WQSWcDDADp3hYqU48WBWXlydgvUGJw0Y7YLW9nJ2n2lYqQ44TJC3cvzqsQeAAQAHD5j70yXqyyXj402bXRRkc/o0FjpJnCzj1pDXqim1PXH8UvufMkbRXdHDDTU3hwQGaiBPEKkTq8tddKNuBuauFrUBCioFbCRud0nimUjbDrwyv5CiMBsFXx0a8M9A6/y7VopxAEt3L9bKarUVDiqXHmUxUD/DXImuMwBridoNEnyq43OXHqv1QQph1fFn/mHjBxSVGdMQDvB48Awcr5HSgUv6CRGlSGNBLWMfTgeHAylsA18NEzOg2ciDjXO3EP5uLYyrCXAvnkahdjPSFaLxxewIsPWQbZD4pMqGvD9Tdm7zkz2X+RU5KtAcS8bFiDJLMUroO7zKCRuISS1QL5mBct0DBkZv5SEXMv/srbpyw5vnvIzlu8X3EmssQ5s6QAAAAIyXJY9OJInxuz0QKRSODYMLWhOZ2v8QhASOe9jb6fhZnsQXLSU/LdDkUQuKRsQnBuswTkb2vrasVA53IcVGTG8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANFEXWqfm76acyrGeJmxBC9s4TrBIXt3QfV6yNQs1d9wb5q0pPGVjcCpyUw/tywHmVhD7aSF46JPEMaTmfgZlA8MNf+pBVqOVo2o97wHVhUnTPHJLKQfQACcUWqkFMJ8cE8ZT6M3J/OGbp5xWV4xXJkmYowmTTeOMaSXPsSRTbbtBggBEQUC8EkCAAgACQOquWUAAAAAAAkGAAEACgsSAQEMEBMPCgIDAQALEgQUFQUGDQ4RALiCAQAAAAAAmZLtjQAAAAALAgAQDAIAAADoAwAAAAAAAAsCAAcMAgAAAEBCDwAAAAAAAV9ha7N8hvRWYU7kzy/NF6mrriKPQdpj9soxZDbVmkt8AiMxBXQEEBEP"
        
        return self.send_axiom_transaction(buy_transaction)
    
    def test_sell_transaction(self):
        """Test the sell transaction from your curl command"""
        
        print("💸 Testing SELL transaction from curl command")
        print("=" * 50)
        
        # This is the exact transaction from your sell curl command
        sell_transaction = "AWPn36n6ue8uSk8mjf3MBzdmt7ipXXU8tFsxMLQikufbLteNPmKgmydkLQ66WnX9bgGfqwBvpdFVnE1F+gMdAQqAAQAGDJj70yXqyyXj402bXRRkc/o0FjpJnCzj1pDXqim1PXH8AQoqBWwkbndJ4plI2w68Mr+QojAbBV8dGvDPQOv8u1aKcQBLdy/Wymq1FQ4qlx5lMVA/w1yJrjMAa4naDRJ8qlL7nzJG0V3Rww01N4cEBmogTxCpE6vLXXSjbgbmrha143OXHqv1QQph1fFn/mHjBxSVGdMQDvB48Awcr5HSgUsIszkmQ2qMWWVuVj16L1sokM7ACT6JTcJVbiKrivtIcAMGRm/lIRcy/+ytunLDm+e8jOW7xfcSayxDmzpAAAAAAVbg9pNmWs9E2xVovxdbqlGJy5f10v87ZV0rtv1tGLCexBctJT8t0ORRC4pGxCcG6zBORva+tqxUDnchxUZMbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb5q0pPGVjcCpyUw/tywHmVhD7aSF46JPEMaTmfgZlA8MNf+pBVqOVo2o97wHVhUnTPHJLKQfQACcUWqkFMJ8cGbBaCoYXInh2JGjtx8JlMvmjEeIQcvfhRZQGAtjhplwBQYBDgUC8EkCAAYACQOquWUAAAAAAAcODwwIAQIDAAkEEBEHCgsYM+aFpAF/g61xpOSpAAAAAOm4AAAAAAAACQIADQwCAAAAFAMAAAAAAAAJAgAFDAIAAABAQg8AAAAAAAFfYWuzfIb0VmFO5M8vzRepq64ij0HaY/bKMWQ21ZpLfAIrOQR0EAQR"
        
        return self.send_axiom_transaction(sell_transaction)
    
    def analyze_transaction(self, transaction_base64: str):
        """Analyze a transaction to understand its structure"""
        
        print("🔍 Analyzing transaction structure...")
        print("=" * 40)
        
        try:
            # Decode the base64 transaction
            transaction_bytes = base64.b64decode(transaction_base64)
            print(f"Transaction size: {len(transaction_bytes)} bytes")
            
            # Try to parse with solders if available
            try:
                from solders.transaction import VersionedTransaction
                
                transaction = VersionedTransaction.from_bytes(transaction_bytes)
                print(f"✅ Successfully parsed as VersionedTransaction")
                print(f"Message type: {type(transaction.message)}")
                
                # Get account keys
                if hasattr(transaction.message, 'account_keys'):
                    account_keys = transaction.message.account_keys
                    print(f"Account keys ({len(account_keys)}):")
                    for i, key in enumerate(account_keys[:5]):  # Show first 5
                        print(f"  {i}: {str(key)}")
                    if len(account_keys) > 5:
                        print(f"  ... and {len(account_keys) - 5} more")
                
                return transaction
                
            except Exception as e:
                print(f"❌ Could not parse as VersionedTransaction: {e}")
                
        except Exception as e:
            print(f"❌ Could not decode base64: {e}")
            
        return None

def main():
    """Test the direct Axiom implementation"""
    
    print("🎯 Direct Axiom Trade Implementation Test")
    print("=" * 60)
    print("Testing with the exact curl transactions from Axiom website")
    
    client = DirectAxiomTradeClient()
    
    # Analyze the transactions first
    print("\n1️⃣ Analyzing BUY transaction...")
    buy_tx = "AW84w5CYMZQPWj1uOwEbOgNkzvN2WQSWcDDADp3hYqU48WBWXlydgvUGJw0Y7YLW9nJ2n2lYqQ44TJC3cvzqsQeAAQAHD5j70yXqyyXj402bXRRkc/o0FjpJnCzj1pDXqim1PXH8UvufMkbRXdHDDTU3hwQGaiBPEKkTq8tddKNuBuauFrUBCioFbCRud0nimUjbDrwyv5CiMBsFXx0a8M9A6/y7VopxAEt3L9bKarUVDiqXHmUxUD/DXImuMwBridoNEnyq43OXHqv1QQph1fFn/mHjBxSVGdMQDvB48Awcr5HSgUv6CRGlSGNBLWMfTgeHAylsA18NEzOg2ciDjXO3EP5uLYyrCXAvnkahdjPSFaLxxewIsPWQbZD4pMqGvD9Tdm7zkz2X+RU5KtAcS8bFiDJLMUroO7zKCRuISS1QL5mBct0DBkZv5SEXMv/srbpyw5vnvIzlu8X3EmssQ5s6QAAAAIyXJY9OJInxuz0QKRSODYMLWhOZ2v8QhASOe9jb6fhZnsQXLSU/LdDkUQuKRsQnBuswTkb2vrasVA53IcVGTG8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANFEXWqfm76acyrGeJmxBC9s4TrBIXt3QfV6yNQs1d9wb5q0pPGVjcCpyUw/tywHmVhD7aSF46JPEMaTmfgZlA8MNf+pBVqOVo2o97wHVhUnTPHJLKQfQACcUWqkFMJ8cE8ZT6M3J/OGbp5xWV4xXJkmYowmTTeOMaSXPsSRTbbtBggBEQUC8EkCAAgACQOquWUAAAAAAAkGAAEACgsSAQEMEBMPCgIDAQALEgQUFQUGDQ4RALiCAQAAAAAAmZLtjQAAAAALAgAQDAIAAADoAwAAAAAAAAsCAAcMAgAAAEBCDwAAAAAAAV9ha7N8hvRWYU7kzy/NF6mrriKPQdpj9soxZDbVmkt8AiMxBXQEEBEP"
    
    client.analyze_transaction(buy_tx)
    
    print("\n2️⃣ Analyzing SELL transaction...")
    sell_tx = "AWPn36n6ue8uSk8mjf3MBzdmt7ipXXU8tFsxMLQikufbLteNPmKgmydkLQ66WnX9bgGfqwBvpdFVnE1F+gMdAQqAAQAGDJj70yXqyyXj402bXRRkc/o0FjpJnCzj1pDXqim1PXH8AQoqBWwkbndJ4plI2w68Mr+QojAbBV8dGvDPQOv8u1aKcQBLdy/Wymq1FQ4qlx5lMVA/w1yJrjMAa4naDRJ8qlL7nzJG0V3Rww01N4cEBmogTxCpE6vLXXSjbgbmrha143OXHqv1QQph1fFn/mHjBxSVGdMQDvB48Awcr5HSgUsIszkmQ2qMWWVuVj16L1sokM7ACT6JTcJVbiKrivtIcAMGRm/lIRcy/+ytunLDm+e8jOW7xfcSayxDmzpAAAAAAVbg9pNmWs9E2xVovxdbqlGJy5f10v87ZV0rtv1tGLCexBctJT8t0ORRC4pGxCcG6zBORva+tqxUDnchxUZMbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb5q0pPGVjcCpyUw/tywHmVhD7aSF46JPEMaTmfgZlA8MNf+pBVqOVo2o97wHVhUnTPHJLKQfQACcUWqkFMJ8cGbBaCoYXInh2JGjtx8JlMvmjEeIQcvfhRZQGAtjhplwBQYBDgUC8EkCAAgACQOquWUAAAAAAAcODwwIAQIDAAkEEBEHCgsYM+aFpAF/g61xpOSpAAAAAOm4AAAAAAAACQIADQwCAAAAFAMAAAAAAAAJAgAFDAIAAABAQg8AAAAAAAFfYWuzfIb0VmFO5M8vzRepq64ij0HaY/bKMWQ21ZpLfAIrOQR0EAQR"
    
    client.analyze_transaction(sell_tx)
    
    print(f"\n⚠️  IMPORTANT NOTE:")
    print("These transactions are pre-signed and contain specific wallet addresses.")
    print("They cannot be executed directly as they're tied to the original wallet.")
    print("This analysis helps us understand the exact format Axiom uses.")
    
    # Uncomment below to test sending (will likely fail as transactions are pre-signed)
    # print("\n3️⃣ Testing BUY transaction...")
    # buy_result = client.test_buy_transaction()
    # print(f"Buy result: {buy_result}")
    
    # print("\n4️⃣ Testing SELL transaction...")  
    # sell_result = client.test_sell_transaction()
    # print(f"Sell result: {sell_result}")

if __name__ == "__main__":
    main()
