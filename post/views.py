from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required 
from .forms import CreatPostForm ,CommentForm
from django.contrib import messages
from .models import Posts,Comment
from django.http import JsonResponse
from users.models import MyUser
from django.views.decorators.http import require_POST

# Create your views here.


def detail_post(request,pk):
    posts = Posts.objects.get(id=pk)
    comment = Comment.objects.filter(post=posts)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.post = posts
            user.save()
            return redirect('posts:detail_post',posts.id)
        else:
            messages.error(request,'for is not valid!!')
    return render(request,"posts/detail.html",{'detail':posts,'form':form,'comments':comment,})



@login_required(login_url='account:login')
def create_post(request,username):
    form = CreatPostForm()
    if request.method == "POST":
        form = CreatPostForm(request.POST,files=request.FILES,)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect("profiles:profile",request.user)
        else:
            messages.error(request,"form is not valid")
    else:
        form = CreatPostForm()
    return render(request,"posts/create_post.html",{'form':form})


@login_required(login_url='account:login')
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Posts, id=pk)
    
    try:
        user = MyUser.objects.get(id=request.user.id)
        
        if user in post.user_like.all():
            post.user_like.remove(user)
            return JsonResponse({'status':'like'})
        else:
            post.user_like.add(user)
            return JsonResponse({'status':'liked'})
    except:
        return JsonResponse({'status':'error'})
        

def delete_comment(request,pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return redirect("posts:detail_post",comment.post.id)

def delete_post(request,pk):
    post = Posts.objects.get(id=pk)
    post.delete()
    return redirect("profiles:profile",request.user)
