# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView
from bookmarks.models import ProductBookmark
from shop.models import ProductVariant


def add_product_to_bookmarks(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    product_id = request.POST.get('product_id')

    try:
        product = ProductVariant.objects.get(id=product_id)
    except ProductVariant.DoesNotExist as e:
        return HttpResponseBadRequest('Selected product is incorrect')

    user = request.user

    try:
        ProductBookmark.objects.get(user=user, product=product)
        return JsonResponse({
            'error': 'This bookmark already exists'
        })
    except ProductBookmark.DoesNotExist:
        bookmark = ProductBookmark.objects.create(user=user, product=product)
        return JsonResponse({
            'success': bookmark.id
        })


def del_product_from_bookmarks(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    user = request.user
    bookmark_id = request.POST.get('bookmark_id')

    try:
        bookmark = ProductBookmark.objects.get(id=bookmark_id)
    except ProductVariant.DoesNotExist as e:
        return HttpResponseBadRequest('Selected bookmark is incorrect')

    if user != bookmark.user:
        return HttpResponseForbidden()

    bookmark.delete()

    return JsonResponse({'success': bookmark.id})
