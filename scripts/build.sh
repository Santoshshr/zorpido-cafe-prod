#!/bin/bash
# Build script for Render.com deployment
# This script is called by Render's build process

set -e  # Exit on error

echo "=== Installing Dependencies ==="
pip install -r requirements.txt

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput --clear

echo "=== Running Database Migrations ==="
python manage.py migrate --noinput

echo "=== Build Complete ==="
echo "Static files collected to: $(python manage.py shell -c 'from django.conf import settings; print(settings.STATIC_ROOT)')"
echo "Ready for deployment!"
