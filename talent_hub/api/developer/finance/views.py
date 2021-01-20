from rest_framework import viewsets
from ...permission import IsDeveloper
from .serializers import ClientSerializer
from finance.models import Client

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsDeveloper]
    queryset = Client.objects.all()
