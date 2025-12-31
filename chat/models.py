from django.db import models
from users.models import MyUser

# Create your models here.

class PrivateMessage(models.Model):
    sender = models.ForeignKey(MyUser,related_name='my_message',on_delete=models.CASCADE)
    handler = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"sned{self.sender} {self.handler}"