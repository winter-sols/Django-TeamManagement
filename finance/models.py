from django.db import models
from jsonfield.fields import JSONField
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . import constants
from .manager import ProjectQuerySet, FinancialRequestQuerySet, TransactionQuerySet
from .signals import fr_post_save


class Project(models.Model):
    objects = ProjectQuerySet.as_manager()
    title = models.CharField(max_length=100)
    type = models.IntegerField(choices=constants.PROJECT_TYPES)
    weekly_limit = models.IntegerField(default=40, null=True, blank=True)
    price = models.FloatField(null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    participants = models.ManyToManyField('user.User', related_name='projects')
    project_starter = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='related_project_starter')
    started_at = models.DateField(null=True)
    ended_at = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=constants.PROJECT_STATUS)

    def __str__(self):
        return '{}({})'.format(self.title, self.type)


class FinancialRequest(models.Model):
    objects = FinancialRequestQuerySet.as_manager()
    type = models.IntegerField(choices=constants.FINANCIAL_TYPES)
    status = models.IntegerField(choices=constants.FINANCIAL_STATUS, default=constants.FINANCIAL_STATUS_PENDING)
    amount = models.FloatField(null=True)
    # counter_party_type =  models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # counter_party_id = models.PositiveIntegerField()
    # counter_party = GenericForeignKey('counter_party_type', 'counter_party_id')
    address = models.CharField(max_length=200, null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey('user.User', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, **kwargs):
        fr = FinancialRequest.objects.get(id=self.id) if self.id is not None else None
        super().save(**kwargs)
        fr_post_save.send(sender=self.__class__, instance=self, prev_inst=fr, **kwargs)

    def __str__(self):
        return 'req={}  project={}'.format(self.requester, self.project)


class Transaction(models.Model):
    description = models.TextField(null=True)
    created_at = models.DateField(null=True)
    gross_amount = models.FloatField()
    net_amount = models.FloatField()
    payment_platform = models.CharField(choices=constants.PAYMENT_PLATFORMS, max_length=10)
    financial_request = models.ForeignKey('FinancialRequest', on_delete=models.CASCADE)
    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return '{} {}'.format(self.financial_request.requester, self.financial_request.project)


class Partner(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_num = models.CharField(max_length=50, null=True, blank=True)
    contact_method = JSONField()
    # financial_requests = GenericRelation(FinancialRequest, content_type_field='counter_party_type', object_id_field='counter_party_id',)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return '{}({})'.format(self.full_name, self.email)


class Client(models.Model):
    type = models.IntegerField(choices=constants.CLIENT_TYPES)
    full_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    started_at = models.DateField()
    # financial_requests = GenericRelation(FinancialRequest, content_type_field='counter_party_type', object_id_field='counter_party_id',)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return '{}({})'.format(self.full_name, self.type)
