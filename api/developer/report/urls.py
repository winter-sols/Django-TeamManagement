from django.urls import path

from .views import (
    DeveloperMonthlyReportView,
    DeveloperQuarterlyReportView,
    DeveloperWeeklyReportView
)


urlpatterns = [
    path('this-month/', DeveloperMonthlyReportView.as_view(), name='reports_developer_this-month'),
    path('this-quarter/', DeveloperQuarterlyReportView.as_view(), name='report_developer_quarterly'),
    path('this-week/', DeveloperWeeklyReportView.as_view(), name='report_developer_weekly'),
]