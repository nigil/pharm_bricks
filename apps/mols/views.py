from mols.forms import CatalogueImportForm
from django.views.generic.edit import FormView
from mols.services.import_catalogue import RDKitClient
from django.urls import reverse_lazy
from django.shortcuts import render


class CatalogueImport(FormView):
    template_name = 'mols/admin/catalogue_import.html'
    form_class = CatalogueImportForm
    success_url = reverse_lazy('catalogue_import')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            sdf_source = request.FILES['import_file']

            import_log = RDKitClient.import_sdf_to_catalog(sdf_source)

            # return self.form_valid(form)
            return render(request, self.template_name, {'form': form, 'import_log': import_log})
        else:
            return self.form_invalid(form)
