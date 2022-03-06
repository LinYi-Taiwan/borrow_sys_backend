from channels.generic.websocket import AsyncWebsocketConsumer

socket_list = []


class ChatService(AsyncWebsocketConsumer):
    async def connect(self):
        print('gogogo')
        await self.accept()
        # socket_list.append(self)

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)  
        for ws in socket_list:  
            ws.send(text_data) 

    async def disconnect(self, code):
        pass
