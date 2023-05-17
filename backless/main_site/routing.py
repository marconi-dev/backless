from django.urls import path
from .consumers import WaitRoomConsumer as WRc


websocket_urls = [
    path('ws/wait/<int:pk>', WRc.as_asgi(), name='wait-consumer')
]

