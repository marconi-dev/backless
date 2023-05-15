from django.urls import path
from .views import IndexView, wait_room
from .tasks import remove_background

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('wait/', wait_room, name='wait-room'),
    path('_tasks/remove-background/', remove_background, name='bg-remove-task')
]
