from .models import MonthlyFormLine
from django.db.models import Sum
from datetime import datetime, timedelta


def get_report_sums(start_date, end_date):
    """Подсчет общего кол-ва молодых специалистов"""
    report_data = MonthlyFormLine.objects.filter(
        monthly_form_header__report_start_date__gte=start_date,
        monthly_form_header__report_end_date__lte=end_date,
    ).aggregate(
        total_distribution_count=Sum("distribution_count"),
        total_target_distribution_count=Sum("target_distribution_count"),
    )

    total_distribution_count = report_data.get("total_distribution_count", 0) or 0
    total_target_distribution_count = (
        report_data.get("total_target_distribution_count", 0) or 0
    )
    total = total_distribution_count + total_target_distribution_count
    return total


def get_report_sums2(specialist_indicator_id, start_date, end_date):
    """Подсчет общего кол-ва молодых специалистов в зависимости от статьи(id)"""
    report_data = MonthlyFormLine.objects.filter(
        monthly_form_header__report_start_date__gte=start_date,
        monthly_form_header__report_end_date__lte=end_date,
        specialist_indicator_id=specialist_indicator_id,
    ).aggregate(
        total_distribution_count=Sum("distribution_count"),
        total_target_distribution_count=Sum("target_distribution_count"),
    )

    total_distribution_count = report_data.get("total_distribution_count", 0) or 0
    total_target_distribution_count = (
        report_data.get("total_target_distribution_count", 0) or 0
    )
    total = total_distribution_count + total_target_distribution_count
    return total_distribution_count, total_target_distribution_count, total
