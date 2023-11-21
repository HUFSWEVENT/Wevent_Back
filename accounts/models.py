from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=email,
            password = password,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(AbstractUser):
    email = models.EmailField('이메일 주소', unique=True)
    phoneNumber = models.CharField('전화번호', max_length=11, blank=True)
    first_name = None
    last_name = None
    

    objects = UserManager()

    def __str__(self):
        return self.email
    
class CodeForAuth(models.Model):
    email = models.EmailField(max_length=50)
    code = models.CharField(max_length=6, null=True, blank=True)