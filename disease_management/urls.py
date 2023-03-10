from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^diseases/$', apis.DiseaseAPI.as_view(), name='DiseaseAPI'),
    url(r'^my_plans/$', apis.PatientPersonalizedAPI.as_view(), name='PersonalizedPlans'),
]