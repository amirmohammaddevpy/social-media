from channels.generic.websocket import AsyncJsonWebsocketConsumer
from users.models import MyUser
from .models import PrivateMessage
from channels.db import database_sync_to_async

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return 
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.other_user = await self.get_user_by_username(self.other_username)
        
        if not self.other_username:
            self.close()
            return
        
        self.room_name = await self.get_name_room(self.user, self.other_user)
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )
        
        await self.accept()
    
    @database_sync_to_async
    def get_user_by_username(self,username):
        try:
            return MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return None
        
    @database_sync_to_async
    def get_name_room(self,sender,handler):
        ids = sorted([sender.id ,handler.id])
        return f"chat_{ids[0]}_{ids[1]}"
    
    @database_sync_to_async
    def save_message(self,message):
        return PrivateMessage.objects.get_or_create(
            sender = self.user,
            handler = self.other_user,
            message = message
        )
    
    
    
    async def receive_json(self, content):
        message = content.get('message')
        
        if not message:
            return None
        
        await self.save_message(message)
        
        await self.channel_layer.group_send(
            self.room_name,{
                'type':'private_message',
                'message':message,
                'sender':self.user.username
            }
        )
    
    async def private_message(self,event):
        message = event['message']
        sender = event['sender']
        await self.send_json({
            'message':message,
            'sender':sender
        })