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


class PaymentAccount(models.Model):
    platform = models.CharField(choices=constants.PAYMENT_PLATFORMS, max_length=10)
    address = models.CharField(max_length=250)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '{}({})'.format(self.platform, self.address)


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
    payment_account = models.ForeignKey('PaymentAccount', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, **kwargs):
        fr = FinancialRequest.objects.get(id=self.id) if self.id is not None else None
        super().save(**kwargs)
        fr_post_save.send(sender=self.__class__, instance=self, prev_inst=fr, **kwargs)

    def __str__(self):
        return 'req={}  project={}'.format(self.requester, self.project)


class Transaction(models.Model):
    owner = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=1000, null=True)
    project = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateField(null=True)
    gross_amount = models.FloatField()
    net_amount = models.FloatField()
    financial_request = models.ForeignKey('FinancialRequest', on_delete=models.CASCADE, null=True, blank=True)
    payment_account = models.ForeignKey('PaymentAccount', on_delete=models.CASCADE, null=True)
    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return '{} {}'.format(self.owner, self.address)


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
