#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

This manage.py defaults to using the local settings module for development
but respects an existing DJANGO_SETTINGS_MODULE environment variable.
It also attempts to load a local `.env` file if python-dotenv is installed.
"""
import os
import sys
import traceback
from pathlib import Path


def main():
    BASE_DIR = Path(__file__).resolve().parent

    try:
        from dotenv import load_dotenv
    except Exception:
        load_dotenv = None

    if load_dotenv:
        dotenv_path = BASE_DIR / '.env'
        if dotenv_path.exists():
            try:
                load_dotenv(dotenv_path)
            except Exception:
                # If loading fails, continue but print a warning
                print('Warning: failed to load .env file', file=sys.stderr)

    # Default to local settings when DJANGO_SETTINGS_MODULE not provided
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'zorpido_config.settings.local'))

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except Exception:
        # Print full traceback to stderr so startup errors are visible (not silent)
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()
