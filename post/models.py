from django.db import models
from users.models import MyUser
from django.conf import settings
from django.core.validators import FileExtensionValidator

# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.FileField(upload_to='post/users',validators=[FileExtensionValidator(allowed_extensions=['mp4','webm','ogg','ogv','jpg','jpeg','png','svg','webp','gif'])])
    descriptions = models.TextField(blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='post_like',blank=True)
    total_like = models.PositiveBigIntegerField(default=0)
    user_save = models.ManyToManyField(MyUser,related_name="post_saves",blank=True)
    
    
    def __str__(self):
        return self.user.username
    

class Comment(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class ReportPost(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='reports')
    subject = models.CharField(max_length=200)
    
    class Meta:
        unique_together = ('post','user')
        
    def __str__(self):
        return self.user.username