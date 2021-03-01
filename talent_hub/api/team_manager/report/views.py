import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsTeamManager
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning,
    get_custom_earning,
    get_custom_project_earning
)
from user.models import User, Team
from api.common.report.serializers import (
    TeamMonthlyReportSerializer,
    TeamQuarterlyReportSerializer,
    TeamWeeklyReportSerializer,
)
from api.common.report.filters import TeamReportFilter


class TeamMonthlyReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    serializer_class = TeamMonthlyReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter

    def get_queryset(self):
        return Team.objects.filter(id=self.request.user.team.id)


class TeamQuarterlyReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    serializer_class = TeamQuarterlyReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter

    def get_queryset(self):
        return Team.objects.filter(id=self.request.user.team.id)


class TeamWeeklyReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    serializer_class = TeamWeeklyReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter

    def get_queryset(self):
        return Team.objects.filter(id=self.request.user.team.id)
