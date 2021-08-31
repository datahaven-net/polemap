"""
Django settings for foo project.

Generated by 'django-admin startproject' using Django 1.9.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from __future__ import unicode_literals

#------------------------------------------------------------------------------

import os

#------------------------------------------------------------------------------

if os.environ.get('DOCKER_ENV'):
    from main import params_docker as params

else:
    from main import params


#------------------------------------------------------------------------------
#--- Sentry config
SENTRY_ENABLED = getattr(params, 'SENTRY_ENABLED', False)
if SENTRY_ENABLED:
    SENTRY_DSN = getattr(params, 'SENTRY_DSN', '')
    import sentry_sdk  # @UnresolvedImport
    from sentry_sdk.integrations.django import DjangoIntegration  # @UnresolvedImport
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), ],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

#------------------------------------------------------------------------------
#--- Basic Django settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = '/home/zenaida/live/current'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
REPO_ROOT = os.path.dirname(SRC_PATH)
CONTENT_DIR = BASE_DIR


#------------------------------------------------------------------------------
#--- Quick-start development settings
# Unsuitable for production!
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
DEBUG = getattr(params, 'DEBUG', False)
DEBUGTOOLBAR_ENABLED = False
METRICS_ENABLED = False
CACHE_BACKEND = 'django.core.cache.backends.memcached.MemcachedCache'
CACHE_LOCATION = '127.0.0.1:11211'
CACHE_PREFIX = 'polemap'

# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = getattr(params, 'SECRET_KEY', 'must be declared in src/main/params.py directly  !')

ALLOWED_HOSTS = ['*', ]

SITE_ID = 1
SITE_BASE_URL = getattr(params, 'SITE_BASE_URL', 'http://localhost:8000')

ROOT_URLCONF = 'main.urls'


#------------------------------------------------------------------------------
#--- Logging configuration

LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console', ],
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        'timestamped': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'timestamped',
            'filters': [],
        },
    },
    'loggers': {
        'django.request': {
            'level': LOG_LEVEL,
            'propagate': False,
            'handlers': ['console', ],
        },
    },
}

#------------------------------------------------------------------------------
#--- Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#------------------------------------------------------------------------------
#--- Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

#------------------------------------------------------------------------------
#--- Application definition
INSTALLED_APPS = [
    # basic Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',

    # html templates: https://django-bootstrap4.readthedocs.io/en/stable/quickstart.html
    'bootstrap4',

    # useful things: https://django-extensions.readthedocs.io/en/latest/command_extensions.html
    'django_extensions',
    'main',
]

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['bootstrap4.templatetags.bootstrap4'],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


#------------------------------------------------------------------------------
#--- Sentry defaults
SENTRY_DSN = None


#------------------------------------------------------------------------------
#--- STANDALONE ?
ENV = getattr(params, 'ENV')
STANDALONE = True
if ENV in ['production', 'docker', ]:  # pragma: no cover
    STANDALONE = False


#------------------------------------------------------------------------------
#--- DATABASE DEFAULTS
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES_OPTIONS = {}
DATABASES_TEST = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
TEST_RUNNER = 'main.testing.DatabaselessTestRunner'

#------------------------------------------------------------------------------
#--- Caches
CACHES = {
    'default': {
        'BACKEND': CACHE_BACKEND,
        'LOCATION': CACHE_LOCATION,
        'KEY_PREFIX': CACHE_PREFIX
    }
}


#------------------------------------------------------------------------------
#--- Django Rest Framework
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_AUTHENTICATION_CLASSES' : [],
    'DEFAULT_PERMISSION_CLASSES' : [],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SESSION_COOKIE_NAME = 'polemap_sid'
CSRF_COOKIE_NAME = 'polemap_csrftoken'

#------------------------------------------------------------------------------
#--- django-extensions graph models
# https://django-extensions.readthedocs.io/en/latest/graph_models.html
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

#------------------------------------------------------------------------------
#--- ADMIN PANEL RESTRICTIONS
RESTRICT_ADMIN = getattr(params, 'RESTRICT_ADMIN', False)
ALLOWED_ADMIN_IPS = getattr(params, 'ALLOWED_ADMIN_IPS', ['127.0.0.1', '::1'])
ALLOWED_ADMIN_IP_RANGES = getattr(params, 'ALLOWED_ADMIN_IP_RANGES', ['127.0.0.0/24', '::/1'])
RESTRICTED_APP_NAMES = ['admin']
TRUST_PRIVATE_IP = getattr(params, 'TRUST_PRIVATE_IP', False)

#------------------------------------------
#--- Last line is just for testing purposes
LOADED_OK = 'OK'
