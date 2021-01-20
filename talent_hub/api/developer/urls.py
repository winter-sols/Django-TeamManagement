from django.urls import  include, path
from rest_framework import routers
from .finance.views import ClientViewSet, PartnerViewSet

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)

urlpatterns = router.urls