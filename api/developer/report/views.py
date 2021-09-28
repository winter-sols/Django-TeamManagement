import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsDeveloper
from user.models import User, Team
from api.common.report.serializers import (
    DeveloperProjectSerializerForDeveloper
    # DeveloperCustomReportSerializer
)
from api.common.report.filters import DeveloperReportFilter
from api.common.report import constants


class DeveloperReportView(ListAPIView):
    permission_classes = [IsDeveloper]
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        return DeveloperProjectSerializerForDeveloper
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        period = self.request.query_params.get('period')
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')
        kwargs['context'] = {'period': period, 'start_date': start_date, 'end_date': end_date}
        return serializer_class(*args, **kwargs)
