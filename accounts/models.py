from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phoneNumber = models.CharField('전화번호', max_length=13)