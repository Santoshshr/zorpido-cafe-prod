#!/usr/bin/env bash
set -euo pipefail

# Build script for Render (or CI) — run migrations and collectstatic
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build script finished"
