from rest_framework import generics, views, permissions, response, status
from notifications.models import Notification
from notifications.models import PatientSuccessRate
from notifications.serializers import NotificationGetSerializer, NotificationStatusSerializer
from drf_yasg.utils import swagger_auto_schema
from utils.constants import NotificationStatusEnum


class NotificationAPI(generics.ListAPIView):
    serializer_class = NotificationGetSerializer
    model = Notification

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).exclude(action=NotificationStatusEnum.READ.value)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer_class()
        serializer_data = serializer(queryset, many=True)
        return response.Response(data={"result": serializer_data.data}, status=status.HTTP_200_OK)


class OpenNotificationView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializers_class = NotificationStatusSerializer

    @swagger_auto_schema(
        request_body=NotificationStatusSerializer,
        operation_id="NotificationStatusSerializer")
    def post(self, request, *args, **kwargs):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            action_state = int(serializer.validated_data['action_state'])
            notification = Notification.objects.filter(id=serializer.validated_data['notification_id']).first()
            notification.action = action_state
            notification.save()
            if action_state == NotificationStatusEnum.READ.value:
                PatientSuccessRate.objects.create(user_id=self.request.user.id, notification_id=notification.id)
            return response.Response({"msg": "Notification successfully marked."}, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
