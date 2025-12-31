from django.shortcuts import render ,get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import MyUser
from post.models import Posts
# Create your views here.

@login_required(login_url='account:login')
def home(request):
    follow = get_object_or_404(MyUser,username=request.user)
    post_followers = Posts.objects.filter(user__in= follow.following.all())
    print(post_followers)
    
    return render(request,"home/home.html",{'follow':follow,'post':post_followers})


@login_required(login_url='account:login')
def explore(request):
    post = Posts.objects.all()
    return render(request,'home/explore.html',{'posts':post})

@login_required(login_url='account:login')
def search(request):
    search_bar = request.GET.get('q',' ')
    res = MyUser.objects.filter(username=search_bar)
    
    return render(request,"home/search.html",{'results':res})