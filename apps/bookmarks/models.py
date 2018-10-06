# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from shop.models import ProductVariant
from users.models import User


def generator_result_path(_, filename):
    return os.path.join('bookmarks', filename)


class ProductBookmark(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(ProductVariant)
    user = models.ForeignKey(User, related_name='product_bookmarks')

    class Meta:
        unique_together = ('product', 'user')


class GeneratorResultBookmark(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=generator_result_path, null=True)
    user = models.ForeignKey(User, related_name='generator_bookmarks')

    class Meta:
        unique_together = ('file', 'user')
