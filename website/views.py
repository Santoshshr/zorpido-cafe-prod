import os
import logging
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.cache import cache

from menu.models import MenuItem, FeaturedMenu
from blogs.models import BlogPost
from gallery.models import GalleryImage
from users.models import User
from users.forms import CustomerMessageForm
from .models import Testimonial, FeaturedImage

logger = logging.getLogger(__name__)


import os
import logging

from django.shortcuts import render
from django.core.cache import cache

from menu.models import MenuItem, FeaturedMenu
from blogs.models import BlogPost
from gallery.models import GalleryImage
from users.models import User
from .models import Testimonial, FeaturedImage

logger = logging.getLogger(__name__)


def safe_query(label, fn, default):
    """
    Executes a DB or cache operation safely.
    Logs exception and returns default on failure.
    """
    try:
        return fn()
    except Exception:
        logger.exception(f"{label} failed")
        return default


def home(request):
    # Populate context with homepage data
    featured_menus = safe_query("FeaturedMenu", lambda: FeaturedMenu.objects.filter(is_active=True), [])
    featured_images = safe_query("FeaturedImage", lambda: FeaturedImage.objects.filter(is_active=True), [])
    testimonials = safe_query("Testimonial", lambda: Testimonial.objects.filter(is_active=True), [])
    latest_blogs = safe_query("BlogPost", lambda: BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3], [])
    context = {
        'featured_menus': featured_menus,
        'featured_images': featured_images,
        'testimonials': testimonials,
        'latest_blogs': latest_blogs,
    }
    return render(request, "website/home.html", context)

# --- Other views remain unchanged ---
def about(request):
    return render(request, 'website/about.html')


def contact(request):
    if request.method == 'POST':
        form = CustomerMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('website:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerMessageForm()

    return render(request, 'website/contact.html', {'form': form})


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'website/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    try:
        post.increment_views()
    except Exception as e:
        logger.error(f"Increment views failed: {e}")
    related_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]
    return render(request, 'website/blog_detail.html', {'post': post, 'related_posts': related_posts})


def gallery_view(request):
    category = request.GET.get('category', 'all')
    if category and category != 'all':
        images = GalleryImage.objects.filter(is_active=True, category=category)
    else:
        images = GalleryImage.objects.filter(is_active=True)
    categories = getattr(GalleryImage, 'CATEGORY_CHOICES', [])
    return render(request, 'website/gallery.html', {'images': images, 'categories': categories, 'current_category': category})


def terms(request):
    return render(request, 'terms.html')


def workflow(request):
    return render(request, 'website/workflow.html')
