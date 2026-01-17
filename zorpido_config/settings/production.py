from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from pathlib import Path

# Load .env only for local dev (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --------------------------
# DEBUG / SECRET
# --------------------------
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY environment variable is required in production")

# --------------------------
# ALLOWED_HOSTS
# --------------------------
raw_allowed = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(",") if h.strip()]

if not ALLOWED_HOSTS:
    if not DEBUG:
        raise ImproperlyConfigured("ALLOWED_HOSTS environment variable must be set in production")
    else:
        ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CSRF trusted origins
raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if raw_csrf:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in raw_csrf.split(',') if u.strip()]

# --------------------------
# DATABASES
# --------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Get DATABASE_URL from environment
# Configure DATABASES unconditionally using dj-database-url.
# This ensures `ENGINE` is always present; when `DATABASE_URL` is set
# a PostgreSQL config will be returned, otherwise we fall back to SQLite.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{}'.format(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# --------------------------
# STATIC FILES
# --------------------------
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------
# MEDIA / CLOUDINARY
# --------------------------
cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
api_key = os.environ.get('CLOUDINARY_API_KEY')
api_secret = os.environ.get('CLOUDINARY_API_SECRET')

if not (cloud_name and api_key and api_secret):
    raise ImproperlyConfigured("Cloudinary environment variables are required in production")

INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': cloud_name,
    'API_KEY': api_key,
    'API_SECRET': api_secret
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --------------------------
# SECURITY
# --------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True') == 'True'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# --------------------------
# LOGGING
# --------------------------
LOGGING['handlers']['console'] = {
    'level': 'ERROR',
    'class': 'logging.StreamHandler',
}
LOGGING['loggers']['django']['handlers'] = ['console']
