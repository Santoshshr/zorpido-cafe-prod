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

# Ensure logging writes to a local file so the logging config's file handler
# can be configured in development (prevents errors when filename is empty).
LOGGING['handlers']['file']['filename'] = str(BASE_DIR / 'logs' / 'errors.log')

# Cloudinary is not used locally
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'cloudinary']

# Comment: Use this settings file for local development only.

# Create logs dir if not present to avoid startup errors when logging to file
try:
    (BASE_DIR / 'logs').mkdir(parents=True, exist_ok=True)
except Exception:
    pass
