from asyncio.log import logger
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.core.cache import cache

from menu.models import MenuItem, FeaturedMenu
from blogs.models import BlogPost
from gallery.models import GalleryImage
from users.forms import CustomerMessageForm
from users.models import User
from .models import Testimonial, FeaturedImage


def home(request):
    # Featured menu items
    featured_items = FeaturedMenu.objects.filter(
        is_active=True,
        menu_item__is_active=True
    ).select_related("menu_item")

    # Fallback menu items (if no featured)
    fallback_items = []
    if not featured_items.exists():
        fallback_items = MenuItem.objects.filter(
            is_active=True,
            is_featured=True
        )[:6]

    # Featured blogs
    featured_blogs = BlogPost.objects.filter(
        is_published=True,
        is_featured=True
    )[:3]

    # Gallery images
    gallery_images = GalleryImage.objects.filter(
        is_active=True,
        is_zorpido_glimpses=True
    )

    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:6]

    # Featured images / banners
    featured_images = FeaturedImage.objects.filter(
        is_active=True
    ).order_by("order")[:10]

    # Leaderboard users
    leaderboard_users = cache.get("homepage_leaderboard_users")

    if leaderboard_users is None:
        leaderboard_users = User.objects.filter(
            is_active=True,
            user_type="customer"
        ).order_by("-loyalty_points")[:20]
        cache.set("homepage_leaderboard_users", leaderboard_users, 60)

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
