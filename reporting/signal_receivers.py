from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Log
from user.models import User
from notification.models import Notification
from user.constants import ROLE_ADMIN, ROLE_TEAM_MANAGER, ROLE_DEVELOPER


@receiver(post_save, sender=Log)
def create_notification_whenever_logged(sender, instance, created, **kwargs):
    print(User.objects.filter_admins())
    if instance.owner.is_team_manager:
        for admin in User.objects.filter_admins():
            Notification.objects.create(
                notify_to=admin,
                creator=instance.owner,
                message='{{creator}} logged his {{object}}',
                content_object=instance
            )
    if instance.owner.is_developer and instance.owner.team_manager is not None:
        Notification.objects.create(
            notify_to=instance.owner.team_manager,
            creator=instance.owner,
            message='{{creator}} logged his {{object}}',
            content_object=instance
        )
