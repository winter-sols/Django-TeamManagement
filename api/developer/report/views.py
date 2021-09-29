import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.permission import IsDeveloper
from user.models import User, Team
from api.common.report.serializers import (
    ReportDeveloperProjectSerializer
    # DeveloperCustomReportSerializer
)
from api.common.report.filters import DeveloperReportFilter
from api.common.report import constants


class ReportDeveloperView(ListAPIView):
    permission_classes = [IsDeveloper]
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        return ReportDeveloperProjectSerializer
    
    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        query_params = self.request.query_params
        serializer_context['period'] = query_params.get('period')
        serializer_context['start_date'] = query_params.get('from')
        serializer_context['end_date'] = query_params.get('to')
        return serializer_context
