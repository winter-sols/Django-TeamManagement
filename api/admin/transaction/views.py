from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsAdmin
from api.common.finance.serializers import TransactionDetailSerializer
from .filters import TransactionFilter
from finance.models import Transaction



class TransactionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = TransactionDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):

        return Transaction.objects \
        .filter_by_period(self.request.query_params) \
        .order_by('-created_at')
