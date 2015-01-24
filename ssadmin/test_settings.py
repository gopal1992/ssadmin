# -*- coding: utf-8 -*-

from .base_settings import *

SECRET_KEY      =   'x8!)h@uc7o-&tz7j5rul)!s^w6&0p!b$(nqu5i@mt7#ql%d^^c'

THIRD_PARTY_APPS += ('django_extensions', )

OUR_APPS += ('ssadmin_tests',)

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OUR_APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'test.db'),
     }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "localhost:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {'max_connections': 100}
        }
    }
}
