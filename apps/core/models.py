from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


class EnumBase(object):
    @classmethod
    def get_listed_values(cls, list_):
        return {key: cls.values[key] for key in list_}

    @classmethod
    def get_choices(cls):
        return ((key, val) for key, val in cls.values.items())


class RelatedLink(models.Model):
    title = models.CharField(max_length=255, blank=True)
    link = models.URLField("Link", max_length=510)

    panels = [
        FieldPanel('title'),
        FieldPanel('link'),
    ]

    class Meta:
        abstract = True


@register_setting
class PharmBricksSettings(BaseSetting):
    phone = models.CharField(max_length=30)
    sender_email = models.EmailField(default='info@pharmbricks.com')
    info_email = models.EmailField(default='info@pharmbricks.com')
    admin_email = models.EmailField(default='info@pharmbricks.com')
    address = models.TextField(blank=True, default='')
    linkedin_link = models.CharField(blank=True, max_length=200, default='')
    twitter_link = models.CharField(blank=True, max_length=200, default='')
    footer = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'PharmBricks settings'
