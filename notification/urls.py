from django.urls import path
from . import views

app_name = "notification"

urlpatterns = [
    path('read/',views.read_notification,name='read')
]