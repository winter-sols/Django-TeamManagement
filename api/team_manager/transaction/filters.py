from rest_framework import filters
from django_filters import FilterSet

from finance.models import Transaction


class TransactionFilter(FilterSet):
    """
    filter transactions by created_at, payment_platform
    """
    class Meta:
        model = Transaction
        fields = ['created_at', 'payment_platform']
