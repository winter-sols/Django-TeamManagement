import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsAdmin
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning
)
from user.models import User, Team
from .serializers import (
    DeveloperMonthlyReportSerializer,
    DeveloperQuarterlyReportSerializer,
    DeveloperWeeklyReportSerializer, 
    TeamMonthlyReportSerializer,
    TeamQuarterlyReportSerializer,
    TeamWeeklyReportSerializer
)
from .filters import DeveloperReportFilter, TeamReportFilter


class DeveloperMonthlyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperMonthlyReportSerializer
    queryset = User.objects.all()


class DeveloperQuarterlyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperQuarterlyReportSerializer
    queryset = User.objects.all()


class DeveloperWeeklyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperWeeklyReportSerializer
    queryset = User.objects.all()


class TeamMonthlyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TeamMonthlyReportSerializer
    queryset = Team.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter


class TeamQuarterlyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TeamQuarterlyReportSerializer
    queryset = Team.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter


class TeamWeeklyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TeamWeeklyReportSerializer
    queryset = Team.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter
