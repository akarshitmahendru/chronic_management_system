from django.contrib import admin
from content.models import KnowledgeBase
# Register your models here.


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'video_link', "image_link")
    search_fields = ('disease__disease_name',)

    def disease_name(self, obj):
        return obj.disease.disease_name
