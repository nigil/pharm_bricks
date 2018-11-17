from django.core.mail.message import EmailMessage
from django.template.loader import get_template
from django.conf import settings
from wagtail.wagtailcore.models import Site


class HTMLTemplateMailer:
    def __init__(self, recipeint_email, subject, template_name, context=None,
                 sender_email=settings.EMAIL_SENDER_EMAIL, attachments=None):
        context = context or {}
        cur_sites = Site.objects.filter(is_default_site=True).all()
        if len(cur_sites):
            cur_site = cur_sites[0]
            pharmbrickssettings = cur_site.pharmbrickssettings
            context['settings'] = {
                'core': {
                    'PharmBricksSettings': pharmbrickssettings
                }
            }

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


