from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

    # Create your models here.
class MyManagerUser(BaseUserManager):
    def create_user(self,email,first_name,last_name,username,password=None):
        if not email:
            return ValueError("You have to import Email address")
        if not username:
            return ValueError("You have to import username")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email,username,first_name="",last_name="",password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=255,verbose_name="first name")
    last_name = models.CharField(max_length=255,verbose_name="last name")
    username = models.CharField(max_length=20,verbose_name="username",unique=True)
    bio = models.TextField(null=True,blank=True)
    email = models.EmailField(max_length=255,verbose_name="Email",unique=True)
    avatar = models.ImageField(default="image/default.png",upload_to="images/profile/%Y/%m/%d")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    following = models.ManyToManyField("self",through="Contact",related_name="followers",symmetrical=False)
        
    objects = MyManagerUser()
        
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    
    def has_module_perms(self,app_label):
        return True
    
    
class Contact(models.Model):
    user_form = models.ForeignKey(MyUser,related_name="rel_from_set",on_delete=models.CASCADE)
    user_to = models.ForeignKey(MyUser,related_name="rel_to_set",on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_form} follow {self.user_to}"