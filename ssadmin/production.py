# -*- coding: utf-8 -*-

from .base_settings import *

## Production Base Settings
SECRET_KEY      =   'x8!)h@uc7o-&tz7j5rul)!s^w6&0p!b$(nqu5i@mt7#ql%d^^c'
ALLOWED_HOSTS   =   ['*']

## Database, Cache & Other Credentials

# MS SQL Server

DATABASES = {
     'default': {
         'ENGINE'   : 'sql_server.pyodbc',
         'NAME'     : 'Stag-admin-db',
         'USER'     : 'asdbadmin@pugq1r5ah8',
         'PASSWORD' : 'sqldb@123@Azure',
         'HOST'     : 'pugq1r5ah8.database.windows.net',
         'PORT'     : '',

         'OPTIONS': {
             # 'driver': 'SQL Server Native Client 11.0',
             # 'MARS_Connection': True,
             'dsn': 'ssadmindatasource',
          },
     }
}

# Redis
CACHES = {
    "default": {
        "BACKEND"   : "redis_cache.cache.RedisCache",
        "LOCATION"  : "localhost:6379:1",
        "OPTIONS": {
            "PASSWORD"              : "foopassword",
            "CLIENT_CLASS"          : "redis_cache.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {'max_connections': 100}
        }
    }
}


## Third Party Service Keys

# E-Mail Notification
MANDRILL_API_KEY    = "4GpVfZ7_NMoKxu_eSaO7yg"
EMAIL_HOST          = "smtp.mandrillapp.com"
EMAIL_PORT          = 587
EMAIL_HOST_USER     = "ss-admin@shieldsquare.com"
EMAIL_BACKEND       = "djrill.mail.backends.djrill.DjrillBackend"
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER


## Site Notifications

ADMINS = (
              ('Shield Square Support Team','django@shieldsquare.com'),
              ('Siva',      'siva@pydan.com'),
              ('Krace',     'krace@pydan.com'),
              ('Jagadesh',  'jagadesh@pydan.com'),
              ('Ganesh',    'ganesh@pydan.com'),
          )
