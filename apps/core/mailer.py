from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import os


class HTMLTemplateMailer:
    def __init__(self, recipeint_email, subject, template_name, context=None, sender_email=None):
        self.sender_email = sender_email if sender_email else settings.EMAIL_SENDER_EMAIL
        self.recipient_email = recipeint_email
        self.subject = subject
        self.template = get_template(template_name)
        self.context = context or {}

    def send(self):
        message = self.template.render(self.context)
        mail.send_mail(
            subject=self.subject,
            message=message,
            html_message=message,
            from_email=self.sender_email,
            recipient_list=[self.recipient_email],
            fail_silently=False
        )
        return mail


