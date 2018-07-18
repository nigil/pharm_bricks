from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string

from mols.models import Molecule
from wagtail.wagtailsearch.models import Query


def search(request):
    search_query = request.GET.get('q', None)

    return render(request, 'search/search.html', {
        'search_query': search_query
    })


class SearchList(ListView):
    queryset = Molecule.objects.live()
    allow_empty = True
    paginate_by = 16
    template_name = 'mols/mols_list.html'

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()

        self.object_list = self.get_queryset()

        if request.GET.get('size'):
            self.paginate_by = request.GET.get('size')

        search_query = request.GET.get('q', None)
        if search_query:
            self.object_list = self.object_list.search(search_query)

            Query.get(search_query).add_hit()
        else:
            self.object_list = self.object_list.none()

        context = self.get_context_data()

        html = render_to_string(self.template_name, context, request)
        return JsonResponse({
            'mols': html,
            'page_num': context['page_obj'].number,
            'pages_cnt': context['paginator'].num_pages
        })
