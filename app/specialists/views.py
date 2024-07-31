from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MonthlyFormHeader, MonthlyFormLine
from .serializers import MonthlyFormHeaderSerializer, MonthlyFormLineSerializer
from django.shortcuts import render
import xlsxwriter
from django.http import HttpResponse
from .utils import get_current_period_and_year, get_start_end_dates
from django.views import View
from .orm import *
from django.db.models import Sum


class MonthlyFormHeaderListCreate(APIView):
    def get(self, request):
        headers = MonthlyFormHeader.objects.all()
        serializer = MonthlyFormHeaderSerializer(headers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MonthlyFormHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonthlyFormLineListCreate(APIView):
    def get(self, request):
        lines = MonthlyFormLine.objects.all()
        serializer = MonthlyFormLineSerializer(lines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MonthlyFormLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDownloadView(View):
    def get(self, request):
        return render(request, "specialists/report.html")


class DownloadReportView(APIView):

    def get(self, request, *args, **kwargs):
        if request.method == "GET":

            # Получение данных из формы
            period, year = get_current_period_and_year(request)
            start_date, end_date = get_start_end_dates(period, year)

            total = get_report_sums(
                start_date, end_date
            )  # общая численность специалистов
            total_distribution_count1, total_target_distribution_count1, total1 = (
                get_report_sums2(1, start_date, end_date)
            )  # Кол-во Направлен комиссией на основании
            total_distribution_count4, total_target_distribution_count4, total4 = (
                get_report_sums2(4, start_date, end_date)
            )  # Кол-во уволенных специалистов
            total_distribution_count10, total_target_distribution_count10, total10 = (
                get_report_sums2(10, start_date, end_date)
            )  # Кол-во истечение срока об. отработки
            total_distribution_count9, total_target_distribution_count9, total9 = (
                get_report_sums2(9, start_date, end_date)
            )  # Кол-во призыв на срочную службу
            total_distribution_count8, total_target_distribution_count8, total8 = (
                get_report_sums2(8, start_date, end_date)
            )  # Кол-во поступления в учреждения образования
            total_distribution_count7, total_target_distribution_count7, total7 = (
                get_report_sums2(7, start_date, end_date)
            )  # Кол-во переезд в другую местность
            total_distribution_count6, total_target_distribution_count6, total6 = (
                get_report_sums2(6, start_date, end_date)
            )  # Кол-во дискредитирующие обстоятельства
            total_distribution_count5, total_target_distribution_count5, total5 = (
                get_report_sums2(5, start_date, end_date)
            )  # Кол-во отсутствие жилья

            # Создание HTTP-ответа с указанием на скачивание Excel файла
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f"attachment; filename=report_{year}.xlsx"

            # Создание книги Excel
            workbook = xlsxwriter.Workbook(response, {"in_memory": True})
            worksheet = workbook.add_worksheet()

            # Определение формата для жирного текста
            bold_format = workbook.add_format(
                {
                    "bold": True,
                    "align": "center",
                }
            )

            format = workbook.add_format(
                {
                    "align": "center",
                }
            )

            # Определение формата для слияния ячеек и центрирования текста
            merge_format = workbook.add_format(
                {"align": "center", "valign": "vcenter", "border": 1, "text_wrap": True}
            )

            # Определение формата для вертикального текста с границами и центрированием
            vertical_format = workbook.add_format(
                {"align": "center", "valign": "vcenter", "border": 1, "rotation": 90}
            )

            # Слияние ячеек от A2 до X2 и добавление текста
            worksheet.merge_range("A2:X2", "молодые специалисты", bold_format)

            # Слияние ячеек от A3 до X3 и добавление текста с данными из формы
            worksheet.merge_range("A3:X3", f"{period} {year} года", format)

            # Слияние ячеек от A4 до A6 и добавление текста "наименование организации"
            worksheet.merge_range("A4:A6", "наименование организации", merge_format)

            # Слияние ячеек от A4 до A6 и добавление текста "наименование организации"
            worksheet.merge_range(
                "B4:B6", "Общая численность молодых специалистов", merge_format
            )

            worksheet.merge_range(
                "C4:E4", "Направлен комиссией на основании", merge_format
            )

            worksheet.merge_range("C5:C6", "Всего", merge_format)

            worksheet.merge_range(
                "D5:E5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("D6", "Целевое", vertical_format)

            worksheet.write("E6", "Распределение", vertical_format)

            worksheet.merge_range(
                "F4:F6", "Количество уволенных молодых специалистов", merge_format
            )

            worksheet.merge_range(
                "G4:I4", "Истечение срока обязательной отработки", merge_format
            )

            worksheet.merge_range("G5:G6", "Всего", merge_format)

            worksheet.merge_range(
                "H5:I5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("H6", "Целевое", vertical_format)

            worksheet.write("I6", "Распределение", vertical_format)

            worksheet.merge_range("J4:L4", "Призыв на срочную службу", merge_format)

            worksheet.merge_range("J5:J6", "Всего", merge_format)

            worksheet.merge_range(
                "K5:L5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("K6", "Целевое", vertical_format)

            worksheet.write("L6", "Распределение", vertical_format)

            worksheet.merge_range(
                "M4:O4", "Поступление в учреждение образования", merge_format
            )

            worksheet.merge_range("M5:M6", "Всего", merge_format)

            worksheet.merge_range(
                "N5:O5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("N6", "Целевое", vertical_format)

            worksheet.write("O6", "Распределение", vertical_format)

            worksheet.merge_range("P4:R4", "Переезд в другую местность", merge_format)

            worksheet.merge_range("P5:P6", "Всего", merge_format)

            worksheet.merge_range(
                "Q5:R5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("Q6", "Целевое", vertical_format)

            worksheet.write("R6", "Распределение", vertical_format)

            worksheet.merge_range(
                "S4:U4", "Дискредитирующие обстоятельства", merge_format
            )

            worksheet.merge_range("S5:S6", "Всего", merge_format)

            worksheet.merge_range(
                "T5:U5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("T6", "Целевое", vertical_format)

            worksheet.write("U6", "Распределение", vertical_format)

            worksheet.merge_range("V4:X4", "Отсутствие жилья", merge_format)

            worksheet.merge_range("V5:V6", "Всего", merge_format)

            worksheet.merge_range(
                "W5:X5", "Категория источника приема на работу", merge_format
            )

            worksheet.write("W6", "Целевое", vertical_format)

            worksheet.write("X6", "Распределение", vertical_format)

            worksheet.write("A7", "Итого:", merge_format)

            worksheet.write_number("B7", total, bold_format)

            worksheet.write_number("C7", total1, bold_format)
            worksheet.write_number("D7", total_distribution_count1, bold_format)
            worksheet.write_number("E7", total_target_distribution_count1, bold_format)

            worksheet.write_number("F7", total4, bold_format)

            worksheet.write_number("G7", total10, bold_format)
            worksheet.write_number("H7", total_distribution_count10, bold_format)
            worksheet.write_number("I7", total_target_distribution_count10, bold_format)

            worksheet.write_number("J7", total9, bold_format)
            worksheet.write_number("K7", total_distribution_count9, bold_format)
            worksheet.write_number("L7", total_target_distribution_count9, bold_format)

            worksheet.write_number("M7", total8, bold_format)
            worksheet.write_number("N7", total_distribution_count8, bold_format)
            worksheet.write_number("O7", total_target_distribution_count8, bold_format)

            worksheet.write_number("P7", total7, bold_format)
            worksheet.write_number("Q7", total_distribution_count7, bold_format)
            worksheet.write_number("R7", total_target_distribution_count7, bold_format)

            worksheet.write_number("S7", total6, bold_format)
            worksheet.write_number("T7", total_distribution_count6, bold_format)
            worksheet.write_number("U7", total_target_distribution_count6, bold_format)

            worksheet.write_number("V7", total5, bold_format)
            worksheet.write_number("W7", total_distribution_count5, bold_format)
            worksheet.write_number("X7", total_target_distribution_count5, bold_format)

            # Закрытие книги
            workbook.close()

            return response

        return render(request, "form_template.html")
