from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib import messages
from news.models import NewsPost
from news.utils import UserUnsubscriber
from users.models import User
from static_page.models import StaticPage


class NewsPageView(TemplateView):
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['page'] = get_object_or_404(StaticPage, slug='news')
        kwargs['news'] = NewsPost.objects.live().order_by('-first_published_at')

        return kwargs


class Unsubscribe(TemplateView):
    template_name = 'news/unsubscribe.html'

    def get_context_data(self, **kwargs):
        if kwargs.get('email_base64') and kwargs.get('token'):
            unsubscriber = UserUnsubscriber()
            user_email = unsubscriber.parse_unsubscribe_link(kwargs['email_base64'],
                                                             kwargs['token'])
            try:
                User.objects.filter(email=str(user_email)).update(subscribed_on_news=False)
                messages.add_message(
                    self.request,
                    messages.INFO,
                    'You have been successfully unsubscribed. '
                    'To change your subscribe settings follow '
                    '<a href="{}">link</a>.'.format(reverse('user_subscribe'))
                )
            except User.DoesNotExist:
                messages.add_message(self.request, messages.ERROR,
                                     'This is incorrect unsubscribe link.')

            redirect('unsubscribe_news_response')
        else:
            return kwargs
