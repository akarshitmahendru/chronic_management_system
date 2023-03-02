from django.db import models

from utils.constants import PLAN_FREQUENCY, PlanEnum, PlanFrequencyEnum, PATIENT_PLAN, PLAN_STATUS, PlanStatusEnum


# Create your models here.


class Disease(models.Model):
    disease_name = models.CharField(db_index=True, max_length=128)
    is_chronic = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="disease_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.disease_name


class PatientPersonalizedPlan(models.Model):
    from accounts.models import User

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_plan")
    plan = models.IntegerField(choices=PATIENT_PLAN, default=PlanEnum.MEDICATIONS.value)
    name = models.CharField(max_length=120, null=True, blank=True)
    frequency = models.IntegerField(choices=PLAN_FREQUENCY, default=PlanFrequencyEnum.HOURS.value)
    magnitude = models.PositiveIntegerField(default=1)
    value = models.CharField(max_length=32, null=True, blank=True)
    plan_status = models.IntegerField(choices=PLAN_STATUS, default=PlanStatusEnum.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.patient.first_name:
            patient_identifier = f"{self.patient.get_full_name()}"
        elif self.patient.email:
            patient_identifier = f"{self.patient.email}"
        else:
            patient_identifier = f"{self.patient.phone_number}"
        return f"{self.get_plan_display()} Plan of {patient_identifier} => {self.name}"



