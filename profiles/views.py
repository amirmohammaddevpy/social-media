from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from users.models import MyUser ,Contact
from .forms import EditProfile
from django.contrib import messages
from post.models import Posts
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.
@login_required(login_url="account:register")
def profile(request,username):
    profile = get_object_or_404(MyUser,username=username)
    post = Posts.objects.filter(user=profile)
    return render(request,"profile/profile.html",{"profile":profile,'post':post})

@require_POST
def follow(request,username):
    user_get_follow = get_object_or_404(MyUser,username=username)
    
    try:
        user = Contact.objects.filter(user_form = request.user , user_to = user_get_follow)
        if user.exists():
            user.delete()
            return JsonResponse({'status':'unfollow'})
        else:
            Contact.objects.create(user_form=request.user,user_to=user_get_follow)
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
    print(followers)
    
    return render(request,"profile/followers.html",{'followers':followers,})


def list_following(request,username):

    get_user = get_object_or_404(MyUser,username=username)
    following_user = get_user.following.all()
    return render(request,"profile/following.html",{'following':following_user})

def delete_account(requst,pk):
    MyUser.objects.filter(id=pk).delete()
    return redirect("account:register")