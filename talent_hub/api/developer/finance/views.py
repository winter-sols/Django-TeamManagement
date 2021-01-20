from rest_framework import viewsets
from ...permission import IsDeveloper
from .serializers import ClientSerializer, PartnerSerializer
from finance.models import Client, Partner

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsDeveloper]
    queryset = Client.objects.all()


class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    permission_classes = [IsDeveloper]
    queryset = Partner.objects.all()
