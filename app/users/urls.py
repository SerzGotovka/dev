from django.urls import path
from .views import (
    OrganizationListCreate, 
    SpecialistIndicatorListCreate, 
)


urlpatterns = [
    path('organizations/', OrganizationListCreate.as_view(), name='organization-list-create'),
    path('specialist-indicators/', SpecialistIndicatorListCreate.as_view(), name='specialist-indicator-list-create'),
]