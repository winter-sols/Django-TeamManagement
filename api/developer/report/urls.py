from django.urls import path

from .views import (
    DeveloperReportView
)


urlpatterns = [
    path('', DeveloperReportView.as_view(), name='reports_developer'),
]