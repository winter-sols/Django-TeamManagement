from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=constants.ROLE_TYPES, default=constants.ROLE_DEVELOPER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

# class Profile(models.Model):
#     type = 
