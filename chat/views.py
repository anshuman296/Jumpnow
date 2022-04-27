from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import Group, User


from django.shortcuts import render
from chat.models import ChatGroup, ChatMessage

def main(request):
    #TODO: make sure user assigned to existing group
    assigned_groups = list(request.user.groups.values_list('id', flat=True))
    groups_participated = ChatGroup.objects.filter(id__in=assigned_groups)

    return render(request, 'chat/main.html', {
        'groups_participated': groups_participated
    })

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name
#     })

def get_participants(group_id=None, group_obj=None, user=None):
    """ function to get all participants that belong the specific group """
    
    if group_id:
        chatgroup = ChatGroup.objects.get(id=id)
    else:
        chatgroup = group_obj

    temp_participants = []
    for participants in chatgroup.user_set.values_list('username', flat=True):
        if participants != user:
            temp_participants.append(participants.title())
    temp_participants.append('You')
    return ', '.join(temp_participants)


@login_required
def room(request, room_name):
    if request.user.groups.filter(id=room_name).exists():
        chatgroup = ChatGroup.objects.get(id=room_name)
        other_user = User.objects.filter(groups__id=room_name).exclude(id=request.user.id)[0]
        assigned_groups = list(request.user.groups.values_list('id', flat=True))
        groups_participated = ChatGroup.objects.filter(id__in=assigned_groups)
        return render(request, 'chat/room.html', {
            'chatgroup': chatgroup,
            'participants': get_participants(group_obj=chatgroup, user=request.user.username),
            'groups_participated': groups_participated,
            'other_user': other_user
        })
    else:
        return HttpResponseRedirect(reverse("unauthorized"))

@login_required
def unauthorized(request):
    return render(request, 'chat/unauthorized.html', {})


@login_required
def history(request, room_id):
    chat_message = list(ChatMessage.objects.filter(room_id=room_id).order_by('date_created').values('message', 'username__username', 'date_created'))
    print(chat_message[-1], "(((((((((")
    return JsonResponse(chat_message, safe=False)

@login_required
@csrf_exempt
def save(request):
    message = request.POST.get('message', False)
    room_id = request.POST.get('room_id', False )
    if message and room_id:
        if request.user.is_authenticated:
            cgroup = ChatGroup.objects.get(id=room_id)
            chat_message = ChatMessage.objects.create(room_id=cgroup,
            message=message,
            username=request.user,
            message_type='text'
            )
            print(chat_message, "**")
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)
    return HttpResponse(status=200)

@login_required
@csrf_exempt
def file_save(request, room_name):
    files = request.FILES.getlist('files[]')
    print(files, type(files))
    user = request.user

    room_id = ChatGroup.objects.get(id=room_name)
    return_files = []
    for f in files:
        cm = ChatMessage.objects.create(
            room_id=room_id,
            username=user,
            message_type='file',
            file_field=f
        )
        cm.message = f'<a href="{cm.file_field.url}" target="_blank">View Attachment</a>'
        cm.save()
        file_obj = {
            'name': cm.file_field.name,
            'url': cm.file_field.url
        }
        return_files.append(file_obj)
    return_data = {
        'status': 'success',
        'files': return_files
    }
    return JsonResponse(return_data, status=200)
