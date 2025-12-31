import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()  # load .env early so environment variables are available
except Exception:
    # If python-dotenv is not installed, direct envs should still work
    pass

# BASE_DIR is the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# In development a default may be present; in production the secret must be
# provided via the DJANGO_SECRET_KEY environment variable.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-secret-key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogs',
    'gallery',
    'loyalty',
    'website',
    'menu',
    'orders',
    'pos',
    'users',
    'utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zorpido_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'zorpido_config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Defaults for where collectstatic will place files and where uploaded media will live.
# Local settings will override these for developer convenience.
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# If this project uses a custom user model in `users` app, declare it here
AUTH_USER_MODEL = 'users.User'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '',  # will be set below so imports can override
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Ensure a logs directory exists and set a sensible default filename for the file handler.
try:
    LOGS_DIR = BASE_DIR / 'logs'
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if not LOGGING['handlers']['file'].get('filename'):
        LOGGING['handlers']['file']['filename'] = str(LOGS_DIR / 'errors.log')
except Exception:
    # If directory creation fails for any reason, fall back to using STDOUT handled elsewhere.
    pass


# Optional: import Cloudinary configuration helper. This is safe — the helper
# will not raise on missing environment variables and only logs informative
# messages. Use `zorpido_config.cloudinary.require_cloudinary()` in views that
# must ensure credentials are present.
try:
    # Importing the module runs `init_cloudinary()` but will not crash
    # the app if credentials are absent or the cloudinary package is not installed.
    from zorpido_config import cloudinary as cloudinary_config  # noqa: F401
except Exception:
    import logging as _logging

    _logging.getLogger(__name__).warning(
        'Could not import zorpido_config.cloudinary; Cloudinary integration will remain disabled.'
    )
