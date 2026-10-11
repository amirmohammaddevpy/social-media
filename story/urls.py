from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('',views.story,name="story"),
    path('story/delete/<int:pk>/',views.delete_story,name="delete_story"),
    path('<int:pk>/seen/',views.seen_story,name='seen_story')
]
