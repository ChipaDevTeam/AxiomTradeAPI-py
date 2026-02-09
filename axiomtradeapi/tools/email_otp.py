import imaplib
import email
from email.header import decode_header
import re
import time
import logging
from typing import Optional

class EmailOTPHandler:
    """
    Handles retrieval of OTP codes from email for automated login.
    """
    
    def __init__(self, email_address: str, email_password: str, 
                 imap_server: str = "imap.gmail.com", imap_port: int = 993,
                 sender_filter: str = "axiom.trade", 
                 subject_filter: str = "security code",
                 check_interval: float = 2.0,
                 timeout: float = 60.0):
        """
        Initialize EmailOTPHandler
        
        Args:
            email_address: The email address to check
            email_password: The password or app-specific password for the email
            imap_server: IMAP server address (default: imap.gmail.com)
            imap_port: IMAP port (default: 993)
            sender_filter: Filter for email sender (partial match)
            subject_filter: Filter for email subject (partial match)
            check_interval: Time to wait between checks in seconds
            timeout: Maximum time to wait for OTP in seconds
        """
        self.email_address = email_address
        self.email_password = email_password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.sender_filter = sender_filter
        self.subject_filter = subject_filter
        self.check_interval = check_interval
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def get_otp(self) -> Optional[str]:
        """
        Connects to email and waits for the OTP code.
        
        Returns:
            str: The OTP code if found, None otherwise.
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Connecting to IMAP server {self.imap_server}...")
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select("inbox")
            
            self.logger.info(f"Waiting for OTP from '{self.sender_filter}'...")
            
            # Record current number of messages to ignore old ones efficiently
            # or better, search for UNSEEN mostly, or within last few minutes.
            # For simplicity, we'll keep checking UNSEEN messages.
            
            while time.time() - start_time < self.timeout:
                status, messages = mail.search(None, '(UNSEEN)')
                
                if status == "OK":
                    email_ids = messages[0].split()
                    
                    # Process from newest
                    for email_id in reversed(email_ids):
                        status, msg_data = mail.fetch(email_id, "(RFC822)")
                        if status != "OK":
                            continue
                            
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                
                                subject = self._decode_header_str(msg["Subject"])
                                sender = self._decode_header_str(msg["From"])
                                
                                # Check matches
                                if (not self.sender_filter or self.sender_filter.lower() in sender.lower()) and \
                                   (not self.subject_filter or self.subject_filter.lower() in subject.lower()):
                                   
                                    self.logger.info(f"Found matching email: {subject} from {sender}")
                                    
                                    # Extract body
                                    body = self._get_email_body(msg)
                                    otp = self._extract_otp(body)
                                    
                                    if otp:
                                        self.logger.info(f"Extracted OTP: {otp}")
                                        mail.close()
                                        mail.logout()
                                        return otp

                
                time.sleep(self.check_interval)
                # Re-select inbox to refresh (some servers need this)
                mail.select("inbox")
                
            self.logger.warning("Timeout waiting for OTP email")
            mail.close()
            mail.logout()
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving OTP: {e}")
            return None

    def _decode_header_str(self, header_value) -> str:
        """Decode email header value"""
        if not header_value:
            return ""
        decoded_list = decode_header(header_value)
        decoded_parts = []
        for content, encoding in decoded_list:
            if isinstance(content, bytes):
                if encoding:
                    try:
                        decoded_parts.append(content.decode(encoding))
                    except LookupError:
                        decoded_parts.append(content.decode('utf-8', errors='ignore'))
                else:
                    decoded_parts.append(content.decode('utf-8', errors='ignore'))
            else:
                decoded_parts.append(str(content))
        return "".join(decoded_parts)

    def _get_email_body(self, msg) -> str:
        """Extract plain text body from email"""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""

    def _extract_otp(self, text: str) -> Optional[str]:
        """Extract 6-digit OTP code from text"""
        # Look for 6 digit number
        # Enhanced regex to avoid picking up 2024 (year) or similar if possible
        # Usually OTP is standalone or labeled.
        # Simple approach first: find all 6 digit sequences
        matches = re.findall(r'\b\d{6}\b', text)
        if matches:
            # Prefer the one near "code" or "verification" if multiple?
            # For now return the first one
            return matches[0]
        return None
