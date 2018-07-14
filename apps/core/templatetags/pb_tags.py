from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag
def mols_breadcrumbs(items_list):
    if items_list:
        breadcrumbs_list = ['<a href="{}">{}</a>'.format(item.url, item.title)
                            for item in items_list[:-1]]

        last_item = items_list[-1]
        breadcrumbs_list.append(last_item.title.upper()
                                if last_item.content_type.model == 'molecule'
                                else last_item.title)

        return mark_safe(' / '.join(breadcrumbs_list))
