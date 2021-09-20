from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.common.logging.serializers import LogDetailSerializer
import datetime
from reporting.models import Log
from ...permission import IsTeamManager


class DailyLogsForTodayView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        return Log.objects.daily_logs_for_today_for_team(self.request.user)


class WeeklyLogsForThisWeekView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]
    queryset = Log.objects.weekly_logs_for_thisweek()


class DailyLogsForCertainDateView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        dt = datetime.date(year, month, day)
        return Log.objects.daily_logs_for_date_for_team(dt, self.request.user)


class WeeklyLogsforCertainWeekView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes =[IsTeamManager]

    def get_queryset(self):
        year = self.kwargs['year']
        week = self.kwargs['week']
        return Log.objects.weekly_logs_for_week(year, week)


class DailyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Log.objects.none()
        else:
            return Log.objects.daily_logs_for_team(self.request.user)


class MonthlyLogsForThisMonthView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        return Log.objects.monthly_logs_for_this_month_for_team(self.request.user)


class MonthlyLogsForCertainMonthView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Log.objects.monthly_logs_for_month_for_team(year, month, self.request.user)


class MonthlyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Log.objects.none()
        else:
            return Log.objects.monthly_logs_for_team(self.request.user)


class WeeklyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]
    queryset = Log.objects.weekly_logs_for_thisweek()
