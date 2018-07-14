from django.conf.urls import url
from users.views import Profile

urlpatterns = [
    url('^$', Profile.as_view(), name='profile'),
    # url('^orders/$', views.blog.archive),
    # url('^libraries/$', views.blog.archive),
    # url('^subscribe/$', views.blog.archive),
]