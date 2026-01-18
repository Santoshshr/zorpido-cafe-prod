from .base import *
# Do NOT redefine BASE_DIR here; use BASE_DIR from base.py so path
# calculations (STATIC_ROOT, MEDIA_ROOT, etc.) remain consistent
# across environments. Removing any local override prevents missing
# or mis-pointed static/media directories which can break management
# commands like `collectstatic`.
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

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


DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL is not set")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}



# --------------------------
# STATIC FILES
# --------------------------
# Use the STATIC_* settings from base.py (BASE_DIR and defaults)
# Ensure WhiteNoise handles static files; Cloudinary is configured
# below only for media (DEFAULT_FILE_STORAGE).
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

# Cloudinary is used for MEDIA (uploads). Do not use Cloudinary as the
# STATICFILES_STORAGE; that would prevent `collectstatic` from managing
# static assets via WhiteNoise.
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
