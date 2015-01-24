# -*- coding: utf-8 -*-

from .base_settings import *

THIRD_PARTY_APPS += ('django_extensions', )


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OUR_APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#      }
# }
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'ss2-sqldb',
        'USER': 'asdbadmin@pugq1r5ah8',
        'PASSWORD': 'sqldb@123@Azure',
        'HOST': 'pugq1r5ah8.database.windows.net',
        'PORT': '',

        'OPTIONS': {
            # 'driver': 'SQL Server Native Client 11.0',
        #     'MARS_Connection': True,
            'dsn': 'mssql',
         },
    }
}
