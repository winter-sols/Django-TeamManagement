from django.urls import  include, path
from rest_framework import routers
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from .finance.views import CancelFinanicalRequestView
from api.common.dashboard.views import WeeklyIncomingView

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('financial-requests', FinancialRequestViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = router.urls + [
    path('financial-requests/<int:pk>/cancel/', CancelFinanicalRequestView.as_view(), name='cancel_financial_request'),
    path('dashboard/', WeeklyIncomingView.as_view(), name='dashboard_weekly_incoming')
]