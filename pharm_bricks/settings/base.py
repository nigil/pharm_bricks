"""
Django settings for pharm_bricks project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from __future__ import absolute_import, unicode_literals
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SECRET_KEY = os.getenv('SECRET_KEY')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

DEBUG = True if os.getenv('DEBUG', None) == 'true' else False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party apps
    'modelcluster',
    'taggit',
    'easy_thumbnails',
    'cities_light',

    # project apps
    'core.apps.CoreConfig',
    'home',
    'search',
    'users.apps.UsersConfig',
    'news.apps.NewsConfig',
    'static_page.apps.StaticPageConfig',
    'mols.apps.MolsConfig',
    'shop.apps.ShopConfig',
    'screening_libraries.apps.ScreeningLibrariesConfig',
    'bookmarks.apps.BookmarksConfig',

    # wagtail_apps
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.modeladmin',
    'wagtailmenus',
    'wagtail.contrib.settings',
    'wagtail.contrib.postgres_search',
    
    # longclaw_apps
    'longclaw.longclawcore',
    'longclaw.longclawsettings',
    # 'longclaw.longclawshipping',
    'longclaw.longclawproducts',
    # 'longclaw.longclaworders',
    # 'longclaw.longclawcheckout',
    'longclaw.longclawbasket',
    # 'longclaw.longclawstats',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware'
]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365

ROOT_URLCONF = 'pharm_bricks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
                'longclaw.longclawsettings.context_processors.currency'
            ],
        },
    },
]

WSGI_APPLICATION = 'pharm_bricks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.getenv('DB_HOST'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'PORT': os.getenv('DB_PORT')
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TMP_DIR = 'tmp'
TEMP_FILES_DIR = os.path.join(MEDIA_ROOT, TMP_DIR)
MEDIA_URL = '/media/'
MEDIA_TMP_URL = MEDIA_URL + TMP_DIR + '/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

USE_I18N = False

# Wagtail settings
WAGTAIL_SITE_NAME = "pharm_bricks"

WAGTAIL_USER_EDIT_FORM = 'users.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'users.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['organization', 'phone', 'country',
                              'city', 'delivery_address', 'postcode']
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 5 * 1024 * 1024

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
        'AUTO_UPDATE': True,
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
    }
}

# User settings
WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'users/login.html'
WAGTAIL_FRONTEND_LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'login'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG \
    else 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SENDER_EMAIL = os.getenv('EMAIL_SENDER_EMAIL')
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
INFO_EMAIL = os.getenv('INFO_EMAIL')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

# Longclaw settings

# The payment gateway to use. `BasePayment` is a dummy payment gateway for testing.
# Longclaw also offers 'BraintreePayment', 'PaypalVZeroPayment' and 'StripePayment'
PAYMENT_GATEWAY = 'longclaw.longclawcheckout.gateways.BasePayment'

PRODUCT_VARIANT_MODEL = 'shop.ProductVariant'

THUMBNAIL_ALIASES = {
    'mols.Molecule.image': {
        'small': {
            'size': (32, 32), 'crop': 'scale'
        },
        'middle': {
            'size': (209, 170), 'crop': ',', 'quality': 95
        }
    },
    'screening_libraries.ScreeningLibrary.image': {
        'small': {
            'size': (32, 32), 'crop': True
        },
        'middle': {
            'size': (288, 303), 'crop': True, 'quality': 95
        }
    },
    'screening_libraries.ScreeningLibrary.detail_image': {
        'big': {
            'size': (403, 383), 'crop': True, 'quality': 95
        }
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.getenv('ALLOWED_HOST')]
HOSTNAME = os.getenv('HOSTNAME')

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']

COMPANY_PHONE = '00 567-244-5678'
COMPANY_PHONE_2 = '0065 96432266'
