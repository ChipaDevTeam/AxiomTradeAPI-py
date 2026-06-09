"""
Test browser-based login via nodriver.

Run this directly in a terminal (NOT as a background process) since it:
  1. Opens a real Chrome window
  2. Waits for you to enter the OTP from your email

Usage:
    python tests/test_browser_login.py
"""
import asyncio
import logging
import os
import dotenv

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

from axiomtradeapi.auth.auth_manager import AuthManager


async def main():
    email = os.getenv("AXIOM_EMAIL")
    password = os.getenv("AXIOM_PASSWORD")

    if not email or not password:
        print("❌ Set AXIOM_EMAIL and AXIOM_PASSWORD in your .env file")
        return

    print(f"Logging in as: {email}")

    am = AuthManager(
        username=email,
        password=password,
        use_saved_tokens=True,  # save tokens on success
    )

    success = await am._login_with_browser()

    if success and am.tokens:
        print("\n✅ Login successful!")
        print(f"   Access token  : {am.tokens.access_token[:50]}...")
        print(f"   Refresh token : {am.tokens.refresh_token[:50]}...")
        import time, datetime
        exp = datetime.datetime.fromtimestamp(am.tokens.expires_at)
        print(f"   Expires at    : {exp}")
        if am.cf_clearance:
            print(f"   cf_clearance  : {am.cf_clearance[:40]}...")
    else:
        print("\n❌ Login failed — check the logs above for details")


if __name__ == "__main__":
    asyncio.run(main())
