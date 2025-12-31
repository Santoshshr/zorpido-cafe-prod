Cloudinary integration

Overview

This project includes a safe, reusable Cloudinary integration helper at `zorpido_config/cloudinary.py`.

Installation

Add these packages to your environment:

```bash
pip install cloudinary python-dotenv
```

Environment variables

- `CLOUDINARY_CLOUD_NAME` — your Cloudinary cloud name
- `CLOUDINARY_API_KEY` — API key
- `CLOUDINARY_API_SECRET` — API secret
- Or set a single `CLOUDINARY_URL` of the form `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`

Local development

- Create a `.env` in the project root (the project already loads `.env` in `zorpido_config/settings/base.py`).
- Add the Cloudinary vars to `.env`.

Production

- Set the environment variables in your host (cPanel / Render / your server environment variable settings).

Usage examples

- Example upload view: `gallery.views_cloudinary_example.upload_image`
- Example display view: `gallery.views_cloudinary_example.show_image`
- Template: `templates/cloudinary_example.html`

Notes

- The helper is intentionally tolerant: it will not crash the application if Cloudinary is not configured. Use `from zorpido_config.cloudinary import require_cloudinary` in code paths that must have Cloudinary and call it to raise an explicit `ImproperlyConfigured` error.
