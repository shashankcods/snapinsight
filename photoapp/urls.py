from django.urls import path
from .views import home, results, deletePhoto, aboutPage

urlpatterns = [
    path('', home, name='home'),
    path('results/', results, name='results'),
    path('delete/<int:photo_id>/', deletePhoto, name='delete_photo'),
    path('aboutpage.html', aboutPage, name='about' )
]
