from django.shortcuts import redirect 
from .models import Notification
from django.http import JsonResponse

# Create your views here.
def read_notification(request):
    Notification.objects.filter(
        receiver = request.user,
        is_read = False
    ).update(is_read=True)
    
    return JsonResponse({'status':'ok'})