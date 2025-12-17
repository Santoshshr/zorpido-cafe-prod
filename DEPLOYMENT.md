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

   7) Migrating data from local SQLite to PostgreSQL

       - The repository includes a helper script `scripts/migrate_sqlite_to_postgres.sh`.
       - Steps (local machine):

             ```bash
             # 1) Create a Postgres DB (e.g. on Render) and get the DATABASE_URL
             export DATABASE_URL="postgres://user:pass@host:5432/dbname"

             # 2) (optional) activate your virtualenv and install deps
             pip install -r requirements.txt

             # 3) Run the migration script from the repo root
             ./scripts/migrate_sqlite_to_postgres.sh
             ```

       - What the script does:
          - Dumps Django data from the current DB into `/tmp/zorpido_data.json` (excludes contenttypes, permissions, sessions).
          - Installs dependencies, runs `migrate` against the Postgres DB specified in `DATABASE_URL`, then runs `loaddata` to import the data.

       - Important notes:
          - Large or complex apps (custom fields, third-party apps storing binary blobs) may require manual adjustments to the fixture.
          - Admin users, passwords, and permissions will be preserved if included in the dump.
          - Always back up the source `db.sqlite3` before starting.
          - After a successful migration, remove `/tmp/zorpido_data.json` or store it securely.

