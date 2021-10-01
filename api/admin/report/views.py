import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsAdmin
from api.utils.provider import (
    get_earnings,
    get_queryset_with_developer_earnings,
    get_queryset_with_team_earnings
)
from finance import constants as cs
from user.models import User, Team
from user.constants import ROLE_DEVELOPER, ROLE_TEAM_MANAGER
from api.common.report.serializers import (
    ReportProjectEarningsSerializer,
    ReportDeveloperSerializer,
    ReportTeamSerializer,
)
from api.common.report.filters import DeveloperReportFilter, TeamReportFilter
from api.utils.download import get_download_response
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
        res =  {'total_earnings': get_earnings(viewer, period, None, None, start_date, end_date)}
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


class ReportProjectEarningsListView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    
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


# class DeveloperThisMonthReportDownloadView(RetrieveAPIView):
#     permission_classes = [IsAdmin]
#     serializer_class = DeveloperMonthlyReportSerializer
#     queryset = User.objects.all()

#     def get(self, request):
#         queryset = User.objects.all()
#         count = queryset.count()

#         full_name = list(range(count))
#         earning = list(range(count))
        
#         for idx in range(count):
#             user = queryset[idx]
#             full_name[idx] = user.first_name + ' ' + user.last_name
#             earning[idx] = get_earnings(user, 'this-month', None, user)
        
#         df = pd.DataFrame({
#             'full name': full_name,
#             'earning': earning
#         }, index=range(1, count + 1))

#         return get_download_response(df, "developer.csv")


# class DeveloperThisQuarterReportDownloadView(RetrieveAPIView):
#     permission_classes = [IsAdmin]
#     serializer_class = DeveloperQuarterlyReportSerializer
#     queryset = User.objects.all()

#     def get(self, request):
#         queryset = User.objects.all()
#         count = queryset.count()

#         full_name = list(range(count))
#         earning = list(range(count))
        
#         for idx in range(count):
#             user = queryset[idx]
#             full_name[idx] = user.first_name + ' ' + user.last_name
#             earning[idx] = get_earnings(user, 'this-quarter', None, user)
        
#         df = pd.DataFrame({
#             'full name': full_name,
#             'earning': earning
#         }, index=range(1, count + 1))

#         return get_download_response(df, "developer.csv")


# class DeveloperThisWeekReportDownloadView(RetrieveAPIView):
#     permission_classes = [IsAdmin]
#     serializer_class = DeveloperWeeklyReportSerializer
#     queryset = User.objects.all()

#     def get(self, request):
#         queryset = User.objects.all()
#         count = queryset.count()

#         full_name = list(range(count))
#         earning = list(range(count))
        
#         for idx in range(count):
#             user = queryset[idx]
#             full_name[idx] = user.first_name + ' ' + user.last_name
#             earning[idx] = get_earnings(user, 'this-week')
        
#         df = pd.DataFrame({
#             'full name': full_name,
#             'earning': earning
#         }, index=range(1, count + 1))

#         return get_download_response(df, "developer.csv")


# class DeveloperCustomReportDownloadView(RetrieveAPIView):
#     permission_classes = [IsAdmin]
#     serializer_class = DeveloperWeeklyReportSerializer
#     queryset = User.objects.all()

#     def get(self, request):
#         start_date = self.request.query_params.get('from')
#         end_date = self.request.query_params.get('to')
#         queryset = User.objects.all()
#         count = queryset.count()
#         full_name = list(range(count))
#         earning = list(range(count))
#         for idx in range(count):
#             user = queryset[idx]
#             full_name[idx] = user.first_name + ' ' + user.last_name
#             earning[idx] = get_earnings(user, ROLE_DEVELOPER, start_date, end_date)

#         df = pd.DataFrame({
#             'full name': full_name,
#             'earning': earning
#         }, index=range(1, count + 1))

#         return get_download_response(df, "developer.csv")
