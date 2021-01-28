from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from ...permission import IsDeveloper
from api.common.finance.serializers import ClientSerializer, PartnerSerializer, ProjectSerializer, FinancialRequestDetailSerializer, FinancialRequestSerializer
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

class FinancialRequestViewSet(  mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    queryset = FinancialRequest.objects.all()
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return FinancialRequest.objects.all()
        elif self.request.user.is_developer:
            return FinancialRequest.objects.filter(requester=self.request.user)
        elif self.request.user.is_team_manager:
            sets = FinancialRequest.objects.filter(requester__in=self.request.user.team.user_set.all())
            return sets


        #return FinancialRequest.objects.filter(requester=self.request.user)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinancialRequestDetailSerializer
        elif self.request.method in ['POST', 'PUT']:
            return FinancialRequestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = FinancialRequestDetailSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        updated = serializer.update(instance, serializer.validated_data)
        formated = FinancialRequestDetailSerializer(updated)
        return Response(formated.data)
