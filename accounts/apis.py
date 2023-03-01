from rest_framework import views, permissions, response, status
from accounts.models import User
from drf_yasg.utils import swagger_auto_schema
from accounts.serializers import LoginSerializer


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
