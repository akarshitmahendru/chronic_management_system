from django.db import models
from accounts.models import User
from disease_management.models import PatientPersonalizedPlan
from utils.constants import NotificationStatusEnum, NOTIFICATION_STATUS


# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_plan = models.ForeignKey(PatientPersonalizedPlan, on_delete=models.CASCADE)
    action = models.IntegerField(default=NotificationStatusEnum.NO_ACTION.value, choices=NOTIFICATION_STATUS)
    notification_title = models.TextField(null=True, blank=True)
    notification_body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PatientSuccessRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationsScheduler(models.Model):
    patient_plan = models.OneToOneField(PatientPersonalizedPlan, on_delete=models.CASCADE)
    is_triggered = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


