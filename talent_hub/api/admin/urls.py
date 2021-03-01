from django.urls import  include, path
from rest_framework import routers
from api.common.user.views import UserAdminViewSet, TeamListViewSet, ProfileListAdminView, ProfilesAdminViewSet, AccountListByProfileIdView, AccountsAdminViewSet, TeamUserListView
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from api.admin.finance.views import ApproveFinanicalRequestView, DeclineFinanicalRequestView
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
)

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
    path('reports/developer/this-quarter/', DeveloperQuarterlyReportView.as_view(), name='report_developer_quarterly'),
    path('reports/developer/this-week/', DeveloperWeeklyReportView.as_view(), name='report_developer_weekly'),
    path('reports/team/this-month/', TeamMonthlyReportView.as_view(), name='report_team_monthly'),
    path('reports/team/this-quarter/', TeamQuarterlyReportView.as_view(), name='report_team_quarterly'),
    path('reports/team/this-week/', TeamWeeklyReportView.as_view(), name='report_team_weekly'),
    path('reports/developer/custom/', DeveloperCustomReportView.as_view(), name='report_dev_custom'),
    path('reports/team/custom/', TeamCustomReportView.as_view(), name='report_team_custom')
]
