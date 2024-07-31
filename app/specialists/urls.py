from django.urls import path
from .views import DownloadReportView, MonthlyFormLineListCreate, MonthlyFormHeaderListCreate, ReportDownloadView


urlpatterns = [
    path('monthly-form-headers/', MonthlyFormHeaderListCreate.as_view(), name='monthly-form-header-list-create'),
    path('monthly-form-lines/', MonthlyFormLineListCreate.as_view(), name='monthly-form-line-list-create'),
    path('download_report/', ReportDownloadView.as_view(), name='download-report'),
    path('export_report/', DownloadReportView.as_view(), name='export-report'),

]