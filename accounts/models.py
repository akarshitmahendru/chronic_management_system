from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from rest_framework_jwt.settings import api_settings
from accounts.entities.model_managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from utils.constants import RoleEnum, ROLES, SexEnum, SEX
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """
        model to store user infomation
    """
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    email = models.EmailField(max_length=254, db_index=True, unique=True, null=True)
    phone_number = PhoneNumberField(unique=True, db_index=True)
    role = models.IntegerField(default=RoleEnum.DOCTOR.value, choices=ROLES)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def get_jwt_token_for_user(self):
        """ get jwt token for the user """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)
        return token


class PatientDetail(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_detail")
    weight = models.FloatField(default=0)
    dob = models.DateField(null=True, blank=True)
    sex = models.IntegerField(choices=SEX, default=SexEnum.MALE.value)
    diseases = models.ManyToManyField('disease_management.Disease', blank=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="provider")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


