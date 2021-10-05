from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsDeveloper
from finance.models import Project
from api.utils.download import get_download_response
from api.utils.provider import (
    get_queryset_with_project_earnings,
    get_report_project_data_frame,
)


class ReportDeveloperProjectDownloadView(ListAPIView):
    permission_classes = [IsDeveloper]
    pagination_class = None

    def get_queryset(self):
        return get_queryset_with_project_earnings(
            Project.objects.filter(financialrequest__requester=self.request.user),
            self.request.query_params
        )

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        df = get_report_project_data_frame(query_set)
        return get_download_response(df, 'my_project_list.csv')
