import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsTeamManager
from api.utils.provider import (
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


class TeamCustomReportView(APIView):
    permission_classes = [IsTeamManager]

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = Team.objects.filter(id=self.request.user.team.id)
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
                earning = get_custom_earning(user, user.role, start_date, end_date)
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
