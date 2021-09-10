from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Project
from .models import FinancialRequest
from notification.models import Notification
from user.models import User
from .signals import fr_post_save
from .constants import PROJECT_STATUS_ONGOING, PROJECT_STATUS_PAUSED, PROJECT_STATUS_ENDED, FINANCIAL_STATUS_CANCELED


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



@receiver(fr_post_save, sender=FinancialRequest)
def create_financial_request_notification(sender, instance, prev_inst, **kwargs):
    message = '{{creator}} created a new {{object}}.'
    if prev_inst is not None:
        if prev_inst.status != instance.status and instance.status == FINANCIAL_STATUS_CANCELED:
            message =  '{{creator}} canceled a {{object}}.'
        else :
            message = '{{creator}} updated a {{object}}.'
    
    if instance.requester.is_developer and instance.requester.team_manager is not None:
          Notification.objects.create(
            notify_to=instance.requester.team_manager,
            creator=instance.requester,
            message= message,
            content_object=instance
        )
    if instance.requester.is_admin == False:
        for admin in User.objects.filter_admins():
            Notification.objects.create(
                notify_to=admin,
                creator=instance.requester,
                message= message,
                content_object=instance
            )

