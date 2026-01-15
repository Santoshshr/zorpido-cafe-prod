# Quick Start: Deploy to Render in 5 Minutes

> **TL;DR** - Your Zorpido Web app is ready to deploy to Render.com! Follow these 5 steps.

## Prerequisites
- GitHub account with repo pushed
- Render.com account (free)
- PostgreSQL connection string or Render's managed database

---

## 🚀 Deploy Now (5 Steps)

### Step 1: Generate Django Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**Copy the output** - you'll need it in Step 3.

---

### Step 2: Push Code to GitHub
```bash
cd /Users/santoshshrestha/Downloads/Zorpido_web
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

---

### Step 3: Deploy via Render Blueprint

1. **Go to:** https://dashboard.render.com
2. **Click:** "New" → "Blueprint"
3. **Select:** Your GitHub repository
4. **Branch:** `main` (default)
5. **Review** the configuration from `render.yaml`
6. **Click:** "Create New Services"
7. **Wait:** 5-10 minutes for build and deployment

---

### Step 4: Set Environment Variables

After services are created, add these in Render dashboard:

**In your Web Service → Environment:**

```
DJANGO_SECRET_KEY=<paste-from-step-1>
ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com,https://your-domain.com
```

*(Leave other variables as-is, DATABASE_URL is auto-set)*

---

### Step 5: Verify It Works

1. **Visit your app:** `https://your-app.onrender.com`
2. **Check admin:** `https://your-app.onrender.com/admin/`
3. **View logs:** Render dashboard → Logs (should show successful build)

**✅ Done! Your app is live!**

---

## 🔧 If Deployment Fails

| Error | Solution |
|-------|----------|
| Database connection error | Check `DATABASE_URL` is set from PostgreSQL service |
| Static files 404 | Click "Deploy" again to re-run `collectstatic` |
| "SECRET_KEY required" | Set `DJANGO_SECRET_KEY` in environment variables |
| "ALLOWED_HOSTS invalid" | Verify `ALLOWED_HOSTS` includes Render domain |
| Build fails on dependencies | Verify `requirements.txt` is valid: `pip install -r requirements.txt` |

**Need more help?** See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for troubleshooting.

---

## 📋 What Changed

- ✅ `zorpido_config/settings/production.py` - Render-ready settings
- ✅ `requirements.txt` - Production packages only
- ✅ `Procfile` - Optimized gunicorn command
- ✅ `render.yaml` - **NEW** - One-click deployment blueprint
- ✅ Documentation - Guides and checklists

---

## 🔐 Security Notes

- ✅ DEBUG is False
- ✅ HTTPS enforced
- ✅ Cookies are secure
- ✅ CSRF protection enabled
- ✅ No MySQL (PostgreSQL only)
- ✅ No hardcoded secrets

---

## 📞 Support

- **Deployment Guide:** [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)
- **Checklist:** [RENDER_DEPLOYMENT_CHECKLIST.md](./RENDER_DEPLOYMENT_CHECKLIST.md)
- **Env Vars:** [.env.render.example](./.env.render.example)
- **Full Summary:** [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)

---

**Ready? Go to https://dashboard.render.com and click "Blueprint"** 🚀

*Your app will be live in 5-10 minutes!*
