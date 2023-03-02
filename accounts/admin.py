from django.contrib import admin
from django.utils.safestring import mark_safe
from accounts.models import User, PatientDetail, PatientMedicalHistory
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'role')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('role',)
    exclude = ('password', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')


@admin.register(PatientDetail)
class PatientDetailAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_contact_information', 'doctor_name', 'dob', 'sex')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__email', 'patient__phone_number',
                     'doctor__first_name', 'doctor__last_name', 'doctor__email', 'doctor__phone_number')
    autocomplete_fields = ('diseases', 'patient', 'doctor')

    def doctor_name(self, obj):
        if obj.doctor:
            return f"{obj.doctor.first_name} {obj.doctor.last_name}"
        return "-"

    def patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def patient_contact_information(self, obj):
        email_str = 'Email&nbsp;Address&nbsp;:&nbsp;' + str(obj.patient.email) + '<br/>'
        phone_str = 'Phone&nbsp;Number&nbsp;:&nbsp;' + str(obj.patient.phone_number) + '<br/>'
        details_str = email_str + phone_str
        return mark_safe(details_str)


@admin.register(PatientMedicalHistory)
class PatientMedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'attribute', 'value')

    def patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
