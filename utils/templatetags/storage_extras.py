from django import template
from django.conf import settings
from django.core.files.storage import default_storage

register = template.Library()
# Provides a filter to get the correct media URL for a file, compatible with both local and Cloudinary storage.
@register.filter
def media_url(path):
	"""
	Returns the correct media URL for a given file path, compatible with both local and Cloudinary storage.
	Usage: {{ object.image|media_url }}
	"""
	if not path:
		return ''
	try:
		return default_storage.url(str(path))
	except Exception:
		return settings.MEDIA_URL + str(path)


