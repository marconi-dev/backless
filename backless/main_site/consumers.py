from channels.generic.websocket import AsyncJsonWebsocketConsumer
from main_site.models import Storage
from django.core.exceptions import ObjectDoesNotExist


class WaitRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs'].get('pk')
        await self.create_group(str(self.group_name))
        return await self.accept()

    async def create_group(self, group_name):
        args = (group_name, self.channel_name)
        return await self.channel_layer.group_add(*args)

    async def wait_inform(self, event):
        return await self.send(text_data=event["data"])

    async def disconnect(self, code):
        id = int(self.group_name)
        status = await self.delete_storage(id)
        return status

    async def delete_storage(self, id):
        try:
            storage = await Storage.objects.aget(id=id) 
            await storage.adelete()
            return "storage-deleted"
        except ObjectDoesNotExist:
            return "not-found"

