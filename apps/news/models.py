from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


# class NewsPage(Page):
#     body = RichTextField()
#
#     content_panels = Page.content_panels + [
#         FieldPanel('body', classname="full")
#     ]
#
#     template = 'news/news_page.html'


class NewsPost(Page):
    body = RichTextField()
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('body', classname='full')
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration")
    ]
