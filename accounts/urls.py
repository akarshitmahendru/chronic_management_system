from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/$', apis.LoginAPI.as_view(), name='login'),
    url(r'^patient_details/$', apis.PatientDataViewSet.as_view(), name='PatientData'),
    url(r'^doctors/$', apis.DoctorAPI.as_view(), name='DoctorAPI'),
    url(r'^medical_history/$', apis.PatientMedicalHistoryView.as_view(), name='MedicalHistory'),
]

