Production readiness checklist

- Required environment variables (set in your host/service):
  - `DJANGO_SECRET_KEY` (required) — a long random secret.
  - `DATABASE_URL` (required in production) — Postgres connection string.
  - `ALLOWED_HOSTS` (required) — comma-separated hostnames.
  - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` (if using Cloudinary for media).
  - Optional toggles: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `CSRF_TRUSTED_ORIGINS`.

- Commands to prepare and run on the server (example using virtualenv):

```bash
# activate env
source env/bin/activate

# install production deps
pip install -r requirements-prod.txt

# export settings to production (set in environment in most hosts)
export DJANGO_SETTINGS_MODULE=zorpido_config.settings.production

# run migrations
python manage.py migrate --noinput

# collect static files
python manage.py collectstatic --noinput

# create superuser (interactive) if needed
python manage.py createsuperuser

# run gunicorn (Procfile used by platform like Render or Heroku)
gunicorn zorpido_config.wsgi:application --workers 3 --bind 0.0.0.0:8000 --log-file -
```

- Notes:
  - `zorpido_config/settings/production.py` already enforces `DEBUG=False` and raises errors when required env vars are missing to fail-fast in production.
  - `Procfile` starts Gunicorn; the platform should set `PORT` and provide the `DATABASE_URL` service.
  - Do not commit secrets to the repository. Use your host's environment settings or a secrets store.

- Quick platform tips:
  - Render: add a Postgres service and the app will get `DATABASE_URL` automatically; set the other env vars in the service dashboard.
  - VPS: use a systemd service file (see README_DEPLOYMENT.md) and ensure `EnvironmentFile` points to a `.env` with production values (permissions restricted).
