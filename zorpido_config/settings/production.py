from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# Production must be explicit
DEBUG = False

# SECRET_KEY must be provided via environment in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY environment variable is required in production')

# ALLOWED_HOSTS must be provided in environment for production. Accept comma-separated list.
raw_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured('ALLOWED_HOSTS environment variable is required in production')

# CSRF trusted origins - comma-separated, include scheme (https://)
raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if raw_csrf:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in raw_csrf.split(',') if u.strip()]

# Database: require DATABASE_URL in production (Postgres or MySQL)
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ImproperlyConfigured('DATABASE_URL environment variable is required in production')

# Parse the DATABASE_URL and set a reasonable connection age to reuse connections
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=int(os.environ.get('CONN_MAX_AGE', 600)))
}

# Static and media
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Use WhiteNoise for static file serving unless another storage is configured
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'whitenoise.storage.CompressedManifestStaticFilesStorage')

# Cloudinary for media is optional in production; fall back to local filesystem if not configured.
cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
cloud_key = os.environ.get('CLOUDINARY_API_KEY')
cloud_secret = os.environ.get('CLOUDINARY_API_SECRET')
if cloud_name and cloud_key and cloud_secret:
    INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': cloud_name,
        'API_KEY': cloud_key,
        'API_SECRET': cloud_secret,
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Default to filesystem media storage in production when Cloudinary isn't configured
    DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')

# Security headers and cookies
# When behind a reverse proxy (Passenger/Apache), ensure this header is set if your proxy sets it
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True') == 'True'

# Recommended headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Ensure logging writes to production logs (base already set a default; override here if needed)
LOGGING['handlers']['file']['filename'] = str(BASE_DIR / 'logs' / 'errors.log')
