import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsTeamManager
from api.utils.provider import (
    get_total_earnings
)
from user.models import User, Team
from api.common.report.serializers import (
    DeveloperReportSerializer,
    IndividualDeveloperProjectSerializer
)
from api.common.report.filters import DeveloperReportFilter, DeveloperReportFilter
from api.common.report import constants


class ReportTotalView(ListAPIView):
    permission_classes = [IsTeamManager]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)

    def get(self, obj):
        users = self.get_queryset()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        res =  {'total_earnings': get_total_earnings(users, period, start_date, end_date)}
        return Response(res)


class DevelopersReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    
    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)

    def get_serializer_class(self):
        return DeveloperReportSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)    


class IndividualDeveloperReportView(RetrieveAPIView):
    permission_classes = [IsTeamManager]
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))
    
    def get_serializer_class(self):
        return DeveloperReportSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)


class IndividualDeveloperProjectReportView(RetrieveAPIView):
    permission_classes = [IsTeamManager]
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))
    def get_serializer_class(self):
        return IndividualDeveloperProjectSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)
