import pandas as pd
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permission import IsDeveloper, IsTeamManager
from finance.models import Project
from api.utils.provider import (
    get_weekly_income,
    get_ongoing_projects,
    get_pending_financial_requests,
    get_this_month_expectation,
    get_this_month_earning,
    get_this_quarter_expectation,
    get_this_quarter_earning,
    get_approved_financial_requests
)
from api.common.finance.serializers import (
    ProjectListSerializer,
    FinancialRequestDetailSerializer
)
from user.models import User, Team


class BaseDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def validate_query_params(self):
        team_id = self.request.query_params.get('team')
        user_id = self.request.query_params.get('user')
        if team_id is not None:
            team_qs = Team.objects.filter(id=team_id)
            self.team = get_object_or_404(team_qs)
        else:
            self.team = None
        
        if user_id is not None:
            user_qs = User.objects.filter(id=user_id)
            self.user = get_object_or_404(user_qs)
        else:
            self.user = None


class WeeklyIncomeView(BaseDashboardView):

    def get(self, request):
        self.validate_query_params()
        
        viewer = self.request.user
        income_series = get_weekly_income(viewer, self.team, self.user)
        return Response(income_series.to_list())


class OngoingProjectsView(BaseDashboardView):

    def get(self, request):
        self.validate_query_params()

        viewer = self.request.user
        queryset = get_ongoing_projects(viewer, self.team, self.user)
        project_count = queryset.count()
        ongoing_projects = list(range(project_count))
        for index in range(project_count):
            ongoing_projects[index] = ProjectListSerializer(queryset[index]).data
        return Response(ongoing_projects)
from user.models import User, Team

class PendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = self.request.user
        team_id = self.request.query_params.get('team')
        user_id = self.request.query_params.get('user')
        queryset = get_pending_financial_requests(viewer, team_id, user_id)
        requests_count = queryset.count()
        pending_requests = list(range(requests_count))
        for index in range(requests_count):
            pending_requests[index] = FinancialRequestDetailSerializer(queryset[index]).data
        return Response(pending_requests)


class ApprovedRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = self.request.user
        team_id = self.request.query_params.get('team')
        user_id = self.request.query_params.get('user')
        queryset = get_approved_financial_requests(viewer, team_id, user_id)
        requests_count = queryset.count()
        approved_requests = list(range(requests_count))
        for index in range(requests_count):
            approved_requests[index] = FinancialRequestDetailSerializer(queryset[index]).data
        return Response(approved_requests)


class StatsView(BaseDashboardView):
    def get(self, request):
        self.validate_query_params()
        viewer = self.request.user
        this_month_expectation = get_this_month_expectation(viewer, self.team, self.user)
        this_month_earning = get_this_month_earning(viewer, self.team, self.user)
        this_quarter_expectation = get_this_quarter_expectation(viewer, self.team, self.user)
        this_quarter_earning = get_this_quarter_earning(viewer, self.team, self.user)

        return Response({
            "this_month_expectation": this_month_expectation,
            "this_month_earning": this_month_earning,
            "this_quarter_expectation": this_quarter_expectation,
            "this_quarter_earning": this_quarter_earning,
        })
