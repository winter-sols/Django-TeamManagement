from rest_framework import filters
from django_filters import FilterSet

from user.models import User


class UserFilter(FilterSet):
    """
    Filter users by team
    """
    class Meta:
        model = User
        fields = ['team']
