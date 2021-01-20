from rest_framework import viewsets
from ...permission import IsDeveloper
from .serializers import ClientSerializer, PartnerSerializer, ProjectSerializer
from finance.models import Client, Partner, Project

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsDeveloper]
    queryset = Client.objects.all()


class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    permission_classes = [IsDeveloper]
    queryset = Partner.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsDeveloper]
    queryset = Project.objects.all()
