from django.urls import  include, path
from .user.views import UserAdminViewSet, TeamListViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserAdminViewSet)
router.register('teams', TeamListViewSet)
urlpatterns = router.urls
