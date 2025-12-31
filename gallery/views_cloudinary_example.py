"""Example views showing Cloudinary usage.

This file demonstrates two simple endpoints:
- `upload_image` — simple upload handler using `cloudinary.uploader.upload`.
- `show_image` — renders an example template that displays a Cloudinary URL.

These are examples only; adapt to your project's URL patterns and security needs.
"""
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages

from zorpido_config import cloudinary as cloudinary_config


def upload_image(request: HttpRequest):
    """Handle a basic image upload form and upload to Cloudinary.

    - If Cloudinary is not configured, the view will add an error message and
      render the template without raising an exception.
    - On success, it returns the Cloudinary `secure_url` in the template context.
    """
    uploaded_url = None

    if request.method == 'POST':
        image = request.FILES.get('image')
        if not image:
            messages.error(request, 'No file uploaded.')
            return redirect(request.path)

        if not cloudinary_config.CLOUDINARY_ENABLED:
            messages.error(request, 'Cloudinary not configured. See settings.')
        else:
            try:
                # Import here to avoid import errors if package missing
                import cloudinary.uploader

                result = cloudinary.uploader.upload(image)
                # Cloudinary response includes `secure_url` and `public_id`
                uploaded_url = result.get('secure_url') or result.get('url')
                messages.success(request, 'Upload successful.')
            except Exception as exc:
                messages.error(request, f'Upload failed: {exc}')

    return render(request, 'cloudinary_example.html', {'uploaded_url': uploaded_url})


def show_image(request: HttpRequest):
    """Render a template showing how to generate Cloudinary URLs for a known public id.

    Replace `sample_public_id` with your actual public id or model field value.
    """
    sample_public_id = request.GET.get('public_id') or 'sample'
    image_url = None

    if cloudinary_config.CLOUDINARY_ENABLED:
        try:
            # Cloudinary helper imports done lazily
            from cloudinary.utils import cloudinary_url

            url, options = cloudinary_url(sample_public_id, secure=True)
            image_url = url
        except Exception:
            image_url = None

    context = {'image_url': image_url, 'cloudinary_enabled': cloudinary_config.CLOUDINARY_ENABLED}
    return render(request, 'cloudinary_example.html', context)
