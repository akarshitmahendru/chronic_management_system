from rest_framework import serializers
from utils.fields import PhoneNumberField


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False,
        required=True
    )
