from rest_framework import viewsets
from user.models import User, Team
from .serializers import UserAdminSerializer, TeamListSerializer
from ...permission import IsAdmin

class UserAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer

class TeamListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Team.objects.all()
    serializer_class = TeamListSerializer