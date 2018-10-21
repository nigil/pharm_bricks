from django.core.mail.message import EmailMessage
from django.template.loader import get_template
from django.conf import settings


class HTMLTemplateMailer:
    def __init__(self, recipeint_email, subject, template_name, context=None,
                 sender_email=settings.EMAIL_SENDER_EMAIL, attachments=None):
        context = context or {}

        if isinstance(recipeint_email, basestring):
            recipeint_email = (recipeint_email,)

        self.email_message = EmailMessage(
            subject,
            body=get_template(template_name).render(context),
            to=recipeint_email,
            from_email=sender_email,
            attachments=attachments
        )
        self.email_message.content_subtype = 'html'

    def send(self):
        return self.email_message.send()


