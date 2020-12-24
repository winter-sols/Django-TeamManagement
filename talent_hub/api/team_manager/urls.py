from django.urls import  include, path
from .user.views import TeamView
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('users/', UserTeamViewSet)

urlpatterns = [
    path('team/', TeamView.as_view(), name='team')
] + router.urls
