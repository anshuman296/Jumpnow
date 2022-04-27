from django.db import models
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone

class ChatGroup(Group):
    """ extend Group model to add extra info"""
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        
        return reverse('room', args=[str(self.id)])


def message_file_path(instance, filename):

    return f'{instance.room_id.id}/{instance.username.username}_{filename}'

class ChatMessage(models.Model):
    """ use to store chat history message
        make used of tortoise ORM since its support asyncio ORM
    """ 
    room_id = models.ForeignKey(ChatGroup, null=True, blank=True, on_delete=models.CASCADE)
    username = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    message_type = models.CharField(max_length=50, null=True)
    file_caption = models.CharField(max_length=50, null=True)
    file_field = models.FileField(upload_to=message_file_path, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
