from rest_framework import serializers
from .models import MonthlyFormHeader, MonthlyFormLine


class MonthlyFormHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyFormHeader
        fields = "__all__"


class MonthlyFormLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyFormLine
        fields = "__all__"
