from notifications.models import Notification
from rest_framework import serializers
from utils.constants import NOTIFICATION_STATUS
from utils.constants import NotificationStatusEnum


class NotificationGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id', 'notification_title', 'notification_body', 'action')


class NotificationStatusSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField(required=True, allow_null=False)
    action_state = serializers.ChoiceField(choices=NOTIFICATION_STATUS, required=True)

    def validate_notification_id(self, notification_id):
        if not Notification.objects.filter(id=notification_id).exists():
            raise serializers.ValidationError("Notification not exists.")
        if Notification.objects.filter(id=notification_id, status=NotificationStatusEnum.READ.value).exists():
            raise serializers.ValidationError("Notification already marked as read.")
        return notification_id

    class Meta:
        fields = ('notification_id', 'action_state',)
