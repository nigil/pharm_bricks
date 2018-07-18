from django.conf.urls import url
from search.views import search, SearchList

urlpatterns = [
    url('^load_mols', SearchList.as_view(), name='search_list'),
    url('^$', search, name='search'),
]
