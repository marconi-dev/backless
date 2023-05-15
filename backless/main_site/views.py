from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import StorageForm


# Create your views here.
class IndexView(CreateView):
    form_class = StorageForm
    template_name = 'main_site/index.html'
    success_url = reverse_lazy('wait-room')


def wait_room(request):
    ws_url = 'ws://test/'
    return render(request, 'main_site/wait_room.html', {'ws': ws_url})

