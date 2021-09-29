import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsTeamManager
from api.utils.provider import (
    get_earnings
)
from user.models import User, Team
from api.common.report.serializers import (
    ReportDeveloperSerializer,
    ReportProjectEarningsSerializer
)
from api.common.report.filters import DeveloperReportFilter, DeveloperReportFilter
from api.common.report import constants


class ReportTotalView(GenericAPIView):
    permission_classes = [IsTeamManager]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get(self, obj):
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        viewer = self.request.user
        res =  {'total_earnings': get_earnings(viewer, period, None, None, start_date, end_date)}
        return Response(res)


class ReportDeveloperListView(ListAPIView):
    permission_classes = [IsTeamManager]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)

    def get_serializer_class(self):
        return ReportDeveloperSerializer
    
    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        query_params = self.request.query_params
        serializer_context['period'] = query_params.get('period')
        serializer_context['start_date'] = query_params.get('from')
        serializer_context['end_date'] = query_params.get('to')
        return serializer_context


class ReportDeveloperDetailView(RetrieveAPIView):
    permission_classes = [IsTeamManager]
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))
    
    def get_serializer_class(self):
        return ReportDeveloperSerializer
    
    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        query_params = self.request.query_params
        serializer_context['period'] = query_params.get('period')
        serializer_context['start_date'] = query_params.get('from')
        serializer_context['end_date'] = query_params.get('to')
        return serializer_context


class ReportProjectEarningsListView(RetrieveAPIView):
    permission_classes = [IsTeamManager]
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))
    def get_serializer_class(self):
        return ReportProjectEarningsSerializer
    
    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        query_params = self.request.query_params
        serializer_context['period'] = query_params.get('period')
        serializer_context['start_date'] = query_params.get('from')
        serializer_context['end_date'] = query_params.get('to')
        return serializer_context
