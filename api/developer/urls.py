from django.urls import  include, path
from rest_framework import routers
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, TransactionViewSet
from api.common.user.views import ProfilesAdminViewSet, AccountsAdminViewSet


router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)
router.register('transactions', TransactionViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)

urlpatterns = router.urls + [
    path('financial-requests/', include('api.developer.finance.urls')),
    path('dashboard/', include('api.common.dashboard.urls')),
    path('notifications/', include('api.common.notification.urls')),
    path('my-logs/', include('api.common.logging.urls')),
    path('report/earnings/', include('api.developer.report.urls')),
]
