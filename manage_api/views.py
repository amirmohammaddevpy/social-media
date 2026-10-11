
from django.shortcuts import redirect ,get_object_or_404 , get_list_or_404
from django.db.models import Q

from users.models import MyUser ,Contact ,BlockUser
from . import serializers
from post.models import Posts ,Comment
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from chat.models import PrivateMessage
from story.models import Story
from django.utils import timezone
import datetime
from notification.models import Notification


@api_view(['GET'])
def list_post(request):
    if not request.user.is_authenticated:
        return redirect("api:token_obtain_pair")

    post = Posts.objects.filter(user=request.user)
    serializer = serializers.PostSerializer(post,many=True)
    return Response({"posts":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET','POST','DELETE'])
def detail_post(request,pk):
    post = get_object_or_404(Posts,id=pk)
    serializer = serializers.PostDetailSerializer(post)
    comment = Comment.objects.filter(post=post)
    serializer_comment = serializers.CommentSerializer(comment,many=True)

    if request.method == "POST":
        create_comment_seria = serializers.CreateNewComment(data=request.data)
        if create_comment_seria.is_valid():
            create_comment_seria.save(user=request.user , post=post)
            return  Response(create_comment_seria.data,status=status.HTTP_201_CREATED)
        return Response(create_comment_seria.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.user == post.user:
        if request.method == "DELETE":
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({
        "post": serializer.data,
        "likes": post.user_like.count(),
        "comments": serializer_comment.data,
        'request_id':request.user.id,

    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def explore(request):
    post = Posts.objects.all()
    serializer = serializers.PostSerializer(post,many=True)
    return  Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def profile(request,username):
    profiles = get_object_or_404(MyUser,username=username)
    i_blocked_them = BlockUser.objects.filter(blocker=request.user , blocked=profiles).exists()
    them_blocked_me = BlockUser.objects.filter(blocker = profiles,blocked=request.user).exists()
    
    if i_blocked_them:
        return Response({'status':'you blcked user'})
    elif them_blocked_me:
        return Response({'status':'user blocked you'})
    else:
        post = Posts.objects.filter(user=profiles).count()
        serializer = serializers.ListUserSerializer(profiles)
        list_posts = Posts.objects.filter(user=profiles)
        serializer_post = serializers.PostSerializer(list_posts,many=True)
        return Response({
            "profile":serializer.data,
            "following":profiles.following.count(),
            "followers":profiles.followers.count(),
            "posts_count":post,
            "post":serializer_post.data
        },status=status.HTTP_200_OK)

@api_view(['POST'])
def create_post(request):
    serializer = serializers.CreatePostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data ,status=status.HTTP_201_CREATED)
    return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edite_profile(request,username):
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user == user:
        serializer = serializers.EditeProfileUser(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def like_post(request,pk):
    post = get_object_or_404(Posts,id=pk)
    try:
        user = MyUser.objects.get(id=request.user.id)
    except MyUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user in post.user_like.all():
        post.user_like.remove(user)
        Notification.objects.create(
            user = request.user,
            receiver = post.user,
            message = f"{request.user} like post"
        )
        return Response({"status":'dislike'},status=status.HTTP_202_ACCEPTED)
    else:
        post.user_like.add(user)
        Notification.objects.create(
            user = request.user,
            receiver = post.user,
            message = f"{request.user} like post"
        )
        return Response({"status":'like'},status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def following(request,username):
    myuser = get_object_or_404(MyUser,username=username)
    
    i_blocked_them = BlockUser.objects.filter(blocker=request.user , blocked=myuser).exists()
    them_blocked_me = BlockUser.objects.filter(blocker = myuser,blocked=request.user).exists()
    
    if i_blocked_them:
        return Response({'status':'you blcked user'})
    elif them_blocked_me:
        return Response({'status':'user blocked you'})
    else:
        followings = myuser.following.all()
        serializer = serializers.FollowingList(followings,many=True)
        return Response({"following":serializer.data},status.HTTP_200_OK)
@api_view(['GET'])
def follower(request,username):
    myuser = get_object_or_404(MyUser,username=username)
    i_blocked_them = BlockUser.objects.filter(blocker=request.user , blocked=myuser).exists()
    them_blocked_me = BlockUser.objects.filter(blocker = myuser,blocked=request.user).exists()
    
    if i_blocked_them:
        return Response({'status':'you blcked user'})
    elif them_blocked_me:
        return Response({'status':'user blocked you'})
    else:

        followers = myuser.followers.all()
        serializer = serializers.FollowingList(followers,many=True)
        return Response({"followers":serializer.data},status.HTTP_200_OK)

@api_view(['POST'])
def follow_and_unfollow(request,username):
    try:
        myuser = get_object_or_404(MyUser,username=username)
    except MyUser.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    try:
        user = Contact.objects.filter(user_form=request.user,user_to=myuser)
        if user.exists():
            user.delete()
            Notification.objects.create(
            user = request.user,
            receiver = myuser,
            message = f"{request.user} end follow you"
        )
            return Response({"detail":"Unfollow"},status=status.HTTP_200_OK,)
        else:
            Contact.objects.create(user_form=request.user,user_to = myuser)
            Notification.objects.create(
            user = request.user,
            receiver = myuser,
            message = f"{request.user} Start follow you"
        )
            return Response({"detail":"Follow"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def my_story(request):
    get_story = Story.objects.filter(user=request.user)
    serializer = serializers.MyStory(get_story,many=True)
    return Response({'story':serializer.data},status.HTTP_200_OK)

@api_view(['GET'])
def story_them(request,username):
    get_user = get_object_or_404(MyUser,username=username)
    get_story_user = Story.objects.filter(user=get_user)
    i_blocked_them = BlockUser.objects.filter(blocker=request.user , blocked=get_user).exists()
    them_blocked_me = BlockUser.objects.filter(blocker = get_user,blocked=request.user).exists()
    
    if not get_story_user.exists():
        return Response({'status':'story is not found'})
        
    if i_blocked_them:
        return Response({'status':'you blcked user'})
    elif them_blocked_me:
        return Response({'status':'user blocked you'})
    else:
        serializer = serializers.MyStory(get_story_user,many=True)
        return Response({'story':serializer.data},status.HTTP_200_OK)
    

@api_view(['POST'])
def creat_story(request):
    serializer = serializers.CreateStory(data=request.data)
    get_file = request.FILES.get('story')
    if serializer.is_valid():
        if get_file and get_file.size > 10*1024*1024:
            return Response({'status':'File is bigger 10MB'})
        serializer.save(user=request.user)
        return  Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_story(request,pk):
    story_user = get_object_or_404(Story,id=pk)
    if request.user == story_user.user:
        story_user.delete()
        return Response({'status':'delete '},status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status':'You not the owner of this story'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def delete_old_story(request):
    get_story = Story.objects.filter()
    now = timezone.now()
    finally_time = now - datetime.timedelta(hours=24)
    for time in get_story:
        if time.date > finally_time:
            get_story.delete()
    return Response({'status':'upfate story'})

@api_view(['GET'])
def saved(request):
    post = Posts.objects.filter(user_save=request.user)
    serializer = serializers.Saved(post,many=True)
    return Response({'posts':serializer.data})

@api_view(['POST'])
def save_post(request,pk):
    post = get_object_or_404(Posts,id=pk)
    user = post.user_save.all()
    if request.user in user:
        post.user_save.remove(request.user)
        return Response({'status':'unsave post'})
    else:
        post.user_save.add(request.user)
        return Response({'status':'save post'})


@api_view(['GET'])
def all_notification(request):
    mynotif = Notification.objects.filter(receiver=request.user)
    serializer = serializers.Notifications(mynotif,many=True)
    return Response({'notification':serializer.data})

@api_view(['PUT'])
def notification_read(request):
    Notification.objects.filter(receiver=request.user,is_read=False).update(is_read=True)
    return Response({'status':'notification is read'})

@api_view(['POST'])
def block_unblock_user(request,username):
    my_user = get_object_or_404(MyUser,username=username)
    try:
        if BlockUser.objects.filter(blocker=request.user,blocked=my_user).exists():
            get_object_or_404(BlockUser,blocker=request.user , blocked=my_user).delete()
            return Response({'status':'unblock'})
        else:
            BlockUser.objects.create(
                blocker = request.user,
                blocked = my_user
            )
            return Response({'status':'block'})
    except Exception as e:
        return Response({'status':f'Erorr {e}'})

@api_view(['GET'])
def list_block_user(request):
    block_users = BlockUser.objects.filter(blocker=request.user)
    serializer = serializers.ListBlockUser(block_users,many=True)
    return Response({'block_user':serializer.data},status.HTTP_200_OK)