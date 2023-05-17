from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from main_site.models import Storage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def inform_progress(group_name, data):
    channel_layer = get_channel_layer()
    args = (group_name, {"type":"wait.inform", "data": data})
    async_to_sync(channel_layer.group_send)(*args)

@csrf_exempt
def remove_background(request):
    id = request.body.decode('utf-8')
    inform_progress(group_name=id, data="task-received")

    image = Storage.objects.get(id=int(id))
    image.remove_background()
    image_url = image.image.url
    image_name = image.image.name
    data = f'{image_url} {image_name}'

    inform_progress(group_name=id, data=data)
    return JsonResponse({'task': 'completed'})

