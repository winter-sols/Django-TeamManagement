from rest_framework.generics import ListAPIView, RetrieveAPIView 
from api.common.logging.serializers import LogDetailSerializer
import datetime
from reporting.models import Log
from ...permission import IsAdmin

class DailyLogsForTodayView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]
    queryset = Log.objects.daily_logs_for_today()


class DailyLogsForCertainDateView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsAdmin]

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

