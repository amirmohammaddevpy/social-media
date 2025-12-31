from django.db import models
from users.models import MyUser
from django.conf import settings
# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.ImageField(upload_to="posts/%Y/%m/%d")
    descriptions = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='post_like',blank=True)
    total_like = models.PositiveBigIntegerField(default=0)
    
    
    def __str__(self):
        return self.user.username
    

class Comment(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return self.user.username
