from mols.forms import CatalogueImportForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from mols.services.import_catalogue import RDKitClient
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from mols.models import MoleculesGroup, Molecule
from static_page.models import StaticPage
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string


def get_catalogue_sections(request, **kwargs):
    extra_context = {}

    catalogue_root = MoleculesGroup.objects.child_of(StaticPage.objects.get(slug='home')) \
        .get(slug='catalogue')
    extra_context['catalogue_page'] = catalogue_root

    section_slug = request.GET.get('section') or kwargs.get('section')
    sub_section_slug = request.GET.get('sub_section') or kwargs.get('sub_section')
    if section_slug:
        section = get_object_or_404(MoleculesGroup.objects.child_of(catalogue_root),
                                    slug=section_slug)
        extra_context['section'] = section

        if sub_section_slug:
            sub_section = get_object_or_404(MoleculesGroup.objects.child_of(section),
                                            slug=sub_section_slug)
            extra_context['sub_section'] = sub_section

    return extra_context


def add_breadcrumbs(context):
    breadcrumbs_list = []
    for item in [context.get('section'), context.get('sub_section'), context.get('object')]:
        if item:
            breadcrumbs_list.append(item)
    context['breadcrumbs'] = breadcrumbs_list


class CatalogueImport(FormView):
    template_name = 'mols/admin/catalogue_import.html'
    form_class = CatalogueImportForm
    success_url = reverse_lazy('catalogue_import')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            sdf_source = request.FILES['import_file']

            import_log = RDKitClient.import_sdf_to_catalog(sdf_source)

            return render(request, self.template_name, {'form': form, 'import_log': import_log})
        else:
            return self.form_invalid(form)


class CatalogueList(TemplateView):
    template_name = 'mols/catalogue_list.html'

    def get(self, request, *args, **kwargs):
        context = get_catalogue_sections(request, **kwargs)
        add_breadcrumbs(context)

        return self.render_to_response(context)


class MolsList(ListView):
    queryset = Molecule.objects.live().order_by('-title')
    allow_empty = True
    paginate_by = 9
    template_name = 'mols/mols_list.html'

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        extra_context = get_catalogue_sections(request)

        if request.GET.get('size'):
            self.paginate_by = request.GET.get('size')

        if extra_context.get('section'):
            if extra_context.get('sub_section'):
                self.object_list = self.object_list.child_of(extra_context['sub_section'])
            else:
                self.object_list = self.object_list.descendant_of(extra_context['section'])

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list,
                                                                              'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0

            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })

        context = self.get_context_data()
        context.update(extra_context)

        html = render_to_string(self.template_name, context, request)
        return JsonResponse({
            'mols': html,
            'page_num': context['page_obj'].number,
            'pages_cnt': context['paginator'].num_pages
        })


class CatalogueDetail(DetailView):
    model = Molecule
    slug_url_kwarg = 'mol_slug'
    template_name = 'mols/catalogue_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context = self.get_context_data(object=self.object)
        context.update(get_catalogue_sections(self.request, **kwargs))
        add_breadcrumbs(context)

        return self.render_to_response(context)
