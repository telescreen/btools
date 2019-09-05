# -*- Coding: utf-8 -*-

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%j0#tdfz+!d$jmvm&i$(c9#+n!ozm*kqjlpir6&)1zfr0fyu)i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
    },
}


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'btools-development.sqlite3'
    }
}

## CELERY specific settings
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
