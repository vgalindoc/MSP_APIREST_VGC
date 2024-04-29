from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):   
    def create_user(self, email, password=None, **extra_fields):
        if not email:
           raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)       
        return user
 
# Create super user
   
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)       
        return user
   
# User Model for authentication
 
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
   
    objects = UserManager()
   
    USERNAME_FIELD = 'email'

class Cliente (models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    nombre  = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20)    
    def __str__(self):
        return self.nombre
    
 