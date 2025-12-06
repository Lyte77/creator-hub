
from allauth.account.adapter import DefaultAccountAdapter
from .utils.resend_emails import send_resend_email

class ResendAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        subject = self.render_mail_subject(template_prefix, context)
        html = self.render_mail_body(template_prefix, context)

        send_resend_email(
            to=email,
            subject=subject,
            html=html
        )
