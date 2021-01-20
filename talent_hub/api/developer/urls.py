from django.urls import  include, path
from rest_framework import routers
from .finance.views import ClientViewSet, PartnerViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('projects', ProjectViewSet)

urlpatterns = router.urls