from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WaitRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        group_name = self.scope['url_route']['kwargs'].get('pk')
        await self.create_group(str(group_name))
        return await self.accept()

    async def create_group(self, group_name):
        args = (group_name, self.channel_name)
        return await self.channel_layer.group_add(*args)

    async def wait_inform(self, event):
        return await self.send(text_data=event["data"])

