from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse
from .forms import StorageForm
from backless.settings import WS_URL


# Create your views here.
class IndexView(CreateView):
    form_class = StorageForm
    template_name = 'main_site/index.html'
   
    def get_success_url(self):
        pk = self.object.id
        return reverse('wait-room', kwargs={'pk': pk})


def wait_room(request, pk):
    ws_url = {"ws_url": f'{WS_URL}/ws/wait/{pk}'}
    return render(request, 'main_site/wait_room.html', ws_url)

