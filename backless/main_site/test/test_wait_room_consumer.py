from channels.consumer import get_channel_layer
from channels.testing import WebsocketCommunicator
from main_site.routing import websocket_urls
from channels.routing import URLRouter
from django.test import TestCase


class WaitRoomTestCase(TestCase):
    async def test_websocket_connection_success(self):
        application = URLRouter(websocket_urls)
        communicator = WebsocketCommunicator(application, "ws/wait/1")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_channels_group_created_correctly(self):
        channel_layer = get_channel_layer()
        application = URLRouter(websocket_urls)
        communicator = WebsocketCommunicator(application, "ws/wait/1")
        await communicator.connect()
        await channel_layer.group_send("1", {"type":"wait.inform",
                                             "data": "task-received"})
        data = await communicator.receive_from()
        self.assertEqual(data, "task-received")
        await communicator.disconnect()

