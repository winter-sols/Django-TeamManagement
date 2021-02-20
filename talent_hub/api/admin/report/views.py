import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsAdmin
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning
)
from user.models import User, Team
from .serializers import (
    DeveloperReportSerializer, 
    TeamReportSerializer
)
from .filters import DeveloperReportFilter

class DeveloperMonthlyReportView(APIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get(self, request):
        queryset = User.objects.all()
        count = queryset.count()
        reports = list(range(count))

        for index in range(count):
            reports[index] = DeveloperReportSerializer(queryset[index]).data
            reports[index]['earning'] = get_this_month_earning(queryset[index])

        return Response(reports)


class TeamMonthlyReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Team.objects.all()
        count = queryset.count()
        reports = list(range(count))

        for index in range(count):
            reports[index] = TeamReportSerializer(queryset[index]).data
            member_set = queryset[index].user_set.all()
            member_cnt = member_set.count()
            team_earnings = list(range(member_cnt))
            for member_index in range(member_cnt):
                team_earnings[member_index] = get_this_month_earning(member_set[member_index])
            reports[index]['earning'] = np.sum(team_earnings)
        
        return Response(reports)


class DeveloperQuarterlyReportView(APIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get(self, request):
        queryset = User.objects.all()
        count = queryset.count()
        reports = list(range(count))

        for index in range(count):
            reports[index] = DeveloperReportSerializer(queryset[index]).data
            reports[index]['earning'] = get_this_quarter_earning(queryset[index])

        return Response(reports)


class TeamQuarterlyReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Team.objects.all()
        count = queryset.count()
        reports = list(range(count))

        for index in range(count):
            reports[index] = TeamReportSerializer(queryset[index]).data
            member_set = queryset[index].user_set.all()
            member_cnt = member_set.count()
            team_earnings = list(range(member_cnt))
            for member_index in range(member_cnt):
                team_earnings[member_index] = get_this_quarter_earning(member_set[member_index])
            reports[index]['earning'] = np.sum(team_earnings)
        
        return Response(reports)


class DeveloperWeeklyReportView(APIView):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get(self, request):
        queryset = User.objects.all()
        count = queryset.count()
        reports = list(range(count))

        for index in range(count):
            reports[index] = DeveloperReportSerializer(queryset[index]).data
            reports[index]['earning'] = get_this_week_earning(queryset[index])

        return Response(reports)


class TeamWeeklyReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Team.objects.all()
        count = queryset.count()
        reports = list(range(count))

        for index in range(count):
            reports[index] = TeamReportSerializer(queryset[index]).data
            member_set = queryset[index].user_set.all()
            member_cnt = member_set.count()
            team_earnings = list(range(member_cnt))
            for member_index in range(member_cnt):
                team_earnings[member_index] = get_this_week_earning(member_set[member_index])
            reports[index]['earning'] = np.sum(team_earnings)
        
        return Response(reports)
