from django.contrib import admin

# Register your models here.
from notifications.models import NotificationsScheduler, Notification


@admin.register(NotificationsScheduler)
class NotificationSchedularAdmin(admin.ModelAdmin):
    list_display = ('patient_plan', 'scheduled_time', 'last_triggered_on')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'patient_plan', 'action', 'notification_title')
