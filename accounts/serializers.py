from rest_framework import serializers

from utils.constants import PATIENT_ATTRIBUTES
from utils.fields import PhoneNumberField, CustomEmailSerializerField
from accounts.models import PatientDetail, User, PatientMedicalHistory


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False,
        required=True
    )


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'display_picture')


class PatientMedicalHistorySerializer(serializers.ModelSerializer):
    attribute = serializers.ChoiceField(choices=PATIENT_ATTRIBUTES, required=True, allow_null=False)
    value = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = PatientMedicalHistory
        fields = ("attribute", "value")


class PatientDataSerializer(serializers.ModelSerializer):
    email = CustomEmailSerializerField(required=False, allow_null=True)
    doctor_id = serializers.IntegerField(required=False, allow_null=True)
    diseases = serializers.JSONField(default=list, required=False)
    display_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = PatientDetail
        fields = ('email', 'dob', 'sex', 'doctor_id', 'diseases', 'display_picture')


class PatientDataGetSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    display_picture = serializers.SerializerMethodField()
    diseases = serializers.SerializerMethodField()
    doctor_details = serializers.SerializerMethodField()
    medical_history = serializers.SerializerMethodField()

    def get_diseases(self, obj):
        from disease_management.serializers import DiseaseSerializer
        qs = obj.diseases.all()
        return DiseaseSerializer(instance=qs, many=True).data

    def get_doctor_details(self, obj):
        if obj.doctor:
            return {"full_name": f"{obj.doctor.get_full_name()}", "email": obj.doctor.email,
                    "display_picture": obj.doctor.display_picture if obj.doctor.display_picture else None,
                    "phone_number": str(obj.doctor.phone_number)}
        return {}

    def get_full_name(self, obj):
        return obj.patient.get_full_name()

    def get_email(self, obj):
        return obj.patient.email

    def get_phone_number(self, obj):
        return str(obj.patient.phone_number)

    def get_display_picture(self, obj):
        if obj.patient.display_picture:
            return obj.patient.display_picture
        return None

    def get_medical_history(self, obj):
        qs = PatientMedicalHistory.objects.filter(patient_id=obj.patient_id).first()
        if qs:
            return PatientMedicalHistorySerializer(data=qs, many=False).data
        return []

    class Meta:
        model = PatientDetail
        fields = ("patient_id", "full_name", "email", "phone_number", "display_picture", "sex", "dob", "diseases",
                  "doctor_details", "medical_history")
