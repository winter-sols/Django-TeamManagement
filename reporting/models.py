from django.utils.functional import cached_property
from django.db import models
from . import constants
import datetime


class LogManager(models.Manager):
    def for_today(self, owner=None):
        return super().get_queryset().filter(created_at==datetime.date.today())
    
    def for_date(self, date, owner=None):
        return super().get_queryset().filter(created_at=date)

        
class Log(models.Model):
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    plan = models.TextField(null=True)
    achievements = models.TextField(null=True)
    log_type = models.CharField(choices=constants.REPORTING_LOG_TYPE, max_length=20)
    created_at = models.DateField('Created Date of Log', null=True)
    updated_at = models.DateTimeField('Updated Date of Log', auto_now=True, null=True)
    interval = models.CharField(choices=constants.REPORTING_INTERVAL, max_length=20)

    objects = LogManager()

    def __str__(self):
        return '{} log for {} ({})'.format(self.interval, self.owner, self.created_at)

    class Meta:
        unique_together = ['owner', 'created_at']
