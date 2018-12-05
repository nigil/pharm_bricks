# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path
from tempfile import NamedTemporaryFile
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from django.template.loader import get_template
from longclaw.longclawbasket.models import BasketItem
from longclaw.longclawbasket import utils
from shop.forms import OrderForm
from shop.models import Order, OrderItem
from core.mailer import HTMLTemplateMailer
from core.models import PharmBricksSettings
from xhtml2pdf import pisa


class Basket(FormView):
    template_name = 'shop/basket.html'
    form_class = OrderForm
    success_url = reverse_lazy('basket')

    def form_valid(self, form):
        # checkout
        cur_user = self.request.user
        site_settings = PharmBricksSettings.for_site(self.request.site)

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

        # # utils.destroy_basket(self.request)
        # cur_user.basket_id = None
        # cur_user.save(update_fields=('basket_id',))
        # self.request.session[utils.BASKET_ID_SESSION_KEY] = ''
        #
        # # send email
        # mail_subject = 'Your order confirmation - № {}'.format(order.number)

        # prepare invoice
        # invoice_file = NamedTemporaryFile(bufsize=0)
        invoice_file = open('/app/test.pdf', 'w+b')
        print(invoice_file.name)
        invoice_html = get_template('email/invoice.html').render({
            'site_settings': site_settings,
            'order': order,
            'site_host': settings.HOSTNAME
        })
        pisa.CreatePDF(invoice_html, invoice_file)

        print(invoice_html)
        print(invoice_file)
        print(invoice_file.read())

        # print(pdf_out)

        # invoice_file.seek(0)
        # pdf_content = invoice_file.read()
        #
        # for email in (cur_user.email, site_settings.admin_email):
        #     mailer = HTMLTemplateMailer(
        #         email,
        #         mail_subject,
        #         'email/checkout.html',
        #         {
        #             'order': order,
        #             'user': cur_user,
        #             'site_host': settings.HOSTNAME
        #
        #         },
        #         attachments=(
        #             ('invoice.pdf', pdf_content, 'application/pdf'),
        #         )
        #     )
        #     mailer.send()
        #
        # os.remove(invoice_file.name)
        #
        # messages.add_message(self.request, messages.INFO,
        #                      'Please check your email for an order confirmation.')
        #
        # return super(Basket, self).form_valid(form)
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
