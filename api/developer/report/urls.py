from django.urls import path

from .views import (
    DeveloperMonthlyReportView,
    DeveloperQuarterlyReportView,
    DeveloperWeeklyReportView,
    DeveloperCustomReportView,
    DeveloperReportView
)


urlpatterns = [
    path('', DeveloperReportView.as_view(), name='reports_developer'),
    path('this-month/', DeveloperMonthlyReportView.as_view(), name='reports_developer_this-month'),
    path('this-quarter/', DeveloperQuarterlyReportView.as_view(), name='report_developer_quarterly'),
    path('this-week/', DeveloperWeeklyReportView.as_view(), name='report_developer_weekly'),
    path('custom/', DeveloperCustomReportView.as_view(), name='report_developer_custom')
]