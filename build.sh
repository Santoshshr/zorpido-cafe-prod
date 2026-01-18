#!/usr/bin/env bash
set -euo pipefail

# Run from repository root
cd "$(dirname "$0")" || exit 1

# Ensure Render build uses production settings for collectstatic/migrate
# Respect existing DJANGO_SETTINGS_MODULE if the environment sets it.
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-zorpido_config.settings.production}

# Pick python
if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

# Install dependencies
"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements.txt

# Apply migrations and collect static files non-interactively
"$PY" manage.py migrate --noinput
"$PY" manage.py collectstatic --noinput
