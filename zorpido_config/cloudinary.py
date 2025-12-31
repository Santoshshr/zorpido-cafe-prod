"""Cloudinary configuration helper.

This module reads Cloudinary credentials from environment variables and
initializes the `cloudinary` SDK in a safe, reusable way.

Behavior:
- Loads credentials from `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`,
  and `CLOUDINARY_API_SECRET` environment variables (or `CLOUDINARY_URL`).
- Works locally when a `.env` file is present (project's `settings.base` already
  calls `dotenv.load_dotenv()`).
- If the Cloudinary package is not installed, this module will mark Cloudinary
  as disabled and log a helpful message instead of raising during import.
- Provides `init_cloudinary()` to (re)initialize config, and
  `require_cloudinary()` helper to raise a clear error if credentials are
  required but missing.

Usage:
  from zorpido_config.cloudinary import init_cloudinary, require_cloudinary
  init_cloudinary()

  # In views when you need to ensure Cloudinary is configured
  require_cloudinary()  # raises ImproperlyConfigured with a clear message

"""
from __future__ import annotations

import logging
import os
from typing import Dict, Optional

from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

# Module-level flags/state
CLOUDINARY_ENABLED = False
CLOUDINARY_CONFIG: Dict[str, Optional[str]] = {
    'cloud_name': None,
    'api_key': None,
    'api_secret': None,
}


def _read_env() -> Dict[str, Optional[str]]:
    """Read Cloudinary credentials from the environment.

    Supports explicit env vars and the consolidated `CLOUDINARY_URL`.
    """
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME') or os.environ.get('CLOUDINARY_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')

    # If CLOUDINARY_URL is provided (cloudinary://key:secret@name), prefer it
    cloudinary_url = os.environ.get('CLOUDINARY_URL')
    if cloudinary_url and (not cloud_name or not api_key or not api_secret):
        # Let the cloudinary SDK parse CLOUDINARY_URL if available; still return
        # the explicit parts if present.
        return {
            'cloud_name': cloud_name,
            'api_key': api_key,
            'api_secret': api_secret,
            'cloudinary_url': cloudinary_url,
        }

    return {
        'cloud_name': cloud_name,
        'api_key': api_key,
        'api_secret': api_secret,
    }


def init_cloudinary() -> None:
    """Initialize the cloudinary SDK if credentials and package are available.

    This function is idempotent and safe to call from `settings.py`.
    It will not raise on missing env vars; instead it sets `CLOUDINARY_ENABLED`
    to False and logs a warning. When the app actually needs to upload images
    call `require_cloudinary()` to raise a clear ImproperlyConfigured error.
    """
    global CLOUDINARY_ENABLED, CLOUDINARY_CONFIG

    creds = _read_env()
    CLOUDINARY_CONFIG.update({
        'cloud_name': creds.get('cloud_name'),
        'api_key': creds.get('api_key'),
        'api_secret': creds.get('api_secret'),
    })

    try:
        import cloudinary
        # If CLOUDINARY_URL is set, cloudinary.config() will parse it automatically
        if creds.get('cloudinary_url'):
            cloudinary.config()  # uses env var
            CLOUDINARY_ENABLED = True
            logger.info('Cloudinary configured from CLOUDINARY_URL')
            return

        # Only configure explicitly if all three required parts are present
        if CLOUDINARY_CONFIG['cloud_name'] and CLOUDINARY_CONFIG['api_key'] and CLOUDINARY_CONFIG['api_secret']:
            cloudinary.config(
                cloud_name=CLOUDINARY_CONFIG['cloud_name'],
                api_key=CLOUDINARY_CONFIG['api_key'],
                api_secret=CLOUDINARY_CONFIG['api_secret'],
            )
            CLOUDINARY_ENABLED = True
            logger.info('Cloudinary configured from environment variables')
        else:
            CLOUDINARY_ENABLED = False
            logger.warning(
                'Cloudinary credentials not fully set. Set CLOUDINARY_CLOUD_NAME, '
                'CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET (or CLOUDINARY_URL) to enable Cloudinary.'
            )

    except Exception as exc:  # ImportError or cloudinary configuration errors
        CLOUDINARY_ENABLED = False
        logger.warning('Cloudinary package not available or failed to configure: %s', exc)


def require_cloudinary() -> None:
    """Raise a helpful error if Cloudinary is not configured.

    Use this in views or code paths that must access Cloudinary.
    """
    if not CLOUDINARY_ENABLED:
        # Build a helpful message distinguishing local vs production
        msg_lines = [
            'Cloudinary is not configured. To enable it, set the following environment variables:',
            '  - CLOUDINARY_CLOUD_NAME',
            '  - CLOUDINARY_API_KEY',
            '  - CLOUDINARY_API_SECRET',
            'Alternatively set CLOUDINARY_URL (cloudinary://API_KEY:API_SECRET@CLOUD_NAME).',
            '',
            'Local development: add these to your .env file (project already loads .env in settings).',
            'Production: set them in your host (cPanel / Render / server environment variables).',
        ]
        raise ImproperlyConfigured('\n'.join(msg_lines))


# Initialize at import so settings can import this module and have it ready.
# This is safe: init_cloudinary() will not raise if env vars are missing.
init_cloudinary()
