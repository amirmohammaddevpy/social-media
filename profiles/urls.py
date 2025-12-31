from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("<str:username>/",views.profile,name="profile"),
    path("edit/<str:username>/",views.edit_profile,name="edit_profile"),
    path("follow/user/<str:username>",views.follow,name="follow"),
    path('followers/<str:username>/',views.list_followers,name="followers"),
    path('following/<str:username>/',views.list_following,name="following"),
    path("delete/<int:pk>/",views.delete_account,name="delete"),
    
]