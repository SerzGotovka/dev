from django.db import models
from users.models import SpecialistIndicator, Organization
from django.contrib.auth.models import User


class MonthlyFormHeader(models.Model):
    """Форма 2: Шапка месячных форм молодых специалистов"""

    report_start_date = models.DateField(verbose_name="Дата начала отчетного периода")
    report_end_date = models.DateField(verbose_name="дата окончания отчетного периода")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Организация"
    )
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "form_header"
        verbose_name = "Шапка форм"
        verbose_name_plural = "Шапки форм"

    def __str__(self):
        return f'{self.organization}: {self.report_start_date} - {self.report_end_date}'

class MonthlyFormLine(models.Model):
    """Форма 3: Линии месячных форм молодых специалистов"""

    specialist_indicator = models.ForeignKey(
        SpecialistIndicator, on_delete=models.CASCADE, verbose_name="Специалист"
    )
    monthly_form_header = models.ForeignKey(
        MonthlyFormHeader,
        on_delete=models.CASCADE,
        verbose_name="Форма молодого специалиста",
    )
    distribution_count = models.IntegerField(
        verbose_name="Специалистов по распределению"
    )
    target_distribution_count = models.IntegerField(
        verbose_name="Специалистов по целевому"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кем изменено",
    )
    modified_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "form_liner"
        verbose_name = "Линия форм"
        verbose_name_plural = "Линии форм"

    def __str__(self):
        return self.specialist_indicator