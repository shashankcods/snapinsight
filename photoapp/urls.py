from django.urls import path
from .views import home, results, aboutPage
from .views import getPhotos, uploadPhoto, deletePhoto

urlpatterns = [
    path('', home, name='home'),
    path('results/', results, name='results'),
    path('about/', aboutPage, name='about' ),
    
    # API ENDPOINTS
    path('api/images/', getPhotos, name='api-images'),
    path('api/upload/', uploadPhoto, name='api-upload'),
    path('api/delete/<int:photo_id>/', deletePhoto, name='api-delete'),
]
