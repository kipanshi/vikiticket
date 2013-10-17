# -*- coding: utf-8 -*-
# Django settings for vikiticket project.

import os

gettext = lambda s: s

DIRNAME = os.path.normpath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERVE_STATIC_FILES = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS + (
    # ('Your Name', 'your_email@example.com'),
)

AUTH_PROFILE_MODULE = 'core.UserProfile'

# --------------
# Email settings
# --------------
EMAIL_SUBJECT_PREFIX = '[Vikiticket] '


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'vikiticket_db', # Or path to database file if using sqlite3.
        'USER': 'vikiticket_u', # Not used with sqlite3.
        'PASSWORD': 'di2GaR89vc', # Not used with sqlite3.
        'HOST': 'postgresql.alwaysdata.com', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(DIRNAME, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(DIRNAME, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = 'http://dartz.spb.ru/vikiticket/static/'
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = 'http://dartz.spb.ru/vikiticket/static/admin/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3=c3a*qlibjfl=-9hx-rv_cc)^p+$34b7-x8@p+j60lb)b!a68'

# -------------
# Site settings
# -------------
SITE_ID = 1
SITE_URL = 'please, set proper url in local_settings.py'

# -----------------
# Template settings
# -----------------
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

BASE_MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

LOCAL_MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'vikiticket.urls'

# -----------------------
# Installed apps settings
# -----------------------
BASE_INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # External apps
    'tinymce',
    'south',
    # Custom apps
    'core',
)

LOCAL_INSTALLED_APPS = ()

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

#------------------#
# Tinymce settings #
#------------------#

#TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'mode': "textareas",
    'theme': "advanced",
#    'content_css' = "/appmedia/blog/style.css",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_buttons1': "fullscreen,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,media,cleanup,help,separator,code",
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'auto_cleanup_word': True,
    'plugins': "table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,searchreplace,print,contextmenu,fullscreen,media",
    'plugin_insertdate_dateFormat': "%m/%d/%Y",
    'plugin_insertdate_timeFormat': "%H:%M:%S",
    'extended_valid_elements': "a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style|frame|frameset|rel]",
    'fullscreen_settings': {
        'theme_advanced_path_location': "top",
        'theme_advanced_buttons1': "fullscreen,separator,preview,separator,media,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
        'theme_advanced_buttons2': "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
        'theme_advanced_buttons3': "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
    },
    'advimage_update_dimensions_onchange': True,
    'auto_cleanup_word': True,
    'dialog_type': 'modal',
    'object_resizing': True,
    'cleanup_on_startup': True,
    'forced_root_block': 'p',
    'remove_trailing_nbsp': True,
    'height': '350',
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'vikiticket@gmail.com'
EMAIL_HOST_PASSWORD = '55isourtrain'
DEFAULT_FROM_EMAIL = 'vikiticket@gmail.com'

# Try to load local settings
try:
    from local_settings import *
except ImportError:
    pass

INSTALLED_APPS = BASE_INSTALLED_APPS + LOCAL_INSTALLED_APPS
MIDDLEWARE_CLASSES = BASE_MIDDLEWARE_CLASSES + LOCAL_MIDDLEWARE_CLASSES

#============================
# VikiTicket Pages Settings 
#============================

VIKITICKET_PAGES = (
    ('read', gettext(u'Почитать'), 1),    # slug, title, ordering
    ('watch', gettext(u'Посмотреть'), 2),
    ('listen', gettext(u'Послушать'), 3),
)

VIKITICKET_STAGE = (
    5, 17, gettext(u'Стоячий партер'),  # Number of rows, number of seats, placement name,
    'yellow', 300             # Price category color, price
)

