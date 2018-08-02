# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView, TemplateView
from longclaw.longclawbasket.models import BasketItem
from longclaw.longclawbasket import utils


class Basket(TemplateView):
    template_name = 'shop/basket.html'

    def get_context_data(self, **kwargs):
        items, _ = utils.get_basket_items(self.request)
        total_price = sum(item.total() for item in items)

        items_ids = [item.id for item in items]

        items_full = (BasketItem.objects
                      .prefetch_related('variant__product__prices')
                      .filter(id__in=items_ids)
                      .order_by('id'))

        return {
            "basket": items_full,
            "total_price": total_price
        }
