from django import forms


class CatalogueImportForm(forms.Form):
    import_file = forms.FileField()
