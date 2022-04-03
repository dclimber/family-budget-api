from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '..' / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / '..' / 'sent-emails'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
