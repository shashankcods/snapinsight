from django import forms
from .models import Photo

class photoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image"]
