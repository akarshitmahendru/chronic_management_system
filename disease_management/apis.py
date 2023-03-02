from rest_framework import generics, permissions, status, response
from disease_management.models import Disease
from disease_management.serializers import DiseaseSerializer


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
