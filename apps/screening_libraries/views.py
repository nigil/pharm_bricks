# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from rdkit import Chem
from rdkit.Chem import AllChem, ForwardSDMolSupplier
from static_page.models import StaticPage
from screening_libraries.models import ScreeningLibrary, BuildingBlock, BuildingBlockReagent


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
    building_block_id = request.POST.get('building_block_id')
    reagent_ids = request.POST.getlist('reagent_ids[]')

    if not all((editor_smiles, building_block_id, reagent_ids)):
        return HttpResponseBadRequest('One of terms is\'t set')

    building_block = BuildingBlock.objects.get(id=building_block_id)
    reagents = BuildingBlockReagent.objects.filter(id__in=[int(r_id) for r_id in reagent_ids])

    editor_mol = Chem.MolFromSmiles(editor_smiles)

    for reagent in reagents:
        rxn = AllChem.ReactionFromRxnFile(str(reagent.file.file.path))
        # rxn = AllChem.ReactionFromSmarts(str('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]'))

        rxn.Initialize()
        nWarn, nError, nReacts, nProds, reactantLabels = PreprocessReaction(rxn)
        print(nWarn)
        print(nError)
        print(nReacts)
        print(nProds)
        print(reactantLabels)

        print(rxn.GetNumProductTemplates())
        path = building_block.sdf_file.file.path
        mols = ForwardSDMolSupplier(building_block.sdf_file.file)
        mols = [mol for mol in mols if mol is not None]

        for mol in mols:
            ps = rxn.RunReactants((mol, editor_mol))
            print(len(ps))

