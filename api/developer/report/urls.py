from django.urls import path

from .views import (
    ReportDeveloperView
)


urlpatterns = [
    path('', ReportDeveloperView.as_view(), name='reports_developer'),
]