import requests
import json
from typing import Dict, Optional

class AxiomAuth:
    """
    Handles authentication for Axiom Trade API
    """
    
    def __init__(self):
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }
    
    def login_step1(self, email: str, b64_password: str) -> str:
        """
        First step of login - send email and password to get OTP JWT token
        Returns the OTP JWT token needed for step 2
        """
        url = 'https://api6.axiom.trade/login-password-v2'
        headers = {
            **self.base_headers,
            'Content-Type': 'application/json'
        }
        
        data = {
            "email": email,
            "b64Password": b64_password
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result.get('otpJwtToken')
    
    def login_step2(self, otp_jwt_token: str, otp_code: str, email: str, b64_password: str) -> Dict:
        """
        Second step of login - send OTP code to complete authentication
        Returns authentication tokens and credentials
        """
        url = 'https://api10.axiom.trade/login-otp'
        headers = {
            **self.base_headers,
            'Content-Type': 'application/json',
            'Cookie': f'auth-otp-login-token={otp_jwt_token}'
        }
        
        data = {
            "code": otp_code,
            "email": email,
            "b64Password": b64_password
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Get the response data
        result = response.json()
        
        # Extract tokens from cookies if available
        access_token = response.cookies.get('auth-access-token')
        refresh_token = response.cookies.get('auth-refresh-token')
        
        # Add tokens to the result if they exist
        if access_token:
            result['access_token'] = access_token
        if refresh_token:
            result['refresh_token'] = refresh_token
        
        return result
    
    def complete_login(self, email: str, b64_password: str, otp_code: str) -> Dict:
        """
        Complete the full login process
        Returns authentication tokens and credentials
        """
        print("Step 1: Sending email and password...")
        otp_jwt_token = self.login_step1(email, b64_password)
        print("OTP JWT token received")
        
        print("Step 2: Sending OTP code...")
        credentials = self.login_step2(otp_jwt_token, otp_code, email, b64_password)
        print("Login completed successfully")
        
        return credentials
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Refresh the access token using a refresh token
        Returns the new access token
        """
        url = 'https://api9.axiom.trade/refresh-access-token'
        headers = {
            **self.base_headers,
            'Cookie': f'auth-refresh-token={refresh_token}',
            'Content-Length': '0'
        }
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        # Try to get token from cookies first, then from JSON response
        new_access_token = response.cookies.get('auth-access-token')
        
        if not new_access_token:
            # If not in cookies, try JSON response
            try:
                json_response = response.json()
                new_access_token = json_response.get('auth-access-token') or json_response.get('access_token')
            except:
                pass
        
        if not new_access_token:
            raise ValueError("No access token found in refresh response")
        
        return new_access_token
