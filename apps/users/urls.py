from django.conf.urls import url
from users.views import Profile, Orders, Bookmarks, Subscribe, change_news_subscribe

urlpatterns = [
    url('^$', Profile.as_view(), name='profile'),
    url('^orders/$', Orders.as_view(), name='user_orders'),
    url('^libraries/$', Bookmarks.as_view(), name='user_libraries'),
    url('^subscribe/$', Subscribe.as_view(), name='user_subscribe'),
    url('^change_subscribe/$', change_news_subscribe, name='change_subscribe')
]
