from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^notifications/$', apis.NotificationAPI.as_view(), name='Notifications'),
    url(r'^open_notification/$', apis.OpenNotificationView.as_view(), name='OpenNotifications'),
]