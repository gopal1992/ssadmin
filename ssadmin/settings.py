"""
Django settings for ssadmin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from configurations import Configuration


class Dev(Configuration):
    DEBUG = True


class Production(Configuration):
    DEBUG = False
