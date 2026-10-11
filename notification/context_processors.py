from .models import Notification
from django.http import JsonResponse

def notifications(request):
    if not request.user.is_authenticated:
        return {}
    
    notifications = Notification.objects.filter(receiver = request.user).select_related('user').order_by('-created_at')[:10]
    notif = Notification.objects.filter(receiver=request.user ,is_read=False).count()
    
    return {
        'notifications':notifications,
        'unread_notifications_count':notif,
    }
 