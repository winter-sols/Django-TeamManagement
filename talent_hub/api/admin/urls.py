from django.urls import  include, path
from .user.views import UserAdminViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserAdminViewSet)

urlpatterns = router.urls
