from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('create/post/<str:username>/',views.create_post,name="create_post"),
    path('detail/<int:pk>/',views.detail_post,name="detail_post"),
    path('delete/<int:pk>/',views.delete_post,name="delete_post",),
    path('delete/comment/<int:pk>/',views.delete_comment,name='delete_comment'),
    path('like/post/<int:pk>',views.like_post,name='like')
]
