from django.shortcuts import render,redirect,get_object_or_404
from .models import Story
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from users.models import BlockUser
# Create your views here.

def story(request,):
    story_user = Story.objects.filter(user=request.user)

    
    data_story = [
        {
            'id':s.id,
            'avatar':s.user.avatar.url,
            'username':s.user.username,
            'url':s.story.url,
            'type': 'video' if s.story.name.lower().endswith(
                ('.mp4', '.mov', '.webm', '.avi')
            ) else 'image',
        }
        for s in story_user
    ]
    
    
    return render(request,"story/story.html",{'stories':story_user,'stories_json':data_story})

@require_POST
def delete_story(request,pk):
    get_story = get_object_or_404(Story,id=pk)
    if request.user == get_story.user.username:
        get_story.delete()
        return JsonResponse({'status':'delete'})
    return JsonResponse({'status':''})


def seen_story(request,pk):
    get_story = Story.objects.get(id=pk)
    get_story.seen = True
    get_story.save()
    return JsonResponse({'status':'Seen'})