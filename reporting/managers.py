from django.db import models
import datetime
from .constants import REPORTING_INTERVAL_DAILY, REPORTING_INTERVAL_WEEKLY, REPORTING_INTERVAL_MONTHLY


class LogManager(models.Manager):
    def daily_logs_for_today(self):
        return super().get_queryset().filter(
            created_at=datetime.date.today(),
            interval=REPORTING_INTERVAL_DAILY
        )
    
    def daily_logs_for_date(self, date):
        return super().get_queryset().filter(
            created_at=date,
            interval=REPORTING_INTERVAL_DAILY
        )
    
    def daily_logs(self):
        return super().get_queryset().filter(interval=REPORTING_INTERVAL_DAILY)

    def daily_logs_for_today_for_team(self, team_manager):
        return super().get_queryset().filter(
            created_at=datetime.date.today(),
            owner__in=team_manager.team.user_set.all(),
            interval=REPORTING_INTERVAL_DAILY
        )

    def daily_logs_for_date_for_team(self, date, team_manager):
        return super().get_queryset().filter(
            created_at=date,
            owner__in=team_manager.team.user_set.all(),
            interval=REPORTING_INTERVAL_DAILY
        )

    def daily_logs_for_team(self, team_manager):
        return super().get_queryset().filter(
            owner__in=team_manager.team.user_set.all(),
            interval=REPORTING_INTERVAL_DAILY
        )
    
    def monthly_logs_for_this_month(self):
        dt = datetime.datetime.now()
        this_month = datetime.date(dt.year, dt.month, 1)
        return super().get_queryset().filter(created_at=this_month, interval=REPORTING_INTERVAL_MONTHLY)
    
    def monthly_logs_for_month(self, year, month):
        month = datetime.date(year, month, 1)
        return super().get_queryset().filter(created_at=month, interval=REPORTING_INTERVAL_MONTHLY)

    def monthly_logs(self):
        return super().get_queryset().filter(interval=REPORTING_INTERVAL_MONTHLY)

    def monthly_logs_for_this_month_for_team(self, team_manager):
        dt = datetime.datetime.now()
        this_month = datetime.date(dt.year, dt.month, 1)
        return super().get_queryset().filter(
            created_at=this_month,
            owner__in=team_manager.team.user_set.all(),
            interval=REPORTING_INTERVAL_MONTHLY
        )

    def monthly_logs_for_month_for_team(self, year, month, team_manager):
        month = datetime.date(year, month, 1)
        return super().get_queryset().filter(
            created_at=month,
            owner__in=team_manager.team.user_set.all(),
            interval=REPORTING_INTERVAL_MONTHLY
        )

    def monthly_logs_for_team(self, team_manager):
        return super().get_queryset().filter(
            owner__in=team_manager.team.user_set.all(),
            interval=REPORTING_INTERVAL_MONTHLY
        )
    