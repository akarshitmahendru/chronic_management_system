from django.db import models
from accounts.models import User
from disease_management.models import PatientPersonalizedPlan

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_plan = models.ForeignKey(PatientPersonalizedPlan, on_delete=models.CASCADE)
    action = models.IntegerField()
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


