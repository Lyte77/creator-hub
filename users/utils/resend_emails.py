# utils/resend_email.py
import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY

def send_resend_email(to, subject, html):
    return resend.Emails.send({
        "from": settings.FROM_EMAIL,
        "to": to,
        "subject": subject,
        "html": html
    })




