from rest_framework.generics import  RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import TeamUserSerializer, TeamSerializer
from api.permission import IsTeamManager
from user.models import User, Team


class TeamView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsTeamManager]
    serializer_class = TeamSerializer


