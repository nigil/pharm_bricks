# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.core.files import File
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.conf import settings
from core.mailer import HTMLTemplateMailer
from bookmarks.models import ProductBookmark, GeneratorResultBookmark
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


def add_generator_result_to_bookmarks(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    result_url = request.POST.get('result_url', None)
    if not result_url:
        return HttpResponseBadRequest()

    result_name = os.path.basename(result_url)
    result_path = os.path.join(settings.TEMP_FILES_DIR, str(request.user.id), result_name)
    result_file = File(open(result_path, 'r'))

    bookmark = GeneratorResultBookmark.objects.create(user=request.user)
    bookmark.file.save(result_name, result_file)
    try:
        bookmark.save()
        os.remove(result_path)
        return HttpResponse('success')
    except Exception:
        return HttpResponse('error')


def send_price_request(request, id):
    if not request.is_ajax():
        return HttpResponseForbidden()

    user = request.user

    try:
        bookmark = GeneratorResultBookmark.objects.get(user=user, id=id)
    except GeneratorResultBookmark.DoesNotExist as e:
        return HttpResponseBadRequest()

    bookmark_filename = os.path.basename(bookmark.file.path)
    bookmark_content = open(bookmark.file.path).read()

    mailer = HTMLTemplateMailer(
        settings.ADMIN_EMAIL,
        'Library generator. Price request.',
        'email/price-request.html',
        {'user': user},
        attachments=((bookmark_filename, bookmark_content, 'text/html'),)
    )
    mailer.send()

    return HttpResponse()


def delete_bookmark(request, id):
    if not request.is_ajax():
        return HttpResponseForbidden()

    user = request.user
    bookmark_type = request.POST.get('type')

    bookmark_class = ProductBookmark
    if bookmark_type == 'generator':
        bookmark_class = GeneratorResultBookmark

    bookmark_class.objects.filter(user=user, id=id).update(active=False)

    return HttpResponse()


def restore_bookmark(request, id):
    if not request.is_ajax():
        return HttpResponseForbidden()

    user = request.user
    bookmark_type = request.POST.get('type')

    bookmark_class = ProductBookmark
    if bookmark_type == 'generator':
        bookmark_class = GeneratorResultBookmark

    bookmark_class.objects.filter(user=user, id=id).update(active=True)

    return HttpResponse()
