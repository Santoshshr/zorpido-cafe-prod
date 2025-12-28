from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from dotenv import load_dotenv

# Load .env if present — useful when deploying from a repo with an env file
load_dotenv()

# Production MUST be explicit
DEBUG = False

# SECRET_KEY must be provided via environment in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY environment variable is required in production')

# ALLOWED_HOSTS must be provided in environment for production.
# Use a comma-separated list: "example.com,www.example.com,1.2.3.4"
raw_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured('ALLOWED_HOSTS environment variable is required in production')

# Database: require DATABASE_URL in production (PostgreSQL)
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ImproperlyConfigured('DATABASE_URL environment variable is required in production')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Cloudinary: require credentials in production and use it as MEDIA storage
INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']

CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
if not (CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET):
    raise ImproperlyConfigured('Cloudinary credentials (CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET) are required in production')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Static file storage for production (compressed, hashed). collectstatic will
# produce filenames that WhiteNoise can serve; Nginx may be used to serve
# the static files from STATIC_ROOT in front of Gunicorn.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security headers and cookies
# When behind a reverse proxy (nginx) ensure this header is set so Django knows request is secure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True') == 'True'

# X-Content-Type-Options and other recommended headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins (comma-separated, include scheme e.g. https://example.com)
raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if raw_csrf:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in raw_csrf.split(',') if u.strip()]

# Logging: ensure errors are persisted for debugging server-side issues
LOGGING['handlers']['file']['filename'] = BASE_DIR / 'errors.log'
