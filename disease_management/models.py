from django.db import models

# Create your models here.


class Disease(models.Model):
    disease_name = models.CharField(db_index=True, max_length=128)
    is_chronic = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="disease_images", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.disease_name


