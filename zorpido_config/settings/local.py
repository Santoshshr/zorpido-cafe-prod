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
# Local development: load .env (base.py already calls load_dotenv). Cloudinary
# is optional locally — developers can add credentials to `.env` to test.
try:
    # Import our helper which attempts to initialize cloudinary safely.
    from zorpido_config import cloudinary as cloudinary_config  # noqa: F401

    if cloudinary_config.CLOUDINARY_ENABLED:
        # If the SDK was initialized and credentials are present, enable apps
        INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']
        # Configure Django to use Cloudinary for media files in local dev
        DEFAULT_FILE_STORAGE = os.environ.get(
            'DEFAULT_FILE_STORAGE', 'cloudinary_storage.storage.MediaCloudinaryStorage'
        )
    else:
        # Keep filesystem storage locally when Cloudinary is not configured
        DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
except Exception:
    # If something goes wrong importing the helper, fall back to filesystem.
    DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')

# Comment: Use this settings file for local development only.

# Create logs dir if not present to avoid startup errors when logging to file
try:
    (BASE_DIR / 'logs').mkdir(parents=True, exist_ok=True)
except Exception:
    pass
