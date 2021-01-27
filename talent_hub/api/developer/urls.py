from django.urls import  include, path
from rest_framework import routers
from api.common.finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet, FinancialRequestListCreateView

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)

urlpatterns = router.urls + [
    path('financial-requests/', FinancialRequestListCreateView.as_view(), name='financial-request')
]