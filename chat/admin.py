from django.contrib import admin
from chat.models import ChatGroup, ChatMessage

# Register your models here.
class ChatGroupAdmin(admin.ModelAdmin):
    """ enable Chart Group admin """
    list_display = ('id', 'name', 'description', 'icon', 'mute_notifications', 'date_created', 'date_modified')
    list_filter = ('id', 'name', 'description', 'icon', 'mute_notifications', 'date_created', 'date_modified')
    list_display_links = ('name',)

admin.site.register(ChatGroup, ChatGroupAdmin)

admin.site.register(ChatMessage)