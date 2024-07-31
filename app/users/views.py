from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization, SpecialistIndicator
from .serializers import OrganizationSerializer, SpecialistIndicatorSerializer


class OrganizationListCreate(APIView):
    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialistIndicatorListCreate(APIView):
    def get(self, request):
        indicators = SpecialistIndicator.objects.all()
        serializer = SpecialistIndicatorSerializer(indicators, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecialistIndicatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
