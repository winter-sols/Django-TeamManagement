from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsAdmin
from api.utils.provider import get_transaction_queryset_by_period
from api.common.finance.serializers import TransactionDetailSerializer
from .filters import TransactionFilter



class TransactionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = TransactionDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):
        return get_transaction_queryset_by_period(self.request.query_params).order_by('-created_at')