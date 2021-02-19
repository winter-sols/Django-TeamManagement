from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsAdmin
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning
)
from user.models import User
from .serializers import DeveloperReportSerializer
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
