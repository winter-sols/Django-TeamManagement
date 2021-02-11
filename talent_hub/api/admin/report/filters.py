from rest_framework import filters
from django_filters import FilterSet
from user.models import User

class DeveloperReportFilter(FilterSet):
    """
    filter financial reports by developer and team
    """
    class Meta:
        model = User
        fields = ['id', 'team']
