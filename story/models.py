from django.db import models
from users.models import MyUser
from django.core.validators import FileExtensionValidator

# Create your models here.
class Story(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    story = models.FileField(upload_to='story/users',validators=[FileExtensionValidator(allowed_extensions=['mp4','webm','ogg','ogv','jpg','jpeg','png','svg','webp','gif'])])
    caption = models.TextField(max_length=200,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username