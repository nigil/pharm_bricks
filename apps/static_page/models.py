import os
from django.db import models
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from core.fields import BodyStreamBlock
from core.storage import OverwriteStorage


def slider_image_path(instance, filename):
    return os.path.join('slider', filename)


class StaticPage(Page):
    template = 'pages/static_page.html'

    body = StreamField(BodyStreamBlock(), null=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class HomePage(StaticPage):
    template = 'pages/home_page.html'

    footer = StreamField(BodyStreamBlock(), null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        StreamFieldPanel('footer')
    ]


class HomeSlider(StaticPage):
    image = models.ImageField(upload_to=slider_image_path,
                              storage=OverwriteStorage(),
                              null=True,
                              blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        StreamFieldPanel('body'),
    ]


