from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from dotenv import load_dotenv
load_dotenv()
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ADMINS: disable error emails in production (can be enabled if email is configured)
ADMINS = []

# SECRET_KEY must be provided via environment in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY environment variable is required in production')

# ALLOWED_HOSTS must be provided in environment for production. Accept comma-separated list.
# For Render, include the default domain: app-name.onrender.com
raw_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured('ALLOWED_HOSTS environment variable is required in production')

# CSRF trusted origins - comma-separated, include scheme (https://)
raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if raw_csrf:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in raw_csrf.split(',') if u.strip()]

# Database: Use dj-database-url for PostgreSQL via DATABASE_URL (Render sets this automatically)
# This supports both Render's managed PostgreSQL and any other PostgreSQL database
if os.environ.get('DATABASE_URL'):
            DATABASES = {
                'default': dj_database_url.config(
                    default='sqlite:///db.sqlite3',
                    conn_max_age=600,
                    ssl_require=True
                )
            }



# ============================================================================
# STATIC FILES CONFIGURATION FOR RENDER
# ============================================================================
# WhiteNoise is already in MIDDLEWARE (from base.py) and handles static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================================
# MEDIA FILES CONFIGURATION
# ============================================================================
# Use Cloudinary for media if configured, otherwise use filesystem
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# ============================================================================
# CLOUDINARY CONFIGURATION (OPTIONAL)
# ============================================================================
# Cloudinary for media is optional in production; fall back to local filesystem if not configured.
# If not provided, fall back to filesystem storage.
cloud_url = os.environ.get('CLOUDINARY_URL')

if cloud_url:
    # When CLOUDINARY_URL is provided, the cloudinary storage backend will parse it.
    INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']
    CLOUDINARY_STORAGE = {'CLOUDINARY_URL': cloud_url}
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Fall back to filesystem storage if Cloudinary is not configured
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# ============================================================================
# SECURITY CONFIGURATION FOR RENDER
# ============================================================================
# When behind a reverse proxy (Render uses this), trust X-Forwarded-Proto header
# This ensures HTTPS detection works correctly
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Enforce HTTPS in production
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'

# Secure cookies
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'

# HSTS (HTTP Strict Transport Security) - tells browsers to only use HTTPS
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True') == 'True'

# Additional security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ============================================================================
# LOGGING CONFIGURATION FOR RENDER
# ============================================================================
# Log errors to file (if logs directory is writable) and to console (for Render logs)
LOGGING['handlers']['file']['filename'] = str(BASE_DIR / 'logs' / 'errors.log')

# Also log errors to console for debugging in production (visible in Render logs)
LOGGING['handlers']['console'] = {
    'level': 'ERROR',
    'class': 'logging.StreamHandler',
}
LOGGING['loggers']['django']['handlers'].append('console')
