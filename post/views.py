from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required 
from .forms import CreatPostForm ,CommentForm ,ReportPostForm
from django.contrib import messages
from .models import Posts,Comment,ReportPost
from django.http import JsonResponse
from users.models import MyUser
from django.views.decorators.http import require_POST
from notification.models import Notification
from django.http import JsonResponse

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
            Notification.objects.create(
                user = request.user,
                message = "comment your post",
                receiver = posts.user
            )
            return redirect('posts:detail_post',posts.id)
        else:
            messages.error(request,'for is not valid!!')
    return render(request,"posts/detail.html",{'detail':posts,'form':form,'comments':comment,})



@login_required(login_url='account:login')
def create_post(request,username):
    form = CreatPostForm()
    if request.method == "POST":
        form = CreatPostForm(request.POST,files=request.FILES,)
        post = request.FILES.get('post')
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            if post and post.size > 10*1024*1024:
                messages.error(request,"file is bigger")
                return redirect("profiles:profile",request.user)
                
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
            Notification.objects.create(
                user = request.user,
                message = 'disliked your post',
                receiver = post.user
            )
            post.user_like.remove(user)
            return JsonResponse({'status':'like'})
        else:
            Notification.objects.create(
                user = request.user,
                message = "liked your post",
                receiver = post.user
            )
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

def save_post(request,pk):
    post = get_object_or_404(Posts,id=pk)
    
    if request.user in post.user_save.all():
        post.user_save.remove(request.user)
        return JsonResponse({'status':'unsave'})
    post.user_save.add(request.user)
    return JsonResponse({'status':'saved'})

def saved(request):
    post = request.user.post_saves.all()
    return render(request,"posts/save_postlist.html",{'save':post})

@require_POST
def report_post(request,pk):
    post = get_object_or_404(Posts,id=pk)
    
    if ReportPost.objects.filter(post=post,user=request.user).exists():
        return JsonResponse({'status': 'already_reported'})
    
    form = ReportPostForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    report = form.save(commit=False)
    report.user = request.user
    report.post = post
    report.subject = request.POST.get('subject')
    report.save()
    
    count_report = post.reports.count()
    if count_report >=5:
        post.delete()
    
    return JsonResponse({'status': 'reported'})