# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel


class BuildingBlockType(Page, Orderable):
    subpage_types = ('screening_libraries.BuildingBlockType', 'screening_libraries.BuildingBlock')


class BuildingBlock(Page):
    sdf_file = models.OneToOneField(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    content_panels = [
        FieldPanel('title'),
        DocumentChooserPanel('sdf_file')
    ]
