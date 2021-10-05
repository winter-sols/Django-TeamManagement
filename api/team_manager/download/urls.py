from django.urls import path

from .views import (
    ReportDeveloperListDownloadView,
    ReportDeveloperDetailDownloadView,
    ReportDeveloperProjectDownloadView,
)

urlpatterns = [
    path('developers/', ReportDeveloperListDownloadView.as_view(), name='report_developer_list_download'),
    path('developers/<int:pk>/', ReportDeveloperDetailDownloadView.as_view(), name='report_developer_detail_download'),
    path('developers/<int:pk>/projects/', ReportDeveloperProjectDownloadView.as_view(), name='report_developer_project_download'),
]
