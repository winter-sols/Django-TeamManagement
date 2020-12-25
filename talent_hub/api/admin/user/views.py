from rest_framework import viewsets
from user.models import User, Team
from .serializers import UserAdminSerializer
from ...permission import IsAdmin
from ...common.serializers import TeamSerializer

class UserAdminViewSet(viewsets.ModelViewSet):
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()

class TeamListViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAdmin]
    queryset = Team.objects.all()
