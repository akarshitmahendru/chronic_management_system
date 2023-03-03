from django.db import models
from disease_management.models import Disease
from rest_framework.exceptions import ValidationError
from ckeditor.fields import RichTextField
# Create your models here.


class KnowledgeBase(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    video_link = models.TextField(null=True, blank=True)
    description = RichTextField()
    image_link = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.image_link or not self.video_link:
            return ValidationError(f"Please mention either of video or image link")
        return self

