from django.contrib.auth.base_user import BaseUserManager
from . import constants


class UserManager(BaseUserManager):
    def filter_admins(self):
        return super().get_queryset().filter(role=constants.ROLE_ADMIN)

    def filter_team_managers(self):
        return super().get_queryset().filter(role=constants.ROLE_TEAM_MANAGER)
    
    def filter_developers(self):
        return super().get_queryset().filter(role=constants.ROLE_DEVELOPER)
