from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from ...permission import IsDeveloper, IsTeamManager
from api.common.finance.serializers import (
    ClientDetailSerializer,
    ClientUpdateSerializer,
    PartnerSerializer,
    PartnerDetailSerializer,
    ProjectSerializer,
    ProjectListSerializer,
    FinancialRequestDetailSerializer,
    FinancialRequestSerializer,
    TransactionDetailSerializer
)
from finance.models import (
    Client, 
    Partner,
    Project,
    FinancialRequest,
    Transaction
)
from .filters import (
    ProjectFilter,
    FinancialRequestFilter,
    TransactionFilter
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()

    def get_queryset(self):
        if self.request.user.is_admin:
            return Client.objects.all()
        elif self.request.user.is_developer:
            return Client.objects.filter(owner=self.request.user)
        elif self.request.user.is_team_manager:
            return Client.objects.filter(owner__in=self.request.user.team_members)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientDetailSerializer
        elif self.request.method in ['PUT', 'POST']:
            return ClientUpdateSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Partner.objects.all()
        elif self.request.user.is_developer:
            return Partner.objects.filter(owner=self.request.user)
        elif self.request.user.is_team_manager:
            return Partner.objects.filter(owner__in=self.request.user.team_members)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartnerDetailSerializer
        elif self.request.method in ['PUT', 'POST']:
            return PartnerSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.action == 'list':
            return ProjectListSerializer
        else:
            return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        elif user.is_developer:
            return Project.objects.filter(project_starter=user)
        elif user.is_team_manager:
            return Project.objects.filter(project_starter__in=user.team_members)


class FinancialRequestViewSet(  mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    queryset = FinancialRequest.objects.all()
    filterset_class = FinancialRequestFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['requested_at']

    def get_queryset(self):
        if self.request.user.is_admin:
            return FinancialRequest.objects.order_by('-requested_at')
        elif self.request.user.is_developer:
            return FinancialRequest.objects.filter(requester=self.request.user).order_by('-requested_at')
        elif self.request.user.is_team_manager:
            sets = FinancialRequest.objects.filter(requester__in=self.request.user.team_members).order_by('-requested_at')
            return sets


        #return FinancialRequest.objects.filter(requester=self.request.user)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinancialRequestDetailSerializer
        elif self.request.method in ['POST', 'PUT']:
            return FinancialRequestSerializer

    def create(self, request):
        serializer_data = request.data
        serializer_data['requester'] = self.request.user.id
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


class TransactionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TransactionDetailSerializer
    queryset = Transaction.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Transaction.objects.order_by('-created_at')
        elif user.is_developer:
            return Transaction.objects.filter(financial_request__requester=user).order_by('-created_at')
        elif user.is_team_manager:
            return Transaction.objects.filter(financial_request__requester__in=user.team_members).order_by('-created_at')

