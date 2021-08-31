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
from .report.views import (
    DeveloperMonthlyReportView,
    DeveloperQuarterlyReportView,
    DeveloperWeeklyReportView
)

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
]
