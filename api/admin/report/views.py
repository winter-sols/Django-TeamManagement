import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.views import generic
from django.http import HttpResponse

from api.permission import IsAdmin
from api.utils.provider import (
    get_earnings,
    get_queryset_with_developer_earnings,
    get_queryset_with_team_earnings,
    get_queryset_with_project_earnings
)
from finance import constants as cs
from user.models import User, Team
from finance.models import Project
from user.constants import ROLE_DEVELOPER, ROLE_TEAM_MANAGER
from api.common.report.serializers import (
    ReportProjectEarningsSerializer,
    ReportDeveloperSerializer,
    ReportTeamSerializer,
)
from api.common.report.filters import DeveloperReportFilter, TeamReportFilter
from api.common.report import constants


class ReportTotalView(GenericAPIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get(self, obj):
        query_params = self.request.query_params
        viewer = self.request.user
        period = query_params.get('period')
        start_date = query_params.get('from')
        end_date = query_params.get('to')
        res =  {'total_earnings': get_earnings(viewer, period, start_date, end_date)}
        return Response(res)


class ReportDeveloperListView(ListAPIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = ReportDeveloperSerializer
    queryset = User.objects.all()

    def filter_queryset(self, queryset):
        return get_queryset_with_developer_earnings(
            super().filter_queryset(queryset),
            self.request.query_params
        )


class ReportDeveloperDetailView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReportDeveloperSerializer

    def get_queryset(self):
        return get_queryset_with_developer_earnings(
            User.objects.filter(id=self.kwargs.get('pk')),
            self.request.query_params
        )


class ReportProjectEarningsListView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReportProjectEarningsSerializer
    pagination_class = None
    
    def get_queryset(self):
        return get_queryset_with_project_earnings(
            Project.objects.filter(financialrequest__requester=self.kwargs.get('pk')),
            self.request.query_params
        )
    


class ReportTeamListView(ListAPIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter
    serializer_class = ReportTeamSerializer
    pagination_class = None
    queryset = Team.objects.all()

    def filter_queryset(self, queryset):
        return get_queryset_with_team_earnings(
            super().filter_queryset(queryset),
            self.request.query_params
        )


class ReportTeamDetailView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ReportTeamSerializer
    pagination_class = None

    def get_queryset(self):
        return get_queryset_with_team_earnings(
            Team.objects.filter(id=self.kwargs.get('pk')),
            self.request.query_params
        )
