# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField
from modelcluster.fields import ParentalKey
from core.storage import OverwriteStorage
from core.widgets import AdminImageFieldWidget
from core.fields import BodyStreamBlock


def screening_libraries_image_path(instance, filename):
    return os.path.join('screening_libraries', instance.slug, filename)


def screening_libraries_detail_image_path(instance, filename):
    return os.path.join('screening_libraries', instance.slug, 'detail_' + filename)


class ScreeningLibrary(Page):
    catalogue_number = models.CharField(max_length=20, unique=True)

    preview_description = StreamField(BodyStreamBlock(), null=True)
    detail_description = StreamField(BodyStreamBlock(), null=True)

    image = models.ImageField(upload_to=screening_libraries_image_path,
                              storage=OverwriteStorage(),
                              null=True,
                              blank=True)

    detail_image = models.ImageField(upload_to=screening_libraries_detail_image_path,
                                     storage=OverwriteStorage(),
                                     null=True,
                                     blank=True)

    molecules_number = models.IntegerField(default=1)

    in_stock = models.BooleanField(default=True)

    sdf_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    xls_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = [
        index.SearchField('title', partial_match=True, boost=2),
        index.SearchField('catalogue_number'),
    ]

    content_panels = [
        FieldPanel('title'),
        FieldPanel('catalogue_number'),
        StreamFieldPanel('preview_description'),
        StreamFieldPanel('detail_description'),
        FieldPanel('image', widget=AdminImageFieldWidget),
        FieldPanel('detail_image', widget=AdminImageFieldWidget),
        FieldPanel('molecules_number'),
        FieldPanel('in_stock'),
        DocumentChooserPanel('sdf_file'),
        DocumentChooserPanel('xls_file'),
        InlinePanel('prices', label='Prices'),
    ]


class BuildingBlock(Page):
    content_panels = [
        FieldPanel('title'),
        InlinePanel('reactions', label='Reactions')
    ]


class Reaction(Orderable, models.Model):
    building_block = ParentalKey(
        BuildingBlock,
        on_delete=models.CASCADE,
        related_name='reactions'
    )

    reaction_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reaction_files'
    )

    reactant_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reactant_files'
    )

    panels = [
        DocumentChooserPanel('reaction_file'),
        DocumentChooserPanel('reactant_file'),
    ]
