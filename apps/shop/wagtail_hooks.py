from django.conf.urls import url
from django.utils.safestring import mark_safe
from shop.models import Order
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.views import InspectView
from django.contrib.admin.utils import quote
from longclaw.settings import API_URL_PREFIX


class OrderButtonHelper(ButtonHelper):

    detail_button_classnames = []

    def detail_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = ['detail-button']
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.detail_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.get_action_url('detail', quote(pk)),
            'label': 'View',
            'classname': cn,
            'title': 'View this %s' % self.verbose_name,
        }

    # def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
    #                         classnames_exclude=None):
    #     if exclude is None:
    #         exclude = []
    #     if classnames_add is None:
    #         classnames_add = []
    #     if classnames_exclude is None:
    #         classnames_exclude = []
    #
    #     ph = self.permission_helper
    #     usr = self.request.user
    #     pk = quote(getattr(obj, self.opts.pk.attname))
    #     btns = []
    #     if ph.user_can_inspect_obj(usr, obj):
    #         btns.append(self.detail_button(
    #             pk, classnames_add, classnames_exclude))
    #
    #     return btns


class OrderModelAdmin(ModelAdmin):
    model = Order
    menu_order = 100
    menu_icon = 'list-ul'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('number', 'created_date', 'status', 'email', 'delivery_info', 'total')
    list_filter = ('status', 'created_date', 'email')
    ordering = ('-created_date',)
    inspect_view_enabled = False
    # detail_view_class = DetailView
    button_helper_class = OrderButtonHelper

    def delivery_info(self, obj):
        return mark_safe('{country};<br/>'
                         '{city};<br/><br/>'
                         '{delivery_address};<br/><br/>'
                         '{postcode}'.format(
                                country=obj.country,
                                city=obj.city,
                                delivery_address=obj.delivery_address,
                                postcode=obj.postcode)
                         )


modeladmin_register(OrderModelAdmin)
