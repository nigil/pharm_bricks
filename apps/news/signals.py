from django.dispatch import receiver
from django.conf import settings
from wagtail.wagtailcore.signals import page_published
from core.mailer import HTMLTemplateMailer
from users.models import User
from news.models import NewsPost
from news.utils import UserUnsubscriber


@receiver(page_published)
def mailing_after_news_publish(instance, **kwargs):
    if (isinstance(instance, NewsPost)
            and instance.first_published_at == instance.last_published_at):

        unsubscriber = UserUnsubscriber()
        for user in User.objects.filter(subscribed_on_news=True):
            mailer = HTMLTemplateMailer(
                user.email,
                'News from PharmBricks',
                'email/news_mailing.html',
                {
                    'site_host': settings.HOSTNAME,
                    'news_post': instance,
                    'unsubscribe_link': unsubscriber.make_unsubscribe_link(user.email)
                },
            )
            mailer.send()

