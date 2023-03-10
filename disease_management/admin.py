from django.contrib import admin
from disease_management.models import Disease, PatientPersonalizedPlan, DiseaseDefaultPlan
from utils.constants import RoleEnum
from notifications.models import NotificationsScheduler
from utils.push_notifications import FireBaseActions


# Register your models here.


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'is_chronic')
    search_fields = ('disease_name',)
    list_filter = ('is_chronic',)


@admin.register(DiseaseDefaultPlan)
class DiseasePlanAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'priority')
    search_fields = ('disease__disease_name',)
    autocomplete_fields = ('disease',)

    def disease_name(self, obj):
        return obj.disease.disease_name


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

    def save_model(self, request, obj, form, change):
        from notifications.models import NotificationsScheduler, Notification
        data = {}
        if not obj.id:
            data = {"title": f"New {obj.get_plan_display()} has been added.",
                    "body": f"Check the plan suggested by your doctor to boost your health.",
                    "notification_id": "0"}
            FireBaseActions.send_message(user_tokens=[obj.patient.fcm_token], data=data)
        super(PatientPersonalizedPlanAdmin, self).save_model(request, obj, form, change)
        if data:
            Notification.objects.create(user_id=obj.patient_id, patient_plan_id=obj.id,
                                        notification_title=data['title'], notification_body=data['body'])
        scheduled_time = obj.fetch_scheduled_time()
        if scheduled_time and obj.notification_heading:
            NotificationsScheduler.objects.update_or_create(patient_plan_id=obj.id,
                                                            defaults={"scheduled_time": scheduled_time})
