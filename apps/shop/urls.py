from django.conf.urls import url
from shop.views import repeat_order

urlpatterns = [
    url('^repeat_order$', repeat_order, name='repeat_order'),
]
