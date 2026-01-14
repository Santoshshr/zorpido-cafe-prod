from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django import forms
from .models import User, CustomerMessage
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	"""Use Django's built-in UserAdmin to expose permissions and groups."""
	model = User
	# Custom admin form removed; using standard form with profile_picture field
	list_display = ('username', 'profile_thumbnail', 'full_name', 'email', 'user_type', 'is_active', 'is_staff', 'is_superuser', 'created_at')
	list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups')
	search_fields = ('username', 'full_name', 'email')
	readonly_fields = ('created_at', 'updated_at', 'profile_thumbnail')

	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('full_name', 'email', 'phone', 'date_of_birth', 'location', 'profile_picture', 'profile_thumbnail')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'profile_picture')
		}),
	)

	ordering = ('email',)
	filter_horizontal = ('groups', 'user_permissions')

	def profile_thumbnail(self, obj):
		"""Return a small avatar image for list display and detail preview."""
		if obj and getattr(obj, 'profile_picture'):
			# profile_picture is an ImageField; use .url for the public URL
			if obj.profile_picture:
				url = obj.profile_picture.url
				return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />', url)
			return '-'
		return '-'

	profile_thumbnail.short_description = 'Avatar'
	profile_thumbnail.allow_tags = True


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'replied')
	list_filter = ('is_read', 'replied', 'created_at')
	search_fields = ('name', 'email', 'subject')
