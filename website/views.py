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
    """
    Homepage view using centralized error handling.
    Clean, readable, and production-safe.
    """

    featured_items = safe_query(
        "FeaturedMenu",
        lambda: FeaturedMenu.objects.filter(
            is_active=True,
            menu_item__is_active=True
        ).select_related("menu_item"),
        []
    )

    fallback_items = safe_query(
        "Fallback MenuItem",
        lambda: MenuItem.objects.filter(
            is_active=True,
            is_featured=True
        )[:6] if not featured_items or not featured_items.exists() else [],
        []
    )

    featured_blogs = safe_query(
        "Featured BlogPost",
        lambda: BlogPost.objects.filter(
            is_published=True,
            is_featured=True
        )[:3],
        []
    )

    gallery_images = safe_query(
        "GalleryImage",
        lambda: GalleryImage.objects.filter(
            is_active=True,
            is_zorpido_glimpses=True
        ),
        []
    )

    testimonials = safe_query(
        "Testimonial",
        lambda: Testimonial.objects.filter(is_active=True)[:6],
        []
    )

    featured_images = safe_query(
        "FeaturedImage",
        lambda: FeaturedImage.objects.filter(
            is_active=True
        ).order_by("order")[:10],
        []
    )

    def load_leaderboard():
        cache_key = "homepage_leaderboard_users_v1"
        ttl = int(os.environ.get("LEADERBOARD_CACHE_TTL", 60))

        users = cache.get(cache_key)
        if users is not None:
            return users

        users = list(
            User.objects.filter(
                is_active=True,
                user_type="customer"
            )
            .only(
                "id",
                "username",
                "full_name",
                "loyalty_points",
                "profile_picture"
            )
            .order_by("-loyalty_points")[:20]
        )

        cache.set(cache_key, users, ttl)
        return users

    leaderboard_users = safe_query(
        "Leaderboard Users",
        load_leaderboard,
        []
    )

    context = {
        "featured_items": featured_items,
        "fallback_items": fallback_items,
        "featured_blogs": featured_blogs,
        "gallery_images": gallery_images,
        "testimonials": testimonials,
        "featured_images": featured_images,
        "leaderboard_users": leaderboard_users,
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
