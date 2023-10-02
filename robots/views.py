import json
import jsonschema
from jsonschema import validate
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Robot
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

    robots = Robot.objects.all()
    print(robots)

    return JsonResponse({'id': robot.id, 'serial': robot.serial})

