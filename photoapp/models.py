from django.db import models
from django.utils import timezone

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    #scores for each traits
    temperature_score = models.FloatField(null=True, blank=True)
    tint_score = models.FloatField(null=True, blank=True)
    exposure_score = models.FloatField(null=True, blank=True)
    contrast_score = models.FloatField(null=True, blank=True)
    highlights_score = models.FloatField(null=True, blank=True)
    shadows_score = models.FloatField(null=True, blank=True)
    whites_score = models.FloatField(null=True, blank=True)
    blacks_score = models.FloatField(null=True, blank=True)
    vibrance_score = models.FloatField(null=True, blank=True)
    saturation_score = models.FloatField(null=True, blank=True)

    overall_score = models.FloatField(null=True, blank=True)

    def bar_color(self):
        if self.overall_score is None:
            return "gray"
        if self.overall_score > 80:
            return "green"
        elif self.overall_score > 50:
            return "orange"
        return "red"


def __str__(self):
    return f"Photo {self.id} - {self.uploaded_at}"