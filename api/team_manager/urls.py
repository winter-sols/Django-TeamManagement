from django.urls import  include, path
from rest_framework import routers
from .user.views import TeamView, TeamUserListView
from api.common.user.views import ProfilesAdminViewSet, AccountsAdminViewSet
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from .finance.views import CancelFinanicalRequestView
from .logging.views import (
    DailyLogsForTodayView,
    DailyLogsForCertainDateView,
    DailyLogDetailView,
    MonthlyLogsForThisMonthView,
    MonthlyLogsForCertainMonthView,
    MonthlyLogDetailView
)
from api.common.dashboard.views import (
    WeeklyIncomeView,
    OngoingProjectsView,
    PendingRequestsView,
    StatsView,
    ApprovedRequestView
)
from .report.views import (
    TeamMonthlyReportView,
    TeamQuarterlyReportView,
    TeamWeeklyReportView,
    TeamCustomReportView
)
from api.common.notification.views import NotificationListView, NotificationUpdateView


router = routers.DefaultRouter()
# router.register('users/', UserTeamViewSet)

#api end-points for finance app

router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('financial-requests', FinancialRequestViewSet)
router.register('transactions', TransactionViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)

urlpatterns = [
    path('team/', TeamView.as_view(), name='team'),
    path('users/', TeamUserListView.as_view(), name='users'),
    path('financial-requests/<int:pk>/cancel/', CancelFinanicalRequestView.as_view(), name='cancel_financial_request'),
    path('dashboard/weekly-income/', WeeklyIncomeView.as_view(), name='dashboard_weekly_incoming'),
    path('dashboard/ongoing-projects/', OngoingProjectsView.as_view(), name='dashboard_ongoing_projects'),
    path('dashboard/pending-requests/', PendingRequestsView.as_view(), name='dashboard_pending_requests'),
    path('dashboard/stats/', StatsView.as_view(), name='dashboard_stats'),
    path('dashboard/approved-requests/', ApprovedRequestView.as_view(), name='dashboard_approved_requests'),
    path('reports/this-month/', TeamMonthlyReportView.as_view(), name='reports_team_this-month'),
    path('reports/custom/', TeamCustomReportView.as_view(), name='reports_team_custom'),
    path('reports/this-quarter/', TeamQuarterlyReportView.as_view(), name='report_team_quarterly'),
    path('reports/this-week/', TeamWeeklyReportView.as_view(), name='report_team_weekly'),
    path('logging/daily-logs/', DailyLogsForTodayView.as_view(), name='logging_dev_for_manager_today'),
    path('logging/daily-logs/<int:year>-<int:month>-<int:day>/', DailyLogsForCertainDateView.as_view()),
    path('logging/daily-logs/<int:pk>/', DailyLogDetailView.as_view()),
    path('logging/monthly-logs/', MonthlyLogsForThisMonthView.as_view(), name="logging_for_this_month"),
    path('logging/monthly-logs/<int:year>-<int:month>/', MonthlyLogsForCertainMonthView.as_view(), name="logging_for_some_month"),
    path('logging/monthly-logs/<int:pk>/', MonthlyLogDetailView.as_view(), name="monthly_logging_for_team"),
    path('notifications/', NotificationListView.as_view(), name='unread_notification_lists'),
    path('notifications/<int:pk>/read/', NotificationUpdateView.as_view(), name='update_unread_notification'),
] + router.urls
