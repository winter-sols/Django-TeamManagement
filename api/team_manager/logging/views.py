from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.common.logging.serializers import LogDetailSerializer
import datetime
from reporting.models import Log
from ...permission import IsTeamManager

class DailyLogsForTodayView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        return Log.objects.for_today_for_team(self.request.user)


class DailyLogsForCertainDateView(ListAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        dt = datetime.date(year, month, day)
        return Log.objects.for_date_for_team(dt, self.request.user)


class DailyLogDetailView(RetrieveAPIView):
    serializer_class = LogDetailSerializer
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        return Log.objects.for_team(self.request.user)

