"""
Fully automated browser login test.

The browser auto-fills credentials and, if AXIOM_IMAP_PASSWORD is set in .env,
reads the OTP from your inbox automatically. Otherwise it falls back to prompting
you in the terminal.

For Gmail with 2FA you need an App Password:
  https://myaccount.google.com/apppasswords
Add it to .env as:
  AXIOM_IMAP_PASSWORD=your_app_password

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
    imap_password = os.getenv("AXIOM_IMAP_PASSWORD")  # optional — enables auto-OTP

    if not email or not password:
        print("❌ Set AXIOM_EMAIL and AXIOM_PASSWORD in your .env file")
        return

    if imap_password:
        print(f"📬 IMAP auto-OTP enabled (will read from {email} inbox)")
    else:
        print("⌨️  No AXIOM_IMAP_PASSWORD set — will prompt for OTP manually")
        print("   To enable auto-OTP, add AXIOM_IMAP_PASSWORD to your .env")

    print(f"\nLogging in as: {email}\n")

    am = AuthManager(
        username=email,
        password=password,
        imap_password=imap_password,
        use_saved_tokens=True,
    )

    success = await am._login_with_browser()

    if success and am.tokens:
        import datetime
        exp = datetime.datetime.fromtimestamp(am.tokens.expires_at)
        print("\n✅ Login successful!")
        print(f"   Access token  : {am.tokens.access_token[:50]}...")
        print(f"   Refresh token : {am.tokens.refresh_token[:50]}...")
        print(f"   Expires at    : {exp}")
        if am.cf_clearance:
            print(f"   cf_clearance  : {am.cf_clearance[:40]}...")
        print("\n💾 Tokens saved — future runs will use saved tokens without logging in again.")
    else:
        print("\n❌ Login failed — check the logs above for details")


if __name__ == "__main__":
    asyncio.run(main())
