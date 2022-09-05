from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import datetime

from api.common.logging.serializers import LogDetailSerializer
from reporting.models import Log
from api.permission import IsAdmin
from .filters import LogsFilter


class DailyLogsView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner']
    queryset = Log.objects.daily_logs()


class DailyLogsForCertainDateView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LogsFilter
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        dt = datetime.date(year, month, day)
        return Log.objects.daily_logs_for_date(dt)


class DailyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.daily_logs()


class WeeklyLogsView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner']
    queryset = Log.objects.weekly_logs()


class WeeklyLogsforCertainWeekView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes =[IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LogsFilter

    def get_queryset(self):
        year = self.kwargs['year']
        week = self.kwargs['week']
        return Log.objects.weekly_logs_for_week(year, week)


class WeeklyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.weekly_logs()


class MonthlyLogsView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner']                                                                                       
    queryset = Log.objects.monthly_logs()


class MonthlyLogsForCertainMonthView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LogsFilter
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Log.objects.monthly_logs_for_month(year, month)


class MonthlyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.monthly_logs()
