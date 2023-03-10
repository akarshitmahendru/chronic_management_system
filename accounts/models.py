from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from rest_framework_jwt.settings import api_settings
from accounts.entities.model_managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from utils.constants import RoleEnum, ROLES, SexEnum, SEX, PATIENT_ATTRIBUTES
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """
        model to store user infomation
    """
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    email = models.EmailField(max_length=254, db_index=True, unique=True, null=True)
    phone_number = PhoneNumberField(unique=True, db_index=True)
    display_picture = models.ImageField(upload_to="display_pics", null=True, blank=True)
    role = models.IntegerField(default=RoleEnum.DOCTOR.value, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=600, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_jwt_token_for_user(self):
        """ get jwt token for the user """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self)
        phone_number = payload.pop('phone_number')
        username = payload.pop('username')
        payload.update({'phone_number': str(phone_number), 'username': str(username)})
        token = jwt_encode_handler(payload)
        return token

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        if self.first_name:
            return self.get_full_name()
        elif self.email:
            return self.email
        return str(self.phone_number)


class PatientDetail(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_detail")
    dob = models.DateField(null=True, blank=True)
    sex = models.IntegerField(choices=SEX, default=SexEnum.MALE.value)
    diseases = models.ManyToManyField('disease_management.Disease', blank=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="provider")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PatientMedicalHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_history")
    attribute = models.IntegerField(choices=PATIENT_ATTRIBUTES, null=True)
    value = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





