from django.db import models
from . import constants
# Create your models here.
class Log(models.Model):
  owner = models.ForeignKey('User', on_delete=models.CASCADE)
  plan = models.TextField(null=True)
  achievements = models.TextField(null=True)
  log_type = models.CharField(choices=constants.LOG_TYPE, max_length=20)
  created_at = models.DateField('Created Date of Log')
  interval = models.CharField(choices=constants.INTERVAL, max_length=20)

  def __str__(self):
    return '{} log for {} ({})'.format(self.interval, self.owner, self.created_at)
