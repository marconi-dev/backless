import json
from django.conf import settings
from google.cloud import tasks_v2beta3
from .utils import fake_queue_client

if settings.DEBUG:
    client = fake_queue_client()
else:
    client = tasks_v2beta3.CloudTasksClient()


def send_task(url, http_method='POST', payload=None):
    """ Send task to be executed """

    parent = client.queue_path(
        settings.PROJECT_NAME, 
        settings.QUEUE_REGION, 
        queue=settings.QUEUE_ID
    )

    task = {
        'http_request': {
            'http_method': http_method,
            'url': f'{settings.WORKER_URL}/{url}'
        }
    }

    if isinstance(payload, dict):
        payload = json.dumps(payload)

    if payload is not None:
        converted_payload = payload.encode()
        task['http_request']['body'] = converted_payload

    response = client.create_task(parent=parent, task=task)

    return response

