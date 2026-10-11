from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.home,name="home"),
    path('explore/',views.explore,name='explore'),
    path("search/",views.search,name="search"),
    path("api/documentation/",views.api_documentation,name="api_documentation"),
    path('notifications/check/', views.check_notif, name='check_notifications'),
]
