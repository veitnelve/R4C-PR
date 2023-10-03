import json
import jsonschema
import datetime
from jsonschema import validate
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views import View
from django.core.files.temp import NamedTemporaryFile
from .models import Robot
from .logic import create_report
from django.views.decorators.csrf import csrf_exempt


"""Add robot function"""
@csrf_exempt
def add_robot(request):
    data = json.loads(request.body)
    """Web request data validation"""

    with open('schema.json', 'r') as valid_schema:
        schema = json.load(valid_schema)

    try:
        validate(data, schema)

    except jsonschema.ValidationError as e:
        return HttpResponseBadRequest(str(e))
    
    model = data.get('model')
    version = data.get('version')
    created = data.get('created')
    serial = f'{model}-{version}'

    robot = Robot.objects.create(serial=serial, model=model, version=version, created=created)

    return JsonResponse({'id': robot.id, 'serial': robot.serial})

def download_report(request):
     with NamedTemporaryFile() as file_:
        report_workbook = create_report()
        report_workbook.save(file_.name)
        response = HttpResponse(file_, content_type='xlsx')
        response_file_name = f'report-{datetime.datetime.now()}.xlsx'
        response['Content-Disposition'] = f'attachment; filename={response_file_name}'
        return response