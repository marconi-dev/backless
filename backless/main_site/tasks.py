from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseBadRequest, JsonResponse
from main_site.models import Storage


@csrf_exempt
def remove_background(request):
    id = request.body.decode('utf-8')
    image = Storage.objects.get(id=int(id))
    try:
        image.remove_background()
    except:
        return HttpResponseBadRequest()

    return JsonResponse({'task': 'completed'})

