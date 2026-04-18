import requests
import json
import time
from typing import Any, Dict, Optional


TRENDING_V2_FIELDS = [
    "pairAddress",
    "tokenAddress",
    "tokenName",
    "tokenTicker",
    "imageUrl",
    "metadataUrl",
    "chainId",
    "exchangeName",
    "exchangeData",
    "createdAt",
    "website",
    "twitter",
    "telegram",
    "discord",
    "link1",
    "link2",
    "isMigrated",
    "creatorAddress",
    "supply",
    "liquiditySol",
    "completionPercent",
    "migrationInfo",
    "txCount",
    "volume",
    "marketCapUsd",
    "buyCount",
    "sellCount",
    "makerCount",
    "liquidityUsd",
    "priceUsd",
    "priceChange5m",
    "priceChange1h",
    "priceChange6h",
    "priceChange24h",
    "holderRatio",
    "top10HoldersPercent",
    "sniperCount",
    "insiderPercentage",
    "bundlePercentage",
    "developerHoldingPercent",
    "buyers",
    "sellers",
    "sparkline",
    "holderCount",
    "signature",
    "slot",
    "quoteLiquidity",
    "baseLiquidity",
    "pairCreatedAt",
    "pairAddressRaw",
    "reserveAddressA",
    "updatedAt"
]


def _parse_trending_value(value: Any):
    if isinstance(value, str):
        stripped = value.strip()
        if stripped and stripped[0] in "[{":
            try:
                return json.loads(stripped)
            except (json.JSONDecodeError, TypeError, ValueError):
                return value
    return value


def _normalize_trending_token(row: Any) -> Dict:
    if isinstance(row, dict):
        normalized = dict(row)
        normalized.setdefault("raw", row)
        return normalized

    if not isinstance(row, list):
        return {"raw": row}

    token = {f"field_{idx}": _parse_trending_value(value) for idx, value in enumerate(row)}
    for idx, field_name in enumerate(TRENDING_V2_FIELDS):
        if idx < len(row):
            token[field_name] = _parse_trending_value(row[idx])

    token["raw"] = row
    return token


def _normalize_trending_response(payload: Any, time_period: str) -> Dict:
    if isinstance(payload, dict):
        if isinstance(payload.get("tokens"), list):
            payload["tokens"] = [_normalize_trending_token(item) for item in payload["tokens"]]
        elif isinstance(payload.get("data"), list):
            payload["tokens"] = [_normalize_trending_token(item) for item in payload["data"]]

        payload.setdefault("data", payload.get("tokens", []))
        payload.setdefault("timePeriod", time_period)
        payload.setdefault("endpoint", "new-trending-v2")
        return payload

    if isinstance(payload, list):
        tokens = [_normalize_trending_token(item) for item in payload]
        return {
            "tokens": tokens,
            "data": tokens,
            "timePeriod": time_period,
            "endpoint": "new-trending-v2",
            "count": len(tokens),
            "raw": payload,
        }

    return {
        "tokens": [],
        "data": payload,
        "timePeriod": time_period,
        "endpoint": "new-trending-v2",
        "count": 0,
    }

def login_step1(email: str, b64_password: str) -> str:
    """
    First step of login - send email and password to get OTP JWT token
    Returns the OTP JWT token needed for step 2
    """
    url = 'https://api6.axiom.trade/login-password-v2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Origin': 'https://axiom.trade',
        'Connection': 'keep-alive',
        'Referer': 'https://axiom.trade/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }
    
    data = {
        "email": email,
        "b64Password": b64_password
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    result = response.json()
    return result.get('otpJwtToken')

def login_step2(otp_jwt_token: str, otp_code: str, email: str, b64_password: str) -> Dict:
    """
    Second step of login - send OTP code to complete authentication
    Returns client credentials (clientSecret, orgId, userId)
    """
    url = 'https://api10.axiom.trade/login-otp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Origin': 'https://axiom.trade',
        'Connection': 'keep-alive',
        'Referer': 'https://axiom.trade/',
        'Cookie': f'auth-otp-login-token={otp_jwt_token}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }
    
    data = {
        "code": otp_code,
        "email": email,
        "b64Password": b64_password
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()

def complete_login(email: str, b64_password: str, otp_code: str) -> Dict:
    """
    Complete the full login process
    Returns client credentials (clientSecret, orgId, userId)
    """
    print("Step 1: Sending email and password...")
    otp_jwt_token = login_step1(email, b64_password)
    print("OTP JWT token received")
    
    print("Step 2: Sending OTP code...")
    credentials = login_step2(otp_jwt_token, otp_code, email, b64_password)
    print("Login completed successfully")
    
    return credentials

def refresh_access_token(refresh_token):
    url = 'https://api9.axiom.trade/refresh-access-token'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://axiom.trade',
        'Connection': 'keep-alive',
        'Referer': 'https://axiom.trade/',
        'Cookie': f'auth-refresh-token={refresh_token}',
        'Content-Length': '0',
        'TE': 'trailers'
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json().get('auth-access-token')

def get_trending_tokens(access_token, time_period='1h'):
    url = 'https://api3.axiom.trade/new-trending-v2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://axiom.trade',
        'Connection': 'keep-alive',
        'Referer': 'https://axiom.trade/',
        'priority': 'u=1, i',
        'Cookie': f'auth-access-token={access_token}',
    }

    response = requests.get(
        url,
        headers=headers,
        params={
            'timePeriod': time_period,
            'v': int(time.time() * 1000)
        },
        timeout=30
    )
    response.raise_for_status()
    return _normalize_trending_response(response.json(), time_period)

if __name__ == '__main__':
    print("Axiom Trade API - Login and Trending Tokens")
    print("=" * 50)
    
    # Option to either login fresh or use existing refresh token
    use_existing_token = input("Do you have a refresh token? (y/n): ").lower().strip() == 'y'
    
    if use_existing_token:
        refresh_token = input('Enter your refresh token: ')
        try:
            access_token = refresh_access_token(refresh_token)
            print('Access token refreshed successfully.')
        except requests.exceptions.RequestException as e:
            print('Error refreshing token:', e)
            exit(1)
    else:
        # Fresh login process
        email = input('Enter your email: ')
        b64_password = input('Enter your base64 encoded password: ')
        
        try:
            # Step 1: Get OTP token
            otp_jwt_token = login_step1(email, b64_password)
            print('OTP request sent. Check your email/phone for the code.')
            
            # Step 2: Complete login with OTP
            otp_code = input('Enter the OTP code: ')
            credentials = login_step2(otp_jwt_token, otp_code, email, b64_password)
            
            print('Login successful!')
            print(f"Client Secret: {credentials.get('clientSecret')}")
            print(f"Org ID: {credentials.get('orgId')}")
            print(f"User ID: {credentials.get('userId')}")
            
            # For now, we'll need to implement getting access token from credentials
            # This might require additional API calls that aren't shown in the examples
            print("\nNote: You'll need to use these credentials to get access tokens for API calls.")
            exit(0)
            
        except requests.exceptions.RequestException as e:
            print('Login error:', e)
            exit(1)
    
    # Get trending tokens
    try:
        time_period = input('Enter time period (1h, 24h, 7d) [default: 1h]: ').strip() or '1h'
        trending_tokens = get_trending_tokens(access_token, time_period)
        
        print(f'\nTrending tokens for {time_period}:')
        print('=' * 30)
        print(json.dumps(trending_tokens, indent=2))
        
    except requests.exceptions.RequestException as e:
        print('Error fetching trending tokens:', e)
