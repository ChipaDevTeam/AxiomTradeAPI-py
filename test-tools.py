from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.tools import login_with_email_otp

import dotenv
import os

emails = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_APP_PASSWORD')

# 1. Setup client with your Axiom login
client = AxiomTradeClient(username=emails, password=email_password)

# 2. Login using the tool (provides the email app password to read the OTP)
login_result = login_with_email_otp(
    client=client,
    email_password=email_password,  # Provide your email App Password here
    imap_server="imap.gmail.com"             # Default is Gmail
)

if login_result['success']:
    print("Login successful!")
else:
    print("Login failed.")