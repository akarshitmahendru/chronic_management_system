from rest_framework import generics, permissions, status, response, views
from disease_management.models import Disease, DiseaseDefaultPlan, PatientPersonalizedPlan
from disease_management.serializers import DiseaseSerializer
from utils.constants import PlanEnum


class DiseaseAPI(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    model = Disease

    def get_queryset(self):
        chronic = self.request.query_params.get("chronic", 'true')
        if chronic.lower() == "true":
            return self.model.objects.filter(is_chronic=True)
        elif chronic.lower() == "false":
            return self.model.objects.filter(is_chronic=False)
        return self.model.objects.all()

    def get_serializer_class(self):
        return DiseaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer_class()
        serializer_data = serializer(queryset, many=True)
        return response.Response(data={"result": serializer_data.data}, status=status.HTTP_200_OK)


class PatientPersonalizedAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    default_plan_model = DiseaseDefaultPlan
    personalized_plan_model = PatientPersonalizedPlan

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_diseases = list(user.patient_detail.diseases.values_list("id", flat=True))
        result = []
        if not PatientPersonalizedPlan.objects.filter(patient_id=user.id).exists():
            result = list(self.default_plan_model.objects.filter(disease_id__in=user_diseases).order_by(
                "priority", "created_at").values("exercise_plan", "diet_plan", "medication_plan", "monitoring"))
        elif PatientPersonalizedPlan.objects.filter(patient_id=user.id).exists():
            plans = PatientPersonalizedPlan.objects.filter(patient_id=user.id)
            result = []
            for plan_obj in plans:
                resp = {}
                if plan_obj.plan == PlanEnum.MEDICATIONS.value:
                    resp['medication_plan'] = plan_obj.description
                elif plan_obj.plan == PlanEnum.EXERCISE.value:
                    resp['exercise_plan'] = plan_obj.description
                elif plan_obj.plan == PlanEnum.DIET.value:
                    resp['diet_plan'] = plan_obj.description
                elif plan_obj.plan == PlanEnum.MONITORING.value:
                    resp['monitoring'] = plan_obj.description
                elif plan_obj.plan == PlanEnum.OTHERS.value:
                    resp['others'] = plan_obj.description
                if resp:
                    result.append(resp)
        return response.Response(result, status=status.HTTP_200_OK)




