from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Project
from notification.models import Notification
from user.constants import ROLE_TEAM_MANAGER
from user.models import User
from user.constants import ROLE_ADMIN
from .constants import PROJECT_STATUS_ONGOING, PROJECT_STATUS_PAUSED, PROJECT_STATUS_ENDED


@receiver(post_save, sender=Project)
def create_notification_for_project_start(created, instance, **kwargs):
    if created:
        if instance.project_starter.team_manager is not None:
            Notification.objects.create(
                notify_to = instance.project_starter.team_manager,
                creator = instance.project_starter,
                message='{{creator}} started his {{object}}.',
                content_object = instance
            )
        for admin in User.objects.filter_admins():
            Notification.objects.create(
                notify_to=admin,
                creator=instance.project_starter,
                message='{{creator}} started his {{object}}.',
                content_object=instance
            )


@receiver(pre_save, sender=Project)
def create_notification_for_project_status(instance, **kwargs):
    if instance.id:
        prev_inst = Project.objects.get(id=instance.id)
        if prev_inst.status == PROJECT_STATUS_ONGOING and instance.status ==PROJECT_STATUS_PAUSED:
            if instance.project_starter.team_manager is not None:
                Notification.objects.create(
                    notify_to = instance.project_starter.team_manager,
                    creator = instance.project_starter,
                    message='{{creator}} paused his {{object}}.',
                    content_object = instance
                )
            for admin in User.objects.filter_admins():
                Notification.objects.create(
                    notify_to=admin,
                    creator=instance.project_starter,
                    message='{{creator}} paused his {{object}}.',
                    content_object=instance
                )

        if prev_inst.status != instance.status and instance.status ==PROJECT_STATUS_ENDED:
            if instance.project_starter.team_manager is not None:
                Notification.objects.create(
                    notify_to = instance.project_starter.team_manager,
                    creator = instance.project_starter,
                    message='{{creator}} stopped his {{object}}.',
                    content_object = instance
                )
            for admin in User.objects.filter_admins():
                Notification.objects.create(
                    notify_to=admin,
                    creator=instance.project_starter,
                    message='{{creator}} stopped his {{object}}.',
                    content_object=instance
                )
