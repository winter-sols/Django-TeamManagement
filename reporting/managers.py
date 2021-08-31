from django.db import models
import datetime


class LogManager(models.Manager):
    def for_today(self):
        return super().get_queryset().filter(created_at=datetime.date.today())
    
    def for_date(self, date):
        return super().get_queryset().filter(created_at=date)

    def for_today_for_team(self, team_manager):
        return super().get_queryset().filter(
            created_at=datetime.date.today(),
            owner__in=team_manager.team.user_set.all()
        )

    def for_date_for_team(self, date, team_manager):
        return super().get_queryset().filter(
            created_at=date,
            owner__in=team_manager.team.user_set.all()
        )
    
    def for_team(self, team_manager):
        return super().get_queryset().filter(owner__in=team_manager.team.user_set.all())