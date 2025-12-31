from django.urls import path
from . import views
from . import views_cloudinary_example

app_name = 'gallery'

urlpatterns = [
	path('download/<int:image_id>/', views.download_image, name='download_image'),
	# Example Cloudinary routes (optional)
	path('cloudinary/upload/', views_cloudinary_example.upload_image, name='cloudinary_upload'),
	path('cloudinary/show/', views_cloudinary_example.show_image, name='cloudinary_show'),
]