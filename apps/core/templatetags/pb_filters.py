import re
from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def chem_formula(formula):
    return mark_safe(re.sub(r'(\d+)', r'<sub>\1</sub>', formula))
