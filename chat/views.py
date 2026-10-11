from django.shortcuts import render ,get_object_or_404
from django.db.models import Q
from users.models import MyUser ,BlockUser
from .models import PrivateMessage
from django.contrib.auth.decorators import login_required

# Create your views here.


def get_user_for_chat(user):
    message = PrivateMessage.objects.filter(Q(sender=user) | Q(handler=user))
    
    pertners_ids = set()
    for msg in message:
        if msg.sender != user:
            pertners_ids.add(msg.sender.id)
        if msg.handler != user:
            pertners_ids.add(msg.handler.id)
        
    pertners_ids = MyUser.objects.filter(id__in=pertners_ids)
    return pertners_ids

@login_required(login_url='account:login')
def chats(request):
    chat = get_user_for_chat(request.user)
    unread_message = PrivateMessage.objects.filter(Q(handler=request.user),Q(seen=False))
    
    unread_counts = {}
    
    for message in unread_message:
        sender_id = message.sender.id
        
        if sender_id in unread_counts:
            unread_counts[sender_id] += 1
        else:
            unread_counts[sender_id] = 1
    for chats in chat:
        chats.unread_count = unread_counts.get(chats.id,0)
    
    return render(request,"chat/list_chat.html",{'chats':chat,})


@login_required(login_url='account:login')
def room(request,username):
    other_user = get_object_or_404(MyUser,username=username)
    PrivateMessage.objects.filter(Q(handler=request.user) | Q(sender=other_user)).update(seen=True)
    get_chat = get_user_for_chat(request.user)
    
    unread_message = PrivateMessage.objects.filter(Q(handler=request.user),Q(seen=False))
    
    unread_counts = {}
    
    for message in unread_message:
        sender_id = message.sender.id
        if sender_id in unread_counts:
            unread_counts[sender_id] += 1
        else:
            unread_counts[sender_id] = 1
            
    for chat in get_chat:
        chat.unread_count = unread_counts.get(chat.id,0)
        
    message = PrivateMessage.objects.filter(sender=request.user , handler=other_user) | PrivateMessage.objects.filter(handler=request.user , sender=other_user)
    message = message.order_by('created')
    
    i_blocked = BlockUser.objects.filter(blocker = request.user ,blocked=other_user).exists()
    blocked_me = BlockUser.objects.filter(blocker=other_user,blocked=request.user).exists()
    is_blocked = i_blocked or blocked_me
    
    context = {
    'other_user':other_user,
    'username':username,
    'message':message,
    'i_blocked':i_blocked,
    'blocked_me':blocked_me,
    'is_blocked':is_blocked,
    'chats':get_chat,
    }

    return render(request,"chat/chat.html",context)



def unread_message_count(request):
    if not request.user.is_authenticated:
        return {
            'unread_message_count': 0,
        }
    count_message = PrivateMessage.objects.filter(Q(handler=request.user),Q(seen=False)).count()
    
    return {'unread_messages_count':count_message}
    