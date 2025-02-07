from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.views.decorators import csrf
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Photo
from .image_analysis import analyze_image
from .serializers import photoSerializer
import os

def home(request):
     return render(request, 'homepage.html')


@api_view(['POST'])
@parser_classes([MultiPartParser])
def uploadPhoto(request):
    print(f"Request method: {request.method}")  # Debugging the method
    print(f"Files in request: {request.FILES}")  # Debugging uploaded files
    if "photo" not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

    photo = Photo(image=request.FILES["photo"])
    photo.save()
    
    scores = analyze_image(photo.image.path)
    print(f"Computed Scores: {scores}") 
    
    if scores:
        (photo.temperature_score, 
        photo.tint_score, 
        photo.exposure_score, 
        photo.contrast_score, 
        photo.highlights_score, 
        photo.shadows_score, 
        photo.whites_score, 
        photo.blacks_score, 
        photo.vibrance_score, 
        photo.saturation_score) = (
        scores["temperature"], 
        scores["tint"], 
        scores["exposure"], 
        scores["contrast"], 
        scores["highlights"], 
        scores["shadows"], 
        scores["whites"], 
        scores["blacks"], 
        scores["vibrance"], 
        scores["saturation"])
        
        photo.save()
    print(f"Photo uploaded successfully with ID: {photo.id}")  # Log success
    return Response({"message": "Upload successful!", "photo_id":photo.id})

@api_view(['GET'])
def getPhotos(request):
     photos = Photo.objects.order_by('-uploaded_at').first()
     
     if not photos:
          return Response({"message": "No photos available"}, status=200)
     serializer = photoSerializer(photos)
     return Response(serializer.data)

@api_view(['DELETE'])
def deletePhoto(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))

    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted file: {image_path}")

    photo.delete()
    return Response({"message": f"Deleted photo {photo_id}"})

def home(request):
     return render(request, 'homepage.html')

def aboutPage(request):
    return render(request, 'aboutpage.html')

def results(request):
    photos = Photo.objects.all()
    return render(request, 'results.html', {'photos': photos})