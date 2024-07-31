from datetime import datetime, timedelta
from django.db.models import Sum


def get_current_period_and_year(request):
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    current_month_rus = {
        "January": "Январь",
        "February": "Февраль",
        "March": "Март",
        "April": "Апрель",
        "May": "Май",
        "June": "Июнь",
        "July": "Июль",
        "August": "Август",
        "September": "Сентябрь",
        "October": "Октябрь",
        "November": "Ноябрь",
        "December": "Декабрь",
    }[current_month]

    # Получение данных из формы
    period = request.GET.get("period", f"{current_month_rus}-{current_month_rus}")
    year = request.GET.get("year", str(current_year))

    return period, year


def get_start_end_dates(period, year):
    months_mapping = {
        "Январь": 1,
        "Февраль": 2,
        "Март": 3,
        "Апрель": 4,
        "Май": 5,
        "Июнь": 6,
        "Июль": 7,
        "Август": 8,
        "Сентябрь": 9,
        "Октябрь": 10,
        "Ноябрь": 11,
        "Декабрь": 12,
    }
    start_month, end_month = period.split("-")
    start_date = datetime(int(year), months_mapping[start_month], 1)
    end_date = datetime(int(year), months_mapping[end_month], 1) + timedelta(days=31)
    end_date = end_date.replace(day=1) - timedelta(days=1)
    return start_date, end_date
