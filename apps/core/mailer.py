from django.core.mail.message import EmailMessage
from django.template.loader import get_template
from django.conf import settings
from wagtail.wagtailcore.models import Site


class HTMLTemplateMailer:
    def __init__(self, recipeint_email, subject, template_name, context=None,
                 sender_email=None, attachments=None):
        context = context or {}
        cur_sites = Site.objects.filter(is_default_site=True).all()

        try:
            cur_site = cur_sites[0]
            pharmbrickssettings = cur_site.pharmbrickssettings
            context.update(
                {
                    'settings': {
                        'core': {'PharmBricksSettings': pharmbrickssettings}
                    },
                    'host_name': settings.HOSTNAME
                }
            )
            context['host_name'] = settings.HOSTNAME

            if not sender_email:
                sender_email = pharmbrickssettings.sender_email
        except IndexError:
            raise Exception('Set default site')

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


