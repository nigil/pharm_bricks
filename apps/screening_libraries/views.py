# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.core.files.temp import NamedTemporaryFile
from rdkit import Chem
from rdkit.Chem import AllChem, ForwardSDMolSupplier
from static_page.models import StaticPage
from screening_libraries.models import ScreeningLibrary, BuildingBlock, Reaction
from screening_libraries.services import delete_old_reaction_files


# Create your views here.
class IndexView(TemplateView):
    template_name = 'screening_libraries/list.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['page'] = get_object_or_404(StaticPage, slug='screening-libraries')
        kwargs['libraries'] = ScreeningLibrary.objects.live()

        return kwargs


class LibraryDetailView(DetailView):
    model = ScreeningLibrary
    template_name = 'screening_libraries/detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super(DetailView, self).get_context_data(**kwargs)
        kwargs['active_prices'] = kwargs['object'].prices.filter(active=True)
        kwargs['nonactive_prices'] = kwargs['object'].prices.filter(active=False)
        return kwargs


class Generator(LoginRequiredMixin, TemplateView):
    template_name = 'screening_libraries/generator.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['page'] = get_object_or_404(StaticPage, slug='generator')
        kwargs['building_blocks'] = BuildingBlock.objects.live()

        return kwargs


def make_reaction(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    editor_smiles = request.POST.get('editor_smiles')
    reactions_ids = request.POST.getlist('reactions_ids[]')

    if not editor_smiles:
        return HttpResponseBadRequest('Please fill molecular editor')
    elif not reactions_ids:
        return HttpResponseBadRequest('Please choose one of allowed reagents')

    reactions = Reaction.objects.filter(id__in=[int(r_id) for r_id in reactions_ids])
    editor_mol = Chem.MolFromSmiles(editor_smiles)
    result_file_prefix = '_+_'.join([re.sub(r'\s+', '-', reaction.reaction_file.title.lower())
                                     for reaction in reactions])

    result_file_dir = os.path.join(settings.TEMP_FILES_DIR, str(request.user.id))

    try:
        os.makedirs(result_file_dir)
    except Exception:
        delete_old_reaction_files(result_file_dir)

    result_file = NamedTemporaryFile(mode='w',
                                     dir=result_file_dir,
                                     prefix=result_file_prefix + '_',
                                     suffix='.sdf',
                                     delete=False)

    try:
        success = False
        for reaction in reactions:
            rxn = AllChem.ReactionFromRxnFile(str(reaction.reaction_file.file.path))
            AllChem.SanitizeRxn(rxn)

            mols = ForwardSDMolSupplier(reaction.reactant_file.file)
            mols = [mol for mol in mols if mol is not None]

            for index, mol in enumerate(mols):
                ps = rxn.RunReactants((mol, editor_mol))

                if ps:
                    success = True
                    nice_result = Chem.MolFromSmiles(Chem.MolToSmiles(ps[-1][0]))
                    result_file.write(AllChem.MolToMolBlock(nice_result))

        file_url = os.path.join(settings.MEDIA_TMP_URL,
                                str(request.user.id),
                                result_file.name.split('/')[-1])

        if success:
            return JsonResponse({'success': True,
                                 'file_url': file_url})
    finally:
        result_file.close()

    return HttpResponseBadRequest('No reaction')
