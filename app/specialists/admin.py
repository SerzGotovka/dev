from django.contrib import admin
from .models import MonthlyFormHeader, MonthlyFormLine


admin.site.register(MonthlyFormLine)

admin.site.register(MonthlyFormHeader)

