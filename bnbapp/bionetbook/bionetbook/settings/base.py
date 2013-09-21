# Django settings for bionetbook project.

import os.path
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if 'bionetbook/bionetbook' in PROJECT_ROOT:
    PROJECT_ROOT = PROJECT_ROOT.replace('bionetbook/bionetbook', 'bionetbook')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Grant Viklund', 'gviklund@backcode.com'),
    ('Oren Schaedel', 'oren@bionetbook.com'),
    ('Andrew Mori', 'andrewmori@backcode.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+@6q$m-n3aj^@h*1(ct2hs#hzym@phrc4ylg0x)o^kf^2g&8mo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'profiletools.middleware.LazyProfileMiddleware',
    'profiles.middleware.ConfirmProfile',
    'protocols.middleware.ProtocolSetup',
    'protocols.middleware.ProtocolAccess',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'profiletools.context_processors.fetch_profile',
    'core.context_processors.registration_enabled',
]

ROOT_URLCONF = 'bionetbook.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bionetbook.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

BASE_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #'gunicorn',
    'django_extensions',
    'south',
    'crispy_forms',
    'floppyforms',
    'braces',
    'registration',
    'profiletools',
    'django_wysiwyg',
)

PROJECT_APPS = (
    'core',
    'protocols',
    'profiles',
    'schedule',
    'interest',
    'api',
    'compare',
    'organization',
    'workflow',
    'feedback',
    'experiment',
    'history'
)

INSTALLED_APPS = BASE_APPS + PROJECT_APPS

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
        # 'console':{
        #     'level':'INFO',
        #     'class':'logging.StreamHandler',
        #     'stream': sys.stdout
        # },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },

    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

FIXTURE_DIRS = (
   #'/Users/Oren/Coding/bionetbook/bnbapp/bionetbook/fixtures/',
)

EMAIL_SUBJECT_PREFIX = '[bionetbook]'

# DO MEMCACHE
# from memcacheify import memcacheify
# CACHES = memcacheify()
# CACHE_COUNT_TIMEOUT = 60  # seconds, not too long.

REGISTRATION_ENABLED = False

# django-registration
ACCOUNT_ACTIVATION_DAYS = 3

CRISPY_TEMPLATE_PACK = 'bootstrap'

THUMBNAIL_DEBUG = True


LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/login/'

AUTH_PROFILE_MODULE = 'profiles.Profile'

DJANGO_WYSIWYG_FLAVOR = 'ckeditor'
DJANGO_WYSIWYG_MEDIA_URL = '%sckeditor/' % STATIC_URL


