import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsAdmin
from api.utils.provider import (
    get_earnings,
    get_project_earnings
)
from user.models import User, Team
from user.constants import ROLE_DEVELOPER, ROLE_TEAM_MANAGER
from api.common.report.serializers import (
    DeveloperMonthlyReportSerializer,
    DeveloperQuarterlyReportSerializer,
    DeveloperWeeklyReportSerializer, 
    TeamMonthlyReportSerializer,
    TeamQuarterlyReportSerializer,
    TeamWeeklyReportSerializer,
    # DeveloperCustomReportSerializer
)
from api.common.report.filters import DeveloperReportFilter, TeamReportFilter
from api.utils.download import get_download_response

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
    pagination_class = None


class TeamQuarterlyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TeamQuarterlyReportSerializer
    queryset = Team.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter
    pagination_class = None


class TeamWeeklyReportView(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TeamWeeklyReportSerializer
    queryset = Team.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TeamReportFilter
    pagination_class = None


class DeveloperCustomReportView(GenericAPIView):
    permission_classes = [IsAdmin]
    # serializer_class = DeveloperCustomReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    queryset = User.objects.all()

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = User.objects.filter(team = team_id)
        else:
            queryset = User.objects.all()
        page = self.paginate_queryset(queryset)
        response = []

        for user in queryset:
            response.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'earning': get_earnings(user, start_date=start_date, end_date=end_date),
                'project_earnings': get_project_earnings(user, start_date=start_date, end_date=end_date)
            })

        if page is not None:
            return self.get_paginated_response(response)
        return Response(response)


class TeamCustomReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = Team.objects.all()
        response = []

        for team in queryset:
            userset = team.user_set.all()
            sub_res = []
            total = 0
            for user in userset:
                earning = get_earnings(user, start_date=start_date, end_date=end_date)
                total += earning
                sub_res.append({
                    'id': user.id,
                    'full_name': user.first_name + ' ' + user.last_name,
                    'earning': earning
                })
            
            response.append({
                'earning': sub_res,
                'total': total,
                'id': team.id,
                'name': team.name,
            })
        return Response(response)


class DeveloperThisMonthReportDownloadView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DeveloperMonthlyReportSerializer
    queryset = User.objects.all()

    def get(self, request):
        queryset = User.objects.all()
        count = queryset.count()

        full_name = list(range(count))
        earning = list(range(count))
        
        for idx in range(count):
            user = queryset[idx]
            full_name[idx] = user.first_name + ' ' + user.last_name
            earning[idx] = get_earnings(user, 'this-month', None, user)
        
        df = pd.DataFrame({
            'full name': full_name,
            'earning': earning
        }, index=range(1, count + 1))

        return get_download_response(df, "developer.csv")


class DeveloperThisQuarterReportDownloadView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DeveloperQuarterlyReportSerializer
    queryset = User.objects.all()

    def get(self, request):
        queryset = User.objects.all()
        count = queryset.count()

        full_name = list(range(count))
        earning = list(range(count))
        
        for idx in range(count):
            user = queryset[idx]
            full_name[idx] = user.first_name + ' ' + user.last_name
            earning[idx] = get_earnings(user, 'this-quarter', None, user)
        
        df = pd.DataFrame({
            'full name': full_name,
            'earning': earning
        }, index=range(1, count + 1))

        return get_download_response(df, "developer.csv")


class DeveloperThisWeekReportDownloadView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DeveloperWeeklyReportSerializer
    queryset = User.objects.all()

    def get(self, request):
        queryset = User.objects.all()
        count = queryset.count()

        full_name = list(range(count))
        earning = list(range(count))
        
        for idx in range(count):
            user = queryset[idx]
            full_name[idx] = user.first_name + ' ' + user.last_name
            earning[idx] = get_earnings(user, 'this-week')
        
        df = pd.DataFrame({
            'full name': full_name,
            'earning': earning
        }, index=range(1, count + 1))

        return get_download_response(df, "developer.csv")


class DeveloperCustomReportDownloadView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DeveloperWeeklyReportSerializer
    queryset = User.objects.all()

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = User.objects.all()
        count = queryset.count()
        full_name = list(range(count))
        earning = list(range(count))
        for idx in range(count):
            user = queryset[idx]
            full_name[idx] = user.first_name + ' ' + user.last_name
            earning[idx] = get_earnings(user, ROLE_DEVELOPER, start_date, end_date)

        df = pd.DataFrame({
            'full name': full_name,
            'earning': earning
        }, index=range(1, count + 1))

        return get_download_response(df, "developer.csv")
