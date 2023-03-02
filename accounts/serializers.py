from rest_framework import serializers
from utils.fields import PhoneNumberField, CustomEmailSerializerField
from accounts.models import PatientDetail


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False,
        required=True
    )


class PatientDataSerializer(serializers.ModelSerializer):
    email = CustomEmailSerializerField(required=False, allow_null=True)
    doctor_id = serializers.IntegerField(required=False, allow_null=True)
    diseases = serializers.JSONField(default=list, required=False)
    display_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = PatientDetail
        fields = ('email', 'weight', 'dob', 'sex', 'doctor_id', 'diseases', 'display_picture')


class PatientDataGetSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    display_picture = serializers.SerializerMethodField()
    diseases = serializers.SerializerMethodField()
    doctor_details = serializers.SerializerMethodField()

    def get_diseases(self, obj):
        from disease_management.serializers import DiseaseSerializer
        qs = obj.diseases.all()
        return DiseaseSerializer(instance=qs, many=True).data

    def get_doctor_details(self, obj):
        if obj.doctor:
            return {"full_name": f"{obj.doctor.get_full_name()}", "email": obj.doctor.email,
                    "display_picture": obj.doctor.display_picture, "phone_number": str(obj.doctor.phone_number)}
        return {}

    def get_full_name(self, obj):
        return obj.patient.get_full_name()

    def get_email(self, obj):
        return obj.patient.email

    def get_phone_number(self, obj):
        return str(obj.patient.phone_number)

    def get_display_picture(self, obj):
        return obj.patient.display_picture

    class Meta:
        model = PatientDetail
        fields = ("patient_id", "full_name", "email", "phone_number", "display_picture", "weight", "sex", "dob",
                  "diseases", "doctor_details")



