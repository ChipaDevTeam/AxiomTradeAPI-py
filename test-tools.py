from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.tools import login_with_email_otp

# 1. Setup client with your Axiom login
client = AxiomTradeClient(email="myemail@gmail.com", password="my_axiom_password")

# 2. Login using the tool (provides the email app password to read the OTP)
login_result = login_with_email_otp(
    client=client,
    email_password="my_gmail_app_password",  # Provide your email App Password here
    imap_server="imap.gmail.com"             # Default is Gmail
)

if login_result['success']:
    print("Login successful!")
else:
    print("Login failed.")