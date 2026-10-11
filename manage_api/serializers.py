from rest_framework import serializers
from post.models import Posts ,Comment 
from users.models import MyUser ,BlockUser
from story.models import Story
from notification.models import Notification

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    image = serializers.ImageField(
        source='user.avatar',
        read_only=True
    )
    class Meta:
        model = Posts
        fields = ('id','image','user','post','descriptions','create_at',)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    image = serializers.ImageField(source="user.avatar",read_only=True)

    class Meta:
        model = Comment
        fields = ("image","user","comment",)

class PostDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        source='user.avatar',
        read_only=True
    )
    user = serializers.StringRelatedField()
    class Meta:
        model = Posts
        exclude = ("total_like",)


class CreateNewComment(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment',)

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('post','descriptions',)

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('avatar','username','first_name','last_name','bio','email',)


class EditeProfileUser(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('avatar','bio',)
        
class FollowingList(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    class Meta:
        model = MyUser
        fields = ('username',)
class MyStory(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Story
        fields = ('user','date','story')
    
class CreateStory(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('story',)

class Saved(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Posts
        fields = ('user', 'post', 'descriptions', 'create_at')
        
class Notifications(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Notification
        fields = ('user','message','is_read','created_at')

class ListBlockUser(serializers.ModelSerializer):
    blocked = serializers.StringRelatedField()
    class Meta:
        model = BlockUser
        fields = ('blocked',)