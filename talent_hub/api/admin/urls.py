from django.urls import  include, path
from rest_framework import routers
from .user.views import UserAdminViewSet, TeamListViewSet, ProfileListAdminView, ProfilesAdminViewSet, AccountListByProfileIdView, AccountsAdminViewSet, TeamUserListView
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet, TransactionViewSet
from api.admin.finance.views import ApproveFinanicalRequestView, DeclineFinanicalRequestView
from api.common.dashboard.views import WeeklyIncomingView

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
    path('dashboard/', WeeklyIncomingView.as_view(), name='dashboard_weekly_incoming'),
]
