# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/'
)

# Application definition
DJANGO_APPS = (
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                )

THIRD_PARTY_APPS = (
                    'widget_tweaks',
                    'django_extensions',
                    'mathfilters',
                    )

OUR_APPS = (
                'ip_analysis',
                'health_check',
                'data_migration',
                'user_analysis',
                'aggregator_analysis',
            )

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OUR_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ssadmin.urls'

WSGI_APPLICATION = 'ssadmin.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Number of days delay in syncing db
SYNC_DELAY = 0

# Hourly data is collection information message,
# date format should be "YYYY-MM-DD"
# Format displayed in the message is "September 08, 2014"
HOURLY_DATE = '2014-09-08'

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)

ALLOWED_HOSTS = []

# SESSION Specific settings.

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE              = 720 * 60  # 12 Hours
SESSION_COOKIE_NAME             = "ssdbsession"


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins','file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
