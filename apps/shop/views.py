# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from longclaw.longclawbasket.models import BasketItem
from longclaw.longclawbasket import utils
from shop.forms import OrderForm
from shop.models import Order, OrderItem
from core.mailer import HTMLTemplateMailer


class Basket(FormView):
    template_name = 'shop/basket.html'
    form_class = OrderForm
    success_url = reverse_lazy('basket')

    def form_valid(self, form):
        cur_user = self.request.user

        order = Order.objects.create(
            email=cur_user.email,
            comments=form.cleaned_data.get('comments'),
            country=cur_user.country,
            city=cur_user.city,
            delivery_address=cur_user.delivery_address,
            postcode=cur_user.postcode,
            phone=cur_user.phone,
            user=cur_user
        )

        items, _ = utils.get_basket_items(self.request)

        for item in items:
            OrderItem.objects.create(
                product=item.variant,
                quantity=item.quantity,
                order=order
            )

        utils.destroy_basket(self.request)
        cur_user.basket_id = None
        cur_user.save(update_fields=('basket_id',))
        self.request.session[utils.BASKET_ID_SESSION_KEY] = ''

        # send email
        mail_subject = 'New order on {}'.format(settings.HOSTNAME)
        mailer = HTMLTemplateMailer(cur_user.email,
                                    mail_subject,
                                    'email/checkout.html',
                                    {
                                        'order': order,
                                        'user': cur_user,
                                        'phone': settings.COMPANY_PHONE,
                                        'site_host': settings.HOSTNAME

                                    })
        mailer.send()

        messages.add_message(self.request, messages.INFO,
                             'The order was successfully created. Follow <a href="'
                             + reverse('user_orders')
                             + '">this page</a> to see all your orders')

        return super(Basket, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Basket, self).get_context_data(**kwargs)

        items, _ = utils.get_basket_items(self.request)
        total_price = sum(item.total() for item in items)

        items_ids = [item.id for item in items]

        items_full = (BasketItem.objects
                      .prefetch_related('variant__product__prices')
                      .filter(id__in=items_ids)
                      .order_by('id'))

        context.update({
            "basket": items_full,
            "total_price": total_price
        })

        return context


@login_required
def repeat_order(request):
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)

    if order.user != request.user or not request.is_ajax():
        return HttpResponseForbidden()

    basket, basket_id = utils.get_basket_items(request)

    for order_item in order.items.all():
        find = False
        for basket_item in basket:
            if order_item.product == basket_item.variant:
                basket_item.quantity += order_item.quantity
                basket_item.save()
                find = True
                break

        if not find:
            BasketItem.objects.create(
                basket_id=basket_id,
                quantity=order_item.quantity,
                variant=order_item.product
            )

    return HttpResponse()
