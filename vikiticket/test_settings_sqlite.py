from settings import *
import os


DIRNAME = os.path.normpath(os.path.dirname(__file__))


# -----------------
# Database settings
# -----------------
DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',#'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'vikiticket_db',                      # Or path to database file if using sqlite3.
        'USER': '',#'vikiticket_u',                      # Not used with sqlite3.
        'PASSWORD': 'testing',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
