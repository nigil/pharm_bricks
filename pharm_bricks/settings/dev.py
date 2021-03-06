from __future__ import absolute_import, unicode_literals

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
def show_toolbar(request):
    return DEBUG


INSTALLED_APPS += ['debug_toolbar']


MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'pharm_bricks.settings.dev.show_toolbar',
}

AUTH_PASSWORD_VALIDATORS = []
