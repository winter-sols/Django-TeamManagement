from rest_framework import viewsets
from user.models import User
from .serializers import UserAdminSerializer

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
