from django.urls import path

from .views import (
    DeveloperMonthlyReportView,
    DeveloperQuarterlyReportView,
    DeveloperWeeklyReportView,
    TeamMonthlyReportView,
    TeamQuarterlyReportView,
    TeamWeeklyReportView,
    DeveloperCustomReportView,
    TeamCustomReportView,
    DeveloperThisMonthReportDownloadView,
    DeveloperThisQuarterReportDownloadView,
    DeveloperThisWeekReportDownloadView,
    DeveloperCustomReportDownloadView,
    DevelopersReportView,
    IndividualDeveloperReportView,
    IndividualDeveloperProjectReportView,
    TeamsReportView,
    IndividualTeamReportView,
    ReportTotalView
)

urlpatterns = [
    path('developer/this-month/', DeveloperMonthlyReportView.as_view(), name='report_developer_monthly'),
    path('developer/this-month/download/', DeveloperThisMonthReportDownloadView.as_view(), name='report_developer_monthly_download'),
    path('developer/this-quarter/', DeveloperQuarterlyReportView.as_view(), name='report_developer_quarterly'),
    path('developer/this-quarter/download/', DeveloperThisQuarterReportDownloadView.as_view(), name='report_developer_quarterly'),
    path('developer/this-week/', DeveloperWeeklyReportView.as_view(), name='report_developer_weekly'),
    path('developer/this-week/download/', DeveloperThisWeekReportDownloadView.as_view(), name='report_developer_weekly'),
    path('team/this-month/', TeamMonthlyReportView.as_view(), name='report_team_monthly'),
    path('team/this-quarter/', TeamQuarterlyReportView.as_view(), name='report_team_quarterly'),
    path('team/this-week/', TeamWeeklyReportView.as_view(), name='report_team_weekly'),
    path('developer/custom/', DeveloperCustomReportView.as_view(), name='report_dev_custom'),
    path('developer/custom/', DeveloperCustomReportDownloadView.as_view(), name='report_dev_custom'),
    path('team/custom/', TeamCustomReportView.as_view(), name='report_team_custom'),

    path('total/', ReportTotalView.as_view(), name='report_total'),
    path('developers/', DevelopersReportView.as_view(), name='report_developer'),
    path('developers/<int:pk>/', IndividualDeveloperReportView.as_view(), name='report_individual_developer'),
    path('developers/<int:pk>/projects/', IndividualDeveloperProjectReportView.as_view(), name='project_report_individual_report'),
    path('teams/', TeamsReportView.as_view(), name='report_team'),
    path('teams/<int:pk>/', IndividualTeamReportView.as_view(), name='report_individual_team')
]