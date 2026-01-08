"""
Cloudinary integration helper for Zorpido.

This module provides safe Cloudinary configuration that won't crash the app
if credentials are missing. It initializes Cloudinary on import and provides
utilities for checking configuration.
"""

import os
import logging
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

# Track if Cloudinary is properly configured
_cloudinary_configured = None


def init_cloudinary():
    """
    Initialize Cloudinary configuration from environment variables.

    This function is called automatically when the module is imported.
    It will not raise exceptions if configuration is missing, but will
    log warnings and disable Cloudinary integration.
    """
    global _cloudinary_configured

    try:
        import cloudinary
        from cloudinary import config

        # Try to configure from environment variables
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        cloudinary_url = os.environ.get('CLOUDINARY_URL')

        if cloudinary_url:
            # Use the URL if provided
            config(cloudinary_url=cloudinary_url)
            _cloudinary_configured = True
            logger.info("Cloudinary configured via CLOUDINARY_URL")
        elif cloud_name and api_key and api_secret:
            # Use individual environment variables
            config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            _cloudinary_configured = True
            logger.info("Cloudinary configured via environment variables")
        else:
            _cloudinary_configured = False
            logger.warning(
                "Cloudinary not configured. Set CLOUDINARY_URL or "
                "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET"
            )

    except ImportError:
        _cloudinary_configured = False
        logger.warning("Cloudinary package not installed")
    except Exception as e:
        _cloudinary_configured = False
        logger.warning(f"Failed to configure Cloudinary: {e}")


def require_cloudinary():
    """
    Ensure Cloudinary is properly configured.

    Raises ImproperlyConfigured if Cloudinary is not available.
    Use this in views or code paths that require Cloudinary.
    """
    if _cloudinary_configured is None:
        init_cloudinary()

    if not _cloudinary_configured:
        raise ImproperlyConfigured(
            "Cloudinary is not configured. Set CLOUDINARY_URL or "
            "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET"
        )


def is_cloudinary_enabled():
    """
    Check if Cloudinary is enabled and configured.

    Returns True if Cloudinary is available, False otherwise.
    """
    if _cloudinary_configured is None:
        init_cloudinary()
    return _cloudinary_configured


# Initialize Cloudinary when the module is imported
init_cloudinary()