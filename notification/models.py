from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
  notify_to = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='Receivers')
  creator = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='Creators')
  message = models.TextField('Notification message', null=True)
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type','object_id')
  read = models.BooleanField(default=False)

  def __str__(self):
    return '{} ,created by {}'.format(self.content_object, self.creator)