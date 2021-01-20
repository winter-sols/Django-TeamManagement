from django.db import models
from jsonfield.fields import JSONField
from . import constants

class Client(models.Model):
    type = models.IntegerField(choices=constants.CLIENT_TYPES)
    full_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    started_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}({})'.format(self.full_name, self.type)


class Project(models.Model):
    title = models.CharField(max_length=100)
    type = models.IntegerField(choices=constants.PROJECT_TYPES)
    price = models.FloatField(null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    participants = models.ManyToManyField('user.User', related_name='related_participants')
    project_starter = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='related_project_starter')
    started_at = models.DateField(null=True)
    ended_at = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=constants.PROJECT_STATUS)

    def __str__(self):
        return '{}({})'.format(self.title, self.type)


class FinancialRequest(models.Model):
    type = models.IntegerField(choices=constants.FINANCIAL_TYPES)
    status = models.IntegerField(choices=constants.FINANCIAL_STATUS, default=constants.FINANCIAL_STATUS_PENDING)
    amount = models.FloatField(null=True)
    counter_party = models.CharField(max_length=50)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.type, self.status)


class Transaction(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gross_amount = models.FloatField()
    net_amount = models.FloatField()
    payment_platform = models.CharField(choices=constants.PAYMENT_PLATFORMS, max_length=10)
    related_financial = models.ForeignKey('FinancialRequest', on_delete=models.CASCADE)
    
    def __str__(self):
        return '{} {} ({})'.format(self.client, self.project, self.payment_platform)


class Partner(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200, null=True)
    dob = models.DateField()
    phone_num = models.CharField(max_length=50, null=True)
    contact_method = JSONField()

    def __str__(self):
        return '{}({})'.format(self.full_name, self.email)

