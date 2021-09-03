from django.urls import  include, path
from rest_framework import routers
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from .finance.views import CancelFinanicalRequestView
from api.common.dashboard.views import (
    WeeklyIncomeView,
    OngoingProjectsView,
    PendingRequestsView,
    StatsView,
    ApprovedRequestView
)
from api.common.user.views import ProfilesAdminViewSet, AccountsAdminViewSet
from api.common.logging.views import (
    MyLogCreateView,
    MyDailyLogView,
    MyWeeklyLogView,
    MyMonthlyLogView,
    MyDailyLogForCertainDateView,
    MyWeeklyLogForCertainWeekView,
    MyMonthlyLogForCertainMonthView,
    RetrieveUpdateDestroyLogView
)
from .report.views import (
    DeveloperMonthlyReportView,
    DeveloperQuarterlyReportView,
    DeveloperWeeklyReportView
)
from api.common.notification.views import NotificationListView, NotificationUpdateView, NotificationUpdateListView

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('financial-requests', FinancialRequestViewSet)
router.register('transactions', TransactionViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)

urlpatterns = router.urls + [
    path('financial-requests/<int:pk>/cancel/', CancelFinanicalRequestView.as_view(), name='cancel_financial_request'),
    path('dashboard/weekly-income/', WeeklyIncomeView.as_view(), name='dashboard_weekly_incoming'),
    path('dashboard/ongoing-projects/', OngoingProjectsView.as_view(), name='dashboard_ongoing_projects'),
    path('dashboard/pending-requests/', PendingRequestsView.as_view(), name='dashboard_pending_requests'),
    path('dashboard/stats/', StatsView.as_view(), name='dashboard_stats'),
    path('dashboard/approved-requests/', ApprovedRequestView.as_view(), name='dashboard_approved_requests'),
    path('reports/this-month/', DeveloperMonthlyReportView.as_view(), name='reports_developer_this-month'),
    path('reports/this-quarter/', DeveloperQuarterlyReportView.as_view(), name='report_developer_quarterly'),
    path('reports/this-week/', DeveloperWeeklyReportView.as_view(), name='report_developer_weekly'),
    path('notifications/', NotificationListView.as_view(), name='unread_notification_lists'),
    path('notifications/<int:pk>/read/', NotificationUpdateView.as_view(), name='update_unread_notification'),
    path('notifications/read-all/', NotificationUpdateListView.as_view(), name='update_all_unread_notification'),
    path('my-logs/', MyLogCreateView.as_view(), name='my_log_create'),
    path('my-logs/<int:pk>/', RetrieveUpdateDestroyLogView.as_view(), name='retrieve_update_destroy_log'),
    path('my-logs/daily/',MyDailyLogView.as_view(), name='my_daily_log_today'),
    path('my-logs/weekly/',MyWeeklyLogView.as_view(), name='my_weekly_log_thisweek'),
    path('my-logs/monthly/',MyMonthlyLogView.as_view(), name='my_monthly_log_thismonth'),
    path('my-logs/daily/<int:year>-<int:month>-<int:day>/',MyDailyLogForCertainDateView.as_view(), name='my_daily_log_certain_date'),
    path('my-logs/weekly/<int:year>-<int:week>/',MyWeeklyLogForCertainWeekView.as_view(), name='my_weekly_log_certain_week'),
    path('my-logs/monthly/<int:year>-<int:month>/',MyMonthlyLogForCertainMonthView.as_view(), name='my_monthly_log_certain_month'),                         
]
