# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from static_page.models import StaticPage
from screening_libraries.models import ScreeningLibrary
from django.conf import settings


# Create your views here.
class IndexView(TemplateView):
    template_name = 'screening_libraries/list.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['page'] = get_object_or_404(StaticPage, slug='screening-libraries')
        kwargs['libraries'] = ScreeningLibrary.objects.live()

        return kwargs


class DetailView(DetailView):
    model = ScreeningLibrary
    template_name = 'screening_libraries/detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super(DetailView, self).get_context_data(**kwargs)
        kwargs['phone'] = settings.COMPANY_PHONE_2
        return kwargs
