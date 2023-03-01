from django.contrib import admin
from disease_management.models import Disease


# Register your models here.

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'is_chronic')
    search_fields = ('disease_name',)
    list_filter = ('is_chronic',)
