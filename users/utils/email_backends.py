# myproject/email_backends.py

import logging
from django.core.mail.backends.smtp import EmailBackend
from smtplib import SMTPException
from socket import timeout

logger = logging.getLogger(__name__)

class ErrorCatchingEmailBackend(EmailBackend):
    """
    A custom email backend that wraps the sending process in error handling 
    to catch timeouts, connection failures, and SMTP errors.
    """
    def send_messages(self, email_messages):
        """
        Catches TimeoutError and other related exceptions during email sending.
        """
        try:
            # Call the original (parent) method to attempt sending
            num_sent = super().send_messages(email_messages)
            return num_sent
            
        except timeout as e:
            # Catches TimeoutError (like WinError 10060)
            logger.error(f"EMAIL TIMEOUT ERROR: Failed to connect to SMTP server. Error: {e}")
            # You can log this to a specific file, database, or alert system
            return 0  # Indicate that 0 messages were sent
            
        except SMTPException as e:
            # Catches common SMTP errors (authentication, server refusal, etc.)
            logger.error(f"EMAIL SMTP ERROR: An SMTP server error occurred. Error: {e}")
            return 0
            
        except Exception as e:
            # Catch all other unexpected errors
            logger.critical(f"UNEXPECTED EMAIL SENDING ERROR: {e}")
            return 0