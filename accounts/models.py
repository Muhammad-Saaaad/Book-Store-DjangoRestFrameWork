from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager

""" 
In the fully custom base user model we have to make some functions 
that only admin can access but here they are all custom defined
"""

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'user_type']
    objects = UserManager()