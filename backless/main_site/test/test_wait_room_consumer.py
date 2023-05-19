from channels.consumer import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.core.files.uploadedfile import SimpleUploadedFile
from main_site.routing import websocket_urls
from channels.routing import URLRouter
from django.test import TestCase
from main_site.models import Storage


class WaitRoomTestCase(TestCase):
    async def start_communicator(self, id=1):
        application = URLRouter(websocket_urls)
        communicator = WebsocketCommunicator(application, f"ws/wait/{id}")
        connected, _ = await communicator.connect()
        return connected, communicator

    async def group_send(self, group, data):
        channel_layer = get_channel_layer()
        info = {"type": "wait.inform", "data": data}
        await channel_layer.group_send(str(group), info)

    async def create_storage(self):
        ASSETS_DIR = 'main_site/test/testing_assets'
        image_file = SimpleUploadedFile(
            name="astolfo.jpg",
            content=open(f'{ASSETS_DIR}/astolfo.jpg', 'rb').read(),
            content_type="image/jpeg")
        return await Storage.objects.acreate(image=image_file)

    async def test_websocket_connection_success(self):
        connected, communicator = await self.start_communicator()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_channels_group_created_correctly(self):
        _, communicator = await self.start_communicator()
        await self.group_send(1, "task-received")
        data = await communicator.receive_from()
        self.assertEqual(data, "task-received")
        await communicator.disconnect()

    async def test_storage_deleted_on_disconnect(self):
        storage = await self.create_storage()
        self.assertIsInstance(storage, Storage)
        _, communicator = await self.start_communicator(storage.id) 
        await communicator.disconnect()
        count = await Storage.objects.acount()
        self.assertEqual(count, 0)

