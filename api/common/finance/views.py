from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ...permission import IsDeveloper, IsTeamManager, IsTeamManagerOrDeveloper
from api.common.finance.serializers import (
    ClientDetailSerializer,
    ClientUpdateSerializer,
    PartnerSerializer,
    PartnerDetailSerializer,
    ProjectSerializer,
    ProjectListSerializer,
    FinancialRequestDetailSerializer,
    FinancialRequestSerializer,
    PaymentAccountSerializer
)
from finance.models import (
    Client, 
    Partner,
    Project,
    FinancialRequest,
    PaymentAccount
)
from .filters import (
    ProjectFilter,
    FinancialRequestFilter,
)
import datetime

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Client.objects.none()
        elif self.request.user.is_admin:
            return Client.objects.all()
        elif self.request.user.is_developer:
            return Client.objects.filter(owner=self.request.user)
        elif self.request.user.is_team_manager:
            return Client.objects.filter(owner__in=self.request.user.team_members)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST', 'PATCH']:
            return ClientUpdateSerializer
        return ClientDetailSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Partner.objects.all()
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Partner.objects.none()
        elif self.request.user.is_admin:
            return Partner.objects.all()
        elif self.request.user.is_developer:
            return Partner.objects.filter(owner=self.request.user)
        elif self.request.user.is_team_manager:
            return Partner.objects.filter(owner__in=self.request.user.team_members)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST', 'PATCH']:
            return PartnerSerializer
        return PartnerDetailSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
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
        if user.is_anonymous:
            return Project.objects.none()
        elif user.is_admin:
            return Project.objects.all()
        elif user.is_developer:
            return Project.objects.filter(project_starter=user)
        elif user.is_team_manager:
            return Project.objects.filter(project_starter__in=user.team_members)


class FinancialRequestViewSet(  mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FinancialRequest.objects.all()
    filterset_class = FinancialRequestFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['requested_at']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return FinancialRequest.objects.none()
        elif self.request.user.is_admin:
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
        # serializer.data[]
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


class PaymentAccountView(ListAPIView):
    serializer_class = PaymentAccountSerializer
    permission_classes = [IsTeamManagerOrDeveloper]
    queryset = PaymentAccount.objects.all()

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return PaymentAccount.objects.none()
        elif self.request.user.is_team_manager or self.request.user.is_developer:
            return PaymentAccount.objects.all()
