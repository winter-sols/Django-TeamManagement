from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_TYPE = [
        ('ROLE_ADMIN', 'admin'),
        ('ROLE_TEAM_MANAGER', 'team manager'),
        ('ROLE_DEVELOPER', 'developer')
    ]

    role = models.CharField(max_length=20, choices=ROLE_TYPE, default='ROLE_DEVELOPER')
    