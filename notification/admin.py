from django.contrib import admin
from .models import Notification


class NotificationModelAdmin(admin.ModelAdmin):
  list_display = ('notify_to', 'creator','message', 'content_object', 'read')

admin.site.register(Notification, NotificationModelAdmin)

