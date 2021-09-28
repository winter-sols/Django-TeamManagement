import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsDeveloper
from api.utils.provider import (
    get_earnings,
    get_user_project_earnings
)
from user.models import User, Team
from api.common.report.serializers import (
    DeveloperMonthlyReportSerializer,
    DeveloperQuarterlyReportSerializer,
    DeveloperWeeklyReportSerializer,
    IndividualDeveloperProjectSerializer
    # DeveloperCustomReportSerializer
)
from api.common.report.filters import DeveloperReportFilter
from api.common.report import constants

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


class DeveloperReportView(ListAPIView):
    permission_classes = [IsDeveloper]
    pagination_class = None
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        return IndividualDeveloperProjectSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)


class DeveloperCustomReportView(GenericAPIView):
    permission_classes = [IsDeveloper]
    # serializer_class = DeveloperCustomReportSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = User.objects.filter(id=self.request.user.id)
        user_cnt = queryset.count()
        response = list(range(user_cnt))
        pagination_queryset = get_user_project_earnings(queryset[0], start_date=start_date, end_date=end_date)
        page = self.paginate_queryset(pagination_queryset)

        for idx in range(user_cnt):
            user = queryset[idx]
            response[idx] = {
                'id': user.id,
                'earning': get_earnings(user, start_date=start_date, end_date=end_date),
                'project_earnings': get_user_project_earnings(user, start_date=start_date, end_date=end_date)
            }

        if page is not None:
            return self.get_paginated_response(response)

        return Response(response)
