# Render.com Deployment Guide for Zorpido Web

This document outlines how to deploy the Zorpido Django application to Render.com using a managed PostgreSQL database.

## Prerequisites

- Render.com account (free tier available)
- Git repository with all code
- Domain name (optional, can use Render's default domain)

## Deployment Steps

### 1. Prepare the Repository

Ensure all changes are committed to git:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy via render.yaml (Recommended)

**Option A: Using the render.yaml file (Automatic)**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New" → "Blueprint"**
3. Connect your GitHub repository
4. Select the `render.yaml` file
5. Review the services configuration
6. Click **"Create New Services"**

Render will automatically:
- Create a PostgreSQL database
- Deploy the web service
- Run migrations (`python manage.py migrate`)
- Collect static files (`python manage.py collectstatic`)
- Start the gunicorn web server

**Option B: Manual Service Creation**

If not using `render.yaml`, create services manually:

#### Step 2a: Create PostgreSQL Database

1. Go to **Databases → New Database**
2. Select **PostgreSQL**
3. Configure:
   - **Name:** `zorpido-postgres`
   - **Database:** `zorpido_db`
   - **User:** `zorpido_user`
   - **Region:** Choose your region
   - **Plan:** Free tier (or paid)
4. Click **Create Database**
5. Copy the connection string (DATABASE_URL)

#### Step 2b: Create Web Service

1. Go to **Web Services → New Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `zorpido-web`
   - **Runtime:** Python 3.11
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     python manage.py collectstatic --noinput
     python manage.py migrate --noinput
     ```
   - **Start Command:**
     ```bash
     gunicorn zorpido_config.wsgi:application --workers 3 --bind 0.0.0.0:$PORT --log-file -
     ```
   - **Region:** Same as database
   - **Plan:** Free tier (or paid)

### 3. Set Environment Variables

In the **Environment** section of the web service, add:

```
DJANGO_SETTINGS_MODULE=zorpido_config.settings.production
DEBUG=False
DJANGO_SECRET_KEY=<generate-a-random-key>
ALLOWED_HOSTS=<your-app>.onrender.com,your-domain.com
CSRF_TRUSTED_ORIGINS=https://<your-app>.onrender.com,https://your-domain.com
DATABASE_URL=<automatically-set-from-database-connection>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

#### Generate a Secure Django Secret Key

Run this command locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as `DJANGO_SECRET_KEY` in Render.

### 4. Connect the Database to the Web Service

1. Go to your web service settings
2. Under **Environment**, add `DATABASE_URL` as a reference to the PostgreSQL service:
   - Key: `DATABASE_URL`
   - Value: Select the PostgreSQL service connection

Or manually add the PostgreSQL connection string if available.

### 5. Deploy

1. Click **Deploy** on the web service
2. Monitor the deployment logs in the **Logs** tab
3. Wait for "Build successful" message

### 6. Verify Deployment

1. Visit your app URL: `https://<your-app>.onrender.com`
2. Check for any errors in the **Logs** tab
3. Test key functionality:
   - Admin panel: `/admin/`
   - API endpoints
   - Static files loading
   - Database connectivity

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `DJANGO_SETTINGS_MODULE` | Points to production settings | `zorpido_config.settings.production` |
| `DEBUG` | Must be False in production | `False` |
| `DJANGO_SECRET_KEY` | Django secret key for security | Long random string |
| `ALLOWED_HOSTS` | Allowed domain names | `app.onrender.com,example.com` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |
| `SESSION_COOKIE_SECURE` | HTTPS-only session cookies | `True` |
| `CSRF_COOKIE_SECURE` | HTTPS-only CSRF cookies | `True` |
| `SECURE_HSTS_SECONDS` | HSTS duration in seconds | `31536000` (1 year) |
| `CLOUDINARY_URL` | Cloudinary media storage (optional) | `cloudinary://key:secret@cloud` |

## Troubleshooting

### Build Fails: "Module not found"

- Check `requirements.txt` is in the root directory
- Ensure all dependencies are listed
- Re-run: `pip install -r requirements.txt` locally to test

### Database Connection Error

- Verify `DATABASE_URL` environment variable is set
- Check PostgreSQL service is running
- Ensure database credentials are correct
- Check ALLOWED_HOSTS includes the Render domain

### Static Files Not Loading

- Run locally: `python manage.py collectstatic --noinput`
- Verify `STATIC_ROOT` and `STATIC_URL` are configured correctly
- Check WhiteNoise is in MIDDLEWARE
- Look for 404 errors in logs

### Admin Panel Not Working

- Run: `python manage.py createsuperuser` (after connecting to production database)
- Verify media files path configuration

### HTTPS/SSL Issues

- Ensure `SECURE_SSL_REDIRECT=True`
- Check `SECURE_PROXY_SSL_HEADER` is set correctly
- Wait 5-10 minutes for SSL certificate to be issued

## Accessing Production Database

### Via Render Dashboard

1. Go to your PostgreSQL service
2. Click **Connect**
3. Use the connection string in your database client

### Via psql (Command Line)

```bash
psql <DATABASE_URL>
```

### Running Django Management Commands

In the **Shell** tab of your web service:

```bash
python manage.py createsuperuser
python manage.py migrate --noinput
python manage.py shell
```

## Auto-Deployment

If using `render.yaml`:
- Deployments trigger automatically on git push to `main` branch
- Modify `autoDeploy: false` in `render.yaml` to disable

## Scaling and Optimization

### For Free Tier

- Limited to 1 instance
- Auto-pauses after 15 minutes of inactivity
- Database query limits

### For Paid Plans

1. Increase workers in Procfile
2. Upgrade instance size
3. Enable auto-scaling
4. Use Redis for caching

## Media Files (Uploads)

### Option 1: Render's Disk Storage (Default)

- Media files stored on `/var/data` directory
- Survives container redeploys
- Suitable for small volumes

### Option 2: Cloudinary (Recommended)

For production, consider Cloudinary for reliable media hosting:

1. Sign up at [Cloudinary](https://cloudinary.com)
2. Get `CLOUDINARY_URL` from account settings
3. Add to Render environment variables
4. Django will automatically use Cloudinary for uploads

## Production Checklist

- [ ] `DEBUG=False`
- [ ] `DJANGO_SECRET_KEY` is set and random
- [ ] `ALLOWED_HOSTS` includes all expected domains
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] Database is PostgreSQL (not SQLite)
- [ ] Migrations have run successfully
- [ ] Static files collected
- [ ] Email configuration tested
- [ ] Error logging configured
- [ ] Backup strategy in place (for database)
- [ ] CORS headers configured if needed
- [ ] Media storage solution chosen (Cloudinary or disk)

## Support and Resources

- [Render Documentation](https://docs.render.com)
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [dj-database-url](https://github.com/jacobian/dj-database-url)

## Next Steps

1. Test the deployment thoroughly
2. Set up monitoring and error tracking (e.g., Sentry)
3. Configure email backend for production
4. Set up regular database backups
5. Monitor resource usage and plan scaling

---

**Last Updated:** January 15, 2026  
**Django Version:** 4.2.27  
**Python Version:** 3.9+
