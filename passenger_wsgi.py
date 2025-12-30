"""
Passenger WSGI entrypoint for shared hosting (cPanel / Passenger).

This file ensures the production settings module is used by default when
Passenger launches the Python application. It mirrors the standard Django
WSGI entrypoint but is placed at the project root where cPanel/Passenger
expects to find it.
"""
import os
from django.core.wsgi import get_wsgi_application

# Default to production settings for hosted deployments; the host can override
# DJANGO_SETTINGS_MODULE if needed via the control panel environment.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'zorpido_config.settings.production'))

application = get_wsgi_application()
