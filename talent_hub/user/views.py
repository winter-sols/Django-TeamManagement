from rest_framework import viewsets
from .models import User
from .serializer import UserSerializer

class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    