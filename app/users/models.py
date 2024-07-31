from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "organization"
        verbose_name = "Организация"
        verbose_name_plural = "организации"

    def __str__(self):
        return self.name


class SpecialistIndicator(models.Model):
    """Форма 1: Показатели молодых специалистов"""

    date_actual = models.DateField(verbose_name="Дата актуальности")
    article_name = models.CharField(max_length=255, verbose_name="Название статьи")
    article_order = models.IntegerField(verbose_name="Порядок статей")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="Изменение статьи")
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кем изменена статья",
    )

    class Meta:
        db_table = "specialist"
        verbose_name = "Специалист"
        verbose_name_plural = "специалисты"

    def __str__(self):
        return self.article_name
