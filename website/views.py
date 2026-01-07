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


def home(request):
    """
    Production-safe homepage view.
    Handles empty DB, cache failures, and query errors without crashing.
    """

    featured_items = []
    fallback_items = []
    featured_blogs = []
    gallery_images = []
    testimonials = []
    featured_images = []
    leaderboard_users = []

    # ─────────────────────────────
    # Featured menu items
    # ─────────────────────────────
    try:
        featured_items = (
            FeaturedMenu.objects.filter(
                is_active=True,
                menu_item__is_active=True
            )
            .select_related('menu_item')
        )
    except Exception as e:
        logger.exception("FeaturedMenu query failed")

    # ─────────────────────────────
    # Fallback menu items
    # ─────────────────────────────
    try:
        if not featured_items.exists():
            fallback_items = (
                MenuItem.objects.filter(
                    is_active=True,
                    is_featured=True
                )[:6]
            )
    except Exception:
        logger.exception("Fallback MenuItem query failed")

    # ─────────────────────────────
    # Featured blogs
    # ─────────────────────────────
    try:
        featured_blogs = (
            BlogPost.objects.filter(
                is_published=True,
                is_featured=True
            )[:3]
        )
    except Exception:
        logger.exception("Featured BlogPost query failed")

    # ─────────────────────────────
    # Gallery images
    # ─────────────────────────────
    try:
        gallery_images = (
            GalleryImage.objects.filter(
                is_active=True,
                is_zorpido_glimpses=True
            )
        )
    except Exception:
        logger.exception("GalleryImage query failed")

    # ─────────────────────────────
    # Testimonials
    # ─────────────────────────────
    try:
        testimonials = Testimonial.objects.filter(is_active=True)[:6]
    except Exception:
        logger.exception("Testimonial query failed")

    # ─────────────────────────────
    # Featured images
    # ─────────────────────────────
    try:
        featured_images = (
            FeaturedImage.objects.filter(is_active=True)
            .order_by('order')[:10]
        )
    except Exception:
        logger.exception("FeaturedImage query failed")

    # ─────────────────────────────
    # Leaderboard users (cache-safe)
    # ─────────────────────────────
    try:
        cache_key = "homepage_leaderboard_users_v1"
        cache_ttl = int(os.environ.get("LEADERBOARD_CACHE_TTL", 60))

        leaderboard_users = cache.get(cache_key)

        if leaderboard_users is None:
            leaderboard_users = list(
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
            cache.set(cache_key, leaderboard_users, cache_ttl)

    except Exception:
        logger.exception("Leaderboard users query failed")
        leaderboard_users = []

    # ─────────────────────────────
    # Context
    # ─────────────────────────────
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
