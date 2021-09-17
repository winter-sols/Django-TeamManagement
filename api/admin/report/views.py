import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsAdmin
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning,
    get_custom_earning,
    get_custom_project_earning
)
from user.models import User, Team
from api.common.report.serializers import (
    DeveloperMonthlyReportSerializer,
    DeveloperQuarterlyReportSerializer,
    DeveloperWeeklyReportSerializer, 
    TeamMonthlyReportSerializer,
    TeamQuarterlyReportSerializer,
    TeamWeeklyReportSerializer,
    DeveloperCustomReportSerializer
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    queryset = User.objects.all()

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = User.objects.all()
        user_cnt = queryset.count()
        response = list(range(user_cnt))
        page = self.paginate_queryset(queryset)

        for idx in range(user_cnt):
            user = queryset[idx]
            response[idx] = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'earning': get_custom_earning(user, start_date, end_date),
                'project_earnings': get_custom_project_earning(user, start_date, end_date)
            }

        if page is not None:
            return self.get_paginated_response(response)
        return Response(response)


class TeamCustomReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = Team.objects.all()
        team_cnt = queryset.count()
        response = list(range(team_cnt))

        for idx in range(team_cnt):
            team = queryset[idx]
            userset = team.user_set.all()
            user_cnt = userset.count()
            sub_res = list(range(user_cnt))
            total = 0
            for usr_idx in range(user_cnt):
                user = userset[usr_idx]
                earning = get_custom_earning(user, start_date, end_date)
                total += earning
                sub_res[usr_idx] = {
                    'id': user.id,
                    'full_name': user.first_name + ' ' + user.last_name,
                    'earning': earning
                }
            
            response[idx] = {
                'earning': sub_res,
                'total': total,
                'id': team.id,
                'name': team.name,
            }
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
            earning[idx] = get_this_month_earning(user)
        
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
            earning[idx] = get_this_quarter_earning(user)
        
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
            earning[idx] = get_this_week_earning(user)
        
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
            earning[idx] = get_custom_earning(user, start_date, end_date)

        df = pd.DataFrame({
            'full name': full_name,
            'earning': earning
        }, index=range(1, count + 1))

        return get_download_response(df, "developer.csv")
