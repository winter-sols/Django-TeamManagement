from django.urls import  include, path
from .user.views import TeamView, TeamUserListView
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('users/', UserTeamViewSet)

urlpatterns = [
    path('team/', TeamView.as_view(), name='team'),
    path('users/', TeamUserListView.as_view(), name='users')

] + router.urls
