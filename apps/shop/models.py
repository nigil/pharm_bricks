# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel, FieldPanel, InlinePanel, FieldRowPanel
from longclaw.settings import PRODUCT_VARIANT_MODEL
from core.utils import ReadOnlyPanel
from cities_light.models import Country, City
from users.models import User
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


def order_number():
    last_order = Order.objects.all().order_by('id').last()
    if last_order:
        last_order_number_int = int(last_order.number.lstrip('0'))
    else:
        last_order_number_int = 0

    new_order_number = '{:0>8}'.format(last_order_number_int+1)

    return new_order_number


@python_2_unicode_compatible
class Order(ClusterableModel):
    NEW = 1
    FINISHED = 2
    CANCELLED = 3

    ORDER_STATUSES = ((NEW, 'New'),
                      (FINISHED, 'Finished'),
                      (CANCELLED, 'Cancelled'))

    number = models.CharField(max_length=8, default=order_number, editable=False, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=NEW)
    status_note = models.CharField(max_length=128, blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    # contact info
    email = models.EmailField(max_length=128)
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    delivery_address = models.CharField(max_length=500)
    postcode = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)

    user = models.ForeignKey(User, related_name='orders')

    def __str__(self):
        return "Order #{} - {}".format(self.number,
                                       self.created_date.strftime('%Y-%m-%d %H:%M:%S'))

    @property
    def total(self):
        """Total cost of the order
        """
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def total_items(self):
        """The number of individual items on the order
        """
        return self.items.count()

    class Meta:
        db_table = 'shop_order'

    panels = [
        MultiFieldPanel(
            [
                ReadOnlyPanel('number'),
                ReadOnlyPanel('created_date'),
                FieldPanel('status'),
                FieldPanel('status_note'),
                FieldPanel('comments')
            ],
            heading='Order properties'
        ),
        MultiFieldPanel(
            [
                FieldPanel('email'),
                FieldPanel('country'),
                FieldPanel('city'),
                FieldPanel('delivery_address'),
                FieldPanel('postcode'),
                FieldPanel('phone')
            ],
            heading='Contact information'
        ),

        FieldPanel('user'),

        InlinePanel('items', label='Products'),

        ReadOnlyPanel('total')
    ]


@python_2_unicode_compatible
class OrderItem(Orderable, models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = ParentalKey(Order, related_name='items', on_delete=models.CASCADE)

    @property
    def name(self):
        return '{} - {}'.format(self.product.product.chemical_name, self.product.ref)

    @property
    def price(self):
        return self.product.price

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())

    panels = [
        FieldPanel('product'),
        ReadOnlyPanel('price'),
        FieldPanel('quantity')
    ]


class ProductVariantManager(models.Manager):
    def __init__(self):
        self._all_objects = None
        super(ProductVariantManager, self).__init__()

    def all(self):
        if not self._all_objects:
            self._all_objects = self.get_queryset()

        return self._all_objects

    pass


class ProductVariant(models.Model):
    product = ParentalKey(Page, on_delete=models.CASCADE, related_name='prices')
    ref = models.CharField(max_length=32, verbose_name='Quantity')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)

    objects = ProductVariantManager()

    def __str__(self):
        return "{} - {}".format(self.product.title, self.ref)

    def get_product_title(self):
        return self.product.title

    class Meta:
        ordering = ('id',)
