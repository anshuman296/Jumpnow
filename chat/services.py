from chat.models import ChatMessage
from channels.db import database_sync_to_async

async def connect(self):
    self.message = await database_sync_to_async(self.chat_save_message)()

def chat_save_message(self, username, room_id, message):

    """ function to store chat message in sqlite """

    ChatMessage.objects.create(room_id=room_id,  
                            username=username,
                            message=message, 
                       )