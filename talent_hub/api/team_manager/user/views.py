from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from ...common.serializers import TeamSerializer
from .serializers import TeamUserListSerializer
from api.permission import IsTeamManager
from django.shortcuts import get_object_or_404
from user.models import User, Team


class TeamView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_object(self):
        return self.request.user.team


class TeamUserListView(ListAPIView):
    serializer_class = TeamUserListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.team.user_set.all()
