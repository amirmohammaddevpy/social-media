from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name= 'api'

urlpatterns = [
    path("",views.list_post,name="home"),
    path("<int:pk>/",views.detail_post,name="detail"),
    path('token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("explore/",views.explore,name="explore"),
    path("create/post/",views.create_post,name="create_post"),
    path('profile/<str:username>/',views.profile,name="profile"),
    path("profile/edite/<str:username>/",views.edite_profile,name="edite_profile"),
    path('like/post/<int:pk>/',views.like_post,name="like_post"),
    path("profile/following/<str:username>/",views.following,name="following"),
    path("profile/followers/<str:username>/",views.follower,name="follower"),
    path("follow/<str:username>/",views.follow_and_unfollow,name="follow"),
    path('my/story/',views.my_story,name="my_story"),
    path('story/<str:username>/',views.story_them,name="story_them"),
    path('create/story/',views.creat_story,name="create_story"),
    path('delete/story/<int:pk>/',views.delete_story,name="delete_story"),
    path("update/story/",views.delete_old_story,name="delete_old_story"),
    path("saved/",views.saved,name="saved"),
    path('save/<int:pk>/post/',views.save_post,name="save_post"),
    path('notifications/',views.all_notification,name="notification"),
    path('read/notification/',views.notification_read,name='read_notif'),
    path('block/<str:username>/',views.block_unblock_user,name="block"),
    path('blocked/',views.list_block_user,name='list_block_user')
]