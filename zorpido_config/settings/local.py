from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles-dev'

# Cloudinary is not used locally
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'cloudinary']

# Comment: Use this settings file for local development only.
