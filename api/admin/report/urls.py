from django.urls import path

from .views import (
    DevelopersReportView,
    IndividualDeveloperReportView,
    IndividualDeveloperProjectReportView,
    TeamsReportView,
    IndividualTeamReportView,
    ReportTotalView
)

urlpatterns = [
    path('total/', ReportTotalView.as_view(), name='report_total'),
    path('developers/', DevelopersReportView.as_view(), name='report_developer'),
    path('developers/<int:pk>/', IndividualDeveloperReportView.as_view(), name='report_individual_developer'),
    path('developers/<int:pk>/projects/', IndividualDeveloperProjectReportView.as_view(), name='project_report_individual_report'),
    path('teams/', TeamsReportView.as_view(), name='report_team'),
    path('teams/<int:pk>/', IndividualTeamReportView.as_view(), name='report_individual_team')
]