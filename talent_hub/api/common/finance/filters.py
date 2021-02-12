from rest_framework import filters
from django_filters import FilterSet

from finance.models import (
    Project
)

class ProjectFilter(FilterSet):
    """
    filter projects by type and status
    """
    class Meta:
        model = Project
        fields = ['type', 'status']
