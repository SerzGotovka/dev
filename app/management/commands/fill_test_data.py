from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Organization, SpecialistIndicator
from specialists.models import MonthlyFormHeader, MonthlyFormLine
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        # Создаем организацию
        organization = Organization.objects.create(name='Test Organization')

        # Создаем пользователей
        user1 = User.objects.create_user(username='user1', password='password')
        user2 = User.objects.create_user(username='user2', password='password')

        # Создаем SpecialistIndicator
        for i in range(10):
            SpecialistIndicator.objects.create(
                date_actual=datetime.now().date(),
                article_name=f'Article {i+1}',
                article_order=i+1,
                modified_by=user1 if i % 2 == 0 else user2
            )

        # Создаем MonthlyFormHeader
        for i in range(3):
            header = MonthlyFormHeader.objects.create(
                report_start_date=datetime.now().date() - timedelta(days=i*30),
                report_end_date=datetime.now().date() - timedelta(days=(i-1)*30),
                organization=organization
            )

            # Создаем MonthlyFormLine
            for j in range(5):
                MonthlyFormLine.objects.create(
                    specialist_indicator=SpecialistIndicator.objects.all()[j],
                    monthly_form_header=header,
                    distribution_count=10 + j,
                    target_distribution_count=5 + j,
                    modified_by=user1 if j % 2 == 0 else user2
                )

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with test data'))