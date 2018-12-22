import os
import re
from bs4 import BeautifulSoup
from django import template
from django.utils.html import mark_safe
from django.utils.safestring import SafeBytes
from wagtail.wagtailcore.models import Site

register = template.Library()


@register.filter
def chem_formula(formula):
    return mark_safe(re.sub(r'(\d+)', r'<sub>\1</sub>', formula))


@register.filter
def filename(file):
    return os.path.basename(file.path)


@register.filter
def prepare_html_to_mail(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    links = soup.find_all('a')
    for link in links:
        link['class'] = 'p_green'
        link['style'] = ('border-bottom: 1px solid #fff;'
                         'color:#009846;'
                         'font-family:Arial;'
                         'text-decoration:none')

    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        paragraph['style'] = ('color:#464646;'
                              'font-family: Arial;'
                              'font-size: 18px;'
                              'margin: 0 0 30px 0;'
                              'padding: 0;'
                              'text-align:left')

    return str(soup)


@register.filter
def force_text_split(text, chunk_size):
    return re.sub(r'(\S{' + str(chunk_size) + '})', r'\1 ', text)


@register.filter
def content_vars(content):
    if not isinstance(content, unicode):
        content = str(content)
        if isinstance(content, SafeBytes):
            content = content.decode('utf-8')

    cur_site = Site.objects.filter(is_default_site=True).all()[0]
    site_settings = cur_site.pharmbrickssettings

    site_props = site_settings.__dict__
    del(site_props['id'], site_props['_site_cache'], site_props['_state'])
    site_prop_keys = site_props.keys()

    potential_vars = re.findall(r'\{\{\s?[\w]+\s?\}\}', content)

    for potential_var in potential_vars:
        cleared_var = potential_var.strip('{} ')
        if cleared_var in site_prop_keys:
            content = re.sub(r'\{\{\s?' + cleared_var + r'\s\}\}', site_props[cleared_var], content)

    return content

