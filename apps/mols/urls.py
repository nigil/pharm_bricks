from django.conf.urls import url
from mols.views import CatalogueList, CatalogueDetail, MolsList

urlpatterns = [
    url('^(?P<section>[a-zA-Z\-_]+)/(?P<sub_section>[a-zA-Z\-_]*)/?(?P<mol_slug>[a-z]{3}[0-9]+)/$',
        CatalogueDetail.as_view(), name='catalogue_detail'),
    url('^(?P<section>[a-zA-Z\-_]+)/(?P<sub_section>[a-zA-Z\-_]+)/$',
        CatalogueList.as_view(), name='catalogue_list'),
    url('^(?P<section>[a-zA-Z\-_]+)/$', CatalogueList.as_view(), name='catalogue_list'),
    url('^load_mols', MolsList.as_view(), name='mols_list'),
    url('^$', CatalogueList.as_view(), name='catalogue_list'),
    # url('^libraries/$', views.blog.archive),
    # url('^subscribe/$', views.blog.archive),
]
