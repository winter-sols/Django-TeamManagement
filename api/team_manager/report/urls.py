from django.urls import path

from .views import (
    TeamMonthlyReportView,
    TeamQuarterlyReportView,
    TeamWeeklyReportView,
    TeamCustomReportView
)

urlpatterns = [
    path('this-month/', TeamMonthlyReportView.as_view(), name='reports_team_this-month'),
    path('custom/', TeamCustomReportView.as_view(), name='reports_team_custom'),
    path('this-quarter/', TeamQuarterlyReportView.as_view(), name='report_team_quarterly'),
    path('this-week/', TeamWeeklyReportView.as_view(), name='report_team_weekly'),
]
