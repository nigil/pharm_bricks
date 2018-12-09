from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from longclaw.longclawproducts.models import ProductVariantBase
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel
)
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtaildocs.models import Document
from modelcluster.fields import ParentalKey
from core.widgets import AdminImageFieldWidget
from core.models import RelatedLink
from core.storage import OverwriteStorage
import os


def mol_image_path(instance, filename):
    page_ancestors = instance.get_ancestors()
    for ancestor in page_ancestors[::-1]:
        if hasattr(ancestor.get_parent(), 'slug') and ancestor.get_parent().slug == 'catalogue':
            return os.path.join('mols', ancestor.slug, filename)

    return os.path.join('mols', instance.get_parent().slug, filename)


class MoleculesGroup(Page, Orderable):
    subpage_types = ('mols.Molecule', 'mols.MoleculesGroup')


class Molecule(Page):
    parent_page_types = ['mols.MoleculesGroup']

    catalogue_number = models.CharField(verbose_name='Catalogue number', max_length=20, unique=True)
    chemical_name = models.CharField(max_length=1000)

    formula = models.CharField(max_length=1000)
    log_p = models.FloatField(verbose_name='Log P, calc', null=True, blank=True)
    log_s = models.FloatField(verbose_name='Log S, calc', null=True, blank=True)
    mw = models.FloatField(verbose_name='Mass', null=True, blank=True)
    cas = models.CharField(max_length=50, null=True, blank=True)
    purity = models.IntegerField(verbose_name='Chemical purity', null=True, blank=True)
    smiles = models.CharField(max_length=500, null=True, blank=True)

    image = models.ImageField(upload_to=mol_image_path,
                              storage=OverwriteStorage(),
                              null=True,
                              blank=True)

    in_stock = models.BooleanField(default=True)

    msds = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = [
        index.SearchField('title', partial_match=True, boost=2),
        index.SearchField('cas'),
        index.SearchField('catalogue_number'),
        index.SearchField('formula')
    ]

    content_panels = [
        FieldPanel('title'),
        FieldPanel('catalogue_number'),
        FieldPanel('image'
                   , widget=AdminImageFieldWidget
                   ),
        MultiFieldPanel(
            [
                FieldPanel('chemical_name'),
                FieldPanel('formula'),
                FieldPanel('log_p'),
                FieldPanel('log_s'),
                FieldPanel('mw'),
                FieldPanel('cas'),
                FieldPanel('purity'),
                FieldPanel('smiles')
            ],
            heading='Molecule properties'
        ),
        FieldPanel('in_stock'),
        InlinePanel('prices', label='Prices'),

        InlinePanel('references', label="References"),

        DocumentChooserPanel('msds'),
        InlinePanel('screening_compounds', label='Screening compounds')
    ]

    show_in_menus_default = True

    #promote_panels = []


class MoleculeReference(Orderable, RelatedLink):
    page = ParentalKey(Molecule, on_delete=models.CASCADE, related_name='references')


class MoleculeScreeningCompound(Orderable):
    page = ParentalKey(Molecule, on_delete=models.CASCADE, related_name='screening_compounds')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        DocumentChooserPanel('document')
    ]
