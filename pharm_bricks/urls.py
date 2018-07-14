from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from search import views as search_views
from users.views import PbLogin, PbRegister, confirm_email, Profile, PbLogout, \
    PbPasswordReset, PbPasswordResetConfirm, PbPasswordResetComplete, \
    PbPasswordChange, PbPasswordChangeDone
from static_page.views import HomePage, ContactsPage
from news.views import NewsPageView

from core.views import load_cities_ajax

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^contacts/$', ContactsPage.as_view(), name='contacts'),
    url(r'^news/$', NewsPageView.as_view(), name='news'),

    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^login/$', PbLogin.as_view(), name='login'),
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

    url(r'^profile/', include('users.urls')),
    url(r'^catalogue/', include('mols.urls')),

    url(r'load-cities/', load_cities_ajax, name='load_cities_ajax'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls))

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
