from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from users.models import MyUser ,Contact ,BlockUser
from .forms import EditProfile
from django.contrib import messages
from post.models import Posts
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from notification.models import Notification
from django.utils import timezone
from datetime import timedelta


# Create your views here.
@login_required(login_url="account:register")
def profile(request,username):
    profile = get_object_or_404(MyUser,username=username)
    i_blocked_them = BlockUser.objects.filter(blocker=request.user , blocked=profile).exists()
    they_blocked_me = BlockUser.objects.filter(blocker=profile,blocked=request.user)
    is_blocked_either_way = i_blocked_them or they_blocked_me
    post = Posts.objects.filter(user=profile)
    block_user = BlockUser.objects.filter(blocker=request.user)
    
    context = {
        "profile":profile,
        'post':post,
        'get_block_user':block_user,
        'i_blocked_them':i_blocked_them,
        'they_blocked_me':they_blocked_me,
        "is_blocked_either_way":is_blocked_either_way,
        "last_seen_seconds":profile.last_seen,  
    }
    return render(request,"profile/profile.html",context)

@require_POST
def follow(request,username):
    user_get_follow = get_object_or_404(MyUser,username=username)
    
    try:
        user = Contact.objects.filter(user_form = request.user , user_to = user_get_follow)
        if user.exists():
            user.delete()
            Notification.objects.create(
                user = request.user,
                message = 'end following you',
                receiver = user_get_follow,
            )
            return JsonResponse({'status':'unfollow'})
        else:
            Contact.objects.create(user_form=request.user,user_to=user_get_follow)
            Notification.objects.create(
                user = request.user,
                message = 'start following you',
                receiver = user_get_follow,
            )
            return JsonResponse({'status':'follow'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})
    

@login_required(login_url="account:register")
def edit_profile(request,username):
    user = MyUser.objects.get(username=username)
    form = EditProfile(instance=user)
    
    if request.user != user:
        return render("profiles:profile",request.user)
    if request.method == "POST":
        form = EditProfile(request.POST,files=request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profiles:profile",request.user)
        else:
            messages.error(request,'form is not valid')
    else:
        form = EditProfile(instance=request.user)
    return render(request,"profile/edite_profile.html",{'form':form,'profile':user})

def list_followers(request,username):
    get_user = get_object_or_404(MyUser,username=username)
    followers = get_user.followers.all()
    
    return render(request,"profile/followers.html",{'followers':followers,})


def list_following(request,username):

    get_user = get_object_or_404(MyUser,username=username)
    following_user = get_user.following.all()
    return render(request,"profile/following.html",{'following':following_user})

def delete_account(requst,pk):
    MyUser.objects.filter(id=pk).delete()
    return redirect("account:register")


@require_POST
def block_unblock_user(request,username):
    get_user = get_object_or_404(MyUser,username=username)
    
    try:
        block_user = BlockUser.objects.filter(blocker=request.user,blocked=get_user)
        if block_user.exists():
            block_user.delete()
            return JsonResponse({'status':'unblock'})
        else:
            block_user.create(
                blocker = request.user,
                blocked = get_user,
            )
            return JsonResponse({'status':'block'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})
    
    
@login_required
@require_POST
def heartbeat(request, username):
    if request.user.username != username:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    request.user.online = True
    request.user.last_seen = timezone.now()
    request.user.save(update_fields=['online', 'last_seen'])

    return JsonResponse({'ok': True})

OFFLINE_THRESHOLD = timedelta(seconds=30)

@login_required
@require_POST
def check_online(request,):
    
    data = json.loads(request.body or {""})
    username = data.get("username")
    if not username:
        return JsonResponse({'error': 'username is required'})
    
    profile = get_object_or_404(MyUser,username=username)
    now = timezone.now()
    seconds_since_seen = (now - profile.last_seen).total_seconds() if profile.last_seen else None
    
    is_really_online = (
        profile.online
        and profile.last_seen is not None
        and (now - profile.last_seen) < OFFLINE_THRESHOLD
    )
    
    
    
    return JsonResponse({
        'online': is_really_online,
        'last_seen_seconds': seconds_since_seen,
    })