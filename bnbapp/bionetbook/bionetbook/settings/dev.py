import sys
from base import *

# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

# git push git@heroku.com:bnbapp.git master

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'database.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'db_name',                      
#         'USER': 'db_user',
#         'PASSWORD': 'db_user_password',
#         'HOST': ''
#     }
# }


# ATTEMPT TO FORCE AN IN-MEMORY DB CREATION
# if 'test' in sys.argv:
#     DATABASES['default']['NAME'] = ':memory:'


REGISTRATION_ENABLED = False

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

DEV_APPS = (
    'stubtools',
    'debug_toolbar',
    'django_coverage',
)

INSTALLED_APPS = INSTALLED_APPS + DEV_APPS

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bionetbook',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
"""

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

