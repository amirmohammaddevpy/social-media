from django.db import models
from users.models import MyUser

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(MyUser,related_name="user",on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    receiver = models.ForeignKey(MyUser,related_name="receiver",on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'user {self.user} receiver {self.receiver}'