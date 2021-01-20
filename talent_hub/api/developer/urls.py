from django.urls import  include, path
from rest_framework import routers
from .finance.views import ClientViewSet
router = routers.DefaultRouter()
router.register('clients', ClientViewSet)

urlpatterns = router.urls