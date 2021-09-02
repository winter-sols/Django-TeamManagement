from rest_framework.generics import ListAPIView, RetrieveAPIView 
from api.common.logging.serializers import LogDetailSerializer
import datetime
from reporting.models import Log
from api.permission import IsAdmin

class DailyLogsForTodayView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.daily_logs_for_today()


class WeeklyLogsForThisWeekView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.weekly_logs_for_thisweek()


class DailyLogsForCertainDateView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        dt = datetime.date(year, month, day)
        return Log.objects.daily_logs_for_date(dt)


class WeeklyLogsforCertainWeekView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes =[IsAdmin]

    def get_queryset(self):
        year = self.kwargs['year']
        week = self.kwargs['week']
        return Log.objects.weekly_logs_for_week(year, week)


class DailyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.daily_logs()


class MonthlyLogsForThisMonthView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]                                                                                            
    queryset = Log.objects.monthly_logs_for_this_month()


class MonthlyLogsForCertainMonthView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
            year = self.kwargs['year']
            month = self.kwargs['month']
            return Log.objects.monthly_logs_for_month(year, month)


class MonthlyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.monthly_logs()


class WeeklyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.weekly_logs_for_thisweek()
