from django.contrib import admin
from disease_management.models import Disease, PatientPersonalizedPlan
from utils.constants import RoleEnum

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        from accounts.models import User
        if db_field.name == "patient":
            kwargs["queryset"] = User.objects.filter(role=RoleEnum.PATIENT.value)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
