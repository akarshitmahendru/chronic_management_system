from disease_management.models import Disease
from rest_framework import serializers


class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ('id', 'disease_name', 'description', 'image')
