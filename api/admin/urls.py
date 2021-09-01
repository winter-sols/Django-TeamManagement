from django.urls import  include, path
from rest_framework import routers
from api.common.user.views import UserAdminViewSet, TeamListViewSet, ProfileListAdminView, ProfilesAdminViewSet, AccountListByProfileIdView, AccountsAdminViewSet, TeamUserListView
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from api.admin.finance.views import ApproveFinanicalRequestView, DeclineFinanicalRequestView
from api.admin.logging.views import (
    DailyLogsForTodayView,
    DailyLogDetailView,
    DailyLogsForCertainDateView,
    MonthlyLogsForThisMonthView,
    MonthlyLogsForCertainMonthView,
    MonthlyLogDetailView
)
from api.admin.logging.views import  WeeklyLogsForThisWeekView, WeeklyLogsforCertainWeekView, WeeklyLogDetailView
from api.common.dashboard.views import (
    WeeklyIncomeView,
    OngoingProjectsView,
    PendingRequestsView,
    StatsView,
    ApprovedRequestView
)
from .report.views import (
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
)
from api.common.notification.views import NotificationListView, NotificationUpdateView



router = routers.DefaultRouter()
router.register('users', UserAdminViewSet)
router.register('teams', TeamListViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)
#api end-points for finance app

router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('financial-requests', FinancialRequestViewSet)
router.register('transactions', TransactionViewSet)


urlpatterns = router.urls + [
    path('users/<int:pk>/profiles/', ProfileListAdminView.as_view(), name='user_profiles'),
    path('profiles/<int:pk>/accounts/', AccountListByProfileIdView.as_view(), name='profile_accounts'),
    path('teams/<int:pk>/users/', TeamUserListView.as_view(), name='users_by_team_id'),
    path('financial-requests/<int:pk>/approve/', ApproveFinanicalRequestView.as_view(), name='approve_financial_requests'),
    path('financial-requests/<int:pk>/decline/', DeclineFinanicalRequestView.as_view(), name='decline_financial_requests'),
    path('dashboard/weekly-income/', WeeklyIncomeView.as_view(), name='dashboard_weekly_incoming'),
    path('dashboard/ongoing-projects/', OngoingProjectsView.as_view(), name='dashboard_ongoing_projects'),
    path('dashboard/pending-requests/', PendingRequestsView.as_view(), name='dashboard_pending_requests'),
    path('dashboard/stats/', StatsView.as_view(), name='dashboard_stats'),
    path('dashboard/approved-requests/', ApprovedRequestView.as_view(), name='dashboard_approved_requests'),
    path('reports/developer/this-month/', DeveloperMonthlyReportView.as_view(), name='report_developer_monthly'),
    path('reports/developer/this-month/download/', DeveloperThisMonthReportDownloadView.as_view(), name='report_developer_monthly_download'),
    path('reports/developer/this-quarter/', DeveloperQuarterlyReportView.as_view(), name='report_developer_quarterly'),
    path('reports/developer/this-quarter/download/', DeveloperThisQuarterReportDownloadView.as_view(), name='report_developer_quarterly'),
    path('reports/developer/this-week/', DeveloperWeeklyReportView.as_view(), name='report_developer_weekly'),
    path('reports/developer/this-week/download/', DeveloperThisWeekReportDownloadView.as_view(), name='report_developer_weekly'),
    path('reports/team/this-month/', TeamMonthlyReportView.as_view(), name='report_team_monthly'),
    path('reports/team/this-quarter/', TeamQuarterlyReportView.as_view(), name='report_team_quarterly'),
    path('reports/team/this-week/', TeamWeeklyReportView.as_view(), name='report_team_weekly'),
    path('reports/developer/custom/', DeveloperCustomReportView.as_view(), name='report_dev_custom'),
    path('reports/developer/custom/', DeveloperCustomReportDownloadView.as_view(), name='report_dev_custom'),
    path('reports/team/custom/', TeamCustomReportView.as_view(), name='report_team_custom'),
    path('logging/daily-logs/', DailyLogsForTodayView.as_view(), name='logging_dev_today'),
    path('logging/daily-logs/<int:year>-<int:month>-<int:day>/', DailyLogsForCertainDateView.as_view()),
    path('logging/daily-logs/<int:pk>/', DailyLogDetailView.as_view()),
    path('logging/monthly-logs/', MonthlyLogsForThisMonthView.as_view(), name="logging_for_this_month"), 
    path('logging/monthly-logs/<int:year>-<int:month>/', MonthlyLogsForCertainMonthView.as_view(), name="logging_for_certain_month"),
    path('logging/monthly-logs/<int:pk>/', MonthlyLogDetailView.as_view(), name="detail_logging_monthly"),
    path('logging/weekly-logs/', WeeklyLogsForThisWeekView.as_view(), name='logging_for_this_week'),
    path('logging/weekly-logs/<int:year>-<int:week>/', WeeklyLogsforCertainWeekView.as_view(), name='logging_for_certain_week'),
    path('logging/weekly-logs/<int:pk>/', WeeklyLogDetailView.as_view(), name='detail_logging_until_thisweek'),
    path('notifications/', NotificationListView.as_view(), name='unread_notification_lists'),
    path('notifications/<int:pk>/read/', NotificationUpdateView.as_view(), name='update_unread_notification'),
]
