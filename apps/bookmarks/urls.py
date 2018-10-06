from django.conf.urls import url
from bookmarks.views import add_product_to_bookmarks, add_generator_result_to_bookmarks, \
    delete_bookmark, send_price_request

urlpatterns = [
    url('^add-product-to-bookmarks', add_product_to_bookmarks, name='add_product_to_bookmarks'),
    url('^add-generator-result-to-bookmarks', add_generator_result_to_bookmarks,
        name='add_generator_result_to_bookmarks'),
    url(r'^send-price-request/(?P<id>[0-9]+)/', send_price_request, name='send_price_request'),
    url(r'^delete/(?P<id>[0-9]+)/', delete_bookmark, name='delete_bookmark')
]
