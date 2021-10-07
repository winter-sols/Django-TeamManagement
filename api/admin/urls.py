from django.urls import  include, path
from rest_framework import routers
from api.common.user.views import  TeamViewSet, ProfilesAdminViewSet, AccountListByProfileIdView, AccountsAdminViewSet
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestViewSet
from api.admin.transaction.views import TransactionViewSet


router = routers.DefaultRouter()
router.register('teams', TeamViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)
#api end-points for finance app

router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('financial-requests', FinancialRequestViewSet)
router.register('transactions', TransactionViewSet, basename="transactions")


urlpatterns = router.urls + [
    path('users/', include('api.common.user.urls')),
    path('profiles/<int:pk>/accounts/', AccountListByProfileIdView.as_view(), name='profile_accounts'),
    path('financial-requests/', include('api.admin.finance.urls')),
    path('dashboard/', include('api.common.dashboard.urls')),
    path('logging/', include('api.admin.logging.urls')),
    path('notifications/', include('api.common.notification.urls')),
    path('my-logs/', include('api.common.logging.urls')),
    path('report/earnings/', include('api.admin.report.urls')),
    path('downloads/report/', include('api.admin.download.urls')),
]
