from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# Production must be explicit
DEBUG = False

# ADMINS: disable error emails in production (can be enabled if email is configured)
ADMINS = []

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "zorpido_web_db"),
        "USER": os.environ.get("DB_USER", "zorpido_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "Zorpido_web_db@1"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}



# Static and media
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Use WhiteNoise for static file serving unless another storage is configured
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'whitenoise.storage.CompressedManifestStaticFilesStorage')

# Cloudinary for media is optional in production; fall back to local filesystem if not configured.
# Cloudinary configuration (production): prefer explicit environment variables.
# If not provided, fall back to filesystem storage.
cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
cloud_key = os.environ.get('CLOUDINARY_API_KEY')
cloud_secret = os.environ.get('CLOUDINARY_API_SECRET')
cloud_url = os.environ.get('CLOUDINARY_URL')

if cloud_url:
    # When CLOUDINARY_URL is provided the cloudinary storage backend will parse it.
    INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']
    CLOUDINARY_STORAGE = {'CLOUDINARY_URL': cloud_url}
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
elif cloud_name and cloud_key and cloud_secret:
    # Use individual environment variables if all are provided
    INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': cloud_name,
        'API_KEY': cloud_key,
        'API_SECRET': cloud_secret,
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Fall back to filesystem storage if Cloudinary is not configured
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

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

# Also log errors to console for debugging in production
LOGGING['handlers']['console'] = {
    'level': 'ERROR',
    'class': 'logging.StreamHandler',
}
LOGGING['loggers']['django']['handlers'].append('console')
