from rest_framework import generics, permissions
from disease_management.models import Disease
from disease_management.serializers import DiseaseSerializer


class DiseaseAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DiseaseSerializer
    model = Disease

    def get_queryset(self):
        chronic = self.request.query_params.get("chronic", 'true')
        if chronic.lower() == "true":
            return self.model.objects.filter(is_chronic=True)
        elif chronic.lower() == "false":
            return self.model.objects.filter(is_chronic=False)
        return self.model.objects.all()
