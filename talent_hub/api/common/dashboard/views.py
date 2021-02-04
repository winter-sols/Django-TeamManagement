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

class WeeklyIncomingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income_series = get_weekly_income(self.request.user)
        print(get_ongoing_projects(self.request.user))
        # print(income_series.values())
        return Response({
            "weekly_income":income_series.to_list()
        })