"""
Token Analysis Tool - Check if token is tradeable
"""

import requests
import json

def analyze_token(token_mint):
    """Analyze token to see if it's tradeable"""
    
    print(f"🔍 Analyzing Token: {token_mint}")
    print("=" * 60)
    
    # 1. Check if token exists on Solana
    print("1️⃣ Checking token existence...")
    rpc_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [token_mint, {"encoding": "base64"}]
    }
    
    try:
        response = requests.post(
            "https://api.mainnet-beta.solana.com",
            json=rpc_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result", {}).get("value"):
                print("   ✅ Token exists on Solana")
                owner = data["result"]["value"]["owner"]
                print(f"   Token Program: {owner}")
            else:
                print("   ❌ Token not found on Solana")
                return False
        else:
            print(f"   ❌ RPC error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 2. Check Jupiter for possible routes
    print("\n2️⃣ Checking Jupiter routing...")
    try:
        quote_url = "https://quote-api.jup.ag/v6/quote"
        quote_params = {
            "inputMint": "So11111111111111111111111111111111111111112",  # SOL
            "outputMint": token_mint,
            "amount": 1000000,  # 0.001 SOL
            "slippageBps": 1000
        }
        
        quote_response = requests.get(quote_url, params=quote_params, timeout=10)
        print(f"   Jupiter response: {quote_response.status_code}")
        
        if quote_response.status_code == 200:
            quote_data = quote_response.json()
            if "routePlan" in quote_data:
                print("   ✅ Jupiter found trading routes!")
                routes = quote_data["routePlan"]
                print(f"   Routes found: {len(routes)}")
                for i, route in enumerate(routes[:3]):  # Show first 3 routes
                    dex = route.get("swapInfo", {}).get("label", "Unknown")
                    print(f"     Route {i+1}: {dex}")
                return True
            else:
                print("   ❌ No Jupiter routes found")
        else:
            error_text = quote_response.text
            print(f"   ❌ Jupiter error: {error_text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ Jupiter check failed: {e}")
    
    # 3. Check popular DEX APIs
    print("\n3️⃣ Checking other DEX support...")
    
    # Check DexScreener (popular token info site)
    try:
        dexscreener_url = f"https://api.dexscreener.com/latest/dex/tokens/{token_mint}"
        dex_response = requests.get(dexscreener_url, timeout=10)
        
        if dex_response.status_code == 200:
            dex_data = dex_response.json()
            pairs = dex_data.get("pairs", [])
            if pairs:
                print(f"   ✅ DexScreener found {len(pairs)} trading pairs")
                for pair in pairs[:3]:
                    dex_name = pair.get("dexId", "Unknown")
                    base_token = pair.get("baseToken", {}).get("symbol", "?")
                    quote_token = pair.get("quoteToken", {}).get("symbol", "?")
                    print(f"     {dex_name}: {base_token}/{quote_token}")
                return True
            else:
                print("   ❌ No pairs found on DexScreener")
        else:
            print(f"   ❌ DexScreener error: {dex_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ DexScreener check failed: {e}")
    
    # 4. Check CoinGecko
    print("\n4️⃣ Checking CoinGecko...")
    try:
        # CoinGecko doesn't have direct mint lookup, but we can try
        print("   ℹ️  CoinGecko requires symbol lookup (skipping for now)")
    except Exception as e:
        print(f"   ❌ CoinGecko check failed: {e}")
    
    print(f"\n📊 Analysis Results:")
    print("   Token exists but has no active trading pairs")
    print("   Possible reasons:")
    print("   - New token with no liquidity yet")
    print("   - Dead/abandoned project")
    print("   - Very low volume token")
    print("   - Only trades on specific/private DEXs")
    
    return False

def suggest_working_tokens():
    """Suggest some tokens that are known to work"""
    
    print(f"\n💡 Suggested Working Tokens:")
    print("=" * 40)
    
    working_tokens = [
        {
            "name": "Bonk",
            "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
            "type": "Meme token, high liquidity"
        },
        {
            "name": "Raydium",
            "mint": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
            "type": "DEX token, very liquid"
        },
        {
            "name": "Jupiter",
            "mint": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
            "type": "Aggregator token"
        },
        {
            "name": "Solana (Wrapped)",
            "mint": "So11111111111111111111111111111111111111112",
            "type": "Native SOL"
        }
    ]
    
    for token in working_tokens:
        print(f"✅ {token['name']}")
        print(f"   Mint: {token['mint']}")
        print(f"   Type: {token['type']}")
        print()

if __name__ == "__main__":
    # Analyze the problematic token
    problem_token = "972LTtg2krARR7ysu6jHWLmdKqeVw7xT5Hs1Mt413dR9"
    
    success = analyze_token(problem_token)
    
    if not success:
        suggest_working_tokens()
        
        print(f"\n🔧 Recommendation:")
        print("Test with one of the suggested tokens above to verify")
        print("that your enhanced trading client works correctly.")
