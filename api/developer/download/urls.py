from django.urls import path

from .views import (
    ReportDeveloperProjectDownloadView,
)

urlpatterns = [
    path('projects/', ReportDeveloperProjectDownloadView.as_view(), name='report_developer_project_download'),
]
