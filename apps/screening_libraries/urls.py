from django.conf.urls import url
from screening_libraries.views import IndexView, DetailView

urlpatterns = [
    url('^$', IndexView.as_view(), name='screening_libraries'),
    url('^(?P<slug>[0-9a-zA-Z\-_]+)/$', DetailView.as_view(), name='screening_library')
]
