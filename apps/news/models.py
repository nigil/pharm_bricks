from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from django.shortcuts import get_object_or_404
from static_page.models import StaticPage


class NewsPost(Page):
    template = 'news/news_page.html'

    body = RichTextField()
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('body', classname='full')
    ]

    def get_context(self, request, *args, **kwargs):
        context = {
            'page': get_object_or_404(StaticPage, slug='news'),
            'self': self,
            'request': request,
            'news': [self]
        }

        return context
