from rest_framework import serializers
from content.models import KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    disease_name = serializers.SerializerMethodField()

    def get_disease_name(self, obj):
        return obj.disease.disease_name

    class Meta:
        model = KnowledgeBase
        fields = ("id", "disease_name", "video_link", "image_link", "description")