import pandas as pd
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ...permission import IsDeveloper, IsTeamManager
from finance.models import Project
from api.utils.provider import (
    get_weekly_income,
    get_ongoing_projects
)
from api.common.finance.serializers import ProjectListSerializer

class WeeklyIncomingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income_series = get_weekly_income(self.request.user)

        queryset = get_ongoing_projects(self.request.user)
        project_count = queryset.count()
        ongoing_projects = list(range(project_count))
        for index in range(project_count):
            ongoing_projects[index] = ProjectListSerializer(queryset[index]).data
        
        return Response({
            "weekly_income":income_series.to_list(),
            "ongoing_projects": ongoing_projects
        })