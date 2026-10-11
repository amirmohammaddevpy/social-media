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

    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name,
            )

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
        return PrivateMessage.objects.create(
            sender = self.user,
            handler = self.other_user,
            message = message
        )

    @database_sync_to_async
    def mark_messages_as_seen(self):
        PrivateMessage.objects.filter(
            sender = self.other_user,
            handler = self.user,
            seen = False,
        ).update(seen=True)



    async def receive_json(self, content):
        if content.get('type') == 'seen':
            await self.mark_messages_as_seen()

            await self.channel_layer.group_send(
                self.room_name, {
                    'type': 'seen_notification',
                    'seer': self.user.username,
                }
            )
            return

        message = content.get('message')
        if not message:
            return

        msg = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_name,{
                'type':'private_message',
                'id': msg.id,
                'message': msg.message,
                'sender': self.user.username,
                'created': msg.created.isoformat(),
                'seen': msg.seen,
            }
        )

    async def private_message(self,event):
        await self.send_json({
            'id': event['id'],
            'message': event['message'],
            'sender': event['sender'],
            'created': event['created'],
            'seen': event['seen'],
        })

    async def seen_notification(self, event):
        await self.send_json({
            'type': 'seen',
            'seer': event['seer'],
        })