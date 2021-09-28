import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsTeamManager
from api.utils.provider import (
    get_earnings,
    get_user_project_earnings
)
from user.models import User, Team
from api.common.report.serializers import (
    DeveloperMonthlyReportSerializer,
    DeveloperQuarterlyReportSerializer,
    DeveloperWeeklyReportSerializer,
    DeveloperReportSerializer,
    IndividualDeveloperProjectSerializer
)
from api.common.report.filters import DeveloperReportFilter, DeveloperReportFilter
from api.common.report import constants

class TeamMonthlyReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    serializer_class = DeveloperMonthlyReportSerializer

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)


class TeamQuarterlyReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    serializer_class = DeveloperQuarterlyReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)


class TeamWeeklyReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    serializer_class = DeveloperWeeklyReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)


class DevelopersReportView(ListAPIView):
    permission_classes = [IsTeamManager]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeveloperReportFilter
    
    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)

    def get_serializer_class(self):
        return DeveloperReportSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)
    


class IndividualDeveloperReportView(RetrieveAPIView):
    permission_classes = [IsTeamManager]
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))
    
    def get_serializer_class(self):
        return DeveloperReportSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)


class IndividualDeveloperProjectReportView(RetrieveAPIView):
    permission_classes = [IsTeamManager]
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))
    def get_serializer_class(self):
        return IndividualDeveloperProjectSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)



class TeamCustomReportView(GenericAPIView):
    permission_classes = [IsTeamManager]

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team.id)
        
    def get(self, request):
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        queryset = self.filter_queryset(self.get_queryset())
        user_cnt = queryset.count()
        response = list(range(user_cnt))
        page = self.paginate_queryset(queryset)

        for idx in range(user_cnt):
            user = queryset[idx]
            response[idx] = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'earning': get_earnings(user, start_date=start_date, end_date=end_date),
                'project_earnings': get_user_project_earnings(user, start_date=start_date, end_date=end_date)
            }

        if page is not None:
            return self.get_paginated_response(response)
        return Response(response)
