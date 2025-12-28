Zorpido Web — Deployment Guide (Hostinger VPS)

This document describes steps to deploy the Django app to a Linux VPS using Gunicorn, Nginx, systemd, PostgreSQL, and Cloudinary for media.

Prerequisites (on VPS):
- Ubuntu 20.04+ or similar
- Python 3.10+ and virtualenv
- PostgreSQL server
- Nginx
- Git

1) Create system user and install system packages

```bash
sudo adduser --disabled-password --gecos '' zorpido
sudo apt update && sudo apt install -y python3-venv python3-pip build-essential libpq-dev nginx git
```

2) Clone repo and create virtualenv

```bash
git clone <repo> /home/zorpido/zorpido
cd /home/zorpido/zorpido
python3 -m venv env
source env/bin/activate
pip install -r requirements-prod.txt
```

3) Environment variables
- Copy `.env.example` to `.env` and fill in secrets (DO NOT commit)

```bash
cp .env.example .env
# edit .env and set real values
```

4) Database
- Create Postgres DB and user, then set `DATABASE_URL` in `.env`.
- Run migrations and collectstatic

```bash
source env/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

5) Gunicorn systemd service example (`/etc/systemd/system/zorpido.service`)

```
[Unit]
Description=gunicorn daemon for Zorpido
After=network.target

[Service]
User=zorpido
Group=www-data
WorkingDirectory=/home/zorpido/zorpido
EnvironmentFile=/home/zorpido/zorpido/.env
ExecStart=/home/zorpido/zorpido/env/bin/gunicorn zorpido_config.wsgi:application \
    --workers 3 \
    --bind unix:/run/zorpido.sock

Restart=always

[Install]
WantedBy=multi-user.target
```

Reload systemd and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now zorpido
```

6) Nginx site example (`/etc/nginx/sites-available/zorpido`)

```
server {
    listen 80;
    server_name example.com www.example.com 1.2.3.4;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/zorpido/zorpido/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/zorpido.sock;
    }
}
```

Enable and test Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/zorpido /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7) SSL (recommended)
- Use Certbot to obtain certificates and set up auto-renewal

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

8) Common troubleshooting
- Gunicorn fails: check `journalctl -u zorpido` and `sudo systemctl status zorpido`.
- Nginx 502: check socket path and permissions; ensure Gunicorn is running and creating `/run/zorpido.sock`.
- Static files not found: confirm `collectstatic` ran and `STATIC_ROOT` exists.
- Missing env var errors: the application will raise `ImproperlyConfigured` to fail loudly; ensure `.env` is loaded and systemd `EnvironmentFile` points to the `.env`.

Final notes:
- Do not store secrets in source control.
- Ensure `DJANGO_SECRET_KEY`, `DATABASE_URL`, and Cloudinary credentials are set in production.
- The project uses Cloudinary for media; uploaded images will be served from the Cloudinary CDN.
