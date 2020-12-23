from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=constants.ROLE_TYPES, default=constants.ROLE_DEVELOPER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)


class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    profile_type = models.IntegerField(choices=constants.PROFILE_TYPES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=50)
    dob = models.DateField('Date of Birth', null=True)
    gender = models.IntegerField(choices=constants.PROFILE_GENDERS, default=constants.PROFILE_GENDER_MALE)
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Account(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    platform_type = models.CharField(max_length=30, choices=constants.PLATFORM_TYPES)
    password = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    recovery_email = models.EmailField()
    url = models.CharField('URL', max_length=200)
    # TODO: Implement Linked Profile here...

    def __str__(self):
        return '{}({})'.format(self.recovery_email, self.platform_type)


class AccountSecurityQA(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return '{} {}'.format(self.question, self.account)
