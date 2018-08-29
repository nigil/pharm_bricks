from django.conf.urls import url
from bookmarks.views import add_product_to_bookmarks

urlpatterns = [
    url('^add_product_to_bookmarks', add_product_to_bookmarks, name='add_product_to_bookmarks'),
]