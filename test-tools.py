from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.tools import login_with_email_otp
from dotenv import load_dotenv
import os
import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Get credentials
# Supports both 'email' (from existing .env) and 'EMAIL_ADDRESS' 
email = os.getenv('email') or os.getenv('EMAIL_ADDRESS')
# Ideally different passwords, but falling back to check common vars
axiom_password = os.getenv('EMAIL_APP_PASSWORD')
email_app_password = os.getenv('EMAIL_PASSWORD')

if not email:
    print("❌ Error: 'email' or 'EMAIL_ADDRESS' not found in environment variables.")
    print("Please check your .env file.")
    exit(1)

if not axiom_password:
    print("❌ Error: 'password' or 'AXIOM_PASSWORD' not found in environment variables.")
    print("Please check your .env file.")
    exit(1)

if not email_app_password:
    print("❌ Error: 'EMAIL_APP_PASSWORD' not found in environment variables.")
    print("This is required to access the OTP from your email.")
    print("Please add it to your .env file.")
    exit(1)

print(f"🔄 Attempting login for: {email}")

# Define storage directory in the root of the workspace
storage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chipadev_data")
print(f"📂 Using token storage: {storage_dir}")

# 1. Setup client with your Axiom login
client = AxiomTradeClient(username=email, password=axiom_password, storage_dir=storage_dir)

# 2. Login using the tool
# Note: axiom_password is for the trade site, email_app_password is for IMAP access
try:
    login_result = login_with_email_otp(
        client=client,
        email_password=email_app_password,
        imap_server="imap.gmail.com"  # Default is Gmail
    )

    if login_result['success']:
        print("✅ Login successful!")
        if 'expires_at' in login_result:
            print(f"Token expires at: {login_result['expires_at']}")
    else:
        print("❌ Login failed.")
        print(f"Message: {login_result.get('message')}")

except Exception as e:
    print(f"❌ An error occurred: {e}")