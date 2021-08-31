from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import datetime

class NotificationManager(models.Manager):
    def unread_items(self, owner):
        return super().get_queryset().filter(notify_to=owner, read_at__isnull=True)
    def read_items(self, owner):
        return super().get_queryset().filter(notify_to=owner, read_at__isnull=False)


class Notification(models.Model):
    notify_to = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='received_notifications')
    creator = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='created_notifications')
    message = models.TextField('Notification message', null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    read_at = models.DateTimeField(null=True, blank=True)

    objects = NotificationManager()
    
    def __str__(self):
        return '{} created by {}'.format(self.message, self.creator)

    def mark_as_read(self):
        self.read_at = datetime.datetime.now()
        self.save()
