from typing import Optional, Dict
from ..client import AxiomTradeClient
from .email_otp import EmailOTPHandler

def login_with_email_otp(client: AxiomTradeClient, 
                        email_password: str, 
                        imap_server: str = "imap.gmail.com",
                        imap_port: int = 993,
                        **kwargs) -> Dict:
    """
    Helper function to login using automatic email OTP retrieval.
    
    Args:
        client: The AxiomTradeClient instance
        email_password: The password for the email account (different from Axiom password)
        imap_server: IMAP server address
        imap_port: IMAP port
        **kwargs: Additional arguments for EmailOTPHandler (sender_filter, subject_filter, etc.)
        
    Returns:
        Dict: Login result
    """
    if not client.auth_manager.username:
        raise ValueError("Client must have username (email) set")
        
    otp_handler = EmailOTPHandler(
        email_address=client.auth_manager.username,
        email_password=email_password,
        imap_server=imap_server,
        imap_port=imap_port,
        **kwargs
    )
    
    # We pass the get_otp method as the callback
    # The client.login() will call this when it needs the OTP
    return client.login(otp_callback=otp_handler.get_otp)
