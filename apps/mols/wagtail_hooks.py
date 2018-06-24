from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem
from django.urls import reverse
from django.conf.urls import url
from mols.views import CatalogueImport


@hooks.register('register_admin_menu_item')
def register_catalog_import_item():
    return MenuItem('Catalogue import', reverse('catalogue_import'), order=1)


@hooks.register('register_admin_urls')
def register_url_catalogue_import():
    return [
        url(r'^catalogue_import/$', CatalogueImport.as_view(), name='catalogue_import'),
    ]
