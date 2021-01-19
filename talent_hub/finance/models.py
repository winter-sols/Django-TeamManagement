from django.db import models
from . import constants

class Client(models.Model):
    type = models.IntegerField(choices=constants.CLIENT_TYPES)
    full_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=True)
    started_at = models.DateField(auto_now_add=True)

class Project(models.Model):
    title = models.CharField(max_length=100)
    type = models.IntegerField(choices=constants.PROJECT_TYPES)
    price = models.FloatField(null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    participants = models.ManyToManyField('user.User', on_delete=models.CASCADE)
    project_starter = models.ForeignKey('user.User', on_delete=models.CASCADE)
    started_at = models.DateField(null=True)
    ended_at = models.DateField(null=True)
    status = models.IntegerField(choices=constants.PROJECT_STATUS)


class FinancialRequest(models.Model):
    type = models.IntegerField(choices=constants.FINANCIAL_TYPES)
    status = models.IntegerField(choices=constants.FINANCIAL_STATUS, default=constants.FINANCIAL_STATUS_PENDING)
    amount = models.FloatField(null=True)
    counter_party = models.CharField(max_length=50)


