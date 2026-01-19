#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput --settings=zorpido_config.settings.production
python manage.py migrate --noinput --settings=zorpido_config.settings.production