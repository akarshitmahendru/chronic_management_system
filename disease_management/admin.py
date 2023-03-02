from django.contrib import admin
from disease_management.models import Disease, PatientPersonalizedPlan


# Register your models here.

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'is_chronic')
    search_fields = ('disease_name',)
    list_filter = ('is_chronic',)


@admin.register(PatientPersonalizedPlan)
class PatientPersonalizedPlanAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    autocomplete_fields = ('patient',)
    list_filter = ('plan', 'plan_status')
    search_fields = ('name', 'patient__first_name', 'patient__last_name', 'patient__email')
