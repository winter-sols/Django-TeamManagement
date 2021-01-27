from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ...permission import IsDeveloper
from .serializers import ClientSerializer, PartnerSerializer, ProjectSerializer, FinancialRequestDetailSerializer, FinancialRequestSerializer
from finance.models import Client, Partner, Project, FinancialRequest

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

class FinancialRequestListCreateView(ListCreateAPIView):
    # serializer_class = FinancialRequestDetailSerializer
    permission_classes = [IsDeveloper]
    queryset = FinancialRequest.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinancialRequestDetailSerializer
        elif self.request.method == 'POST':
            return FinancialRequestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = FinancialRequestDetailSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
