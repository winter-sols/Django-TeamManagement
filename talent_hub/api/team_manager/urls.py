from django.urls import  include, path
from rest_framework import routers
from .user.views import TeamView, TeamUserListView
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from .finance.views import CancelFinanicalRequestView
from api.common.dashboard.views import WeeklyIncomingView

router = routers.DefaultRouter()
# router.register('users/', UserTeamViewSet)

#api end-points for finance app

router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('financial-requests', FinancialRequestViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = [
    path('team/', TeamView.as_view(), name='team'),
    path('users/', TeamUserListView.as_view(), name='users'),
    path('financial-requests/<int:pk>/cancel/', CancelFinanicalRequestView.as_view(), name='cancel_financial_request'),
    path('dashboard/', WeeklyIncomingView.as_view(), name='dashboard_weekly_incoming'),

] + router.urls
