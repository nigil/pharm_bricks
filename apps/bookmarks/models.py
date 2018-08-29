# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from shop.models import ProductVariant
from users.models import User


def generator_result_path(instance, filename):
    return os.path.join('generator_results',
                        instance.user.id,
                        'library_{}'.format(instance.inner_number)
                        )


# def generator_result_num():
#     rand_num = rand_num()


class ProductBookmark(models.Model):
    product = models.ForeignKey(ProductVariant)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('product', 'user')


# class GeneratorResultBookmark(models.Model):
#     file = models.FileField(upload_to=generator_result_path)
#     user = models.ForeignKey(User)
#     inner_number = models.IntegerField(default=generator_result_num)
