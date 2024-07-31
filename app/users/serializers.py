from rest_framework import serializers
from .models import Organization, SpecialistIndicator


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class SpecialistIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistIndicator
        fields = "__all__"
