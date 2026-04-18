# AxiomTradeAPI Tools

This directory contains utility tools for the Axiom SDK.

## Automatic Login with Email OTP

This tool automates the login process by accessing your email to retrieve the OTP code.

### Prerequisites

- You need an email account where Axiom Trade sends OTPs.
- For Gmail, you probably need an **App Password** (Manage your Google Account -> Security -> 2-Step Verification -> App passwords).

### Usage

```python
from axiomtradeapi.client import AxiomTradeClient
from axiomtradeapi.tools import login_with_email_otp

# Initialize client with your Axiom credentials
client = AxiomTradeClient(username="your_email@example.com", password="axiom_password")

# Login automatically (requires your email APP password for IMAP access)
result = login_with_email_otp(
    client, 
    email_password="your_email_app_password",
    imap_server="imap.gmail.com"  # Default
)

if result['success']:
    print("Logged in successfully!")
```

### Configuration

You can customize the email search filters:

```python
result = login_with_email_otp(
    client, 
    email_password="xxxx",
    sender_filter="no-reply@axiom.trade",
    subject_filter="Login Verification"
)
```
