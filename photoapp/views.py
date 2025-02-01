from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Photo
from .utils import analyze_image
from .forms import photoForm
import os

def home(request):
    uploaded = False
    if request.method == "POST":
        form = photoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()

            scores = analyze_image(photo.image.path)
            if scores:
                (photo.brightness_score, 
                 photo.contrast_score, 
                 photo.saturation_score, 
                 photo.sharpness_score, 
                 photo.overall_score) = scores
                photo.save()
            uploaded = True

    else:
        form = photoForm()

    return render(request, 'homepage.html', {'form': form, 'uploaded': uploaded})

def results(request):
    photos = Photo.objects.all()
    return render(request, 'results.html', {'photos':photos})

def deletePhoto(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    image_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted file: {image_path}")

    photo.delete()
    print(f"Deleted photo ID {photo_id}")

    return redirect('results')

def uploadPhoto(request):
    if request.method == "POST" and request.FILES.get("photo"):
        photo = Photo(image=request.FILES["photo"])
        photo.save()

    return render(request, "upload.html")

def aboutPage(request):
    return render(request, 'aboutpage.html')

