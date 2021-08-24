import pandas as pd
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
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
    get_this_week_approved_requests
)
from api.common.finance.serializers import (
    ProjectListSerializer,
    FinancialRequestDetailSerializer
)
class WeeklyIncomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income_series = get_weekly_income(self.request.user)
        return Response(income_series.to_list())


class OngoingProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = get_ongoing_projects(self.request.user)
        project_count = queryset.count()
        ongoing_projects = list(range(project_count))
        for index in range(project_count):
            ongoing_projects[index] = ProjectListSerializer(queryset[index]).data
        return Response(ongoing_projects)


class PendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = get_pending_financial_requests(self.request.user)
        requests_count = queryset.count()
        pending_requests = list(range(requests_count))
        for index in range(requests_count):
            pending_requests[index] = FinancialRequestDetailSerializer(queryset[index]).data
        return Response(pending_requests)


class ApprovedRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        approved_requests = get_this_week_approved_requests(self.request.user)
        return Response(approved_requests)


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        this_month_expectation = get_this_month_expectation(self.request.user)
        this_month_earning = get_this_month_earning(self.request.user)
        this_quarter_expectation = get_this_quarter_expectation(self.request.user)
        this_quarter_earning = get_this_quarter_earning(self.request.user)
        approved_requests = get_this_week_approved_requests(self.request.user)

        return Response({
            "this_month_expectation": this_month_expectation,
            "this_month_earning": this_month_earning,
            "this_quarter_expectation": this_quarter_expectation,
            "this_quarter_earning": this_quarter_earning,
        })