from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=constants.ROLE_TYPES, default=constants.ROLE_DEVELOPER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    profile_type = models.IntegerField(choices=constants.PROFILE_TYPES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=50)
    dob = models.DateField('Date of Birth', null=True)
    gender = models.IntegerField(choices=constants.PROFILE_GENDERS, default=constants.PROFILE_GENDER_MALE)
    