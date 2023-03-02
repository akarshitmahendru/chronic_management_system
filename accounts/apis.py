from rest_framework import views, permissions, response, status, generics
from accounts.models import User, PatientDetail
from drf_yasg.utils import swagger_auto_schema
from accounts.serializers import LoginSerializer, PatientDataSerializer, PatientDataGetSerializer, DoctorSerializer
from utils.constants import RoleEnum


class LoginAPI(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializers_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_id="Login")
    def post(self, request, *args, **kwargs):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(phone_number=serializer.validated_data['phone_number']).first()
            if not user:
                user = User.objects.create(
                    phone_number=serializer.validated_data['phone_number']
                )
            response_dict = dict()
            response_dict['user_id'] = user.id
            response_dict['phone_number'] = str(user.phone_number)
            response_dict['auth-token'] = user.get_jwt_token_for_user()
            return response.Response(response_dict, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDataViewSet(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = PatientDetail

    def get_queryset(self):
        return self.model.objects.filter(patient_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PatientDataSerializer
        return PatientDataGetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        user = self.request.user
        if serializer.is_valid(raise_exception=True):
            diseases, email, display_picture = None
            if "diseases" in serializer.validated_data:
                diseases = serializer.validated_data.pop("diseases")
            if "email" in serializer.validated_data:
                user.email = serializer.validated_data.pop("email")
            if "display_picture" in serializer.validated_data:
                user.display_picture = serializer.validated_data.pop("display_picture")
            patient_detail = self.model.objects.filter(patient_id=self.request.user.id).first()
            if patient_detail:
                self.model.objects.filter(patient_id=self.request.user.id).update(**serializer.validated_data)
            else:
                serializer.validated_data['patient_id'] = self.request.user.id
                patient_detail = self.model.objects.create(**serializer.validated_data)
            if diseases:
                patient_detail.diseases.set(diseases)
            if email or display_picture:
                user.save(update_fields=['email', 'display_picture'])
            return response.Response({"msg": "Patient Details successfully updated"}, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return User.objects.filter(role=RoleEnum.DOCTOR.value)