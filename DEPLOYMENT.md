# Deploying Zorpido to Render (short notes)

1) Add a PostgreSQL database on Render
   - In the Render dashboard choose "New" → "Postgres Database" and create a database (starter/ free plan is fine for testing).
   - After creation, Render provides a `DATABASE_URL` connection string.

2) Create / set environment variables in your Render Web Service
   - In the service's "Environment" / "Variables" section set:
     - `SECRET_KEY` → a long random string
     - `DATABASE_URL` → the connection string from the Postgres add-on (or your external Postgres)
     - `DEBUG` → `False`
     - (optional) `ALLOWED_HOSTS` → comma separated hostnames (if you want to lock hosts)

   Render sets `RENDER_EXTERNAL_HOSTNAME` automatically; the settings file will include it in `ALLOWED_HOSTS`.

3) Build & start commands
   - The provided `render.yaml` uses:
       - `buildCommand`: `pip install -r requirements.txt`
       - `startCommand`: `gunicorn zorpido_config.wsgi --log-file -`
   - You can also configure your service to run `scripts/build.sh` as a pre-deploy step to run migrations and collectstatic.

4) Running initial migrations and creating a superuser
   - To run migrations (if not done by build step): in Render's dashboard you can open a shell and run:

       ```bash
       python manage.py migrate
       python manage.py createsuperuser
       ```

   - Alternatively, run the commands locally against the production DB (use caution).

5) Static files
   - `collectstatic` writes static files to `STATIC_ROOT` and WhiteNoise serves them. Ensure `STATICFILES_STORAGE` is set to `whitenoise.storage.CompressedManifestStaticFilesStorage` (already configured in `settings.py`).

6) Notes
   - Ensure `requirements.txt` contains `psycopg2-binary` and `dj-database-url` (already provided).
   - Keep local `.env` files out of source control; use Render env vars for production secrets.
