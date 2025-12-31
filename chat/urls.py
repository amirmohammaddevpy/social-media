from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path('message/',views.chats,name="chats"),
    path("<str:username>/",views.room,name="room")
]
