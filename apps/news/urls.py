from django.conf.urls import url
from news.views import NewsPageView, Unsubscribe

urlpatterns = [
    url('^(?P<news_slug>[\d\w\-%]+)/$', NewsPageView.as_view(), name='news_detail'),
    url('^$', NewsPageView.as_view(), name='news'),
    url(r'^unsubscribe/(?P<email_base64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/$',
        Unsubscribe.as_view(), name='unsubscribe_news'),
    url(r'^unsubscribe/$', Unsubscribe.as_view(), name='unsubscribe_news_response'),
]
