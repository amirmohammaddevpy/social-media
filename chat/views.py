from django.shortcuts import render ,get_object_or_404
from django.db.models import Q
from users.models import MyUser
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
    
    return render(request,"chat/list_chat.html",{'chats':chat})

def room(request,username):
    other_user = get_object_or_404(MyUser,username=username)
    message = PrivateMessage.objects.filter(sender=request.user , handler=other_user) | PrivateMessage.objects.filter(handler=request.user , sender=other_user)
    message = message.order_by('created')
    return render(request,"chat/chat.html",{'username':username,'message':message})