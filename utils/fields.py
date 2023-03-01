from rest_framework import serializers, exceptions
from phonenumber_field.phonenumber import to_python


class CustomEmailSerializerField(serializers.EmailField):

    def to_internal_value(self, value):
        value = super(CustomEmailSerializerField,
                      self).to_internal_value(value)
        return value.lower()


class PhoneNumberField(serializers.CharField):
    """
    A custom serialize field to represent data of `phone_number` field
    like
    {"phone_number": {"number": "1234567890", "country_code": "+91"}}
    """
    default_error_messages = {
        'invalid': 'Enter a valid phone number.',
    }

    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            raise exceptions.ValidationError(self.error_messages['invalid'])

        return phone_number

    def to_representation(self, value):
        """ break the country code and phone number """
        if value:
            return {
                'country_code': "+" + str(value.country_code),
                'number': str(value.national_number)
            }
