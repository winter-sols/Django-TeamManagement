import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
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


class DeveloperCustomReportView(APIView):
    permission_classes = [IsAdmin]
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = DeveloperReportFilter
    # serializer_class = DeveloperCustomReportSerializer
    # queryset = User.objects.all()

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = User.objects.all()
        user_cnt = queryset.count()
        response = list(range(user_cnt))

        for idx in range(user_cnt):
            user = queryset[idx]
            response[idx] = {
                'id': user.id,
                'full_name': user.first_name + ' ' + user.last_name,
                'earning': get_custom_earning(user, start_date, end_date),
                'project_earnings': get_custom_project_earning(user, start_date, end_date)
            }
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
                'team_earnings': sub_res,
                'total': total
            }
        return Response(response)
