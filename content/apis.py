from rest_framework import generics, permissions, status, response, views
from content.models import KnowledgeBase
from content.serializers import KnowledgeBaseSerializer


class ContentAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = KnowledgeBase

    def get_queryset(self):
        user = self.request.user
        user_diseases = list(user.patient_detail.diseases.values_list("id", flat=True))
        return self.model.objects.filter(disease_id__in=user_diseases)

    def get_serializer_class(self):
        return KnowledgeBaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer_class()
        serializer_data = serializer(queryset, many=True)
        return response.Response(data={"result": serializer_data.data}, status=status.HTTP_200_OK)