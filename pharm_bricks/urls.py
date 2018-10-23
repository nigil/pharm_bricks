from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from longclaw.longclawbasket import urls as basket_urls
from longclaw.longclawbasket import api

from users.views import PbLogin, PbRegister, PbLogout, \
    PbPasswordReset, PbPasswordResetConfirm, PbPasswordResetComplete, \
    PbPasswordChange, PbPasswordChangeDone, confirm_email
from static_page.views import HomePage, ContactsPage
from shop.views import Basket
from core.views import load_cities_ajax
from screening_libraries.views import Generator, make_reaction

basket_list = api.BasketViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'bulk_update'
})


urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^contacts/$', ContactsPage.as_view(), name='contacts'),

    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^login/', PbLogin.as_view(), name='login'),
    url(r'^logout/$', PbLogout.as_view(), name='logout'),
    url(r'^register/$', PbRegister.as_view(), name='register'),
    url(r'^confirm-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        confirm_email, name='confirm_email'),
    url(r'password-reset/$', PbPasswordReset.as_view(), name='password_reset'),
    url(r'password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PbPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'password-reset-complete/$', PbPasswordResetComplete.as_view(), name='password_reset_complete'),
    url(r'password-change/$', PbPasswordChange.as_view(), name='password_change'),
    url(r'password-change-done/$', PbPasswordChangeDone.as_view(), name='password_change_done'),

    url(r'^news/', include('news.urls')),
    url(r'^profile/', include('users.urls')),
    url(r'^catalogue/', include('mols.urls')),
    url(r'^screening-libraries/', include('screening_libraries.urls')),
    url(r'^generator/', Generator.as_view(), name='generator'),
    url(r'^search/', include('search.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^bookmarks/', include('bookmarks.urls')),
    url(r'^make_reaction/', login_required(make_reaction), name='make_reaction'),

    url(r'load-cities/', load_cities_ajax, name='load_cities_ajax'),
    url(r'^basket/$', Basket.as_view(), name='basket'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'^', include(basket_urls)),
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    import debug_toolbar

    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
