import openpyxl
from openpyxl import Workbook
from datetime import datetime, timedelta
from django.db.models import Q, Count, QuerySet
from .models import Robot

date_now = datetime.now()
date_week_ago = str(date_now - timedelta(days=7))

def get_db_data() -> list[QuerySet]:
    models = Robot.objects.values_list('model', flat=True).distinct()
    production = []
    for model in models:
        exact_model = Robot.objects.filter(model=model)
        model_efficiency = exact_model.filter(
            Q(created__gte=date_week_ago) & Q(created__lte=date_now)).values('model', 'version').annotate(count_by_week=Count('serial'))
        production.append(model_efficiency)
    return production


def create_report() -> Workbook:
    production = get_db_data()
    report_data = openpyxl.Workbook()
    for index, note in enumerate(production):
        sheet = report_data.create_sheet(f'Страница{index + 1}', index)
        sheet['A1'] = 'Модель'
        sheet['B1'] = 'Версия'
        sheet['C1'] = 'Количество за неделю'
        row = 2
        for robot in note:
            sheet[row][0].value = robot['model']
            sheet[row][1].value = robot['version']
            sheet[row][2].value = robot['count_by_week']
            row += 1
    return report_data