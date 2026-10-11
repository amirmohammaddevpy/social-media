from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from users.models import MyUser
from post.models import Posts ,ReportPost
from notification.models import Notification
from django.http import JsonResponse
from story.forms import StoryForm
from django.contrib import messages
from story.models import Story
from itertools import groupby
from operator import attrgetter
from django.utils import timezone
import datetime
# Create your views here.

@login_required(login_url='account:login')
def home(request):
    user_profile = get_object_or_404(MyUser, username=request.user)
    following_users = user_profile.following.all()
    post_followers = Posts.objects.filter(user__in=following_users).order_by('-id')
    active_stories = Story.objects.filter(user__in=following_users, seen=False ).order_by('user')
    now = timezone.now()
    finaly_time = now - datetime.timedelta(hours=24)
    
    Story.objects.filter(
        user__in = following_users,
        date__lte=finaly_time,
    ).delete()
    
    for story in active_stories:
        story.date
    
    grouped_stories = []
    for user, user_stories in groupby(active_stories, key=attrgetter('user')):
        grouped_stories.append({
            'user': user,
            'stories': list(user_stories),
        })
    

    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        get_story = request.FILES.get('story')
            
        if form.is_valid():
            if get_story and get_story.size > 10 * 1024 * 1024:
                messages.error(request, "File size is too big! (Max 10MB)")
                return redirect("home:home")
            else:
                new_story = form.save(commit=False)
                new_story.user = request.user
                new_story.save()
                messages.success(request, 'Story uploaded successfully!')
                return redirect("home:home")
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = StoryForm()
        
    context = {
        'follow': following_users,
        'post': post_followers,
        'story':active_stories,
        'form': form,
    }
    return render(request, "home/home.html", context)

@login_required(login_url='account:login')
def explore(request):
    post = Posts.objects.all()
    return render(request,'home/explore.html',{'posts':post})

@login_required(login_url='account:login')
def search(request):
    search_bar = request.GET.get('q',' ')
    res = MyUser.objects.filter(username=search_bar)
    
    return render(request,"home/search.html",{'results':res})

@login_required(login_url='account:login')
def api_documentation(request):
    return render(request ,"home/api_documentation.html")


def check_notif(request):
    notif = Notification.objects.filter(receiver=request.user,is_read=False).select_related('user').order_by('-created_at')
    
    data = [
        {
            'id':n.id,
            'username':n.user.username,
            'avatar':n.user.avatar.url,
            'message':n.message,
            'profile':f'profile/{n.user.username}',
            'created_at':n.created_at,
            'is_read':n.is_read,
        }
        for n in notif
    ]
    return JsonResponse({
        'notifications':data,
        'count':notif.count()
    })
