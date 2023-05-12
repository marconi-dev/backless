import grpc
from google.cloud import tasks_v2beta3
from google.cloud.tasks_v2.services.cloud_tasks.transports import CloudTasksGrpcTransport
from google.cloud.tasks_v2 import CloudTasksClient


def fake_queue_client():
    """
    Uses the local task queue
    local task queue used in this project.
    https://github.com/aertje/cloud-tasks-emulator
    """
    channel = grpc.insecure_channel('localhost:8123')
    transport = CloudTasksGrpcTransport(channel=channel)
    client = CloudTasksClient(transport=transport)
    return client

