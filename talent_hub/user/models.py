from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants

class User(AbstractUser):
    role = models.IntegerField(choices=constants.ROLE_TYPES, default=constants.ROLE_DEVELOPER)
