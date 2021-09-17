import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsDeveloper
from api.utils.provider import (
    get_custom_earning,
    get_custom_project_earning
)
from user.models import User, Team
from api.common.report.serializers import (
    DeveloperMonthlyReportSerializer,
    DeveloperQuarterlyReportSerializer,
    DeveloperWeeklyReportSerializer, 
    DeveloperCustomReportSerializer
)
from api.common.report.filters import DeveloperReportFilter


class DeveloperMonthlyReportView(ListAPIView):
    permission_classes = [IsDeveloper]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperMonthlyReportSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class DeveloperQuarterlyReportView(ListAPIView):
    permission_classes = [IsDeveloper]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperQuarterlyReportSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class DeveloperWeeklyReportView(ListAPIView):
    permission_classes = [IsDeveloper]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperWeeklyReportSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class DeveloperCustomReportView(APIView):
    permission_classes = [IsDeveloper]
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = DeveloperReportFilter
    # serializer_class = DeveloperCustomReportSerializer
    # queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = User.objects.all()
        user_cnt = queryset.count()
        response = list(range(user_cnt))

        for idx in range(user_cnt):
            user = queryset[idx]
            response[idx] = {
                'id': user.id,
                'full_name': user.first_name + ' ' + user.last_name,
                'earning': get_custom_earning(user, user.role, start_date, end_date),
                'project_earnings': get_custom_project_earning(user, start_date, end_date)
            }
        return Response(response)
