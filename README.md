# Zorpido Restaurant

This is a Django-based restaurant project (local copy).

Quick start

1. Create and activate a Python virtual environment

   Windows (cmd.exe):
   ```
   python -m venv env
   env\Scripts\activate
   ```

2. Install dependencies

   ```
   pip install -r requirements.txt
   ```

3. Run migrations and start server

   ```
   python manage.py migrate
   python manage.py runserver
   ```

Notes

- This repository currently has no remote. To upload to GitHub provide a repository URL (HTTPS or SSH) or install and authenticate GitHub CLI (`gh`).
- If you want me to create the remote and push, tell me whether you prefer `HTTPS` or `SSH`, or provide the target repo URL.
# worpido

## Local development (SQLite)

1. Copy the example env and edit secrets:

   ```bash
   cp .env.example .env
   # edit .env and set DJANGO_SECRET_KEY
   ```

2. Create and activate virtualenv and install deps:

   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Run migrations and start server (local SQLite):

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. Test server: open http://127.0.0.1:8000

## Git: safe merge workflow

Use the included script to safely rebase your branch onto `origin/main`, stash uncommitted changes, and push.

Run from repo root:

```bash
./scripts/git-safe-merge.sh [branch]
# if you omit [branch], it uses the current branch
```

If the rebase reports conflicts, resolve them and continue with:

```bash
git add <conflicted-files>
git rebase --continue
```

Notes:
- This script rebases your branch on top of `origin/main` (preferred for a linear history). If you prefer a merge-based approach, perform `git fetch origin` then `git merge origin/main` manually.
- The script will stash uncommitted changes and pop the stash after a successful rebase.

## Production (Render.com) setup

1. Add repository to GitHub and push main branch. Use the safe merge script before pushing to avoid surprises.

2. Create a Render Web Service (Python) and point it at your GitHub repo. Configure the following:

   - **Build command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start command**: `gunicorn zorpido_config.wsgi:application --bind 0.0.0.0:$PORT`
   - **Environment**: Add env vars (see `render.env.example`). Render will also provide a `DATABASE_URL` when you add a Postgres add-on.
   - **Release command** (important): `python manage.py migrate --noinput`

3. Enable automatic deploys on Render from your `main` branch.

## Commands quick-reference

- Run migrations locally: `python manage.py migrate`
- Run migrations on Render: add `python manage.py migrate --noinput` as the service Release Command
- Run tests: `python manage.py test`
- Push safely to GitHub:

  ```bash
  git checkout -b feature/your-change
  git add -A
  git commit -m "Your message"
  ./scripts/git-safe-merge.sh
  git push origin HEAD
  ```

## Do not commit local SQLite DB

`.gitignore` already excludes `db.sqlite3`. Ensure you do not add it accidentally:

```bash
git status --ignored
``` 

If you accidentally committed `db.sqlite3`, remove it from the repo history (careful):

```bash
git rm --cached db.sqlite3
git commit -m "Remove local sqlite database from repo"
git push origin main
```

## Environment variables

- Local: use `.env` in repo root (not committed). Example: see `.env.example`.
- Production/Render: set environment variables in the Render dashboard. Required:
  - `DJANGO_SECRET_KEY` (strong secret)
  - `ALLOWED_HOSTS` (comma-separated)
  - `DATABASE_URL` (Render provides this if you add a Postgres instance)
  - Cloudinary creds if using Cloudinary for media

## Common deployment errors & fixes

- Missing `DJANGO_SECRET_KEY` or `ALLOWED_HOSTS`: set the env vars in Render or the deploy will fail.
- Static files 404: ensure `python manage.py collectstatic --noinput` runs during build and `STATIC_ROOT` is configured; `whitenoise` is included for serving static files from Gunicorn during simple deployments.
- Database connection errors: ensure `DATABASE_URL` is set and Postgres allows connections from Render (if external). Prefer Render's managed Postgres add-on.

