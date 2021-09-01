from django.db import models


class NotificationManager(models.Manager):
    def unread_items(self, owner):
        return super().get_queryset().filter(notify_to=owner, read_at__isnull=True)
    def read_items(self, owner):
        return super().get_queryset().filter(notify_to=owner, read_at__isnull=False)
